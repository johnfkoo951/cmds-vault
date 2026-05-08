---
description: Run a health check on LLMWiki — orphan pages, broken links, contradictions, stale claims, missing frontmatter, index drift. Audits Wiki/Queries under {llmWikiPath} and raw sources under {sourcesPath} (CMDS-canonical 10. Raw Sources/).
allowed-tools: Read, Edit, Glob, Grep, Bash
---

# /cmds-llm-wiki-lint — CMDS-Integrated LLM Wiki Health Check

Audit the wiki for drift. Reports issues; **proposes fixes but does not auto-apply them** unless the user confirms.

> **🧭 Prerequisite**: Read `{llmWikiPath}/Core Context.md` once per session — needed for the snapshot-staleness check and pointer-target verification.

## Process

### Step 0: Resolve paths

1. Read `AGENTS.md` (or `CLAUDE.md` fallback) at vault root → extract `llmWikiPath:` (default `LLMWiki`). Call this `{llmWikiPath}`.
2. Read `{llmWikiPath}/Core Context.md` frontmatter → extract `sourcesPath:` (default `10. Raw Sources`). Call this `{sourcesPath}`.

### Step 1: Inventory

Read `{llmWikiPath}/index.md` for the declared catalog. Then enumerate actual files:

```
Glob "{llmWikiPath}/Wiki/*.md"
Glob "{sourcesPath}/**/*.md"            # filter to type: raw-source — other tools may write here too
Glob "{llmWikiPath}/Queries/*.md"
```

Compare counts. Drift here is an early warning.

### Step 2: Orphan check

For every `Wiki/` page, count inbound `[[links]]` from other `Wiki/` pages and `Queries/` files.

```
Grep "[[{page-name}]]" path="{llmWikiPath}/Wiki/" output_mode="files_with_matches"
```

Pages with **zero inbound links** = orphans. Suggest: link from a thematically-related page or remove if obsolete.

### Step 3: Broken link check

Collect every `[[wikilink]]` across `{llmWikiPath}/Wiki/` and `{llmWikiPath}/Queries/`. For each link target, check whether the file exists (`Glob {llmWikiPath}/Wiki/{target}.md`, then `Glob {sourcesPath}/**/{target}.md`). Missing targets = broken links.

For each broken link:
- Suggest creating the page (if the concept is genuinely missing) OR fixing the link (if it's a typo/rename).

**Pointer-target check (Core Context)**: if Core Context is in pointer mode, verify the pointer targets exist (`BRAIN.md`, `🏛 CMDS Head Quarter.md`, `CMDS.md`). Missing target = degraded Core Context.

### Step 4: Contradiction check

Search for `> [!warning] Contradiction` callouts:

```
Grep "Contradiction" path="{llmWikiPath}/Wiki/" output_mode="content"
```

List each, ask the user whether any have been resolved (and the callout can be removed) or escalated (and need fresh sources).

### Step 5: Staleness check

For every `Wiki/` page with `confidence: low` AND `date modified` >90 days old, flag for revisit.

### Step 6: Frontmatter check

For every page in `{llmWikiPath}/Wiki/`, `{sourcesPath}/**/` (filtered to `type: raw-source`), `{llmWikiPath}/Queries/`:
- 7 required properties present? (`type`, `aliases`, `description`, `author`, `date created`, `date modified`, `tags`)
- For raw sources: `collectionPurpose` filled (not empty, not default placeholder)?
- For wiki pages: `source`, `confidence`, `layer` present?
- For queries: `query`, `reusableFor` present?

Report coverage as percentages: e.g., `collectionPurpose: 12/13 raw sources = 92%`.

### Step 7: Index sync

Compare `{llmWikiPath}/index.md` to actual files:
- Files present but not in index → missing entries (suggest adding)
- Index entries with no corresponding file → stale entries (suggest removing)
- Stats table accurate?

### Step 8: Inbox residue check

```
Glob "00. Inbox/**/*.md"
```

For each file in `00. Inbox/`, check whether it was ingested (look for matching `## Original Content` text in `{sourcesPath}/`). If a duplicate exists, the Inbox file should have been MOVED out — flag as residue.

### Step 9: Core Context freshness

Read `{llmWikiPath}/Core Context.md` frontmatter:
- If `status: template` or `status: seeded` → flag (uninitialized or unreviewed).
- If `snapshot_date` >180 days old → suggest re-running `/cmds-llm-wiki-status` to re-seed pointers.

## Output

Report in this format (keep it scannable):

```
🩺 LLMWiki Lint — {YYYY-MM-DD}
──────────────────────────────
📁 Paths
  llmWikiPath: {llmWikiPath}
  sourcesPath: {sourcesPath}

📊 Inventory
  Sources: {n}    Wiki: {n} (Concepts: {n}, Entities: {n}, Guides: {n}, Maps: {n})    Queries: {n}

🦴 Orphans ({n})
  - [[Page A]] — no inbound links
  - ...

🔗 Broken links ({n})
  - [[Page C]] → [[Missing Page]]    (suggest: create | fix to [[Existing Page]])
  - Core Context pointer → {missing target}

⚠️ Contradictions ({n})
  - [[Page D]]: {one-line summary}

📅 Stale ({n})
  - [[Page E]] — confidence: low, modified {N} days ago

🧪 Frontmatter coverage
  - 7-required: {n}/{N} = {pct}%
  - collectionPurpose (raw sources): {n}/{N} = {pct}%
  - confidence (wiki): {n}/{N} = {pct}%

📥 Inbox residue ({n})
  - {file in 00. Inbox/} appears already ingested at {sourcesPath}/{path} — should have been MOVED

📚 Index drift
  - Missing entries: {n}    Stale entries: {n}    Stats accurate: yes/no

🧭 Core Context: {pointer | inline | template} — snapshot {date} ({n} days ago) — {fresh | stale | unreviewed}

🔧 Suggested fixes (top 5)
  1. ...
```

Then ask the user: **"Which fixes should I apply? (numbers, 'all', or 'none')"**

If the user picks specific fixes, apply them via Edit (not Write). Re-run inventory at the end to confirm the issue count dropped.

## Conservative defaults

- Don't auto-delete orphan pages — they may be intentional staging ground.
- Don't auto-resolve contradictions — they need human judgment.
- Don't backfill `collectionPurpose` — that's a "letter to future self"; only the user can write it.
- Don't auto-MOVE Inbox residue — show the user and let them confirm (could be a fresh re-clip the user wants to handle differently).

## Failure modes

- **Auto-applying fixes without confirmation** → trust violation. Always ask.
- **Reporting raw counts without examples** → the user can't act on "5 orphans". List them.
- **Treating low-confidence pages as wrong** → low confidence is information, not error. Stale + low is the lint signal; low alone isn't.
- **Confusing `{sourcesPath}/` with `{llmWikiPath}/Sources/`** → the latter doesn't exist anymore. Sources live in CMDS-canonical `{sourcesPath}` (default `10. Raw Sources`).
