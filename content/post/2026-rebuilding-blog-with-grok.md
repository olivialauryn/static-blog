---
title: "Rebuilding My Blog with Grok"
date: 2026-03-02T16:30:00-05:00
draft: false
tags: ["AI"]
---

After running a clean, minimal Ghostwriter theme for some time, I recently migrated this site to Hugo-PaperMod. The goal was better performance, built-in dark mode, improved mobile responsiveness, and easier customization while keeping the lightweight blogging feel.

## What is Hugo?

Hugo is a fast, open-source static site generator written in Go. Unlike traditional CMS platforms (WordPress, Ghost, etc.), Hugo compiles Markdown content, templates, and assets into plain HTML, CSS, and JS files at build time—no database, no server-side runtime. This results in blazing-fast page loads, strong security (no attack surface), low hosting costs, and easy version control via Git.

I've been using Hugo since early in this blog's life to host a personal static blog. All content lives as Markdown files in Git, builds happen locally or in CI/CD, and the output deploys to AWS Amplify. The workflow is simple: edit posts → `hugo server` for preview → commit/push → Amplify rebuilds and serves the site instantly.

## Migration Path

- **Source repo**: Full Hugo site (content, config, themes) in GitHub repo `static-blog`
- **Deployment**: AWS Amplify auto-build on push to `main`, using `hugo --gc --minify`
- **Hugo version**: Pinned to v0.157.0 (extended) via Amplify environment variable `HUGO_VERSION=extended_0.157.0`

## Key Steps & Fixes

1. **Theme switch**  
   Removed Ghostwriter submodule, added PaperMod via  
   `git submodule add --depth=1 https://github.com/adityatelange/hugo-PaperMod.git themes/PaperMod`  
   Updated `config.toml`: `theme = "PaperMod"` and added minimal `[params]` block.

2. **BaseURL correction**  
   Initial symptom: homepage loaded, subpages 404’d with “Safari Can’t Connect to the Server”.  
   Root cause: `baseURL` was not set to the live domain (`https://osnowden.com/`). Fixed with trailing slash and `canonifyURLs = true`.

3. **Amplify build configuration**  
   Switched from deploying a pre-built `public/` folder to full source build.  
   Added `amplify.yml`:

   ```yaml
   version: 1
   frontend:
     phases:
       build:
         commands: ['hugo --gc --minify']
     artifacts:
       baseDirectory: public
       files:
         - '**/*'

Set HUGO_VERSION env var to ensure consistent extended Hugo.

4. **Common build errors & resolutions**  
    **Permalink ill-formed** → Removed invalid :contentbasename token from [permalinks] section.

    **Template parse error** (unclosed action in get-page-images.html:9) → Overwrote with upstream master version via submodule commit:
     `cd themes/PaperMod`

    `git checkout master -- layouts/partials/templates/_funcs/get-page-images.html`

    `git add . && git commit -m "Fix parse error"`

    `cd ../..`

    `git add themes/PaperMod && git commit -m "Update PaperMod submodule"`

    `git push`

## Leveraging Grok for Troubleshooting and Guidance

Throughout the migration I used Grok (xAI’s conversational AI) as an interactive troubleshooting partner. It provided precise, context-aware steps for:

- Diagnosing the baseURL mismatch and 404 behavior specific to Amplify-hosted Hugo sites
- Identifying and fixing the exact line-9 syntax error in PaperMod’s get-page-images.html partial
- Crafting valid amplify.yml and environment variable settings for Hugo v0.157 extended
- Verifying local vs. production behavior differences (e.g., hugo server overriding baseURL)

The iterative conversation allowed rapid narrowing of root causes—often faster than scattered forum searches or trial-and-error—while staying grounded in real commands and log snippets from my MacBook Air setup.

## Outcome

Builds are now green, site renders correctly (including search, archives, tags), no localhost references in production HTML, and PaperMod features (TOC, reading time, social cards) work out of the box.

Future changes are as simple as editing Markdown → commit → push.

For anyone doing a similar migration on Amplify: always verify baseURL first, use extended Hugo for resource-heavy themes, and remember submodule changes require two-level commits.
Happy static-site building.

## By the way, I didn't write this blog post. Grok did 😉

— Olivia
