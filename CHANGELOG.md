---
type: documentation
aliases:
  - CMDS Starter Kit Changelog
  - cmds-vault changelog
description: "Version history for the cmds-vault public starter kit. Tracks releases, frontmatter syncs from the mothership, and skill additions. Reference when checking what changed between starter-kit versions."
author:
  - "[[구요한]]"
date created: 2026-04-28
date modified: 2026-10-10
tags:
  - CMDS
  - changelog
  - cmds-vault
---

# Changelog

All notable changes to the cmds-vault starter kit are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/).

## [1.3.0] — 2026-10-10

Minor release — agent settings move to a canonical visible folder; `.claude/` becomes symlinks. Same pattern now runs in the author's main vault and LLM Wiki satellite.

### Changed
- **`.claude/rules/` (7 files) moved to `90. Settings/94. Agent Settings/claude/rules/`**, and the duplicate `.claude/commands/` copies (identical to the canonical ones) were removed. `.claude/agents`, `.claude/commands`, `.claude/rules`, `.claude/skills` are now relative symlinks to `90. Settings/94. Agent Settings/claude/…` (git mode 120000). File contents are unchanged except `directory-structure.md`.
- **`directory-structure.md`** — new "점폴더 동기화 정책" section (why dot-folders are not synced, the 5 rules) and relative-symlink setup instead of absolute `<vault-path>` links.
- **README** — "Symlink the .claude/ folder (advanced, optional)" replaced by "Agent settings: canonical folder + `.claude/` symlinks" (why, setup, Windows, upgrade). WELCOME's onboarding exclude list now names the canonical folder.

### Added
- **`90. Settings/94. Agent Settings/setup-agent-links.sh`** — creates/repairs the links, moves files from an old `.claude/` layout into empty canonical folders, backs up differing folders as `*_backup-<timestamp>`, `--check` verify mode.
- **`setup-agent-links.ps1`** — Windows version; falls back to directory junctions when symlink rights (Developer Mode / admin) are missing. Not yet run on a Windows machine — please report issues.

### Why
Obsidian Sync never syncs dot-folders except `.obsidian`. Live-syncing them another way risks `.git` corruption, secrets from `settings.local.json`/`sessions/` spreading, machine-specific hook paths executing elsewhere, symlinks being replicated as real folders and drifting, and cache churn / JSON merge conflicts. Shareable config lives in a normal synced folder; each machine recreates the links once; machine-local settings never sync.

### Upgrade
Pull or unzip the new version, then run `bash "90. Settings/94. Agent Settings/setup-agent-links.sh"` once.

## [1.2.2] — 2026-07-13

Patch release — inbox folder restructure synced from mothership v4.9.5.

### Changed
- **`00. Inbox/08. Unlisted/` → `08. Transcripts/`** — the unused Unlisted placeholder is repurposed as a raw-transcript landing zone with per-source lanes: `08-1. Plaud/`, `08-2. STT/`, `08-3. Manual/`. Two-layer design: this inbox folder is a *queue* (healthy when empty); processed transcript originals belong in an archive folder (mothership convention: `40. Docs/44. Transcripts/`) or their project folder.
- Docs updated to match: `🏛 CMDS Guide.md` folder tree, `CMDS.md` inbox list, `.claude/rules/directory-structure.md` (also drops the stale STT mention from `06. Automation`), and both `inbox.md` command copies.

### Notes
- `08. Capture/` (orchestrator.yaml placeholder) is intentionally untouched; the 08-number collision it creates with the new `08. Transcripts/` is a pre-existing numbering issue to resolve in a future minor release.

## [1.2.1] — 2026-07-03

Patch release — no new files or capabilities; trigger aliases and documentation corrections accumulated since v1.2.0. Cut primarily to unstick the GitHub Releases channel, which had been serving v1.0.0 as Latest while tags advanced to v1.2.0.

### Added
- **cmds-onboarding skill triggers** — '온보딩해줘' and '처음 시작할게' now invoke the onboarding skill (Korean first-run phrases).

### Fixed
- **🏛 CMDS Guide.md author-attribution rule** — DESIGN.md added to the system-file enumeration (`CLAUDE/AGENTS/CMDS/Guide/HQ/DESIGN/WELCOME/README`). It was shipped as the 6th public system file in v1.2.0 but omitted from this list, so onboarding users could mistake it for a user note and overwrite its upstream `author: [[구요한]]` with `[[Me]]`. (Found by the 2026-07-02 mothership system-files audit; merged via PR #14.)
- CHANGELOG `[1.2.0]` compare-link base corrected (v1.1.0 → v1.1.1).

## [1.2.0] — 2026-05-30

### Added
- **DESIGN.md** — added as the 6th public system file, mirroring the mothership's 8→9 restructure (v4.9.0). The kit now grafts 6 of the mothership's 9 system files (ANTIGRAVITY.md remains excluded as Gemini-vendor-specific).

### Changed
- Self-description updated from "5 system files" to "6 system files" across README, WELCOME, CLAUDE.md, CMDS.md.
- Version manifest aligned: `VERSION` → 1.2.0, README `template-version` → 1.2.0, body banners → 2026-05-30.

## [1.1.1] — 2026-05-27

### Changed
- Frontmatter sync from mothership **v4.8.0** (system-file micro-versions: CLAUDE 3.4 / AGENTS 2.4 / CMDS 2.4 / 🏛 CMDS Guide 2.4 / 🏛 CMDS Head Quarter 1.3). Frontmatter only; starter body unchanged.

## [1.1.0] — 2026-05-05

### Added
- **cmds-llm-wiki skill** — Karpathy's LLM Wiki pattern as a sister skill (Session 2.5 prep).
	- 7-stage workflow: ingest → connect → merge → develop → share → lint → status
	- `cmds-llm-wiki/` skill directory with SKILL.md, references, templates
	- 18 web clipper templates for raw source capture
	- 3-layer architecture: Raw Sources → Wiki → Queries

## [1.0.0] — 2026-05-02

### Added
- Initial public release of cmds-vault starter kit.
- 5 system files (CLAUDE.md, AGENTS.md, CMDS.md, 🏛 CMDS Guide.md, 🏛 CMDS Head Quarter.md) adapted from cmds-system-files.
- `.claude/` agent configuration (commands, rules, skills).
- BRAIN.md / BRAIN_PROMPT.md Gobi persona files.
- `90. Settings/` templates and configuration.
- Boldsign + share link removal across all files.
- gobi onboarding/maintenance/cmds skills.
- orchestrator.yaml.

[1.2.2]: https://github.com/johnfkoo951/cmds-vault/compare/v1.2.1...v1.2.2
[1.2.1]: https://github.com/johnfkoo951/cmds-vault/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/johnfkoo951/cmds-vault/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/johnfkoo951/cmds-vault/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/johnfkoo951/cmds-vault/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/johnfkoo951/cmds-vault/releases/tag/v1.0.0
