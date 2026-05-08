---
description: Search {llmWikiPath}/Wiki/ pages, synthesize a cited answer, and (when substantial) save it back into {llmWikiPath}/Queries/ so it compounds. Reads sources from CMDS-canonical 10. Raw Sources/ when verification needed.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /cmds-llm-wiki-query — CMDS-Integrated LLM Wiki Query

Answer a question by reading the wiki and synthesizing a cited answer. Substantial answers are filed back into `{llmWikiPath}/Queries/` so the wiki compounds with use.

> **🧭 Prerequisite**: Read `{llmWikiPath}/Core Context.md` once per session — it points to canonical CMDS files (`BRAIN.md`, `🏛 CMDS Head Quarter.md`, `CMDS.md`). Tailor the answer to one of the user's reuse axes (HQ Focus Areas + CMDS categories) — a good answer connects to at least one axis explicitly.

## Input

`$ARGUMENTS` — the question (Korean or English, sentence form).

## Process

### Step 0: Resolve paths

1. Read `AGENTS.md` (or `CLAUDE.md` fallback) at vault root → extract `llmWikiPath:` (default `LLMWiki`). Call this `{llmWikiPath}`.
2. Read `{llmWikiPath}/Core Context.md` frontmatter → extract `sourcesPath:` (default `10. Raw Sources`). Call this `{sourcesPath}`.
3. If `{llmWikiPath}/` doesn't exist: tell the user to run `/cmds-llm-wiki-status` first to bootstrap. Don't auto-bootstrap from query.

### Step 1: Index-first read

Read in this order:
1. `{llmWikiPath}/Core Context.md` — establishes user identity + reuse axes (follow pointers to `BRAIN.md`, `🏛 CMDS Head Quarter.md`, `CMDS.md` as needed)
2. `{llmWikiPath}/index.md` — one-liner catalog of every page; identify candidate pages by topic match

Don't crawl `Wiki/` blindly. The index is the entry point.

### Step 2: Drill into candidate pages

For 3–8 candidate pages identified from the index:
- `Read` each in full
- For each, also read its `source` frontmatter to find the raw source files (located under `{sourcesPath}/{NN. category}/`)
- If a key claim needs verification, optionally `Read` the relevant raw source file from `{sourcesPath}/`

If the question spans multiple topics, pull pages from each area.

### Step 3: Synthesize

Compose a comprehensive answer:
- Cite **every claim** with `[[wikilinks]]` to the wiki page that supports it.
- For claims sourced from raw material, cite via the wiki page (which in turn cites the raw source under `{sourcesPath}/`) — don't directly cite raw sources from the user-facing answer.
- Note confidence: high (well-sourced, multiple pages agree) / medium (partial coverage) / low (speculative or conflicting).

### Step 4: Identify gaps

While answering, note:
- **Knowledge gaps** — questions the wiki cannot answer → suggest what to ingest next.
- **Contradictions** — pages that disagree → add `> [!warning] Contradiction` callout to the relevant pages.
- **Missing cross-refs** — concepts that should be linked but aren't → add to `related` properties (an Edit, not a chat-only suggestion).

### Step 5: File back if substantial

If the answer is **substantial** (multi-page synthesis, comparison, analysis worth ~150+ words), file it as a Query Result:

Path: `{llmWikiPath}/Queries/Query - {question slug}.md`

```yaml
---
type: query-result
aliases: []
description: "{1-line English}"
author:
  - "Claude"
date created: {today ISO 8601}
date modified: {today ISO 8601}
tags:
  - query-result
  - {topic tags}
query: "{the original question verbatim}"
source:
  - "[[{wiki page consulted 1}]]"
  - "[[{wiki page consulted 2}]]"
reusableFor: "{which reuse axis — HQ Focus Area or CMDS category}"
status: active
---

# {Question}

## Answer
{the synthesized answer}

## Sources consulted
- [[{wiki page 1}]]
- [[{wiki page 2}]]

## Gaps surfaced
- {what the wiki couldn't answer}
```

If the answer is a **simple factual lookup** (a date, a definition, a name), just reply — don't file.

After filing:
- Append a one-liner to `{llmWikiPath}/index.md` under `## Queries`
- Append a log entry to `{llmWikiPath}/log.md`:

```markdown
## [{YYYY-MM-DD}] query | {short question}

- Pages consulted: [[p1]], [[p2]]
- Filed as: [[Query - {slug}]]
- Axis: {reuse axis}
```

### Step 6: Connect to reuse axis

End the user-facing answer with:

> **이 답변은 {axis}에 활용 가능합니다 — {one-sentence why}.**

(Skip if the answer was a one-liner factual lookup.)

## Output

Reply to the user with:

1. **The answer** — well-cited, organized
2. **Pages consulted** — bullet list of `[[wikilinks]]`
3. **Saved as** — path to query file (or "not saved — single-fact answer")
4. **Gaps** — what the wiki couldn't answer (or "none")
5. **Reuse axis line** — as in Step 6

## Failure modes

- **Synthesizing without citations** → the value of the wiki is lost. Every claim must trace to a wiki page.
- **Skipping the index** → wastes time and risks missing relevant pages.
- **Filing every query** → bloats `Queries/`. Only file substantial syntheses.
- **Citing raw sources directly to the user** → confuses the layered architecture. Wiki pages are the synthesis layer; raw sources under `{sourcesPath}/` are the immutable layer behind them.
