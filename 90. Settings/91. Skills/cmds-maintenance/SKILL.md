---
name: cmds-maintenance
description: Periodic vault maintenance tasks for cmds-vault. Initial scope is HQ Focus Lens — insert/refresh a "currently active categories" lens at the top of 🏛 CMDS Head Quarter.md based on the operator's Current Focus Areas (CMDS.md) and actively-used CMDS subcategories (Permanent Notes frontmatter). Non-destructive — preserves the full 91-category navigation below the lens. Activate when user says "cmds maintenance", "HQ 개인화", "focus lens", "활성 카테고리 갱신", "refresh focus lens", or after a focus shift (new project, new domain, new long-form output).
metadata:
  version: "1.0"
  author: johnfkoo951
  created: 2026-05-02
  base: "https://github.com/johnfkoo951/cmds-vault — Maintenance for personalization that evolves over time"
---

# CMDS Maintenance — Recurring Vault Personalization

Sister skill to `cmds-onboarding` (one-shot setup). Where onboarding fills your vault with first-pass context, **maintenance keeps that context fresh** as your focus shifts. Initial scope: **HQ Focus Lens**.

## When to Use

Activate on any of:
- User says: *"cmds maintenance"*, *"HQ 개인화"*, *"focus lens"*, *"활성 카테고리 갱신"*, *"refresh focus lens"*
- Periodic cadence: monthly, or after any of these life events:
	- New project / new domain / new long-form output
	- Permanent Notes folder reaches 20+ notes (signal: pattern is emerging worth surfacing)
	- CMDS.md `Current Focus Areas` section was edited
- After running `/lint` and noticing HQ no longer reflects daily use

## Maintenance Philosophy

