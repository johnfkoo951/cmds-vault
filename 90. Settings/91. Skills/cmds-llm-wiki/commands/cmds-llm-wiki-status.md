---
description: Bootstrap LLMWiki on first run (configurable location persisted to AGENTS.md, pointer-based Core Context, sources land in 10. Raw Sources/), then show a one-screen overview — counts, recent activity, top-linked pages, Core Context freshness.
allowed-tools: Read, Write, Edit, Glob, Grep, Bash
---

# /cmds-llm-wiki-status — Bootstrap + Status

This command is the **canonical first command** in any vault. On first run it:
1. Asks where to put the `LLMWiki/` folder, persists the choice to `AGENTS.md` frontmatter (`llmWikiPath:`).
2. Bootstraps `{llmWikiPath}/{Wiki,Queries}` + `index.md` + `log.md`. **No `Sources/` subfolder** — raw sources live in CMDS-canonical `10. Raw Sources/`.
3. Seeds `Core Context.md` as a **pointer file** to canonical CMDS files (`BRAIN.md`, `🏛 CMDS Head Quarter.md`, `CMDS.md`) — minimizing duplication. Falls back to inline content for non-CMDS vaults.

After bootstrap it's a fast read-only snapshot.

## Process

### Step 1: Resolve `llmWikiPath`

Read `AGENTS.md` (or `CLAUDE.md`) at the vault root. Look for `llmWikiPath:` in frontmatter.

- If present → use it (e.g., `LLMWiki`, `90. Settings/LLMWiki`, custom). Skip to **Step 2** with that path.
- If missing AND `LLMWiki/` already exists at vault root → use `LLMWiki` (legacy default), skip to Step 2.
- If missing AND no `LLMWiki/` exists → **first-run path prompt**:
  > "Where should I create the LLMWiki folder? Options:
  >   1. `LLMWiki/` (vault root — default, easiest to graduate later)
  >   2. `90. Settings/LLMWiki/` (lives with other settings)
  >   3. Custom path
  > Reply with 1 / 2 / a custom path."
- After the user answers, **persist to `AGENTS.md` frontmatter**: add (or update) `llmWikiPath: "{chosen path}"`. Use Edit with a precise frontmatter block match.
- If `AGENTS.md` doesn't exist (non-CMDS vault), write to `CLAUDE.md` instead. If neither exists, fall back to `LLMWiki/` default and tell the user the choice wasn't persisted.

From here forward, `{llmWikiPath}` = the resolved path.

### Step 2: Existence check

```bash
ls "{llmWikiPath}" 2>/dev/null
```

- If exists → skip to **Step 6: Status output**.
- If missing → run **Step 3: Bootstrap** then **Step 4: Core Context seed**, then continue.

### Step 3: Bootstrap `{llmWikiPath}/` skeleton

Create the folder structure (no `Sources/` subfolder — sources go to `10. Raw Sources/`):

```bash
mkdir -p "{llmWikiPath}/Wiki" "{llmWikiPath}/Queries"
```

