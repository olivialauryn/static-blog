---
title: "Automating My Blog With Claude Code"
date: 2026-03-08T00:00:00-05:00
draft: false
tags: ["ai", "automation", "linux"]
---

I've recently started using Claude — specifically the Claude Code CLI — and it's already changed how I manage this blog. Instead of manually writing posts and running git commands, I can now just describe what I want and Claude handles the rest: writing the post, building the site, committing, and pushing to GitHub. It's pretty wild.

To get started I picked up a Claude Pro subscription, which is required to use Claude Code — the free tier doesn't include it. Totally worth it. Here's how to get it set up on a MacBook Air.

## Installing Claude Code CLI on a MacBook Air

**Prerequisites:**
- macOS 13 (Ventura) or later
- A Claude Pro, Max, Teams, or Enterprise account

### Option 1: Native Installer (Recommended)

Open Terminal and run:

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

This pulls down the latest stable release with no extra dependencies. It also auto-updates in the background, so you'll always be on the latest version.

### Option 2: Homebrew

If you're already a Homebrew user:

```bash
brew install --cask claude-code
```

Note that Homebrew installs won't auto-update — you'll need to run `brew upgrade claude-code` manually when a new version drops.

### Option 3: npm

If you have Node.js 18+ installed:

```bash
npm install -g @anthropic-ai/claude-code
```

Skip the `sudo` — it causes permission headaches and is a security risk.

## Logging In

Once installed, just run `claude` in your terminal. It'll open a browser tab to Anthropic's auth page. Log in with your account, hit Authorize, and head back to your terminal. Your credentials get saved to your Mac's keychain so you only have to do this once.

## What I'm Using It For

Right now I'm using Claude Code to automate my Hugo blog workflow. I tell it what I want to write, it generates the markdown post, rebuilds the site, and pushes everything to GitHub — all from a single conversation in the terminal. No context switching, no manual git commands.

It's a genuinely useful tool, especially if you're already comfortable in the terminal. Worth trying if you haven't already.
