---
name: cmds-onboarding
description: Interview-based vault context capture for cmds-vault. Personalizes BRAIN.md, fills 100 Themes stubs, and optionally fills the CMDS.md Vault Operator profile so AI assistants give context-aware answers from day one. Activate when the user says "cmds onboarding", "context onboarding", "내 컨텍스트로 채워줘", "fill my vault", "personalize my brain", "interview me", or after a fresh clone before exploring slash commands. Complementary to gobi-onboarding (which focuses on Gobi Space publishing).
metadata:
  version: "1.0"
  author: johnfkoo951
  created: 2026-05-01
  base: "https://github.com/johnfkoo951/cmds-system-files"
  cohort: "CMDS x GOBI Cohort 1기 (2026-05) — Session 1 4부 ⭐"
---

# CMDS Onboarding — Vault Context Capture

Interview-led skill that turns the empty cmds-vault into a *vault that knows you*. Total time: **15–20 minutes**. Use **after** WELCOME's batch-replace ritual, or run end-to-end and have this skill drive both.

## When to Use

Activate on any of:
- User says "cmds onboarding", "온보딩", "context onboarding", "내 컨텍스트로 채워줘", "fill my vault", "personalize", "interview me"
- User opens a freshly-cloned `cmds-vault` and says "어떻게 시작하지?" or "where do I start?"
- `BRAIN.md` still contains `(your name)` or `(student / researcher / hobbyist)` placeholders
- `CMDS.md` line 145 still reads `## The Vault Operator: (Your Name)` with the TODO HTML comment intact
- `30. Permanent Notes/` is empty except for `.gitkeep`

This skill is **text-or-voice agnostic**. If the user is in voice mode (Gobi Desktop voice mode active), keep responses short and conversational, ask one question at a time. Otherwise, batch 2–3 questions per turn and use markdown.

## Onboarding Philosophy

1. **Context-first** — fill the vault with *who the user is* before exploring tools. Without context, every `/command` gives a generic answer.
2. **Answer-1-of-many** — the agent asks 5–10 questions per turn but the user only has to answer 1–2. Context accumulates across turns.
3. **Agent-does-the-typing** — the user describes themselves in natural language; the agent writes the structured frontmatter, BRAIN.md sections, and stub notes.
4. **Cohort-friendly** — designed to run *live during 1주차 4부* (15-min budget) and continue at home. Resume logic lets the user pick up where they left off.
5. **Complementary to gobi-onboarding** — this skill fills *vault context*; gobi-onboarding publishes that context to Gobi Space. Run cmds-onboarding first, gobi-onboarding later (or skip Gobi entirely).

## Pre-boarding (verify before starting)

| Check | Command | Expected | Fix if fails |
|-------|---------|----------|--------------|
| Vault root reachable | `ls CMDS.md WELCOME.md` | both files exist | Run from inside cloned `cmds-vault/` folder |
| Claude Code installed | `claude --version` | version string | `npm install -g @anthropic-ai/claude-code` |
| `BRAIN.md` placeholder check | `grep -c '(your name)' BRAIN.md` | `1` (placeholder still there) | If `0`: BRAIN already personalized — confirm user wants to overwrite or skip to Step 5 |
| `[[Me]]` placeholder count | `grep -rln '\[\[Me\]\]' --include='*.md' .` | non-zero (placeholders present) | If empty: WELCOME ritual already done — skip Step 2 |
| `30. Permanent Notes/` empty | `ls "30. Permanent Notes/" \| grep -v gitkeep` | empty output | If has notes: confirm with user before adding stubs |

If any check is unrecoverable, **report state to user and ask whether to skip that step or fix the prerequisite first**.

## Flow

### Step 0 — Greet + scope check (30 sec)

> **Agent says**: "Hi — I'll help you turn this empty cmds-vault into one that knows your domain. About 15 minutes. I'll ask a handful of questions; you only need to answer the ones that feel relevant. The rest I'll leave blank and we'll come back later. Ready?"

