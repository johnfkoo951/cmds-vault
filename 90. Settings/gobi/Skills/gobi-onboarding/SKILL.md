---
name: gobi-onboarding
description: First-run setup guide for cmds-vault — connects Gobi Desktop, personalizes the Brain, syncs to Gobi Space, and sketches the CMDS pipeline. Activate when the user opens a freshly-cloned cmds-vault for the first time, or says "onboarding", "온보딩", "first run", or asks how to set up Gobi.
metadata:
  version: "1.0"
  author: jykim
  created: 2026-04-26
  base: "https://github.com/jykim/ai4pkm-vault/tree/main/_Settings_/Skills/gobi-onboarding"
---

# Gobi Onboarding for cmds-vault

Guide a first-time student through connecting this CMDS-conventions vault to Gobi Desktop and Gobi Space. Total time: ~10 minutes.

## When to Use

Activate on any of:
- User says "onboarding", "온보딩", "start", "시작", "first run", "setup"
- User opens a freshly-cloned `cmds-vault` and asks how to use it
- `gobi --version` returns successfully but `.gobi/settings.yaml` has no `vaultSlug`
- User asks "what's `BRAIN.md`?" or "how do I connect Gobi?"

This skill is **text-or-voice agnostic**. If the user is in voice mode (Gobi Desktop voice mode active), keep responses short and conversational. Otherwise, use markdown formatting.

## Onboarding Philosophy

Borrowed from ai4pkm's gobi-onboarding (jykim/ai4pkm-vault), simplified for class context:

1. **Value-first** — show the Brain page on Gobi Space within the first 5 minutes, before going deep on CMDS theory
2. **Agent-does-it** — for non-destructive steps (file read, settings dump), execute first then summarize. Ask before destructive (overwriting BRAIN.md, posting public updates)
3. **Decision points minimum** — default everything; let the student override after the round-trip succeeds
4. **CMDS-shaped** — frame the pipeline as Connect → Merge → Develop → Share, not "DRB/TIU/PBU" (those are ai4pkm vocabulary)

## Pre-boarding (verify before starting)

These must succeed before the flow proceeds. If any fail, fix them first and resume.

| Check | Command | Expected |
|-------|---------|----------|
| Repo cloned | `ls /path/to/cmds-vault/CMDS.md` | file exists |
| Gobi CLI installed | `gobi --version` | version string (≥0.6.x) |
| Obsidian installed (optional) | `obsidian --version` | version string |
| Logged in to Google | `gobi auth status` | shows account email |

If `gobi` is missing:
```bash
brew tap gobi-ai/tap && brew install gobi
# or: npm install -g @gobi-ai/cli
```

If not logged in:
```bash
gobi auth login    # opens browser for Google OAuth
```

## Flow

### Step 1 — Initialize the vault (1 min)

**Why first**: this writes the real `vaultSlug` and creates the server-side Brain. Without it, sync will fail.

```bash
cd /path/to/cmds-vault
gobi init
```

