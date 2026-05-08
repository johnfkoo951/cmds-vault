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
date modified: 2026-05-07
tags:
  - CMDS
  - skill
  - llm-wiki
license: MIT
metadata:
  upstream: cmds-llm-wiki v1.3.0
  scope: knowledge-management
  version: "0.2.0"
  status: integrated
---

# cmds-llm-wiki — Karpathy LLM Wiki, lightweight in-vault edition

LLM-maintained personal knowledge base inside the user's existing Obsidian vault. The LLM compiles sources into a persistent, cross-referenced wiki once, then keeps it current as new sources arrive — instead of re-retrieving + re-synthesizing on every query (RAG).

## When to use

- User wants to "ingest" an article/paper/transcript and have it integrated into a wiki, not just summarized.
- User asks a question and wants a synthesized, cited answer that compounds back into the wiki.
- User wants to audit the wiki's health (orphans, broken links, contradictions, stale claims).
- User wants a lightweight starting point that can later graduate to a full standalone wiki.

Don't use for: one-off summaries (no compounding needed), code/repo work, transient chats.

## Vault layout (CMDS-integrated, created on first run)

```
{vault root}/
├── AGENTS.md                       # frontmatter `llmWikiPath: "..."` persists the location choice
├── 10. Raw Sources/                # CMDS canonical — sources land here, NOT in {llmWikiPath}/Sources/
│   ├── 11. Articles/
│   ├── 12. Papers/
│   ├── 13. Books/
│   ├── 14. Transcripts/
│   └── 15. Clippings/
└── {llmWikiPath}/                  # default: LLMWiki/ — user picks at first /cmds-llm-wiki-status
    ├── Core Context.md             # POINTER file → BRAIN.md, HQ Focus Areas, CMDS.md (no content dup)
    ├── index.md                    # one-liner catalog of every wiki page
    ├── log.md                      # append-only event log
    ├── Wiki/                       # LLM-maintained synthesis pages
    └── Queries/                    # filed-back Q&A results (compounding)
```

**CMDS-integrated, by design** (v0.2 — driven by walkthrough feedback):
- **Sources live in `10. Raw Sources/`** (CMDS canonical), not `{llmWikiPath}/Sources/`. Single source of truth — sources arriving via Web Clipper to `00. Inbox/` are **MOVED** here on ingest, not copied.
- **Core Context is a pointer file**: §1/§2/§3/§4 link to `BRAIN.md`, `🏛 CMDS Head Quarter#Current Focus Areas`, `CMDS.md`, `🏛 CMDS Guide` respectively. Skill commands dereference at runtime — zero drift, zero snapshot maintenance.
- **Location is configurable**: first run asks where to put `{llmWikiPath}/` and persists the choice to `AGENTS.md` frontmatter (`llmWikiPath:`). Future commands resolve from there.

**Graduation path**: `mv {llmWikiPath}/ ~/my-llm-wiki/` then `mv "10. Raw Sources/" ~/my-llm-wiki/`. Layer the full `cmds-llm-wiki v1.3.0` template on top — schema and file naming match upstream so no content rewrite. (CMDS integration trades graduation simplicity for vault dedup; net win in practice but requires two `mv` steps instead of one.)

**Graph view**: `/cmds-llm-wiki-status` also offers to install `.obsidian/graph.json` with a 4-color-group config (Raw Sources / Wiki / Queries / Core Context) and a path filter that focuses on LLMWiki content. The filter excludes `log.md` and `index.md` from the graph since they accumulate links to every page and obscure the actual cross-reference structure. Open Graph view (`Cmd/Ctrl+G`) to see the structure at a glance. Skipped if your vault already has a customized graph view (you confirm before overwrite).

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
| Source | `10. Raw Sources/{NN. category}/YYYY-MM-DD-{slug}.md` | `10. Raw Sources/11. Articles/2026-04-12-Karpathy-LLM-Wiki.md` |
| Wiki page | `{llmWikiPath}/Wiki/{Topic}.md` | `LLMWiki/Wiki/LLM Wiki Pattern.md` |
| Query | `{llmWikiPath}/Queries/Query - {slug}.md` | `LLMWiki/Queries/Query - RAG vs Compiled Wiki.md` |

Categories: `11. Articles` / `12. Papers` / `13. Books` / `14. Transcripts` / `15. Clippings` (auto-detected from Inbox subfolder, Web Clipper frontmatter, or content inference).