Then check if the user has already done the WELCOME author batch-replace:

```bash
grep -rln '\[\[Me\]\]' --include='*.md' . 2>/dev/null | head -3
```

- If output is empty → **skip Step 1·2**, go to Step 3
- If output has files → continue to Step 1

### Step 1 — Pick operator wikilink (1 min)

Ask: *"What name should your `author` field use? Real name, handle, Korean — your call. You can change later."*

Examples:
- Real name: `[[John Doe]]`
- Handle: `[[johndoe]]`
- Korean: `[[홍길동]]`

Capture the choice. Confirm before proceeding.

### Step 2 — Author batch-replace ritual (1 min)

Reuse [[WELCOME]] § "1B. Run the author batch-replace ritual". Either:

**Option A (Claude Code in-context)**:
```
Batch-replace [[Me]] with [[<name>]] across this vault, scope = all .md files.
Use exact-string replace (case-sensitive). After replacing, verify zero residual [[Me]] and report counts per directory.
```

**Option B (shell)**:
```bash
find . -name '*.md' -type f -not -path './.git/*' \
  -exec sed -i '' 's/\[\[Me\]\]/[[<NAME>]]/g' {} +

# Verify
grep -rn '\[\[Me\]\]' --include='*.md' . && echo "REMAINING ABOVE" || echo "ALL CLEAN"
```

Read the verification output to user. If "ALL CLEAN", proceed.

### Step 3 — Persona interview (5–8 min) ⭐ Core

Ask in batches. User answers 1–2 per batch — that's enough.

**Batch A — Current tools & environment**
1. What tools do you currently use to manage knowledge? (Notion / Evernote / Apple Notes / paper / nothing yet)
2. Where do your *files* mostly live? (cloud / local / mixed)
3. How often do you use AI day-to-day? (daily / weekly / rarely)

**Batch B — Domain & expertise**
4. What's your professional / personal domain in 1–2 sentences?
5. Where in your domain do you feel AI is *weak* — what does AI not understand?
6. What 2–3 keywords are *most central* to your domain?

**Batch C — What you want to remember**
7. Imagine 6 months from now: what *one piece of information* do you really not want to lose track of?
8. What types of input do you want to capture most? (articles / meetings / books / conversations / your own ideas / data)

**Batch D — 12-week intent (cohort-specific)**
9. Over the next 12 weeks, what would you like this vault to help you produce? (book / newsletter / better notes / research / nothing in particular — just to think better)
10. If you had to write a one-line "PKM Mission" — what core question are you trying to answer?

**Batch E — Voice & sharing**
11. Who else, if anyone, will read these notes? (just me / partner / team / public)
12. What tone should this vault speak in when AI represents you? (formal / casual / Korean / English / mixed)

After each batch, **summarize what you learned** in 2–3 sentences and ask if the user wants to add or correct anything.

→ See `references/interview-question-bank.md` for extended question pool by domain (researcher / executive / creator / student variants).

### Step 4 — Fill BRAIN.md (2–3 min)