Gobi will:
1. Confirm your Google account
2. Ask "Use existing vault or create new?" — pick **create new**, name it (e.g. `cmds-class-2026`)
3. Write the auto-generated slug into `.gobi/settings.yaml`
4. Notice the `BRAIN.md` we ship and leave it alone (won't overwrite)

**Verify**:
```bash
grep vaultSlug .gobi/settings.yaml
# → vaultSlug: <something-like-brave-path-zr962w>
```

### Step 2 — Pick a Gobi space (30 sec)

Pick which Gobi space this Brain publishes into. For class use, instructor will give you the space slug (e.g. `cmds-class-2026`).

```bash
gobi space warp
# pick from list, or paste the slug the instructor gave you
```

**Verify**:
```bash
grep selectedSpaceSlug .gobi/settings.yaml
```

### Step 3 — Personalize the Brain (3 min)

Three files describe who this Brain is:

1. **`BRAIN.md`** — the public profile. Replace the "Your Second Brain" template with your name, role, interests, pinned notes.
2. **`BRAIN.jpg`** — the thumbnail. Drop a square 512×512+ JPG/PNG, name it exactly `BRAIN.jpg`. (We ship the CMDS round logo as a placeholder — replace it.)
3. **`BRAIN_PROMPT.md`** — the system prompt for Gobi chat. Define your Brain's voice, scope, refusals.

Open all three:
```bash
obsidian open file=BRAIN.md
obsidian open file=BRAIN_PROMPT.md
open BRAIN.jpg     # macOS Finder
```

**Don't change** the frontmatter keys (`title`, `description`, `thumbnail`, `prompt`, `homepage`) — Gobi looks them up by name.

### Step 4 — First sync (1 min)

```bash
gobi sync --dry-run    # preview — should show 4 files to upload
gobi sync              # actually upload
```

You should see uploads for: `BRAIN.md`, `BRAIN.jpg`, `BRAIN_PROMPT.md`, `app/home.html`. (Pattern lives in `.gobi/syncfiles` — edit if you want to sync more.)

**Verify on Gobi Space**: open `https://gobispace.com/@<your-vault-slug>` in a browser. The Brain page shows your thumbnail, title, description.

If the homepage still looks like the default CMDS template — that's expected, we'll customize it in Step 7.

### Step 5 — First capture (2 min) — *Connect*

Time to write your first note. Pick something on your mind right now — a question, a fact, a fragment.

```bash
# Replace the date and title
echo "---
title: \"My first capture\"
created: $(date '+%Y-%m-%d %H:%M:%S')
tags:
  - inbox
---

## What I'm thinking about today
" > "00. Inbox/01. Daily Notes/$(date '+%Y-%m-%d') first capture.md"

obsidian open file="00. Inbox/01. Daily Notes/$(date '+%Y-%m-%d') first capture.md"
```

Write 3-5 lines. Don't aim for permanent — this is the **Connect** stage, fast & loose.

**Why `00. Inbox/`?** The CMDS taxonomy treats inbox as the universal landing zone. See `.claude/rules/directory-structure.md` for the full layout.

### Step 6 — First Brain Update (2 min) — *Share*

Brain Updates are how your vault talks to the Gobi space. Even if you have nothing distilled yet, share the fact that you exist:

```bash
gobi brain post-update \
  --title "Joined the cmds class" \
  --content "Just set up my Second Brain following CMDS conventions. Looking forward to learning Connect → Merge → Develop → Share."
```

**Verify**: refresh `https://gobispace.com/@<your-vault-slug>` — you should see the update at the top.

### Step 7 — Customize the homepage (optional, 2 min)

The homepage Gobi Space renders is `app/home.html`. We ship a CMDS-themed minimal template that calls `window.gobi.listBrainUpdates()` and `window.gobi.getSessions()`.

To customize colors, layout, sections:
1. Open `90. Settings/gobi/Prompts/Create Brain Homepage (CBH).md` in Claude Code
2. Run the prompt with your customization request:
   - "Add a section listing my pinned notes"
   - "Change accent color to indigo"
   - "Add a quote rotator at top"
3. CBH writes the new `app/home.html` in place
4. `gobi sync` to push

The `window.gobi` API surface CBH can use:
- `gobi.vault` — `{title, description, thumbnailPath, vaultId, webdriveUrl}`
- `gobi.listBrainUpdates({limit, cursor})` — paginated updates
- `gobi.getSessions({limit})` — chat sessions
- `gobi.loadMessages(sessionId)`, `gobi.sendMessage(...)` — chat

## Wrap-up

After all 7 steps, the student has:
- ✅ Vault registered on Gobi server (real slug)
- ✅ Brain published with their identity (BRAIN.md/jpg/PROMPT.md)
- ✅ One inbox capture (Connect)
- ✅ One Brain Update (Share)
- ✅ Optional custom homepage

What's NOT covered (deliberately) — the student picks these up at their own pace:

- **Merge** stage: weekly distillation from `00. Inbox/` → `20. Literature Notes/`
- **Develop** stage: extracting evergreen claims into `30. Permanent Notes/`
- Voice mode setup (uncomment `voiceSettings` in `.gobi/settings.yaml`, install RVA prompt)
- The 7 CMDS rules (`.claude/rules/`) — read on demand, not memorized
- The 5 CMDS files (`CLAUDE.md`, `AGENTS.md`, `CMDS.md`, `CMDS Guide.md`, `🏛 CMDS Head Quarter.md`) — load when AI agents work in the vault

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| `gobi init` says "already initialized" | `cat .gobi/settings.yaml` — if vaultSlug is set, skip to Step 2 |
| `gobi sync` says "no vault" | run Step 1 first |
| Brain page blank on `gobispace.com` | wait 30 sec for indexing, then refresh; if still blank, `gobi sync --full` |
| `obsidian open` fails | Obsidian must be running with this folder opened as a vault |
| `BRAIN.jpg` won't update on space | filename is case-sensitive; must be exactly `BRAIN.jpg` |
| Wikilinks `[[BRAIN.jpg]]` show as missing in Obsidian | Obsidian indexes asynchronously — restart or wait |

## Resume Logic

If the user says "continue onboarding" / "온보딩 이어서 하자" / "where was I", inspect state and resume:

```bash
# Check progress flags
grep vaultSlug .gobi/settings.yaml         # Step 1 done?
grep selectedSpaceSlug .gobi/settings.yaml # Step 2 done?
grep -q "Your Second Brain" BRAIN.md       # Step 3 NOT done if matches
ls .gobi/sync.db 2>/dev/null               # Step 4 done if exists
ls "00. Inbox/01. Daily Notes/"*.md 2>/dev/null   # Step 5 done if files
gobi brain list-updates --mine --limit 1   # Step 6 done if any
diff app/home.html <(curl -s https://raw.githubusercontent.com/jykim/cmds-vault/main/app/home.html) >/dev/null 2>&1 && echo "default" || echo "customized"  # Step 7
```

Resume from the first failing check.

## References

- `90. Settings/gobi/Skills/gobi-cli/SKILL.md` — full Gobi CLI command reference
- `90. Settings/gobi/Prompts/Create Brain Homepage (CBH).md` — customize `app/home.html`
- `.claude/rules/directory-structure.md` — full numeric folder taxonomy
- `🏛 CMDS Head Quarter.md` — vault navigation hub
- Upstream original: [ai4pkm-vault `gobi-onboarding`](https://github.com/jykim/ai4pkm-vault/tree/main/_Settings_/Skills/gobi-onboarding) — voice-first 5-stage flow this skill simplifies for class use
