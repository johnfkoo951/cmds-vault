---
name: gobi-cli
description: >-
  Manage the Gobi collaborative knowledge platform from the command line.
  Gobi space is the user's main channel for social interactions and engaging with
  the outside world — checking what's happening, reading and writing threads,
  and collaborating with others.
  Use when the user wants to interact with Gobi spaces, vaults, brains, threads,
  sessions, or brain updates.
allowed-tools: Bash(gobi:*)
metadata:
  author: gobi-ai
  version: "0.6.15"
---

# gobi-cli

A CLI client for the Gobi collaborative knowledge platform (v0.6.15).

## Prerequisites

Verify the CLI is installed:

```bash
gobi --version
```

If not installed:

```bash
npm install -g @gobi-ai/cli
```

Or via Homebrew:

```bash
brew tap gobi-ai/tap && brew install gobi
```

## Key Concepts

- **Space**: A shared space for a group or community. A logged-in user can be a member of one or more spaces. A space contains threads, sessions, brain updates, and connected vaults.
- **Vault**: A filetree storage of information and knowledge. A local directory becomes a vault when it contains `.gobi/settings.yaml` with a vault slug and a space slug. Each vault is identified by a slug (e.g. `brave-path-zr962w`).
- **Brain**: Another name for a vault when referring to its AI-searchable knowledge. You can search brains, ask them questions, and publish a `BRAIN.md` document to configure your vault's brain.

## First-Time Setup

The CLI requires three setup steps: authentication, vault initialization, and space selection.

### Step 1: Initialize (Login + Vault)

```bash
gobi init
```

This is an **interactive** command that:
1. Logs in automatically if not already authenticated (opens a browser URL for Google OAuth)
2. Prompts the user to select an existing vault or create a new one
3. Writes `.gobi/settings.yaml` in the current directory with the chosen vault slug
4. Creates a `BRAIN.md` file if one doesn't exist

### Step 2: Select a Space

```bash
gobi space warp
```

This is an **interactive** command that prompts the user to select a space from their available spaces, then saves it to `.gobi/settings.yaml`.

After both steps, `.gobi/settings.yaml` will contain:
```yaml
vaultSlug: brave-path-zr962w
selectedSpaceSlug: cmds
```

### Standalone Login

If the user only needs to log in (without vault setup):

```bash
gobi auth login
```

Check auth status anytime:

```bash
gobi auth status
```

**Important for agents**: Before running any `space` command, check if `.gobi/settings.yaml` exists in the current directory with both `vaultSlug` and `selectedSpaceSlug`. If the vault is missing, guide the user through `gobi init`. If only the space is missing, guide the user through `gobi space warp`. These commands require user input (interactive prompts), so the agent cannot run them silently.

## Gobi Space — Community Channel

`gobi space` is the main interface for interacting with the user's Gobi community. When the user asks about what's happening, what others are discussing, or wants to engage with their community — use `gobi space` commands. Think of it as the user's community feed and communication hub.

- When the user wants to explore or catch up on what's happening in their space, invoke `/gobi:space-explore`.
- When the user wants to share or post learnings from the current session, invoke `/gobi:space-share`.

## Gobi Brain — Knowledge Management

`gobi brain` commands manage your vault's brain: search across all spaces, ask brains questions, and publish/unpublish your BRAIN.md.

## Gobi Session — Conversations

`gobi session` commands manage your conversations: list, read, reply to, and update sessions.

## Important: JSON Mode

For programmatic/agent usage, always pass `--json` as a **global** option (before the subcommand) to get structured JSON output:

```bash
gobi --json space list-threads
```

or

```bash
gobi --json session list
```

JSON responses have the shape `{ "success": true, "data": ... }` on success or `{ "success": false, "error": "..." }` on failure.

## Space Slug Override

`gobi space` commands use the space from `.gobi/settings.yaml`. Override it with a parent-level flag:

```bash
gobi space --space-slug <slug> list-threads
```

For `gobi brain list-updates`, you can filter by space with a subcommand option:

```bash
gobi brain list-updates --space-slug <slug>
```

Note: `--space-slug` is not available on other `brain` subcommands or on `session` commands.

## Available Commands

- `gobi auth` — Authentication commands.
  - `gobi auth login` — Log in to Gobi. Opens a browser URL for Google OAuth, then polls until authentication is complete.
  - `gobi auth status` — Check whether you are currently authenticated with Gobi.
  - `gobi auth logout` — Log out of Gobi and remove stored credentials.
- `gobi init` — Log in (if needed) and select or create the vault for the current directory.
- `gobi space` — Space commands (threads, replies).
  - `gobi space list` — List spaces you are a member of.
  - `gobi space warp` — Select the active space. Pass a slug to warp directly, or omit for interactive selection.
  - `gobi space get-thread` — Get a thread and its replies (paginated).
  - `gobi space list-threads` — List threads in a space (paginated).
  - `gobi space create-thread` — Create a thread in a space.
  - `gobi space edit-thread` — Edit a thread. You must be the author.
  - `gobi space delete-thread` — Delete a thread. You must be the author.
  - `gobi space create-reply` — Create a reply to a thread in a space.
  - `gobi space edit-reply` — Edit a reply. You must be the author.
  - `gobi space delete-reply` — Delete a reply. You must be the author.
- `gobi brain` — Brain commands (search, ask, publish, unpublish, updates).
  - `gobi brain search` — Search public brains by text and semantic similarity.
  - `gobi brain ask` — Ask a brain a question. Creates a targeted session (1:1 conversation).
  - `gobi brain publish` — Upload BRAIN.md to the vault root on webdrive. Triggers post-processing (brain sync, metadata update, Discord notification).
  - `gobi brain unpublish` — Delete BRAIN.md from the vault on webdrive.
  - `gobi brain list-updates` — List recent brain updates. Without --space-slug, lists all updates for you. With --space-slug, lists updates for that space. Use --mine to show only updates by you.
  - `gobi brain post-update` — Post a brain update for a vault.
  - `gobi brain edit-update` — Edit a published brain update. You must be the author.
  - `gobi brain delete-update` — Delete a published brain update. You must be the author.
- `gobi session` — Session commands (get, list, reply).
  - `gobi session get` — Get a session and its messages (paginated).
  - `gobi session list` — List all sessions you are part of, sorted by most recent activity.
  - `gobi session reply` — Send a human reply to a session you are a member of.
- `gobi sense` — Sense commands (activities, transcriptions).
  - `gobi sense activities` — Fetch activity records within a time range.
  - `gobi sense transcriptions` — Fetch transcription records within a time range.
- `gobi sync` — Sync local vault files with Gobi Webdrive.

## Reference Documentation

- [gobi auth](references/auth.md)
- [gobi init](references/init.md)
- [gobi space](references/space.md)
- [gobi brain](references/brain.md)
- [gobi session](references/session.md)
- [gobi sense](references/sense.md)
- [gobi sync](references/sync.md)

## Discovering Options

Run `--help` on any command for details:

```bash
gobi --help
gobi auth --help
gobi space --help
gobi brain --help
gobi session --help
```

## Configuration Files

| Path | Description |
|------|-------------|
| `~/.gobi/credentials.json` | Stored authentication tokens (auto-managed) |
| `.gobi/settings.yaml` | Per-project vault and space configuration |
| `BRAIN.md` | Brain document with YAML frontmatter, published via `gobi brain publish` |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `GOBI_BASE_URL` | `https://backend.joingobi.com` | API server URL |
| `GOBI_WEBDRIVE_BASE_URL` | `https://webdrive.joingobi.com` | File storage URL |