Based on answers, **rewrite** BRAIN.md (don't append — overwrite the placeholder template):

```yaml
---
title: "<NAME>'s Second Brain"
description: "<1–2 sentence Brain summary built from interview>"
thumbnail: "[[BRAIN.jpg]]"
prompt: "[[BRAIN_PROMPT.md]]"
tags:
  - profile
  - second-brain
created: <today YYYY-MM-DD>
---

## About Me

- **Name**: <NAME>
- **Role**: <from interview>
- **Active since**: <YYYY>
- **Areas of interest** (7 areas inferred from interview):
  - <area 1>
  - <area 2>
  - <area 3>
  - ...
  - <area 7>

## How I Use This Vault

<2–3 sentences from Batch C answers about capture patterns>

## What I'm Working Toward

<1–2 sentences from Batch D answers — PKM Mission + 12-week intent>

## Pinned

- [[🏛 CMDS Head Quarter]] — vault navigation hub
- [[🏛 CMDS Guide]] — operational standards
- [[WELCOME]] — first-read onboarding
```

**Show the draft to user**. Ask: "Anything to change before I write?" Wait for confirmation. Then write the file.

→ ⚠️ **Don't change the frontmatter keys** (`title`, `description`, `thumbnail`, `prompt`) — Gobi looks them up by name. Only change values.

### Step 5 — Create 100 Themes stubs (3–5 min) ⭐

Based on Batch B (domain keywords) + Batch C (capture types) + Batch D (intent), suggest 5–10 stub notes for the user's themes. **Show the list** before writing.

For each, propose:
- File name: `30. Permanent Notes/<keyword-slug>.md`
- `type: note`
- `CMDS:` value: choose from `📚 101 Interests / 102 Topics / 103 Variables / 104 Terminologies` based on the keyword's nature
  - **Interest** = ongoing passion (e.g., "재즈", "리더십")
  - **Topic** = subject being explored right now (e.g., "조직 문화", "API 설계")
  - **Variable** = research variable to operationalize (e.g., "팀 응집력", "일일 활동량")
  - **Terminology** = term to define (e.g., "SaaS", "OKR")
- 1–2 sentence body — *why this theme* + *what user wants to find here later*

Template per stub:

```markdown
---
type: note
aliases: []
description: "<English 1–2 sentence — what this theme is about and when to add notes here>"
author:
  - "[[<NAME>]]"
date created: <today>
date modified: <today>
tags:
  - theme
  - <kebab-case-keyword>
CMDS: "[[📚 10X <type>]]"
index: "[[🏷 Research Notes]]"
status: inProgress
---

# <Keyword>

## Why this theme matters to me

<1–2 sentences from interview>

## What I want to capture here

<bullet list of triggers — when to add to this note>

## Connections (to fill as you go)

- (links to other notes will accumulate here)
```

Write all stubs in one batch. Report file count + list.

### Step 6 — (Optional) Fill CMDS.md operator profile (3 min)

Ask: *"Do you want to fill in the operator profile in CMDS.md now, or leave it for later? Skipping is fine."*

If yes, locate `## The Vault Operator: (Your Name)` (around line 145), remove the `<!-- TODO ... -->` HTML comment, and replace with:

```markdown
## The Vault Operator: <NAME>

### Professional Identity

- **Role**: <from interview Batch B>
- **Primary work**: <from interview>
- **Background**: <1-line summary from interview>
- **Areas of expertise**: <2–3 from interview>

### Current Focus Areas (1–4개)

1. <focus from Batch D>
2. <focus from Batch B>
3. (...)

### Primary Activities

- <activity 1 from interview>
- <activity 2>

### PKM Mission

> <one-line mission from Batch D>
```

Confirm with user before writing.

### Step 7 — Wrap-up + cohort handoff (1 min)

Summarize what's done:

- ✅ `[[Me]]` → `[[<NAME>]]` replaced across vault
- ✅ `BRAIN.md` filled with 7 areas of interest + How-I-Use + Pinned
- ✅ `30. Permanent Notes/` has `<N>` theme stubs ready to grow
- ✅ (optional) `CMDS.md` operator profile filled

**Suggest immediate next steps**:

1. Try `/status` — see your vault snapshot
2. Try `/connect "<one thought you have right now>"` — your first capture
3. (Cohort 1주차 학생) Read [[Claude Code 온보딩 인터뷰 가이드]] in the cohort guide pack for the post-class checklist
4. (Optional, later) Run `gobi-onboarding` skill to publish your Brain to Gobi Space

> **Cohort 1주차 학생용 메시지**: "Session 2 (5/9) 입력은 *지금 채운 BRAIN.md + 100 Themes stubs*. 이 상태 유지해주세요. 디테일 보강은 한 주 동안 천천히."

## Resume Logic

If the user says "continue onboarding" / "온보딩 이어서" / "where was I", inspect state and resume:

```bash
# Step 1·2 — author wikilink decided & batch-replaced?
grep -rln '\[\[Me\]\]' --include='*.md' . 2>/dev/null > /tmp/me_residue
[ -s /tmp/me_residue ] && echo "Step 2 NOT done — [[Me]] still present" || echo "Step 1·2 done"

# Step 4 — BRAIN.md personalized?
grep -q '(your name)' BRAIN.md && echo "Step 4 NOT done — placeholder still in BRAIN.md" || echo "Step 4 done"

# Step 5 — 100 Themes stubs created?
THEME_COUNT=$(find "30. Permanent Notes" -name '*.md' -not -name '.gitkeep' | wc -l | tr -d ' ')
[ "$THEME_COUNT" -eq 0 ] && echo "Step 5 NOT done — no theme stubs" || echo "Step 5 done — $THEME_COUNT theme stubs"

# Step 6 — CMDS.md operator profile filled?
grep -q '(Your Name)' CMDS.md && echo "Step 6 NOT done — operator profile still placeholder" || echo "Step 6 done"
```

Resume from the first failing check. Report state to user before resuming.

## Voice Mode Adjustments

When `gobiDesktop_voice_mode == active`:
- One question at a time (not batches)
- Skip the "Show the draft" step in Step 4·5·6 — just write and verbally confirm afterward ("BRAIN.md is now filled with your 7 areas. Want me to read it back?")
- Skip CMDS.md operator profile (Step 6) — it's text-heavy
- Wrap-up in 2 sentences max

## Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| "I have nothing to say to questions" | User feels imposter / blank | Switch to *passive mode* — ask user to read 3 random recent web articles or notes; agent infers themes from those. Then summarize back. |
| User answers everything in one paragraph | Voice user / quick typist | Parse the paragraph: tag each sentence to relevant batch (A–E). Confirm mapping. |
| Agent mis-classifies theme keyword (Interest vs Topic vs ...) | Inherent ambiguity | Default to `📚 102 Topics` (most permissive). User can re-classify with `/connect` later. |
| Stub note overlaps existing one in `30. Permanent Notes/` | User had pre-existing notes | Skip duplicate, log warning. |
| User wants to *only* personalize BRAIN.md, skip 100 Themes | Quick path | Only do Steps 0–4 + 7. Acceptable. |
| User wants to do *whole thing for Gobi Space publishing* | Confused with gobi-onboarding | Run cmds-onboarding to fill context, then immediately invoke gobi-onboarding for publish. |

## What This Skill Does NOT Do

- Run Gobi CLI commands (`gobi init`, `gobi sync`, etc.) → use `gobi-onboarding`
- Capture audio / transcribe → out of scope, use a separate STT pipeline
- Suggest specific note templates beyond stubs → use `/connect` after onboarding
- Build custom Brain homepage → use `Create Brain Homepage (CBH)` prompt

## References

- [[WELCOME]] — first-read doc; Steps 1·2 here mirror its "author batch-replace ritual"
- [[BRAIN.md]] · [[BRAIN_PROMPT.md]] — output targets for Step 4
- [[CMDS]] — output target for Step 6 (Vault Operator section)
- [[🏛 CMDS Guide]] — frontmatter standard for stub notes
- `90. Settings/91. Skills/gobi-onboarding/SKILL.md` — sibling skill for Gobi Space publishing
- `90. Settings/91. Skills/gobi-cli/SKILL.md` — full Gobi CLI reference
- `references/interview-question-bank.md` — extended question pool by domain
- Cohort 1주차 학생용: `70. Outputs/73. Courses/CMDS-Gobi-Cohort-1/Guides/Claude Code 온보딩 인터뷰 가이드.md` (cmds-vault 외부, mothership 위치)
