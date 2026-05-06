---
name: cmds-llm-wiki
type: skill
aliases:
  - LLM Wiki
  - Karpathy Wiki
description: Build & maintain a Karpathy-style LLM Wiki inside your current Obsidian vault. Use when the user wants to ingest sources, query a compounding wiki, lint it, or check status. Creates a self-contained `LLMWiki/` folder that can later graduate into a full standalone vault (cmds-llm-wiki).
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash(ls:*)
  - Bash(mkdir:*)
  - Bash(wc:*)
  - WebFetch
author:
  - "[[구요한]]"
date created: 2026-05-05
date modified: 2026-05-05
tags:
  - CMDS
  - skill
  - llm-wiki
license: MIT
metadata:
  upstream: cmds-llm-wiki v1.3.0
  scope: knowledge-management
  version: "0.1.0"
  status: initial
---

# cmds-llm-wiki — Karpathy LLM Wiki, lightweight in-vault edition

LLM-maintained personal knowledge base inside the user's existing Obsidian vault. The LLM compiles sources into a persistent, cross-referenced wiki once, then keeps it current as new sources arrive — instead of re-retrieving + re-synthesizing on every query (RAG).

## When to use

- User wants to "ingest" an article/paper/transcript and have it integrated into a wiki, not just summarized.
- User asks a question and wants a synthesized, cited answer that compounds back into the wiki.
- User wants to audit the wiki's health (orphans, broken links, contradictions, stale claims).
- User wants a lightweight starting point that can later graduate to a full standalone wiki.

Don't use for: one-off summaries (no compounding needed), code/repo work, transient chats.

## Wiki layout (created on first run)

```
LLMWiki/                    # self-contained — copy this folder out to graduate
├── Core Context.md         # who/why/reuse-axes — read FIRST by every command
├── index.md                # one-liner catalog of every page
├── log.md                  # append-only event log
├── Sources/                # raw, immutable original docs
├── Wiki/                   # LLM-maintained synthesis pages
└── Queries/                # filed-back Q&A results (compounding)
```

**Why self-contained**: graduation = `mv LLMWiki/ ~/my-llm-wiki/`. Open as new Obsidian vault, layer the full `cmds-llm-wiki v1.3.0` template on top — no rewrite needed because schema and naming match upstream.

## Commands

| Command | What it does |
|---------|--------------|
| `/cmds-llm-wiki-ingest <URL\|file\|note>` | Ask collection-purpose, save raw source verbatim, compile 5–10 wiki pages, update index/log |
| `/cmds-llm-wiki-query <question>` | Read Core Context + index, synthesize a cited answer, file good answers back into `Queries/` |
| `/cmds-llm-wiki-lint` | Health-check: orphans, broken links, contradictions, stale claims, missing frontmatter |
| `/cmds-llm-wiki-status` | One-screen overview: counts, recent activity, top-linked pages |

Each command is implemented as a markdown prompt in `commands/`.

## Schema (subset of upstream cmds-llm-wiki — graduation-compatible)

Every page carries the 7 required CMDS frontmatter properties (`type`, `aliases`, `description`, `author`, `date created`, `date modified`, `tags`) plus layer-specific extensions:

```yaml
---
type: wiki-page          # or: raw-source, query-result, core-context
aliases: []
description: ""          # English, 1-2 sentences for LLM relevance
author: ["Claude"]
date created: YYYY-MM-DDTHH:mm
date modified: YYYY-MM-DDTHH:mm
tags: []
source: []               # ["[[raw-source-link]]"] for wiki pages
related: []              # ["[[other-page]]"]
collectionPurpose: ""    # filled by /cmds-llm-wiki-ingest — "letter to future self"
confidence: medium       # high | medium | low
layer: concepts          # concepts | entities | guides | maps
status: active
---
```

Naming (matches upstream):

| Layer | Pattern | Example |
|-------|---------|---------|
| Source | `Sources/YYYY-MM-DD-{slug}.md` | `Sources/2026-04-12-Karpathy-LLM-Wiki.md` |
| Wiki page | `Wiki/{Topic}.md` | `Wiki/LLM Wiki Pattern.md` |
| Query | `Queries/Query - {slug}.md` | `Queries/Query - RAG vs Compiled Wiki.md` |

CJK person entities use the native script as filename; romanization goes in `aliases`. Other naming: see [cmds-llm-wiki v1.3.0 CLAUDE.md](../../../../../cmds-llm-wiki-v1.3.0/CLAUDE.md) (the graduation target).

## Core principles (inherited from Karpathy + upstream)

1. **Sources are immutable.** Verbatim. Always.
2. **Wiki is LLM-maintained.** The LLM does the bookkeeping (cross-refs, contradictions, consolidation); the human curates sources and asks questions.
3. **Collection-purpose gate.** Every ingest answers "why am I saving this?" — bound to a reuse axis from `Core Context.md`. No purpose, no ingest.
4. **Index-first reads.** Every command reads `Core Context.md` and `index.md` first. Do not crawl `Wiki/` blind.
5. **Compounding.** Good queries become wiki pages. The wiki gets smarter with use.
6. **Bootstrap from existing knowledge.** `/cmds-llm-wiki-status` is the canonical first command and seeds `Core Context.md` from existing CMDS-style folders (`30. Permanent Notes/`, `Topics/`, `60. Collections/`, `20. Literature Notes/`, `Roundup/`). Users start from their own knowledge, not a blank template — the same Compounding principle, applied at setup time.
7. **Graduation by copy.** When the wiki outgrows its host vault (~100 sources, ~400K words), move `LLMWiki/` out and adopt the full `cmds-llm-wiki v1.3.0` template — no rewrite.

## Conformance

This skill follows existing CMDS rules — does not redefine them:

- **Indentation**: YAML 2 spaces, body TAB → cmds-vault `CLAUDE.md` + cmds-system-files `rules/indentation-rules.md`
- **Wikilinks**: quoted in YAML (`"[[link]]"`), unquoted in body → `wikilink-rules.md`
- **Frontmatter**: 7 required properties → `frontmatter-standard.md`
- **File creation**: respect output paths and naming → `file-creation-rules.md`

Sister skills in cmds-vault (`gobi-cli`, `cmds-onboarding`, `cmds-maintenance`, `daily-book-update`) follow the same conventions and live under the same `90. Settings/91. Skills/` path.

For broken-link checking inside `/cmds-llm-wiki-lint`, defer to the existing `obsidian-links` Claude skill.
For frontmatter validation, defer to the existing `obsidian-yaml-frontmatter` skill.

## Differences from full LLMWiki (cmds-llm-wiki v1.3.0)

Stripped (graduation-only features):
- Mothership-vault cross-linking (`mainVaultRelated`, `mainVaultCmds`, `source-vault`)
- qmd vector search (uses Glob+Grep instead — fine up to ~100 sources)
- Web Clipper integration (`00. Inbox/` subfolders, batch ingest)
- Book Ingest progressive-stub mode
- PostToolUse hooks (verbatim validation, qmd auto-reindex)
- v4 Exploration Gate (`explored: true|false`, Bias Check callouts) — kept optional, not enforced

Kept (so graduation is a copy, not a rewrite):
- 3-layer architecture (Sources → Wiki → Queries)
- Frontmatter schema (7 required + `collectionPurpose`/`confidence`/`layer`)
- File naming conventions
- Ingest → Query → Lint operation cycle
- Index-first reads, append-only log

## Getting started

See `README.md` for install + first-run walkthrough.