1. **Non-destructive** — never delete categories from HQ. Only *surface the active subset above the full list.*
2. **Two signals, one lens** — combine declarative (CMDS.md `Current Focus Areas`) and descriptive (Permanent Notes' actual `CMDS:` metadata distribution) into a single "active categories" view at HQ top.
3. **Idempotent** — running this skill multiple times must produce stable output (or strictly newer; never accumulate stale entries).
4. **Reversible** — Focus Lens lives between explicit HTML markers (`<!-- focus-lens-start -->` ... `<!-- focus-lens-end -->`). User can clear it at any time by deleting between the markers.
5. **Not authoritative** — the Focus Lens is a *view*, not a source of truth. The 91 categories below it remain the canonical reference.

## Pre-boarding (verify before starting)

| Check | Command | Expected | Fix if fails |
|-------|---------|----------|--------------|
| HQ file exists | `ls "🏛 CMDS Head Quarter.md"` | exists | Run from vault root |
| Focus Lens markers present | `grep -c 'focus-lens-start' "🏛 CMDS Head Quarter.md"` | `1` | Add markers (see § Setup) — first-time use |
| CMDS.md operator profile filled | `grep -c '(Your Name)' CMDS.md` | `0` | Run `cmds-onboarding` first |
| Permanent Notes folder has notes | `find "30. Permanent Notes" -name '*.md' -not -name '.gitkeep' \| wc -l` | non-zero | Run `cmds-onboarding` first (or wait until you have 5+ notes) |

## Setup (first-time only — install Focus Lens markers)

If the Focus Lens markers are not yet in HQ.md, insert them. The recommended location is **right under the H1 title and above the existing top-level navigation** — so the lens is the first thing users see when they open HQ. Default position: line ~10 (after frontmatter close + title heading).

```markdown
# 🏛 CMDS Head Quarter

<!-- focus-lens-start -->
<!-- This section is auto-managed by the cmds-maintenance skill.
     Manual edits will be overwritten on next refresh.
     To disable, delete everything between focus-lens-start and focus-lens-end (including markers). -->

<!-- focus-lens-end -->

[... existing HQ content ...]
```

Once markers are present, this skill manages the section between them.

## Flow

### Step 0 — Greet + state inspection (10 sec)

> **Agent says**: "I'll refresh the Focus Lens at the top of your HQ. Reading your CMDS.md profile and active Permanent Notes now."

Then inspect:

```bash
# Read declarative focus areas from CMDS.md
sed -n '/### Current Focus Areas/,/^###/p' CMDS.md | grep -E "^[0-9]+\. \*\*" | head -10

# Read descriptive CMDS: usage from Permanent Notes
grep -h "^CMDS:" "30. Permanent Notes/"*.md 2>/dev/null | \
  sed 's/.*\[\[📚 \([0-9]*\) [^]]*\]\].*/\1/' | \
  sort | uniq -c | sort -rn | head -10
```

### Step 1 — Compose Focus Lens content (15 sec)

The lens has three parts:

**Part A: 🎯 Current Focus Areas** (declarative — from CMDS.md)
List the 1–4 focus areas verbatim from operator's profile. These are *what they say they are working on*.

**Part B: 🔥 Most-used CMDS subcategories** (descriptive — from Permanent Notes)
Top 4–6 `📚 NXX` subcategories by frequency. These are *what they actually write notes about*. Useful when there's drift between intent and behavior.

**Part C: 📊 Vault snapshot** (informational, single line)
- Total Permanent Notes: `<N>` · Inbox items: `<N>` · Last refresh: `<YYYY-MM-DD>`

### Step 2 — Generate Focus Lens markdown (15 sec)

Template (the agent fills in `<...>` from Step 0/1):

```markdown
<!-- focus-lens-start -->
> **Focus Lens** — auto-refreshed by `cmds-maintenance` skill. Last update: <YYYY-MM-DD>.

### 🎯 Current Focus Areas (declared)

<numbered list, 1–4 items, copied from CMDS.md Current Focus Areas section>

### 🔥 Most-used CMDS subcategories (last <N> Permanent Notes)

| # | Category | Note count |
|---|----------|------------|
<top 4–6 rows by descending count>

### 📊 Vault snapshot

- Permanent Notes: **<N>** · Inbox items: **<N>** · Total wikilinks: **<N>**
- Last lens refresh: **<YYYY-MM-DD>** (from `cmds-maintenance` skill)

> The full 91-category navigation continues below. This lens does not replace it — only surfaces what's currently most active in your vault.
<!-- focus-lens-end -->
```

### Step 3 — Replace lens content in HQ (5 sec)

Use awk or sed to replace content between the markers. This must be **idempotent** — running multiple times overwrites cleanly:

```bash
HQ="🏛 CMDS Head Quarter.md"
LENS_FILE=/tmp/cmds-focus-lens.md

# (Agent has written the new lens content to $LENS_FILE)

awk -v lens="$(cat "$LENS_FILE")" '
  /<!-- focus-lens-start -->/ { print; print lens; in_lens=1; next }
  /<!-- focus-lens-end -->/ { in_lens=0; print; next }
  !in_lens { print }
' "$HQ" > "${HQ}.tmp" && mv "${HQ}.tmp" "$HQ"
```

### Step 4 — Verification (5 sec)

```bash
# Marker integrity
grep -c 'focus-lens-start' "🏛 CMDS Head Quarter.md"  # → 1
grep -c 'focus-lens-end' "🏛 CMDS Head Quarter.md"    # → 1

# Last update line is today
grep "Last update:" "🏛 CMDS Head Quarter.md" | head -1
```

### Step 5 — Wrap-up (5 sec)

> **Agent says**: "Focus Lens refreshed. <N> declared focus areas, top <M> active CMDS categories shown. The full 91-category list is unchanged below. Ran in <X> seconds."

Total time budget: ~1 minute.

## Future Scope (not in v1.0)

The skill is named `cmds-maintenance` plural intentionally. Future maintenance tasks to absorb here:

- **Upstream sync check**: compare local `VERSION` against `https://api.github.com/repos/johnfkoo951/cmds-vault/releases/latest` and tell user if a new vault version is available
- **Authorship lint**: flag any system file whose YAML `author:` field is *not* `[[구요한]]` (false attribution detection — could happen if user batch-replaced too broadly with a pre-1.0.0 ritual)
- **Orphan detection**: notes with no incoming or outgoing links (lighter-weight than full `/lint`)
- **CMDS-vs-index direction lint**: catch `CMDS: "[[🏷 ...]]"` mistakes (📚 vs 🏷 swapped)
- **Stale-status sweep**: notes stuck in `inProgress` for >30 days
- **CHANGELOG auto-stub**: when user makes substantial vault structural changes, suggest a `## [Unreleased]` section in their CHANGELOG fork

Each future capability gets its own section in this SKILL.md and its own *trigger phrase set* — single skill, multiple commands, all idempotent and non-destructive.

## Failure Modes

| Symptom | Cause | Fix |
|---------|-------|-----|
| Markers not found in HQ | First-time use, or user deleted them | Run § Setup to insert markers, then re-run |
| Lens wipes on every refresh (no diff visible) | User has no Permanent Notes yet | Skill produces "📊 Vault snapshot: 0 Permanent Notes" — that's correct, not a bug |
| `Current Focus Areas` section in CMDS.md missing or empty | User skipped Step 6 of `cmds-onboarding` | Run `cmds-onboarding` Step 6 first |
| Multiple top-level `<!-- focus-lens-start -->` markers (corrupted) | User accidentally pasted lens twice | Manual cleanup: keep only the first marker pair, delete the rest, re-run |

## Resume Logic

This skill is single-shot per invocation; no multi-step state to resume. If interrupted between Step 1 and Step 3, the HQ.md remains unchanged (the agent writes to a tmp file first).

## References

- [[🏛 CMDS Head Quarter]] — output target
- [[CMDS]] — input source (`Current Focus Areas` section)
- `30. Permanent Notes/` — input source (frontmatter `CMDS:` distribution)
- Sister skill: `90. Settings/91. Skills/cmds-onboarding/SKILL.md` (one-shot setup; this skill = recurring refresh)
- Origin: feedback from [[김진영]] (Jin Kim) on cmds-onboarding 2026-05-02 — *"HQ 목차도 개인 맞춤화되면 좋겠는데"* (CHANGELOG v1.0.0)
