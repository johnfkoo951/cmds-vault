---
description: Ingest a source (URL, file in 00. Inbox/, file path, raw text) — save verbatim to 10. Raw Sources/{NN. category}/, compile 5–10 wiki pages under {llmWikiPath}/Wiki/, with mandatory user-purpose gate. MOVES sources from Inbox; never duplicates.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# /cmds-llm-wiki-ingest — CMDS-Integrated LLM Wiki Ingest

Ingest source material. **Sources land in CMDS-canonical `10. Raw Sources/{NN. category}/`** (matching upstream cmds-llm-wiki layout), not in `LLMWiki/Sources/`. Wiki pages live in `{llmWikiPath}/Wiki/` (path resolved from `AGENTS.md` frontmatter).

This is the lightweight, in-vault variant of [`cmds-llm-wiki v1.3.0 /ingest`](../../../../../cmds-llm-wiki-v1.3.0/.claude/commands/ingest.md) — mothership-linking, qmd search, Book Ingest, and PostToolUse hooks are stripped. Schema and file naming match upstream so the wiki can be graduated by `mv`.

> **🧭 Prerequisite**: Read `{llmWikiPath}/Core Context.md` first (once per session). It points to canonical CMDS files (`BRAIN.md`, `🏛 CMDS Head Quarter.md`, `CMDS.md`) — follow the pointers to ground identity + reuse axes.

## Input

`$ARGUMENTS` — one of:
- A **URL** → fetch with WebFetch
- A **file path under `00. Inbox/`** → read it; will be **MOVED** to `10. Raw Sources/{cat}/` after verbatim copy
- A **file path elsewhere in the vault** (or absolute path) → read it; **NOT** moved (user-managed location)
- **Raw text** → treat the argument itself as source content

## Process (execute ALL steps in order)

### Step 0: Resolve paths (existence check + LLMWiki/AGENTS.md)

1. Read `AGENTS.md` (or `CLAUDE.md` fallback) frontmatter at vault root.
2. Extract `llmWikiPath:` (default `LLMWiki` if missing). Call this `{llmWikiPath}`.
3. Check `ls "{llmWikiPath}" 2>/dev/null`. If missing, **do not bootstrap here**. Tell the user:
   > "`{llmWikiPath}/` 가 아직 없습니다. 먼저 `/cmds-llm-wiki-status` 를 실행하세요 — 위치를 정하고 (AGENTS.md 에 영구 기록), `Core Context.md` 를 CMDS 표준 파일들에 대한 pointer 로 시드합니다. 그 후 다시 이 명령을 실행해주세요."
   **Stop here.**
4. Read `{llmWikiPath}/Core Context.md`. Extract `sourcesPath:` from its frontmatter (default `10. Raw Sources`). Call this `{sourcesPath}`.
5. Follow Core Context pointers to load reuse axes:
   - `Read("BRAIN.md")` for identity (if exists)
   - `Read("🏛 CMDS Head Quarter.md")` and grep `## Current Focus Areas` (if exists)
   - `Read("CMDS.md")` and extract `📚 NNN` category headings (long-term axes)
   - If none exist, use the inline §1/§2 content from `Core Context.md`.
6. If Core Context `status:` is `template` or `seeded`, gently note: "Core Context 가 아직 검토되지 않았습니다 (`status: {seeded|template}`) — ingest 는 진행하지만, 시간 날 때 `status: active` 로 바꾸시는 게 좋습니다."

### Step 1: Ask Collection Purpose (MANDATORY)

Ask one consolidated question — "letter to future self":

> "미래의 내가 이 자료를 다시 볼 때 — 왜 수집했고, 어디에 쓸 예정인지 한 줄 남겨주세요.
> 재활용 축 (Core Context §2 → HQ Focus Areas / CMDS 카테고리): {list axes resolved in Step 0}.
> 예: '(3) 강의 — 5월 코호트 Session 2.5 자료'"

Rules:
- Ask only this question.
- If the user says "알아서 판단해줘" / "자동으로", infer the most likely axis from source content + axes loaded in Step 0, state the inference + reason explicitly, then proceed.
- Save the answer verbatim into `collectionPurpose` (Source frontmatter).

