#!/usr/bin/env python3
"""
blog-pipeline.py — Automated Photo Blog Post Pipeline
Synology NAS → Claude API → Hugo → GitHub

Usage:
  python blog-pipeline.py --config blog-config.yaml
  python blog-pipeline.py --config blog-config.yaml --tone professional --preview
  python blog-pipeline.py --config blog-config.yaml --dry-run

Requirements:
  pip install pyyaml anthropic requests smbprotocol Pillow gitpython
"""

import argparse
import base64
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import anthropic
import yaml
from PIL import Image

# ── Optional SMB import ──────────────────────────────────────────────────────
try:
    import smbclient
    SMB_AVAILABLE = True
except ImportError:
    SMB_AVAILABLE = False

# ── Optional Git import ──────────────────────────────────────────────────────
try:
    from git import Repo
    GIT_AVAILABLE = True
except ImportError:
    GIT_AVAILABLE = False


# ─────────────────────────────────────────────────────────────────────────────
# 1. CONFIG
# ─────────────────────────────────────────────────────────────────────────────

def load_config(config_path: str) -> dict:
    """Load and return the YAML config file."""
    with open(config_path) as f:
        config = yaml.safe_load(f)
    print(f"✅ Config loaded from {config_path}")
    return config


# ─────────────────────────────────────────────────────────────────────────────
# 2. FETCH PHOTOS FROM SYNOLOGY
# ─────────────────────────────────────────────────────────────────────────────

def fetch_photos_from_synology(config: dict, local_staging: Path) -> list[Path]:
    """
    Connect to Synology via SMB and copy photos to a local staging folder.
    Returns a list of local photo paths.
    """
    syn = config["synology"]
    host = syn["host"]
    username = syn["username"]
    password = syn["password"]
    share = syn["photo_share"]
    folder = syn["photo_folder"]

    local_staging.mkdir(parents=True, exist_ok=True)

    if not SMB_AVAILABLE:
        print("⚠️  smbprotocol not installed. Skipping Synology fetch.")
        print("   Install with: pip install smbprotocol")
        print("   Falling back to any photos already in staging/")
    else:
        print(f"📡 Connecting to Synology at {host}...")
        smbclient.register_session(host, username=username, password=password)
        remote_path = f"\\\\{host}\\{share}\\{folder.replace('/', '\\')}"

        photo_exts = {".jpg", ".jpeg", ".png", ".heic", ".webp"}
        for entry in smbclient.scandir(remote_path):
            if Path(entry.name).suffix.lower() in photo_exts:
                remote_file = f"{remote_path}\\{entry.name}"
                local_file = local_staging / entry.name
                with smbclient.open_file(remote_file, mode="rb") as rf:
                    local_file.write_bytes(rf.read())
                print(f"   📷 Downloaded: {entry.name}")

    photos = sorted(local_staging.glob("*"))
    photos = [p for p in photos if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".heic", ".webp"}]

    if not photos:
        print("❌ No photos found in staging folder. Exiting.")
        sys.exit(1)

    print(f"✅ {len(photos)} photo(s) ready for processing.")
    return photos


# ─────────────────────────────────────────────────────────────────────────────
# 3. COPY PHOTOS INTO HUGO STATIC FOLDER
# ─────────────────────────────────────────────────────────────────────────────

def copy_photos_to_hugo(photos: list[Path], config: dict, post_slug: str) -> tuple[Path, list[str]]:
    """
    Copy photos into Hugo's static/images/<post_slug>/ folder.
    Returns (image_dir, list_of_filenames).
    """
    hugo_root = Path(config["hugo"]["site_path"]).expanduser()
    images_root = hugo_root / config["hugo"]["images_path"] / post_slug
    images_root.mkdir(parents=True, exist_ok=True)

    filenames = []
    for photo in photos:
        dest = images_root / photo.name
        shutil.copy2(photo, dest)
        filenames.append(photo.name)
        print(f"   🖼️  Copied to Hugo: static/images/{post_slug}/{photo.name}")

    print(f"✅ {len(filenames)} photo(s) copied to Hugo static folder.")
    return images_root, filenames


# ─────────────────────────────────────────────────────────────────────────────
# 4. ENCODE PHOTOS FOR CLAUDE
# ─────────────────────────────────────────────────────────────────────────────

