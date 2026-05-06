---
description: Ingest a source (URL/file/text) into LLMWiki/Sources/ and compile 5–10 LLMWiki/Wiki/ pages, with a mandatory user-purpose gate.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash, WebFetch
---

# /cmds-llm-wiki-ingest — Lightweight LLM Wiki Ingest

Ingest source material into the user's `LLMWiki/` folder (created lazily on first run). This is the lightweight, in-vault variant of [`cmds-llm-wiki v1.3.0 /ingest`](../../../../../cmds-llm-wiki-v1.3.0/.claude/commands/ingest.md) — mothership-linking, qmd search, and Book Ingest mode are stripped. Schema and file naming match upstream so the wiki can be graduated by `mv`.

> **🧭 Prerequisite**: Read `LLMWiki/Core Context.md` first (once per session). It defines the user's reuse axes — without it, ingest quality collapses.

## Input

`$ARGUMENTS` — one of:
- A **URL** → fetch with WebFetch
- A **file path** (absolute or relative to vault root) → read it
- **Raw text** → treat the argument itself as the source content

## Process (execute ALL steps in order)

### Step 0: Existence check (defer bootstrap to /status)

Check whether `LLMWiki/` exists at the vault root:

```bash
ls LLMWiki 2>/dev/null
```

If missing, **do not bootstrap here**. Tell the user:

> "`LLMWiki/` 가 아직 없습니다. 먼저 `/cmds-llm-wiki-status` 를 실행하세요 — 본인 vault 의 기존 노트 (예: `30. Permanent Notes/`, `Topics/`) 를 읽고 `Core Context.md` 를 자동으로 시드합니다. 그 후 다시 이 명령을 실행해주세요."

**Stop here.** `/cmds-llm-wiki-status` is the canonical bootstrap entry point — it does the smart Core Context seeding from existing CMDS-style folders, which `/ingest` does not.

If `LLMWiki/` exists, read `LLMWiki/Core Context.md` to get the reuse axes. If `Core Context.md` frontmatter `status` is still `template` or `seeded`, gently note: "Core Context 가 아직 검토되지 않았습니다 (`status: {seeded|template}`) — ingest 는 진행하지만, 시간 날 때 검토하고 `status: active` 로 바꾸시는 게 좋습니다." Then proceed.

### Step 1: Ask Collection Purpose (MANDATORY)

Before any file operation, ask the user ONE consolidated question — "letter to future self":

> "미래의 내가 이 자료를 다시 볼 때 — 왜 수집했고, 어디에 쓸 예정인지 한 줄 남겨주세요.
> 재활용 축 (Core Context §2): {list the user's axes from Core Context.md}.
> 예: '(3) 강의 — 5월 코호트 Session 2.5 자료'"

Rules:
- Ask only this question.
- If the user says "알아서 판단해줘" / "자동으로", infer the most likely axis from source content + Core Context, state the inference + reason explicitly, then proceed.
- Save the answer verbatim into `collectionPurpose` (Source frontmatter).

### Step 2: Fetch & Analyze

- If URL: `WebFetch(url=$ARGUMENTS, prompt="Return the full article body verbatim. Preserve images as ![alt](url), preserve code blocks, preserve quotes. Do NOT summarize.")`
- If file path: `Read` it.
- If raw text: use `$ARGUMENTS` as-is.

Read the content and extract:
- 3–8 **key concepts** (abstract ideas worth a Wiki page)
- 1–5 **entities** (people, orgs, products)
- 0–2 **practical guides** (how-to)
- Key claims worth fact-tracking
- Connections to existing wiki pages (read `LLMWiki/index.md` to know what exists)

### Step 3: Save Source verbatim

Write `LLMWiki/Sources/{YYYY-MM-DD}-{slug}.md` (today's date, kebab-case slug from title):

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
source: "{URL or reference}"
collectionPurpose: "{user's verbatim answer from Step 1}"
status: ingested
---

# {Title}

> [!info] Source
> {URL or file path}

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

If verbatim preservation fails, **stop and re-do** before any wiki write. Sources are immutable — they must be right the first time.

### Step 4: Compile Wiki pages (5–10)

For each extracted concept/entity/guide, either **update** an existing page or **create** a new one under `LLMWiki/Wiki/`.

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

### Step 6: Update `LLMWiki/index.md`

For every new page, append a one-liner to the appropriate section (`## Concepts` / `## Entities` / `## Guides` / `## Maps`):

```markdown
- [[{Page Name}]] — {one-line description}
```

Update the Stats table at the top (counts).

### Step 7: Update `LLMWiki/log.md`

Append:

```markdown
## [{YYYY-MM-DD}] ingest | {source title}

- Source: [[{source filename}]]
- **Purpose**: {collectionPurpose verbatim}
- Pages created: [[page1]], [[page2]], ...
- Pages updated: [[page3]], [[page4]], ...
```

### Step 8: Self-review

- Verify every new `[[wikilink]]` points to an existing file (use `Glob LLMWiki/Wiki/{name}.md`).
- Confirm no duplicate pages were created (a fuzzy match against existing names — if "LLM Wiki" exists, don't create "LLM-Wiki" or "LLM Wiki Pattern" without a deliberate reason).
- Confirm `index.md` line count increased by exactly the number of new pages.

## Output

Reply to the user with:

1. **Source**: title + path
2. **Pages created** ({N}): bullet list with one-line each
3. **Pages updated** ({M}): bullet list with what changed
4. **Connections**: 2–3 most interesting new cross-references
5. **Open questions**: gaps or contradictions discovered (none is fine)
6. **Reuse axis**: which axis from Core Context this source feeds

Keep it tight — under 200 words. The wiki itself is the artifact; the reply is just the receipt.

## Failure modes to watch

- **Summarizing the source instead of preserving verbatim** → Sources are corrupt. Stop, re-do.
- **Skipping the collection-purpose gate** → don't. Even if the user is impatient, ask once. If they refuse, infer-and-state.
- **Creating 20 wiki pages** → too granular. Cap at 10. Better to update existing pages than fork.
- **Forgetting `index.md` / `log.md`** → silent failure. The wiki feels healthy until lint catches drift weeks later.
