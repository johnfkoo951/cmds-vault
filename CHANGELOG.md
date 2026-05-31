---
type: documentation
aliases:
  - CMDS Starter Kit Changelog
  - cmds-vault changelog
description: "Version history for the cmds-vault public starter kit. Tracks releases, frontmatter syncs from the mothership, and skill additions. Reference when checking what changed between starter-kit versions."
author:
  - "[[구요한]]"
date created: 2026-04-28
date modified: 2026-05-30
tags:
  - CMDS
  - changelog
  - cmds-vault
---

# Changelog

All notable changes to the cmds-vault starter kit are documented here.
The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project uses [Semantic Versioning](https://semver.org/).

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

[1.2.0]: https://github.com/johnfkoo951/cmds-vault/compare/v1.1.1...v1.2.0
[1.1.1]: https://github.com/johnfkoo951/cmds-vault/compare/v1.1.0...v1.1.1
[1.1.0]: https://github.com/johnfkoo951/cmds-vault/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.com/johnfkoo951/cmds-vault/releases/tag/v1.0.0
