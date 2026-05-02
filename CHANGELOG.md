---
title: cmds-vault — CHANGELOG
description: "Vault template release history. Each entry maps to a git tag (vX.Y.Z) and lists notable changes to system files, skills, slash commands, rules, and onboarding flow. Reference when checking 'what has changed since I cloned' or planning an upstream sync."
author:
  - "[[구요한]]"
date created: 2026-05-02
date modified: 2026-05-02
tags:
  - changelog
  - vault-versioning
---

# Changelog

All notable changes to **cmds-vault** are tracked here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and [Semantic Versioning](https://semver.org/).

The authoritative version source is the git tag (`git tag --list`) on this repo. The `VERSION` file at vault root mirrors the latest released version. The `template-version` field in `README.md` frontmatter mirrors the same.

---

## [1.0.0] — 2026-05-02

First properly versioned release. Driven by feedback from [[김진영]] (Jin) after running `cmds-onboarding` against a fresh clone (see Cohort 1기 5/2 강의 직전 피드백).

### Added

- **Vault versioning mechanism**:
	- `VERSION` file at vault root (single-line semver)
	- `CHANGELOG.md` (this file)
	- `template-version: "1.0.0"` field in `README.md` frontmatter
	- Authoritative source: git tags (`vX.Y.Z`) on this repo
- **`cmds-maintenance` skill** at `90. Settings/91. Skills/cmds-maintenance/SKILL.md`:
	- Initial scope: HQ Focus Lens (insert/refresh "active categories" section at top of `🏛 CMDS Head Quarter.md` based on operator's Current Focus Areas + actively-used CMDS subcategories from `30. Permanent Notes/`)
	- Non-destructive: preserves all 91 categories, adds compact lens above
	- Designed to run periodically (monthly or when focus shifts) — complementary to one-shot `cmds-onboarding`
- **HQ Focus Lens insertion marker** (`<!-- focus-lens-start --> ... <!-- focus-lens-end -->`) at top of `🏛 CMDS Head Quarter.md` body so `cmds-maintenance` can find/replace cleanly without disturbing the rest of the file

### Changed

- **Authorship policy clarification (BREAKING for batch-replace habits)**:
	- **System files** (CLAUDE.md, AGENTS.md, CMDS.md, 🏛 CMDS Guide.md, 🏛 CMDS Head Quarter.md, WELCOME.md, README.md) now have `author: "[[구요한]]"` in YAML frontmatter — **upstream attribution**, not user placeholder.
	- **User-scope batch-replace**: `cmds-onboarding` Step 2 and WELCOME ritual now restrict `[[Me]]` → `[[<NAME>]]` to **user-scope** only (BRAIN.md, BRAIN_PROMPT.md, `00. Inbox/`, `30. Permanent Notes/`, `20. Literature Notes/`, `60. Collections/`, `90. Settings/91. Templates/`). System files, slash commands, rules, skills, prompts are excluded.
	- Body-text `[[Me]]` inside excluded files (frontmatter examples that show what user-created notes should look like) intentionally remain unchanged — they are placeholder examples, not authorship.
	- Rationale: the previous "all .md" scope created false attribution claims (e.g. a student's batch-replace would falsely mark CLAUDE.md as authored by the student).
- **WELCOME.md** Step 1 § "Authorship policy" — added two-identity explanation; § 1B ritual rewritten with INCLUDE/EXCLUDE scope and updated shell snippet
- **CMDS.md** Essential post-compact item #4 — split into "system files = `[[구요한]]`" vs "user notes = `[[Me]]` placeholder"
- **AGENTS.md** "Author placeholder" callout + Essential item #7 — same two-identity wording
- **CLAUDE.md** "Personal context" callout + Pre-Flight Checklist — same two-identity wording
- **🏛 CMDS Guide.md** "저자 표기 규칙" callout + Properties section — same two-identity wording
- **`cmds-onboarding` SKILL.md** Step 0 (Pre-boarding) and Step 2 (Batch-replace) — scope restricted to user-scope; Resume Logic grep updated to user-scope only

### Notes

- This release is **backward compatible** for clones already personalized via the old "all .md" ritual: those vaults will have system files with `author: [[<student-name>]]` instead of `[[구요한]]`. This is *false attribution* but functionally harmless. To correct, re-clone or run a one-time fix:
	```bash
	# WARNING: only run if you previously batch-replaced [[Me]] across all .md files
	for f in CLAUDE.md AGENTS.md CMDS.md "🏛 CMDS Guide.md" "🏛 CMDS Head Quarter.md" WELCOME.md README.md; do
	  awk 'NR <= 30 && /^  - "\[\[<your-name>\]\]"$/ { gsub(/\[\[<your-name>\]\]/, "[[구요한]]") } { print }' "$f" > "${f}.tmp" && mv "${f}.tmp" "$f"
	done
	```
- Acknowledgment: this release is informed by [[김진영]] (Jin Kim, ai4pkm-vault author) running `cmds-onboarding` against a fresh clone and surfacing both the authorship-scope issue and the missing global versioning. See *Feedback on cmds-onboarding* note in cohort archive.

---

## [Pre-1.0.0] — Prior to 2026-05-02

The vault existed before this changelog began. Notable prior milestones (reconstructed from git log):

- `cc66951` (2026-05-01) — Add useful editor hotkeys
- `60e3286` (2026-05-01) — Add cmds-onboarding skill (interview-based vault context capture)
- `6d5a885` — Integrate jykim's gobi-onboarding fixes (PR #1, polish)
- `f1bb42d` — Refresh system files from main vault, depersonalize for class use (PR #2)
- `a181f4f` — Add Living Book scaffolding for 2026-05 cohort (PR #3)
- `de45cfa` — Move Skills/Prompts to 9x folders, drop app/ and .gobi/ from template
- `476101f` — Ensure Gobi compatibility and add streamlined onboarding skill

For full pre-1.0.0 history, see `git log` on this repo.

[1.0.0]: https://github.com/johnfkoo951/cmds-vault/releases/tag/v1.0.0
