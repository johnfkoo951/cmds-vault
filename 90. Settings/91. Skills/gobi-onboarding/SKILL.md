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

**Why first**: this creates `.gobi/settings.yaml` with the real `vaultSlug` and registers the server-side Brain. The repo intentionally does NOT ship `.gobi/` — it must come from `gobi init` so the slug is correct.

```bash
cd /path/to/cmds-vault
gobi init
```

Gobi will:
1. Confirm your Google account
2. Ask "Use existing vault or create new?" — pick **create new**, name it (e.g. `cmds-class-2026`)
3. Create `.gobi/settings.yaml` with the auto-generated slug
4. Notice the `BRAIN.md` we ship and leave it alone (won't overwrite)

**Verify**:
```bash
ls .gobi/settings.yaml
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

### Step 3 — Tell Gobi what to sync (30 sec)

`gobi init` doesn't create `.gobi/syncfiles` for you. Drop one in with the three Brain identity files:

```bash
cat > .gobi/syncfiles <<'EOF'
/BRAIN.jpg
/BRAIN.md
/BRAIN_PROMPT.md
EOF
```

Add `/app/home.html` to that file later, after Step 8 (custom homepage). Each line is a path or glob inside the vault.

### Step 4 — Personalize the Brain (3 min)

Three files describe who this Brain is:

1. **`BRAIN.md`** — the public profile. Replace the "Your Second Brain" template with your name, role, interests, pinned notes.
2. **`BRAIN.jpg`** — the thumbnail. Drop a square 512×512+ JPG/PNG, name it exactly `BRAIN.jpg`. (We ship the CMDS round logo as a placeholder — replace it.)
3. **`BRAIN_PROMPT.md`** — the system prompt for Gobi chat. Define your Brain's voice, scope, refusals.

Open all three:
```bash
obsidian open file=BRAIN.md
obsidian open file=BRAIN_PROMPT.md

# Open BRAIN.jpg in your OS's default image viewer:
#   macOS:   open BRAIN.jpg
#   Linux:   xdg-open BRAIN.jpg
#   Windows: start BRAIN.jpg
# Or just drag a new image onto BRAIN.jpg in your file manager.
```

**Don't change** the frontmatter keys (`title`, `description`, `thumbnail`, `prompt`) — Gobi looks them up by name. (`homepage` is added in Step 8 if you want a custom Brain page.)

### Step 5 — First sync (1 min)

```bash
gobi sync --dry-run    # preview — should show 3 files to upload
gobi sync              # actually upload
```

You should see uploads for: `BRAIN.md`, `BRAIN.jpg`, `BRAIN_PROMPT.md`. (Pattern lives in `.gobi/syncfiles` — edit if you want to sync more.)

**Verify on Gobi Space**: open `https://gobispace.com/@<your-vault-slug>` in a browser. The Brain page shows your thumbnail, title, description, and uses Gobi's default homepage rendering.

To replace the default homepage with a custom HTML page, do Step 8.

### Step 6 — First capture (2 min) — *Connect*

Time to write your first note. Pick something on your mind right now — a question, a fact, a fragment.

The note must satisfy CMDS frontmatter standard (`.claude/rules/frontmatter-standard.md`): all 7 properties (`type`, `aliases`, `description`, `author`, `date created`, `date modified`, `tags`). Filename is kebab-case `YYYY-MM-DD-description.md` per `.claude/rules/file-creation-rules.md`.

```bash
today=$(date +%Y-%m-%d)
now=$(date +%Y-%m-%dT%H:%M)

cat > "00. Inbox/01. Daily Notes/${today}-first-capture.md" <<EOF
---
type: note
aliases: []
description: "First inbox capture written during cmds-vault onboarding. Placeholder until I have something specific to think about."
author:
  - "[[Me]]"
date created: ${now}
date modified: ${now}
tags:
  - inbox
  - onboarding
---

## What I'm thinking about today

EOF

obsidian open file="${today}-first-capture.md"
```

Write 3-5 lines under the heading. Don't aim for permanent — this is the **Connect** stage, fast & loose. Replace `[[Me]]` with your own People note once you have one.

**Why `00. Inbox/`?** The CMDS taxonomy treats inbox as the universal landing zone. See `.claude/rules/directory-structure.md` for the full layout.

### Step 7 — First Brain Update (2 min) — *Share*

Brain Updates are how your vault talks to the Gobi space. Even if you have nothing distilled yet, share the fact that you exist:

```bash
gobi brain post-update \
  --title "Hello — my Second Brain is online" \
  --content "Just finished CMDS-conventions vault setup with Gobi. First topic on my mind: <write 1-2 sentences about something you want to think about this week>."
```

**Verify**: refresh `https://gobispace.com/@<your-vault-slug>` — you should see the update at the top.

### Step 8 — Custom homepage (optional, 3 min)

By default, Gobi Space renders a built-in homepage from `BRAIN.md`. To replace it with custom HTML:

1. Open `90. Settings/92. Prompts/Create Brain Homepage (CBH).md` in Claude Code
2. Run the prompt with your customization request:
   - "Build me a homepage from scratch with a hero, 3-card grid, and recent BU list"
   - "Add a quote rotator at top"
3. CBH creates `app/home.html` (and the `app/` folder if needed) and auto-wires `BRAIN.md` (adds `homepage: "[[app/home.html]]"` frontmatter) and `.gobi/syncfiles` (appends `/app/home.html`). No manual edits needed.
4. `gobi sync` to push

The `window.gobi` API surface CBH can use inside `app/home.html`:
- `gobi.vault` — `{title, description, thumbnailPath, vaultId, webdriveUrl}`
- `gobi.listBrainUpdates({limit, cursor})` — paginated updates
- `gobi.getSessions({limit})` — chat sessions
- `gobi.loadMessages(sessionId)`, `gobi.sendMessage(...)` — chat

## Wrap-up

After all 8 steps, the student has:
- ✅ Vault registered on Gobi server (real slug)
- ✅ Brain published with their identity (BRAIN.md/jpg/PROMPT.md)
- ✅ One inbox capture (Connect)
- ✅ One Brain Update (Share)
- ✅ Optional custom homepage

What's NOT covered (deliberately) — the student picks these up at their own pace:

- **Merge** stage: weekly distillation from `00. Inbox/` → `20. Literature Notes/`
- **Develop** stage: extracting evergreen claims into `30. Permanent Notes/`
- Voice mode setup — out of scope for this vault. To enable: copy a voice prompt (e.g. ai4pkm-vault's [`Real-time Voice Assistant (RVA).md`](https://github.com/jykim/ai4pkm-vault/blob/main/_Settings_/Prompts/Real-time%20Voice%20Assistant%20%28RVA%29.md)) into `90. Settings/92. Prompts/`, then add a `voiceSettings:` block to `.gobi/settings.yaml` referencing that path
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
ls .gobi/settings.yaml 2>/dev/null && grep vaultSlug .gobi/settings.yaml          # Step 1 done?
grep -q selectedSpaceSlug .gobi/settings.yaml 2>/dev/null && echo "Step 2 done"   # Step 2
ls .gobi/syncfiles 2>/dev/null && echo "Step 3 done"                              # Step 3
grep -q "Your Second Brain" BRAIN.md && echo "Step 4 NOT done" || echo "Step 4 done"  # Step 4 not done if template still present
ls .gobi/sync.db 2>/dev/null && echo "Step 5 done"                                # Step 5 done if sync.db exists
ls "00. Inbox/01. Daily Notes/"*.md 2>/dev/null | head -1                         # Step 6 done if any file
gobi brain list-updates --mine --limit 1 2>/dev/null                              # Step 7 done if any
ls app/home.html 2>/dev/null && echo "Step 8 done (app/home.html exists)"         # Step 8
```

Resume from the first failing check.

## References

- `90. Settings/91. Skills/gobi-cli/SKILL.md` — full Gobi CLI command reference
- `90. Settings/92. Prompts/Create Brain Homepage (CBH).md` — build a custom Brain page
- `.claude/rules/directory-structure.md` — full numeric folder taxonomy
- `🏛 CMDS Head Quarter.md` — vault navigation hub
- Upstream original: [ai4pkm-vault `gobi-onboarding`](https://github.com/jykim/ai4pkm-vault/tree/main/_Settings_/Skills/gobi-onboarding) — voice-first 5-stage flow this skill simplifies for class use