def encode_photos_for_claude(photos: list[Path]) -> list[dict]:
    """
    Encode photos as base64 for the Claude Messages API.
    Resizes large images to keep API payload manageable.
    """
    # Register HEIC/HEIF support if available
    try:
        from pillow_heif import register_heif_opener
        register_heif_opener()
    except ImportError:
        pass  # pillow-heif not installed, HEIC files will fail

    encoded = []
    MAX_DIM = 1568  # Claude's recommended max dimension

    for photo in photos:
        img = Image.open(photo)
        if img.mode != "RGB":
            img = img.convert("RGB")

        # Resize if needed
        w, h = img.size
        if max(w, h) > MAX_DIM:
            scale = MAX_DIM / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

        # Re-encode as JPEG
        import io
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=85)
        b64 = base64.standard_b64encode(buf.getvalue()).decode("utf-8")

        encoded.append({
            "filename": photo.name,
            "b64": b64,
        })
        print(f"   🔐 Encoded: {photo.name}")

    print(f"✅ {len(encoded)} photo(s) encoded for Claude.")
    return encoded


# ─────────────────────────────────────────────────────────────────────────────
# 5. CALL CLAUDE API
# ─────────────────────────────────────────────────────────────────────────────

def call_claude(encoded_photos: list[dict], filenames: list[str], post_slug: str, config: dict, tone_override: str = None) -> str:
    """
    Send photos to Claude and return the generated Hugo Markdown blog post.
    """
    claude_cfg = config["claude"]
    tone = tone_override or claude_cfg.get("blog_tone", "conversational")
    topic = claude_cfg.get("blog_topic", "personal blog")
    model = claude_cfg.get("model", "claude-sonnet-4-20250514")
    max_tokens = claude_cfg.get("max_tokens", 2000)

    custom_prompt = claude_cfg.get("custom_system_prompt", "").strip()
    system_prompt = custom_prompt if custom_prompt else (
        f"You are a blog post writer for a Hugo static site. "
        f"This blog is about: {topic}. "
        f"Write in a {tone} tone. "
        f"Always respond with ONLY valid Hugo Markdown — no preamble, no explanation, just the post. "
        f"Include a complete front matter block at the top."
    )

    # Build the message content — images first, then the instruction
    content = []
    for photo in encoded_photos:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": photo["b64"],
            }
        })

    # Build the figure shortcode list for Claude to reference
    shortcodes = "\n".join(
        [f'  {{{{< figure src="/images/{post_slug}/{fn}" caption="[describe this photo]" >}}}}' for fn in filenames]
    )

    content.append({
        "type": "text",
        "text": (
            f"Please write a complete Hugo blog post based on the {len(encoded_photos)} photo(s) above.\n\n"
            f"Requirements:\n"
            f"- Front matter with: title, date ({datetime.now().strftime('%Y-%m-%dT%H:%M:%S+00:00')}), "
            f"draft: false, tags (infer from content), description\n"
            f"- An engaging introduction paragraph\n"
            f"- One section per photo using Hugo figure shortcodes. "
            f"The image paths must use exactly these filenames:\n{shortcodes}\n"
            f"- A conclusion paragraph\n"
            f"- Total length: ~600-800 words\n\n"
            f"Respond with ONLY the Markdown. No code fences. No explanation."
        )
    })

    print(f"🤖 Calling Claude ({model})...")
    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment
    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": content}]
    )

    markdown = response.content[0].text.strip()
    print("✅ Blog post generated by Claude.")
    return markdown


# ─────────────────────────────────────────────────────────────────────────────
# 6. WRITE POST TO HUGO
# ─────────────────────────────────────────────────────────────────────────────

def extract_title_from_markdown(markdown: str) -> str:
    """Extract the title from the Hugo front matter."""
    match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', markdown, re.MULTILINE)
    return match.group(1).strip() if match else "new-post"


