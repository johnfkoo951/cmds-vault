---
description: Bootstrap LLMWiki on first run (smart-seeding Core Context from existing CMDS-style notes if present), then show a one-screen overview — counts, recent activity, top-linked pages, Core Context freshness.
allowed-tools: Read, Write, Glob, Grep, Bash
---

# /cmds-llm-wiki-status — Bootstrap + Status

This command is the **canonical first command** in any vault. On first run it bootstraps `LLMWiki/` and seeds `Core Context.md` from existing CMDS-style knowledge folders (so users don't fill a blank template). After bootstrap it's a fast read-only snapshot.

## Process

### Step 1: Existence check

```bash
ls LLMWiki 2>/dev/null
```

- If `LLMWiki/` exists → skip to **Step 5: Status output**.
- If missing → run **Step 2: Bootstrap** first, then continue.

### Step 2: Bootstrap LLMWiki/ skeleton

Create the folder structure and copy the index/log templates from this skill's `templates/`:

```bash
mkdir -p LLMWiki/Sources LLMWiki/Wiki LLMWiki/Queries
```

Copy:
- `templates/index.md` → `LLMWiki/index.md` (substitute `{your-name}` and `{YYYY-MM-DD}` placeholders).
- Create `LLMWiki/log.md` with minimal frontmatter (`type: log`, today's date) and an empty body.

### Step 3: Smart Core Context seed

Scan the host vault (current working directory) for CMDS-style knowledge folders, in this priority order:

1. `30. Permanent Notes/` (CMDS canonical)
2. `Topics/` (GOBI / generic PKM)
3. `60. Collections/`
4. `20. Literature Notes/`
5. `Roundup/` (GOBI weekly summaries)

```
Glob "30. Permanent Notes/**/*.md"
Glob "Topics/**/*.md"
Glob "60. Collections/**/*.md"
Glob "20. Literature Notes/**/*.md"
Glob "Roundup/**/*.md"
```

**If at least one folder exists with ≥10 notes**, seed Core Context:

1. Pick the highest-priority folder that has content. Sample **5–15 notes** — most recently modified, sampled across subfolders if the folder has them.
2. Read those notes and extract:
   - **User identity hints**: `author:` / `authors:` in frontmatter (most common non-`Claude` author = the user); `BRAIN.md` at vault root if present (operator profile); recurring `[[Me]]` references.
   - **Recurring topic tags** (frontmatter `tags:` patterns + folder names): these become candidate reuse axes.
   - **Topic clusters**: top-level folder names within `30. Permanent Notes/` are typically already category groupings (e.g., `33. Essay/`, `35. Research/`). Promote subfolder names that fit "what is this knowledge for?" into axes.
3. Compose 5–9 reuse axes from the inferred clusters. Examples that should emerge naturally for a CMDS vault: 학술 연구, 저술·출판, 강의·강연, 컨설팅, 제품 개발, 개인 에세이, 커뮤니티 교육.
4. Write a draft `LLMWiki/Core Context.md` with §1 (identity) and §2 (reuse axes) populated from real content. Use the template at `templates/Core Context.md` as the structural skeleton, but replace placeholders with actual inferred values.
5. **Set frontmatter `status: seeded`** (not `template`, not `active`). This signals to `/lint` and the user that the seed needs review.
6. Set `snapshot_date: {today}`, `date created` / `date modified` to today, and `author: "[[{inferred-user}]]"` (or `[[Me]]` if identity unclear).

**If no folder has ≥10 notes** (empty or new vault):
- Copy `templates/Core Context.md` verbatim to `LLMWiki/Core Context.md` with `status: template` (placeholder values intact).
- Skip §1/§2 inference.

### Step 4: Bootstrap report

After seeding, show the user:

```
🌱 Bootstrap complete.

Created:
  LLMWiki/
  ├── Sources/, Wiki/, Queries/  (empty)
  ├── index.md, log.md
  └── Core Context.md  ← {seeded from N notes in `{folder}` | unfilled template}

{If seeded:}
Inferred reuse axes (status: seeded — please review):
  1. {axis 1}
  2. {axis 2}
  3. ...

→ Open LLMWiki/Core Context.md, refine §1/§2, then flip `status: seeded` → `status: active`.

{If not seeded:}
Your vault doesn't have populated CMDS-style folders yet (30. Permanent Notes/, Topics/, ...).
→ Open LLMWiki/Core Context.md and fill §1/§2 manually (5–9 reuse axes), then flip `status: template` → `status: active`.

Next: /cmds-llm-wiki-ingest <file or URL>
```

Then continue to Step 5.

### Step 5: Status output (counts)

```
Glob "LLMWiki/Sources/*.md"           → source count
Glob "LLMWiki/Wiki/*.md"              → wiki page count
Grep "^layer: concepts" path="LLMWiki/Wiki/" → concepts count
Grep "^layer: entities" path="LLMWiki/Wiki/" → entities count
Grep "^layer: guides"   path="LLMWiki/Wiki/" → guides count
Grep "^layer: maps"     path="LLMWiki/Wiki/" → maps count
Glob "LLMWiki/Queries/*.md"           → query count
```

Read `LLMWiki/log.md` and pull the last 5 entries (each starts with `## [YYYY-MM-DD]`).

Top-linked pages: for each `Wiki/` page, count inbound `[[links]]` from other `Wiki/` pages. Show top 5.

Coverage spot-checks:
```
Grep "^collectionPurpose:" path="LLMWiki/Sources/"  → sources with purpose / total
Grep "^confidence: high"   path="LLMWiki/Wiki/"     → high-confidence pages
```

Read `LLMWiki/Core Context.md` frontmatter `snapshot_date` (or fall back to `date modified`).

## Output

```
📊 LLMWiki Status
─────────────────────────────────
Sources:   {n}      (collectionPurpose: {n}/{N} = {pct}%)
Wiki:      {n}      (Concepts: {n}, Entities: {n}, Guides: {n}, Maps: {n})
Queries:   {n}      (filed-back ratio: {q}/{w} = {pct}%)

🧭 Core Context: snapshot {date} ({n} days ago) — {fresh | stale | seeded — please review}

📥 Recent (last 5)
  - {date} ingest | {title}
  - {date} query  | {short q}
  - ...

🔗 Top-linked pages
  1. [[Page A]]    ({n} inbound)
  2. [[Page B]]    ({n} inbound)
  3. ...

🩺 Quick health
  - Orphans (run /cmds-llm-wiki-lint for details)
  - Broken links (run /cmds-llm-wiki-lint for details)
─────────────────────────────────
Tip: run /cmds-llm-wiki-lint weekly · /cmds-llm-wiki-ingest to feed · /cmds-llm-wiki-query to compound.
```

On a freshly bootstrapped vault all counts are zero — show "—" instead of "NaN%" for ratios. The Bootstrap report from Step 4 carries the actionable info.

## Failure modes

- **Auto-promoting `seeded` to `active`** → never. The user must review the inferred axes; that's the whole point of the gate.
- **Sampling too many notes** → keep to 5–15. More doesn't improve axis quality and slows bootstrap.
- **Inventing axes the vault doesn't support** → if you can't find recurring patterns, show fewer axes (3–4) and tell the user the seed is sparse, not bogus.
- **Running expensive scans on every status call** → seed only on the bootstrap path. After `LLMWiki/` exists, status stays read-only and fast.
- **Showing percentages with division by zero** → guard against empty wiki on first run; show "—" instead of "NaN%".
