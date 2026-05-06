---
description: Search LLMWiki/Wiki/ pages, synthesize a cited answer, and (when substantial) save it back into LLMWiki/Queries/ so it compounds.
allowed-tools: Read, Write, Edit, Glob, Grep
---

# /cmds-llm-wiki-query — Lightweight LLM Wiki Query

Answer a question by reading the wiki and synthesizing a cited answer. Substantial answers are filed back into `LLMWiki/Queries/` so the wiki compounds with use.

> **🧭 Prerequisite**: Read `LLMWiki/Core Context.md` once per session. Tailor the answer to one of the user's reuse axes — a good answer connects to at least one axis explicitly.

## Input

`$ARGUMENTS` — the question (Korean or English, sentence form).

## Process

### Step 1: Bootstrap check

If `LLMWiki/` doesn't exist, tell the user `/cmds-llm-wiki-ingest` must run first to create it. Don't auto-bootstrap from query.

### Step 2: Index-first read

Read in this order:
1. `LLMWiki/Core Context.md` — establishes user identity + reuse axes
2. `LLMWiki/index.md` — one-liner catalog of every page; identify candidate pages by topic match

Don't crawl `Wiki/` blindly. The index is the entry point.

### Step 3: Drill into candidate pages

For 3–8 candidate pages identified from the index:
- `Read` each in full
- For each, also read its `source` frontmatter to find the Source files
- If a key claim is referenced, optionally `Read` the relevant `Sources/` file to verify

If the question spans multiple topics, pull pages from each area.

### Step 4: Synthesize

Compose a comprehensive answer:
- Cite **every claim** with `[[wikilinks]]` to the wiki page that supports it.
- For claims sourced from raw material, cite via the wiki page (which in turn cites `Sources/`) — don't directly cite `Sources/` from the user-facing answer.
- Note confidence: high (well-sourced, multiple pages agree) / medium (partial coverage) / low (speculative or conflicting).

### Step 5: Identify gaps

While answering, note:
- **Knowledge gaps** — questions the wiki cannot answer → suggest what to ingest next.
- **Contradictions** — pages that disagree → add `> [!warning] Contradiction` callout to the relevant pages.
- **Missing cross-refs** — concepts that should be linked but aren't → add to `related` properties (an Edit, not a chat-only suggestion).

### Step 6: File back if substantial

If the answer is **substantial** (multi-page synthesis, comparison, analysis worth ~150+ words), file it as a Query Result:

Path: `LLMWiki/Queries/Query - {question slug}.md`

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
reusableFor: "{which reuse axis}"
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
- Append a one-liner to `LLMWiki/index.md` under `## Queries`
- Append a log entry to `LLMWiki/log.md`:

```markdown
## [{YYYY-MM-DD}] query | {short question}

- Pages consulted: [[p1]], [[p2]]
- Filed as: [[Query - {slug}]]
- Axis: {reuse axis}
```

### Step 7: Connect to reuse axis

End the user-facing answer with:

> **이 답변은 {axis}에 활용 가능합니다 — {one-sentence why}.**

(Skip if the answer was a one-liner factual lookup.)

## Output

Reply to the user with:

1. **The answer** — well-cited, organized
2. **Pages consulted** — bullet list of `[[wikilinks]]`
3. **Saved as** — path to query file (or "not saved — single-fact answer")
4. **Gaps** — what the wiki couldn't answer (or "none")
5. **Reuse axis line** — as in Step 7

## Failure modes

- **Synthesizing without citations** → the value of the wiki is lost. Every claim must trace to a wiki page.
- **Skipping the index** → wastes time and risks missing relevant pages.
- **Filing every query** → bloats `Queries/`. Only file substantial syntheses.
- **Citing `Sources/` directly to the user** → confuses the layered architecture. Wiki pages are the synthesis layer; Sources are the immutable layer behind them.