CJK person entities use the native script as filename; romanization goes in `aliases`. Other naming: see [cmds-llm-wiki v1.3.0 CLAUDE.md](../../../../../cmds-llm-wiki-v1.3.0/CLAUDE.md) (the graduation target).

## Core principles (inherited from Karpathy + upstream + CMDS integration)

1. **Sources are immutable.** Verbatim. Always. Live in CMDS-canonical `10. Raw Sources/{NN. category}/`.
2. **No duplication with the host vault.** Sources MOVE from `00. Inbox/` to `10. Raw Sources/` on ingest (single copy). Core Context POINTS to `BRAIN.md` / HQ / `CMDS.md` instead of snapshotting their content.
3. **Wiki is LLM-maintained.** The LLM does the bookkeeping (cross-refs, contradictions, consolidation); the human curates sources and asks questions.
4. **Collection-purpose gate.** Every ingest answers "why am I saving this?" — bound to a reuse axis (HQ Focus Area or `📚 NNN` CMDS category). No purpose, no ingest.
5. **Index-first reads.** Every command reads `Core Context.md` (which dereferences pointers) and `index.md` first. Do not crawl `Wiki/` blind.
6. **Compounding.** Good queries become wiki pages. The wiki gets smarter with use.
7. **Bootstrap from existing knowledge.** `/cmds-llm-wiki-status` is the canonical first command. For CMDS-style vaults it seeds Core Context as pointers to canonical files; for non-CMDS vaults it falls back to inline-seeding axes from sampled notes.
8. **Configurable location.** First run asks where to put `{llmWikiPath}/`; choice is persisted to `AGENTS.md` frontmatter and reused by every subsequent command.
9. **Graduation by copy.** When the wiki outgrows its host vault (~100 sources), move `{llmWikiPath}/` and `10. Raw Sources/` out together; adopt full `cmds-llm-wiki v1.3.0` template — no rewrite.

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
- Web Clipper template bundle (uses host vault's `00. Inbox/` as-is)
- Book Ingest progressive-stub mode
- PostToolUse hooks (verbatim validation, qmd auto-reindex)
- v4 Exploration Gate (`explored: true|false`, Bias Check callouts) — kept optional, not enforced

Kept (so graduation is a copy, not a rewrite):
- 3-layer architecture (Raw Sources → Wiki → Queries)
- Frontmatter schema (7 required + `collectionPurpose`/`confidence`/`layer`)
- File naming conventions
- Ingest → Query → Lint operation cycle
- Index-first reads, append-only log

## Future Work (deferred — not in v0.2)

Captured as ideas; not implemented. Each shifts the skill further toward "CMDS-native" and away from "portable bundle" — open the design tradeoff before tackling.

- **Drop `{llmWikiPath}/index.md`** in favor of letting `cmds-maintenance`'s HQ Focus Lens surface active wiki layers. One less MOC to maintain.
- **Reuse `60. Collections/61. People/` for Wiki entities** — link instead of duplicating; same logic for topic notes under `30. Permanent Notes/`.
- **Add `CMDS:` frontmatter field on wiki pages** (`"[[📚 NNN ...]]"`) so they appear in `🏛 CMDS Head Quarter` navigation and category counts, like Permanent Notes do.
- **Drop `{llmWikiPath}/log.md`** and append ingest events to `BRAIN.md`'s activity section (or whatever the operator's daily activity log is).
- **Bigger reframe**: LLMWiki becomes a *view + ingestion layer* over existing CMDS folders rather than a parallel container — wiki pages get written directly into `30. Permanent Notes/{category}/` with a `wikiSource:` frontmatter field. No `{llmWikiPath}/Wiki/` at all. Most CMDS-native option but **kills the clean graduation story**.
- **Non-CMDS vault config fallback** — when `AGENTS.md` doesn't exist, persist `llmWikiPath` to a small `.cmds-llm-wiki.yml` at vault root instead of failing back to the legacy default silently.
- **Saved graph view alternative** — Obsidian's built-in graph view is single-config. Users wanting LLMWiki view + their existing global view need a community plugin (e.g., Extended Graph). Could ship a sidecar `.obsidian/llmwiki-graph.json` for that workflow.

## Getting started

See `README.md` for install + first-run walkthrough.