Copy templates:
- `templates/index.md` → `{llmWikiPath}/index.md` (substitute `{your-name}` and `{YYYY-MM-DD}` placeholders).
- Create `{llmWikiPath}/log.md` with minimal frontmatter (`type: log`, today's date) and an empty body.

### Step 4: Smart Core Context seed (pointer-based for CMDS vaults)

Read these canonical CMDS files at vault root:

```
Read("BRAIN.md")
Read("🏛 CMDS Head Quarter.md")
Read("CMDS.md")
Read("🏛 CMDS Guide.md")
```

**If at least `BRAIN.md` + (`🏛 CMDS Head Quarter.md` OR `CMDS.md`) exist** → CMDS-style vault detected:

1. Copy `templates/Core Context.md` to `{llmWikiPath}/Core Context.md` verbatim — it's already pointer-shaped (links into BRAIN / HQ / CMDS at runtime).
2. Substitute placeholders: `{your-name}` from `BRAIN.md` frontmatter `author:` (or fallback `[[Me]]`), `{YYYY-MM-DD}` to today.
3. Set frontmatter `status: seeded` and `sourcesPath: "10. Raw Sources"`.
4. Optionally inline a 2–3 line "Active focus snapshot" under §2 by reading `🏛 CMDS Head Quarter.md`'s "Current Focus Areas" section — this gives a static cache for offline reference, but the link remains the source of truth.

**If canonical files are absent** (non-CMDS vault) → fall back to inline seed:

1. Sample 5–15 notes from existing folders in priority order: `30. Permanent Notes/`, `Topics/`, `60. Collections/`, `20. Literature Notes/`, `Roundup/`.
2. Infer §1 (identity from frontmatter `author:` patterns) and §2 (5–9 reuse axes from recurring tags + folder names).
3. Replace the §1/§2 pointer text in the template with the inferred inline content.
4. Set `status: seeded`.

**If neither path applies** (empty vault, no canonical files, no populated folders): copy template verbatim with `status: template` (placeholders intact).

### Step 5: Bootstrap report

Show the user:

```
🌱 Bootstrap complete.

Configured:
  llmWikiPath: {chosen path}    ← persisted to AGENTS.md frontmatter
  sourcesPath: 10. Raw Sources  ← CMDS canonical (created on first ingest)

Created:
  {llmWikiPath}/
  ├── Wiki/, Queries/  (empty)
  ├── index.md, log.md
  └── Core Context.md  ← {pointer-seeded → BRAIN/HQ/CMDS | inline-seeded from N notes | unfilled template}

{If pointer-seeded:}
Core Context now points to:
  §1 Who → [[BRAIN]]
  §2 Why → [[🏛 CMDS Head Quarter#Current Focus Areas]] + [[CMDS]] categories
  §3 What → [[CMDS]]
  §4 How → [[CMDS]] + [[🏛 CMDS Guide]]
→ Review the linked files reflect your current focus, then flip Core Context `status: seeded` → `status: active`.

{If inline-seeded:}
Inferred reuse axes from N notes in `{folder}` (status: seeded):
  1. {axis 1}
  2. ...
→ Open Core Context.md, refine §2, flip `status: seeded` → `status: active`.

{If template:}
Empty vault — Core Context left as template.
→ Open Core Context.md and fill §1/§2 manually, flip `status: template` → `status: active`.

Next: /cmds-llm-wiki-ingest <file path or URL>
  - Local files in 00. Inbox/ get MOVED to 10. Raw Sources/{NN. category}/
  - URLs get fetched and saved fresh to 10. Raw Sources/{NN. category}/
```

Then continue to Step 6.

### Step 6: Status output (counts)

Path resolution: read `AGENTS.md` → `llmWikiPath`; read `Core Context.md` frontmatter → `sourcesPath` (default `10. Raw Sources`).

```
Glob "{sourcesPath}/**/*.md"            → source count (filtered to type: raw-source)
Glob "{llmWikiPath}/Wiki/*.md"          → wiki page count
Grep "^layer: concepts" path="{llmWikiPath}/Wiki/" → concepts count
Grep "^layer: entities" path="{llmWikiPath}/Wiki/" → entities count
Grep "^layer: guides"   path="{llmWikiPath}/Wiki/" → guides count
Grep "^layer: maps"     path="{llmWikiPath}/Wiki/" → maps count
Glob "{llmWikiPath}/Queries/*.md"       → query count
```

Read `{llmWikiPath}/log.md` and pull the last 5 entries (each starts with `## [YYYY-MM-DD]`).

Top-linked pages: for each `Wiki/` page, count inbound `[[links]]` from other `Wiki/` pages. Show top 5.

Coverage spot-checks:
```
Grep "^collectionPurpose:" path="{sourcesPath}/" (filtered to type: raw-source) → coverage
Grep "^confidence: high"   path="{llmWikiPath}/Wiki/"                            → high-confidence pages
```

Read `{llmWikiPath}/Core Context.md` frontmatter `snapshot_date` (or fall back to `date modified`).

## Output

```
📊 LLMWiki Status
─────────────────────────────────
Path:      {llmWikiPath}              (sources at: {sourcesPath})
Sources:   {n}    (collectionPurpose: {n}/{N} = {pct}%)
Wiki:      {n}    (Concepts: {n}, Entities: {n}, Guides: {n}, Maps: {n})
Queries:   {n}    (filed-back ratio: {q}/{w} = {pct}%)

🧭 Core Context: snapshot {date} ({n} days ago) — {fresh | stale | seeded — please review}
   Mode: {pointer (links to BRAIN/HQ/CMDS) | inline (seeded from N notes) | template}

📥 Recent (last 5)
  - {date} ingest | {title}
  - ...

🔗 Top-linked pages
  1. [[Page A]]  ({n} inbound)
  ...

🩺 Quick health
  - Orphans (run /cmds-llm-wiki-lint for details)
  - Broken links (run /cmds-llm-wiki-lint for details)
─────────────────────────────────
Tip: run /cmds-llm-wiki-lint weekly · /cmds-llm-wiki-ingest to feed · /cmds-llm-wiki-query to compound.
```

On a freshly bootstrapped vault all counts are zero — show "—" instead of "NaN%". The Bootstrap report from Step 5 carries the actionable info.

## Failure modes

- **Persisting `llmWikiPath` to the wrong file** → only write to `AGENTS.md` (or `CLAUDE.md` fallback) at vault root. Don't touch system files in `cmds-system-files/`.
- **Auto-promoting `seeded` to `active`** → never. The user must read the pointer targets and confirm.
- **Re-bootstrapping a vault that already has `LLMWiki/`** → don't. Step 2 short-circuits to status output. Re-bootstrap is a manual `rm -r` + re-run.
- **Sampling too many notes during inline seed** → keep to 5–15.
- **Counting sources from `{sourcesPath}` when other tools also write there** → filter to frontmatter `type: raw-source` to avoid counting unrelated files.