def slugify(title: str) -> str:
    """Convert a title to a URL-safe slug."""
    slug = title.lower()
    slug = re.sub(r"[^\w\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    return slug.strip("-")


def write_post_to_hugo(markdown: str, config: dict, post_slug: str) -> Path:
    """Write the generated Markdown to Hugo's content/posts/ folder."""
    hugo_root = Path(config["hugo"]["site_path"]).expanduser()
    posts_dir = hugo_root / config["hugo"]["posts_path"]
    posts_dir.mkdir(parents=True, exist_ok=True)

    date_prefix = config.get("output", {}).get("date_prefix", True)
    prefix = datetime.now().strftime("%Y-%m-%d-") if date_prefix else ""
    filename = f"{prefix}{post_slug}.md"
    post_path = posts_dir / filename

    post_path.write_text(markdown, encoding="utf-8")
    print(f"✅ Post written to: {post_path}")
    return post_path


# ─────────────────────────────────────────────────────────────────────────────
# 7. HUGO PREVIEW
# ─────────────────────────────────────────────────────────────────────────────

def run_hugo_preview(config: dict):
    """Start Hugo's local dev server for preview."""
    hugo_root = Path(config["hugo"]["site_path"]).expanduser()
    port = config["hugo"].get("preview_port", 1313)
    print(f"🌐 Starting Hugo preview at http://localhost:{port} (Ctrl+C to stop)...")
    subprocess.run(["hugo", "server", "-D", f"--port={port}"], cwd=hugo_root)


# ─────────────────────────────────────────────────────────────────────────────
# 8. GIT PUSH
# ─────────────────────────────────────────────────────────────────────────────

def git_push(config: dict, post_title: str, post_path: Path, image_dir: Path):
    """Stage entire repo folder, commit, and push to GitHub."""
    gh = config["github"]
    repo_path = Path(gh["repo_path"]).expanduser()
    branch = gh.get("branch", "main")
    commit_msg = gh.get("commit_message", "Add blog post: %s") % post_title

    if not GIT_AVAILABLE:
        print("⚠️  gitpython not installed. Running git via shell instead.")
        cmds = [
            ["git", "add", "."],  # Stage entire folder
            ["git", "commit", "-m", commit_msg],
            ["git", "push", "origin", branch],
        ]
        for cmd in cmds:
            result = subprocess.run(cmd, cwd=repo_path, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"❌ Git error: {result.stderr}")
                sys.exit(1)
    else:
        repo = Repo(repo_path)
        repo.git.add(".")  # Stage entire folder
        repo.index.commit(commit_msg)
        origin = repo.remote(name="origin")
        origin.push(branch)

    print(f"✅ Pushed to GitHub ({branch}): {commit_msg}")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Automated Photo Blog Post Pipeline")
    parser.add_argument("--config", required=True, help="Path to blog-config.yaml")
    parser.add_argument("--tone", help="Override blog tone from config")
    parser.add_argument("--preview", action="store_true", help="Launch Hugo preview server after generation")
    parser.add_argument("--dry-run", action="store_true", help="Generate post but don't push to GitHub")
    args = parser.parse_args()

    print("\n🚀 Blog Post Pipeline Starting...\n")

    # Step 1: Load config
    config = load_config(args.config)

    # Step 2: Fetch photos from Synology
    staging = Path("/tmp/blog-pipeline-staging")
    photos = fetch_photos_from_synology(config, staging)

    # Use a temporary slug for file organisation (will update after Claude generates title)
    temp_slug = f"post-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # Step 3: Encode photos for Claude
    print("\n📸 Encoding photos...")
    encoded = encode_photos_for_claude(photos)
    filenames = [p.name for p in photos]

    # Step 4: Call Claude
    print("\n🤖 Generating blog post with Claude...")
    markdown = call_claude(encoded, filenames, temp_slug, config, tone_override=args.tone)

    # Step 5: Determine final slug from generated title
    title = extract_title_from_markdown(markdown)
    post_slug = slugify(title)
    print(f"📝 Post title: {title}")
    print(f"🔗 Post slug:  {post_slug}")

    # Update image paths in markdown to use final slug
    markdown = markdown.replace(f"/images/{temp_slug}/", f"/images/{post_slug}/")

    # Step 6: Copy photos to Hugo static folder
    print("\n🖼️  Copying photos to Hugo...")
    image_dir, _ = copy_photos_to_hugo(photos, config, post_slug)

    # Step 7: Write post file
    print("\n📄 Writing post to Hugo...")
    post_path = write_post_to_hugo(markdown, config, post_slug)

    # Step 8: Build Hugo site (optional — only needed if not using CI/CD)
    if config["hugo"].get("build_before_push", False):
        print("\n🔨 Building Hugo site...")
        hugo_root = Path(config["hugo"]["site_path"]).expanduser()
        result = subprocess.run(["hugo"], cwd=hugo_root, capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Hugo build failed:\n{result.stderr}")
            sys.exit(1)
        print("✅ Hugo site built successfully.")

    # Step 9: Preview (optional)
    if args.preview or config["hugo"].get("preview", False):
        run_hugo_preview(config)

    # Step 10: Push to GitHub
    if not args.dry_run and config["github"].get("auto_push", True):
        print("\n🐙 Pushing to GitHub...")
        git_push(config, title, post_path, image_dir)
    elif args.dry_run:
        print("\n⏭️  Dry run — skipping GitHub push.")
    else:
        print("\n⏭️  auto_push is false — skipping GitHub push.")

    # Cleanup staging
    shutil.rmtree(staging, ignore_errors=True)

    print("\n✅ Pipeline complete!\n")
    print(f"   Post file:  {post_path}")
    print(f"   Images:     {image_dir}")
    print(f"   Title:      {title}\n")


if __name__ == "__main__":
    main()
