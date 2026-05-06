---
description: Run a health check on LLMWiki — orphan pages, broken links, contradictions, stale claims, missing frontmatter, index drift.
allowed-tools: Read, Edit, Glob, Grep, Bash
---

# /cmds-llm-wiki-lint — Lightweight LLM Wiki Health Check

Audit the wiki for drift. Reports issues; **proposes fixes but does not auto-apply them** unless the user confirms.

> **🧭 Prerequisite**: Read `LLMWiki/Core Context.md` once per session — needed for the snapshot-staleness check.

## Process

### Step 1: Inventory

Read `LLMWiki/index.md` for the declared catalog. Then enumerate actual files:

```
Glob "LLMWiki/Wiki/*.md"
Glob "LLMWiki/Sources/*.md"
Glob "LLMWiki/Queries/*.md"
```

Compare counts. Drift here is an early warning.

### Step 2: Orphan check

For every `Wiki/` page, count inbound `[[links]]` from other `Wiki/` pages and `Queries/` files.

```
Grep "[[{page-name}]]" path="LLMWiki/Wiki/" output_mode="files_with_matches"
```

Pages with **zero inbound links** = orphans. Suggest: link from a thematically-related page or remove if obsolete.

### Step 3: Broken link check

Collect every `[[wikilink]]` across `LLMWiki/Wiki/` and `LLMWiki/Queries/`. For each link target, check whether the file exists (`Glob LLMWiki/Wiki/{target}.md`). Missing targets = broken links.

For each broken link:
- Suggest creating the page (if the concept is genuinely missing) OR fixing the link (if it's a typo/rename).

### Step 4: Contradiction check

Search for `> [!warning] Contradiction` callouts:

```
Grep "Contradiction" path="LLMWiki/Wiki/" output_mode="content"
```

List each, ask the user whether any have been resolved (and the callout can be removed) or escalated (and need fresh sources).

### Step 5: Staleness check

For every `Wiki/` page with `confidence: low` AND `date modified` >90 days old, flag for revisit.

```bash
# pseudo: Read each page's frontmatter, compare date modified to today - 90 days
```

### Step 6: Frontmatter check

For every page in `Wiki/`, `Sources/`, `Queries/`:
- 7 required properties present? (`type`, `aliases`, `description`, `author`, `date created`, `date modified`, `tags`)
- For `Sources/`: `collectionPurpose` filled (not empty, not default placeholder)?
- For `Wiki/`: `source`, `confidence`, `layer` present?
- For `Queries/`: `query`, `reusableFor` present?

Report coverage as percentages: e.g., `collectionPurpose: 12/13 sources = 92%`.

### Step 7: Index sync

Compare `LLMWiki/index.md` to actual files:
- Files present but not in index → missing entries (suggest adding)
- Index entries with no corresponding file → stale entries (suggest removing)
- Stats table accurate?

### Step 8: Core Context freshness

Read `LLMWiki/Core Context.md` frontmatter. If `status: template` or `snapshot_date` >180 days old, flag — suggest the user re-snapshot.

## Output

Report in this format (keep it scannable):

```
🩺 LLMWiki Lint — {YYYY-MM-DD}
──────────────────────────────
📊 Inventory
  Sources: {n}    Wiki: {n} (Concepts: {n}, Entities: {n}, Guides: {n}, Maps: {n})    Queries: {n}

🦴 Orphans ({n})
  - [[Page A]] — no inbound links
  - [[Page B]] — no inbound links

🔗 Broken links ({n})
  - [[Page C]] → [[Missing Page]]    (suggest: create | fix to [[Existing Page]])
  - ...

⚠️ Contradictions ({n})
  - [[Page D]]: {one-line summary of the contradiction}
  - ...

📅 Stale ({n})
  - [[Page E]] — confidence: low, modified {N} days ago

🧪 Frontmatter coverage
  - 7-required: {n}/{N} = {pct}%
  - collectionPurpose (Sources): {n}/{N} = {pct}%
  - confidence (Wiki): {n}/{N} = {pct}%

📚 Index drift
  - Missing entries: {n}    Stale entries: {n}    Stats accurate: yes/no

🧭 Core Context: snapshot {date} ({n} days ago) — {fresh | stale, suggest re-snapshot}

🔧 Suggested fixes (top 5)
  1. ...
  2. ...
```

Then ask the user: **"Which fixes should I apply? (numbers, 'all', or 'none')"**

If the user picks specific fixes, apply them via Edit (not Write). Re-run inventory at the end to confirm the issue count dropped.

## Conservative defaults

- Don't auto-delete orphan pages — they may be intentional staging ground.
- Don't auto-resolve contradictions — they need human judgment.
- Don't backfill `collectionPurpose` — that's a "letter to future self"; only the user can write it.

## Failure modes

- **Auto-applying fixes without confirmation** → trust violation. Always ask.
- **Reporting raw counts without examples** → the user can't act on "5 orphans". List them.
- **Treating low-confidence pages as wrong** → low confidence is information, not error. Stale + low is the lint signal; low alone isn't.