### Step 2: Fetch & Analyze

- **URL** → `WebFetch(url=$ARGUMENTS, prompt="Return the full article body verbatim. Preserve images as ![alt](url), preserve code blocks, preserve quotes. Do NOT summarize.")`
- **File path under `00. Inbox/`** → `Read` it. Capture its current path for the MOVE step.
- **File path elsewhere** → `Read` it. No MOVE.
- **Raw text** → use `$ARGUMENTS` as-is.

Determine **category** in priority order:
1. Inbox subfolder (if from `00. Inbox/01. Articles/` → Articles, etc.)
2. Web Clipper frontmatter `category:` field
3. Content inference (URL pattern, headings, length)
4. Default: Articles

Category → target subfolder:
| Category | `{sourcesPath}/{NN. category}/` |
|----------|---------------------------------|
| Articles | `{sourcesPath}/11. Articles/` |
| Papers | `{sourcesPath}/12. Papers/` |
| Books | `{sourcesPath}/13. Books/` |
| Transcripts | `{sourcesPath}/14. Transcripts/` |
| Clippings | `{sourcesPath}/15. Clippings/` |

Read the content and extract:
- 3–8 **key concepts** (abstract ideas worth a Wiki page)
- 1–5 **entities** (people, orgs, products)
- 0–2 **practical guides** (how-to)
- Key claims worth fact-tracking
- Connections to existing wiki pages (read `{llmWikiPath}/index.md` to know what exists)

### Step 3: Save Source verbatim to `{sourcesPath}/{NN. category}/`

Create the category subfolder if missing:
```bash
mkdir -p "{sourcesPath}/{NN. category}"
```

Write `{sourcesPath}/{NN. category}/{YYYY-MM-DD}-{slug}.md`:

````markdown
---
type: raw-source
aliases:
  - "{short name}"
description: "{English, 1-2 sentences}"
author:
  - "{original author or [[Unknown]]}"
date created: {today ISO 8601}
date modified: {today ISO 8601}
date ingested: {today ISO 8601}
tags:
  - raw-source
  - {topic tags}
source: "{URL or original file path}"
category: "{Articles|Papers|Books|Transcripts|Clippings}"
collectionPurpose: "{user's verbatim answer from Step 1}"
status: ingested
---

# {Title}

> [!info] Source
> 원본: {URL or original Inbox path}
> 인제스트: {YYYY-MM-DD}

## Original Content
<!-- Verbatim. Do not summarize. Do not abridge. -->

{full source content here}

## Ingest Notes

- {anything you stripped, e.g., obvious clipper duplicates — note here}
````

**Pre-flight before moving on**:
- [ ] `## Original Content` section present and substantive (line count comparable to source)
- [ ] All embedded image markdown preserved (`![alt](url)`)
- [ ] All quote blocks, code blocks, citations preserved
- [ ] All 7 required frontmatter properties present
- [ ] `collectionPurpose` filled
- [ ] YAML uses 2-space indent; wikilinks in YAML are quoted

If verbatim preservation fails, **stop and re-do** before any wiki write or Inbox move. Sources are immutable — they must be right the first time.

### Step 3a: MOVE source out of `00. Inbox/` (if applicable)

If the source originated from `00. Inbox/`:

```bash
rm "00. Inbox/{subfolder}/{original-filename}"
```

This is **mandatory** when source came from Inbox. Inbox is intake; once verbatim-preserved in `{sourcesPath}/`, the original must be removed to prevent re-ingestion on next `/inbox` scan.

| Source origin | Action after Raw Source write |
|---------------|-------------------------------|
| `00. Inbox/{subfolder}/{file}.md` | **Delete** Inbox file |
| URL (WebFetch) | No file to delete |
| Path outside Inbox (user-managed) | No delete |
| Raw text | No file to delete |

> **Why MOVE not COPY**: avoids the duplication the user explicitly called out. Inbox = transient intake. `{sourcesPath}/` = immutable archive. Single source of truth.

### Step 4: Compile Wiki pages (5–10) under `{llmWikiPath}/Wiki/`

For each extracted concept/entity/guide, either **update** an existing page or **create** a new one under `{llmWikiPath}/Wiki/`.

