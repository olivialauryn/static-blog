---
title: "Automating Blog Posts with a Synology NAS and Claude AI"
date: 2026-03-10T00:00:00+00:00
draft: false
tags: ["Home-Lab", "Claude", "Automation", "Hugo", "Networking", "Python"]
description: "How I built a Python pipeline that pulls photos from a Synology DS420j NAS, sends them to the Claude API, and automatically generates and publishes a Hugo blog post to GitHub — all from a single command."
---

When I set up my home lab with a Synology DS420j NAS, I wanted a project that would let me explore Claude's API capabilities in a practical, everyday context. The result is a Python pipeline that takes photos from my NAS, hands them to Claude, and automatically generates and publishes a fully formatted blog post to my Hugo static site on GitHub. Here's how I built it.

## The Hardware

The foundation of this project is straightforward: a **Synology DS420j** — a 4-bay NAS — connected to a home router via a network switch. The NAS serves as the central storage layer, holding photos in a dedicated shared folder (`blog/photos/latest/`) that the pipeline reads from. The DS420j runs Synology's DSM operating system and is accessible at a reserved local IP address, which makes it a reliable and addressable part of the home network.

## The Architecture

The pipeline connects four systems in sequence:

```
MacBook Photos App → Synology NAS → Claude API → Hugo → GitHub
```

Each step is automated by a single Python script (`blog-pipeline.py`) driven by a YAML configuration file (`blog-config.yaml`). Running the whole workflow requires just one command:

```bash
python3 blog-pipeline.py --config blog-config.yaml
```

## What the Script Does

The pipeline executes eight steps in order:

**1. Read configuration** — All settings (NAS credentials, Hugo paths, Claude model, author details, GitHub branch) are loaded from `blog-config.yaml`. This separation of config from code means the script never needs to be edited for routine use.

**2. Fetch photos from Synology** — The script connects to the NAS over SMB using `smbprotocol` and downloads any photos in the configured folder to a local staging directory. HEIC files (the default iPhone format) are automatically renamed to `.jpg` since they'll be re-encoded as JPEG.

**3. Encode photos for Claude** — Each photo is opened with Pillow (with `pillow-heif` for HEIC support), resized if it exceeds Claude's recommended 1568px maximum dimension, and base64-encoded for the API payload.

**4. Call the Claude API** — This is the core of the project. The script sends all encoded photos alongside a structured prompt to the Claude Messages API. The system prompt is dynamically built from the config file — including the author's name, bio, interests, and writing style — so Claude writes every post in first person, as if the author is telling the story themselves.

**5. Generate the post** — Claude returns a complete Hugo Markdown post including front matter (title, date, tags, description), an introduction, one section per photo, and a conclusion. The post uses standard Markdown image syntax: `![](/images/post-slug/filename.jpg)`.

**6. Copy photos to Hugo** — Images are written to `static/images/<post-slug>/` in the Hugo site. A `fix_image_extensions()` function checks the actual files on disk and corrects any extension mismatches (e.g. `.jpeg` vs `.jpg`) in the generated Markdown before the post is saved.

**7. Write the post file** — The Markdown is saved to `content/posts/<date>-<slug>.md` with a date-prefixed filename.

**8. Git push** — The entire site folder is staged with `git add .`, committed with an auto-generated message, and pushed to GitHub. From there, AWS Amplify picks up the new post and makes it public.

## Prompting Claude Effectively

The most important thing I learned during this project is that **the system prompt is the product**. The quality of Claude's output is almost entirely determined by how well you describe the context, constraints, and format you need.

The system prompt for this pipeline does several things:

- Tells Claude what kind of site it is writing for (Hugo static site)
- Describes the author so posts are written in a consistent first-person voice
- Specifies the exact Markdown image syntax to use and provides the actual filenames
- Sets tone, word count target, and structural requirements (front matter, intro, one section per photo, conclusion)
- Instructs Claude to respond with *only* the Markdown — no preamble, no code fences, no explanation

The config file exposes all of this as adjustable parameters, so changing the tone from `conversational` to `professional` at the CLI is a single flag:

```bash
python3 blog-pipeline.py --config blog-config.yaml --tone professional
```

## Configuration-Driven Design

Keeping all behaviour in `blog-config.yaml` rather than hardcoded in the script was a deliberate choice. It means the same script can serve multiple blogs, multiple authors, or multiple NAS configurations without any code changes. The author section in particular is worth filling in carefully:

```yaml
author:
  name: "Olivia Snowden"
  bio: "Technology professional and home lab enthusiast."
  interests:
    - home lab
    - Raspberry Pi
    - networking
  writing_style: "Personal and approachable, with technical detail where relevant."
```

Claude uses all of this as context. The more specific the author description, the more on-brand the output.

## Troubleshooting Along the Way

Getting to a working pipeline involved a handful of real-world issues worth noting for anyone following a similar path:

- **`pip: command not found`** — macOS uses `pip3`, not `pip`. Install packages with `pip3 install ... --break-system-packages` to avoid the Homebrew environment restriction.
- **HEIC support** — Pillow doesn't handle HEIC files by default. `brew install libheif` followed by `pip3 install pillow-heif` adds support, and the script registers it automatically at runtime.
- **API authentication** — The Claude API requires a separate account and API key from a Claude.ai Pro subscription. Set `ANTHROPIC_API_KEY` as an environment variable, ideally in `~/.zshrc` so it persists across Terminal sessions.
- **Image extension mismatches** — Claude occasionally generates `.jpeg` references for files that are actually `.jpg`. The pipeline now includes an automatic correction step that checks the real filenames on disk before writing the post.
- **SMB shared folder** — The `blog` shared folder and `photos/latest/` subfolders need to be created manually in DSM (Control Panel → Shared Folder, then File Station for subfolders) before the pipeline can connect.

## What I Learned About Claude's API

This project gave me hands-on experience with several of Claude's key capabilities:

**Multimodal input** — Sending images as base64-encoded payloads alongside text instructions is straightforward with the Messages API. Claude accurately describes photo content and weaves it into coherent narrative.

**Structured output** — With a precise prompt, Claude reliably returns valid Hugo front matter, correct Markdown syntax, and properly formatted image references. The output is ready to save directly to disk without post-processing.

**System prompts as configuration** — The system prompt is the most powerful lever for controlling output quality. Treating it as a first-class configuration artifact — something to iterate on and store in a config file rather than hardcode — produces far more consistent results.

## Next Steps

The pipeline is functional, but there are several natural extensions worth exploring: automatically clearing the `photos/latest/` folder after a successful run, adding a post review step before pushing, supporting multiple photo folders for different categories, or building a simple web UI hosted on one of the Raspberry Pis to trigger runs without touching the command line.

See the post generated from this project here: https://www.osnowden.com/post/2026-03-10-when-knitting-becomes-a-full-stack-problem-adventures-in-analog-programming/

- Written by Claude
