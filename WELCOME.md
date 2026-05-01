---
type: documentation
aliases:
  - Welcome
  - Onboarding
  - First Read
description: "First-read onboarding doc for the CMDS starter vault. Walks through the 5 system files, the author placeholder batch-replace ritual, and the first Connect→Merge→Develop→Share cycle. Read this BEFORE the gobi-onboarding skill."
author:
  - "[[Me]]"
date created: 2026-04-28
date modified: 2026-04-28
tags:
  - CMDS
  - onboarding
  - guide
audience: First-time vault user
scope: onboarding
precedence: 0
status: completed
---

# 👋 Welcome to your CMDS Vault

This is your first-read document. It will take **about 15 minutes** end-to-end and gets your vault personalized, your operator profile filled in, and your first Connect→Merge→Develop→Share cycle on paper.

If you read only one thing, read this. Everything else flows from here.

---

## What you just cloned

A **CMDS-conventions starter vault**. CMDS is a Personal Knowledge Management (PKM) system designed by 구요한 (Yohan Koo), running on Obsidian, with optional [Gobi Desktop](https://gobi.app) integration so your vault can publish a public "Brain" page.

The framework you'll use:

- **9 categories** (100 Themes, 200 Literature, ..., 900 Divisions) for classifying knowledge
- **CMDS Process** (Connect → Merge → Develop → Share) for moving knowledge through stages
- **8 slash commands** (`/connect`, `/merge`, `/develop`, `/share`, `/inbox`, `/lint`, `/query`, `/status`) that operate the Process from Claude Code
- **5 system files** that document the conventions for both you and AI assistants
- **3 Brain identity files** (`BRAIN.md`, `BRAIN.jpg`, `BRAIN_PROMPT.md`) for Gobi integration

The canonical, fully-populated reference vault is the operator's own — see [system.cmdspace.work](https://system.cmdspace.work) — but **your vault starts mostly empty**, with conventions baked in. You'll fill it as you go.

---

## Read these in order (10 min)

Before doing anything, skim the 5 system files. You don't need to memorize — just know what each one is *for* so you can return to the right one later.

| # | File | Why read it |
|---|------|-------------|
| 1 | **[[CMDS]]** (precedence 3) | The "story" — what CMDS is, the 9 categories explained, the 4-stage Process |
| 2 | **[[🏛 CMDS Head Quarter]]** (precedence 5) | A flat list of all 91 sub-categories — your map |
| 3 | **[[🏛 CMDS Guide]]** (precedence 4) | The standards — Properties, naming, file prefixes (you'll come back here often) |
| 4 | **[[CLAUDE]]** (precedence 1) | Technical rules for Claude Code (skim only if you'll use Claude Code) |
| 5 | **[[AGENTS]]** (precedence 2) | Same as #4 but for Gemini CLI / Codex / Cursor / etc. |

> 💡 **`precedence`** is the load order if multiple AI assistants are reading docs. Lower number = read first. CLAUDE.md (1) is the most authoritative for code workflows; HQ (5) is just navigation.

---

## 🪪 Step 1 — Personalize your operator profile (5 min)

Right now, the system files refer to you as **`[[Me]]`** (a placeholder wikilink). The vault operator profile in [[CMDS]] is also a placeholder template (`(Your Name)` section). Both need to be filled in.

This is intentional: by shipping placeholders, the starter never assumes a name, but it also marks the spots that **must** become *your* identity for AI assistants to give context-aware answers.

### 1A. Pick your operator wikilink

Decide what name your `author` field should use. Options:

| Option | Example | Pros | Cons |
|--------|---------|------|------|
| Real name | `[[John Doe]]` | Identifies you across notes | Public-facing if you publish vault |
| Handle | `[[johndoe]]` | Pseudonymous, consistent | Less natural in citations |
| Korean | `[[홍길동]]` | Native language ergonomics | Mixed with English elsewhere |

Pick one. You can change later (just re-run the ritual below).

### 1B. Run the "author batch-replace" ritual

Open this vault folder in Claude Code (`cd <vault-path> && claude`). Then paste this prompt verbatim, replacing `<Your Name>` with what you chose:

> **Prompt for Claude Code:**
>
> ```
> Batch-replace `[[Me]]` with `[[<Your Name>]]` across this vault, scope = all .md files in:
> - vault root (CLAUDE.md, AGENTS.md, CMDS.md, 🏛 CMDS Guide.md, 🏛 CMDS Head Quarter.md, BRAIN.md, BRAIN_PROMPT.md, WELCOME.md, README.md)
> - .claude/commands/ (8 files)
> - 90. Settings/94. Agent Settings/claude/commands/ (mirror)
> - 90. Settings/91. Skills/ (gobi-cli, gobi-onboarding)
> - 90. Settings/92. Prompts/
> - 00. Inbox/ (any notes I've already started)
> - 30. Permanent Notes/, 20. Literature Notes/, 60. Collections/ etc.
>
> Use exact-string replace (not fuzzy) — only change `[[Me]]` (case-sensitive).
> After replacing, run a verification grep to confirm zero residual `[[Me]]` and report counts per directory.
> ```

Or, if you prefer the shell:

```bash
cd <your-vault-path>

# Preview first
grep -rn '\[\[Me\]\]' --include='*.md' . | head -30

# Run the replace (macOS / BSD sed)
find . -name '*.md' -type f -not -path './.git/*' \
  -exec sed -i '' 's/\[\[Me\]\]/[[Your Name]]/g' {} +

# Verify zero residue
grep -rn '\[\[Me\]\]' --include='*.md' . && echo "REMAINING ABOVE" || echo "ALL CLEAN"
```

> **Why a wikilink?** Author as `[[Your Name]]` means you can later create a People note `Your Name.md` in `60. Collections/61. People/`, and Obsidian's backlink panel will show every note you authored. This is a standard CMDS pattern.

### 1C. Fill in the operator profile in CMDS.md

Open [[CMDS]] and find the section **"## The Vault Operator: (Your Name)"**. It contains a TODO comment with a template. Fill it with:

- **Role**: 학생 / 연구자 / 전문가 / 프리랜서 / 개인사업자 / 회사원 / 아무거나 — 자기 직업 한 줄
- **Primary work**: 지금 시간을 가장 많이 쓰는 활동
- **Background**: 학력·경력 한 줄 요약
- **Current Focus Areas**: 1-4개 — 지금 가장 활발하게 노트가 쌓일 주제들
- **Primary Activities**: 매일/매주 하는 일

Why this matters: when you ask Claude / Gemini / ChatGPT a question and they have access to CMDS.md, this profile shapes whether they give you a generic answer or a context-aware answer. The richer this section, the smarter your AI assistants get.

### 1D. Personalize BRAIN.md

[[BRAIN]] is the public face of your vault on Gobi Space (if you connect Gobi later). Open it and replace placeholder lines:

- `**Name**: (your name)`
- `**Role**: (student / researcher / hobbyist — anything)`
- `**Areas of interest**: ...`
- The "Pinned" list of notes to highlight

If you don't plan to use Gobi yet, BRAIN.md still acts as your "About Me" page inside the vault.

---

## 🚀 Step 2 — Try the CMDS Process commands (5 min)

The vault ships 8 slash commands that operate the CMDS Process. They live in `.claude/commands/`. To use them, open this vault in Claude Code (`claude` from terminal), then type `/<command>`.

### 2A. Quick orientation (zero dialogs)

```
/status
```

Returns a one-screen snapshot: how many notes per stage, what to do next. On a fresh vault, it'll tell you "everything's empty — start with /inbox or /connect."

### 2B. Capture your first idea (Connect)

Pick something on your mind right now — a question, a fact, a fragment. Then type:

```
/connect "<your idea in one sentence>"
```

The command will (a) classify it as interest/topic/variable/terminology, (b) create a stub note in the Theme stage, (c) link it appropriately. Auto-pilot if input is unambiguous, asks at most 1 question if not.

### 2C. (Later, after you have ~3 notes on the same topic) Synthesize

When you have multiple notes about a topic and want one clean Literature note that integrates them:

```
/merge <topic>
```

This is the heaviest command — it'll dialog with you about purpose, candidate notes, angle, and let you review the draft. The output goes to `30. Permanent Notes/` (or appropriate location) classified as `📚 210 Literature Reviews` (or similar).

### 2D. Health check

After a week or two:

```
/lint inbox
```

Reports orphan notes, contradictions, stale frontmatter. Read-only — won't change anything unless you ask.

### What about /develop, /share, /query?

- `/develop` — when you want to apply a method to data, or build code/prompt/curriculum from existing notes
- `/share` — when you want to turn a synthesized note into a newsletter / slide deck / SNS post (auto-delegates to writer skills)
- `/query` — when you want to ask a question across your vault and have the answer filed back as a permanent note

You don't need all 8 from day one. **`/status`, `/inbox`, `/connect`, `/merge` are the daily core.** The others come in as your vault grows.

Full reference: [[CLAUDE]] "CMDS Process Command Suite" section.

---

## 🌐 Step 3 — Connect Gobi (optional, +10 min)

If you want a public Brain page on Gobi Space:

1. Install [Gobi Desktop](https://gobi.app) or `npm install -g @gobi-ai/cli`
2. Follow the **gobi-onboarding** skill at `90. Settings/91. Skills/gobi-onboarding/SKILL.md`

That skill walks 8 steps from `gobi init` to a published Brain Update on `gobispace.com/@<your-slug>`. Total time ~10 min.

If you don't want Gobi right now, **skip this step**. The vault works fully as a local PKM without Gobi. You can come back later.

---

## 📚 Step 4 — Bookmark these for ongoing reference

Once you're past onboarding, the docs you'll come back to most:

- [[🏛 CMDS Guide]] — when creating a new note and want the right Properties / type / template
- [[🏛 CMDS Head Quarter]] — when you've forgotten which 📚 sub-category a note belongs in
- [[CLAUDE]] "CMDS Process Command Suite" — when you're not sure which slash command to use
- `.claude/rules/frontmatter-standard.md` — when YAML formatting feels fiddly
- `.claude/rules/wikilink-rules.md` — when a wikilink isn't resolving

---

## 🛰 Step 5 — Adding satellite vaults (much later, optional)

The CMDS architecture supports **satellite vaults** — separate Obsidian vaults with specialized purposes (e.g., a Karpathy-style LLM Wiki where an LLM ingests external sources and compiles them into a persistent wiki).

You don't need this from day one. When you do want one:

1. Create a separate Obsidian vault folder (independent git repo recommended)
2. Add a row to the "Satellite Vaults" table in [[🏛 CMDS Head Quarter]] and [[CLAUDE]]
3. Use text references (`→ <Vault Name>: <page name>`) for cross-vault citation since Obsidian wikilinks don't cross vault boundaries
4. Optionally register the satellite with `qmd MCP` or similar so Claude Code can search it from any cwd

The mothership↔satellite convention is fully documented in [[CLAUDE]] "🛰 Satellite Vaults" section. Look at it when needed; ignore until then.

---

## 🪧 Cheatsheet — Daily / Weekly Rhythm

```
하루 시작:        /status                 (방향 잡기)
inbox 가득:       /inbox → /connect       (capture)
주간 정리:        /merge <topic>          (synthesis)
산출물 만들기:     /develop or /share      (artifact)
볼트 위생점검:     /lint <scope>           (read-only)
빠른 질문:        /query <topic>          (검색 + 합성)
```

---

## ✅ Onboarding checklist

- [ ] Read CMDS.md and HQ.md (10 min)
- [ ] Skim 🏛 CMDS Guide and CLAUDE.md (5 min)
- [ ] Pick operator wikilink and run author batch-replace (5 min)
- [ ] Fill in `(Your Name)` profile section in CMDS.md (5 min)
- [ ] Personalize BRAIN.md (5 min)
- [ ] Try `/status` and `/connect` once each (5 min)
- [ ] (Optional) Run gobi-onboarding skill (10 min)

After this, you have a personalized vault ready for daily use. Welcome to CMDS.

---

*This vault redistributes the CMDS conventions originally authored by 구요한 (Yohan Koo). Canonical reference: [system.cmdspace.work](https://system.cmdspace.work). Gobi integration adapted from [ai4pkm-vault](https://github.com/jykim/ai4pkm-vault) by Jin Kim.*
