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

## [1.1.0] — 2026-05-05

Driven by 2026-05 코호트 Session 2.5 ("LLMWiki Deep Dive") preparation. Adds Karpathy's LLM Wiki pattern to the vault as a sister skill alongside `gobi-cli`, `cmds-onboarding`, `cmds-maintenance`, `daily-book-update`.

### Added

- **`cmds-llm-wiki` skill** at `90. Settings/91. Skills/cmds-llm-wiki/`:
	- 4 slash commands: `/cmds-llm-wiki-ingest`, `/cmds-llm-wiki-query`, `/cmds-llm-wiki-lint`, `/cmds-llm-wiki-status`
	- Builds a self-contained `LLMWiki/` folder (Sources / Wiki / Queries / index / log / Core Context) inside the host vault — does not entangle with existing CMDS folders (`30. Permanent Notes/`, `60. Collections/`, etc.)
	- Schema-compatible with [`cmds-llm-wiki v1.3.0`](https://github.com/johnfkoo951/cmds-llm-wiki) (matching frontmatter keys: `type`, `collectionPurpose`, `confidence`, `layer`, etc., and matching naming: `Sources/YYYY-MM-DD-{slug}.md`, `Wiki/{Topic}.md`, `Queries/Query - {slug}.md`)
	- Mandatory collection-purpose gate ("미래의 나에게 보내는 편지") on every ingest, bound to the user's reuse axes in `Core Context.md`
	- Targets 5–10 wiki pages per ingest (lightweight cap; upstream targets 10–15)
	- Stripped (graduation-only): mothership cross-linking, qmd vector search, Web Clipper integration, Book Ingest progressive stubs, PostToolUse hooks
- **Templates** under `90. Settings/91. Skills/cmds-llm-wiki/templates/`: `Core Context.md`, `index.md`, `raw-source.md`, `wiki-page.md` — first-run skeletons used by the bootstrap flow inside `/cmds-llm-wiki-status`

### Changed (post-release iteration based on first real-usage walkthrough)

- **`/cmds-llm-wiki-status` is now the canonical bootstrap command.** When `LLMWiki/` doesn't exist, status creates the skeleton AND **smart-seeds `Core Context.md`** by sampling 5–15 notes from existing CMDS-style folders (`30. Permanent Notes/`, `Topics/`, `60. Collections/`, `20. Literature Notes/`, `Roundup/`) — inferring §1 (identity) and §2 (5–9 reuse axes) from real content. Eliminates the "fill the blank template before you can ingest" friction.
- **`Core Context.md` `status:` field gains a `seeded` value** alongside `template` / `active`. Auto-seeded contexts land as `seeded` so `/lint` and the user know it needs review before being treated as authoritative.
- **`/cmds-llm-wiki-ingest` no longer auto-bootstraps** — when `LLMWiki/` is missing it cleanly redirects the user to run `/cmds-llm-wiki-status` first. Keeps ingest focused on ingestion, not setup.
- **Install docs add `/reload-plugins`** as the post-install step (faster than restarting Claude Code). Restart remains the documented fallback.
- **Lecture (Session 2.5) hands-on block** updated to match: shows `/reload-plugins`, explains the `/status`-driven Core Context auto-seed, and demonstrates first ingest with a file path (`{your_first_file}`) rather than a URL — file paths are more reliable for first-time users.

### Graduation path

When the in-vault wiki outgrows the host vault (~100 sources, ~400K words), `mv LLMWiki/ ~/my-llm-wiki` and layer the full `cmds-llm-wiki v1.3.0` template on top — no rewrite needed because schema matches.

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