Filename: `{Topic Name}.md` (no date prefix, no folder split — flat for the lightweight version). For CJK person entities, use native script as filename and put romanization in `aliases`.

**Wiki page frontmatter**:

```yaml
---
type: wiki-page
aliases: []
description: "{1-line English}"
author:
  - "Claude"
date created: {today ISO 8601}
date modified: {today ISO 8601}
tags:
  - {topic tags}
source:
  - "[[{source filename without extension}]]"
related:
  - "[[{related wiki page}]]"
confidence: medium
layer: concepts        # or: entities | guides | maps
status: active
---
```

**Body structure**:

```markdown
# {Topic}

> [!tip] Key Insight
> {one-sentence essence}

## Overview
{2-4 sentences}

## Details
{structured by sub-headings — what the source actually says}

## Related
- [[other wiki page]] — {one-line why related}

## Sources
- [[{source filename}]]
```

**When updating an existing page**:
- Add new info under relevant sections (don't duplicate existing claims)
- Append the new source to `source` list
- Add new cross-refs to `related`
- If new info contradicts existing: add a `> [!warning] Contradiction` callout
- Bump `date modified`

**Target: 5–10 wiki pages touched per ingest** (lightweight version is conservative; upstream targets 10–15).

### Step 5: Connect

- Add `[[wikilinks]]` between all related pages — every new page links from at least one existing page (no orphans).
- Cross-link symmetrically: if A → B is added, also add B → A.

### Step 6: Update `{llmWikiPath}/index.md`

For every new page, append a one-liner to the appropriate section (`## Concepts` / `## Entities` / `## Guides` / `## Maps`):

```markdown
- [[{Page Name}]] — {one-line description}
```

Update the Stats table at the top (counts).

### Step 7: Update `{llmWikiPath}/log.md`

Append:

```markdown
## [{YYYY-MM-DD}] ingest | {source title}

- Source: [[{source filename}]]  → `{sourcesPath}/{NN. category}/`
- Inbox cleanup: {moved | n/a (URL) | n/a (external path) | n/a (raw text)}
- **Purpose**: {collectionPurpose verbatim}
- Pages created: [[page1]], [[page2]], ...
- Pages updated: [[page3]], [[page4]], ...
```

### Step 8: Self-review

- Verify the new raw source file exists at `{sourcesPath}/{NN. category}/...md` and has `## Original Content` with substantive body.
- If source came from Inbox: verify the original Inbox file was deleted (`ls "00. Inbox/{subfolder}/"`).
- Verify every new `[[wikilink]]` points to an existing file (use `Glob "{llmWikiPath}/Wiki/{name}.md"`).
- Confirm no duplicate pages were created (a fuzzy match against existing names).
- Confirm `index.md` line count increased by exactly the number of new pages.

## Output

Reply to the user with:

1. **Source**: title + saved path (`{sourcesPath}/{NN. category}/...`)
2. **Inbox cleanup**: moved / n/a (with reason)
3. **Pages created** ({N}): bullet list with one-line each (paths under `{llmWikiPath}/Wiki/`)
4. **Pages updated** ({M}): bullet list with what changed
5. **Connections**: 2–3 most interesting new cross-references
6. **Open questions**: gaps or contradictions discovered (none is fine)
7. **Reuse axis**: which axis from Core Context this source feeds

Keep it tight — under 200 words. The wiki itself is the artifact; the reply is just the receipt.

## Failure modes to watch

- **Summarizing the source instead of preserving verbatim** → Sources are corrupt. Stop, re-do.
- **Skipping the collection-purpose gate** → don't. Even if the user is impatient, ask once. If they refuse, infer-and-state.
- **Creating 20 wiki pages** → too granular. Cap at 10. Better to update existing pages than fork.
- **Forgetting `index.md` / `log.md`** → silent failure.
- **Forgetting the Inbox MOVE** → duplicate ingest on next `/inbox` scan. Step 3a is mandatory.
- **Writing to `{llmWikiPath}/Sources/`** → wrong layout. Sources go to `{sourcesPath}/{NN. category}/`. The old `LLMWiki/Sources/` path is removed.
