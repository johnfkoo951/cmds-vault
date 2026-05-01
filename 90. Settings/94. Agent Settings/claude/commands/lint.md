---
description: Health check the mothership vault by CMDS Process stage. Pass scope as inbox/connect/merge/develop/share/all. Surfaces orphans, broken wikilinks, contradictions, stale items, frontmatter v2 coverage gaps. Read-only — proposes fixes but does not apply them.
allowed-tools: Read, Glob, Grep, Bash, AskUserQuestion
---

# /lint — CMDS Vault Health Check

Run a focused health check on a CMDS Process stage. **Read-only** — surfaces issues and proposes fixes, but never auto-applies (use `Edit` after user confirms specific fixes).

> **🧭 Prerequisite**: `CMDS.md` for stage definitions. Pre-flight rules in `.claude/rules/frontmatter-standard.md` define what counts as compliant.

## Input

`$ARGUMENTS`

- `inbox` — check 00. Inbox health
- `connect` — check 100 Themes notes
- `merge` — check 200 Literature notes
- `develop` — check 300-600 artifacts (code, prompts, specialty)
- `share` — check 700-800 output notes
- `all` — run every scope (long, summarize per scope)
- **Blank**: ask via AskUserQuestion which scope

## Process

### Step 0: Resolve Scope

If blank, ask:

```
AskUserQuestion (single):
  Q: "어느 단계를 점검할까요?"
  Header: "Lint scope"
  Options:
    - "inbox (가장 자주 권장)" — 묵은 파일, 중복, 미분류
    - "connect (100 Themes)" — 고아 Theme, dupe, 빈 stub
    - "merge (200 Literature)" — 모순, 약한 source, orphan
    - "all" — 전부 (길어요)
```

### Step 1: Run Stage-Specific Checks

Run only the checks for the resolved scope.

---

### Scope: `inbox`

Targets: `00. Inbox/**/*.md`

Checks:

1. **Aging files**: any file unchanged > 90 days (use `find -mtime +90`). Propose: `/connect` or `/merge` or move to `09. Legacy/`
2. **Possible duplicates**: filenames sharing > 80% similarity (e.g., `... 2.md`, `... 3.md` versions). Propose: pick canonical, archive others.
3. **Empty / nearly empty**: files with body < 5 lines (could be lost captures). Propose: review or delete.
4. **Missing frontmatter**: files without YAML at top. Propose: add minimum 7 required properties.
5. **Inbox subfolder counts**: any subfolder > 100 files. Propose: process via `/connect` or `/merge` in batches.

Output table:
```
📥 Inbox lint — {today}
─────────────────────────────────
Aging (>90d):       {n} files
Possible dupes:     {n} groups
Empty/nearly:       {n} files
Missing frontmatter:{n} files
Subfolders >100:    {list}

Top 5 oldest:
  1. {file} ({age}d)
  2. ...
```

---

### Scope: `connect` (100 Themes)

Targets: `30. Permanent Notes/*.md` where frontmatter `CMDS:` points to a 📚 10X subcategory (101/102/103/104). Grep pattern: `CMDS:.*\[\[📚 10`.

Checks:

1. **Orphan Themes**: no inbound `[[wikilinks]]` from any other note (Grep across vault for `[[{theme name}]]`). Propose: link from MOC or related note, or archive.
2. **Stub-only Themes**: `Why this matters` section still has the `(✏️ TODO)` placeholder. Propose: prompt user to fill or `/merge` if multiple captures accumulated.
3. **Duplicate Themes**: titles with > 80% string similarity. Propose: merge into one canonical theme.
4. **Missing `description`**: frontmatter has empty or Korean `description`. (Per rule: must be English, 1-2 sentences.) Propose: regenerate `description` from gist.
5. **Wrong property direction**: `CMDS:` pointing to `[[📖 100 Themes]]` (top-level) instead of a 📚 subcategory, or `index:` pointing to a 📚 instead of a 🏷 Index note. Per 🏛 CMDS Guide: `CMDS:` = 📚 · `index:` = 🏷. Propose: swap values.
6. **Wrong subcategory**: `CMDS:` value doesn't match the four valid 10X categories (101/102/103/104). Propose: re-classify.
7. **Ripening signal**: Themes with `Related captures` >= 3 entries. Propose: `/merge {theme}` ready.

---

### Scope: `merge` (200 Literature)

Targets: `30. Permanent Notes/*.md` where `CMDS:` points to a 📚 2XX subcategory (201/202/204/210/220/240…). Grep pattern: `CMDS:.*\[\[📚 2`.

Checks:

1. **Contradictions**: scan for `> [!warning] Contradiction` callouts. List all + check `date modified` to flag stale ones.
2. **Weak source backing**: `sourceNotes:` array with < 2 entries (synthesis should have ≥ 3 sources by definition). Propose: re-run `/merge` with more candidates or downgrade to `/connect` Theme.
3. **Orphan synthesis**: 200 note with no inbound links from anywhere. Propose: link from MOC.
4. **Missing `mergePurpose`**: post-2026-04-14 200 notes without `mergePurpose`. Propose: backfill via dialog.
5. **Cross-vault refs missing `mainVaultRelated`**: 200 notes that reference LLM Wiki concepts in body but don't list them in frontmatter. Propose: backfill.
6. **Stale Literature Reviews**: `210` notes with `date modified` > 180 days + recent inbox activity on same topic. Propose: refresh via `/merge`.

---

### Scope: `develop` (300-600)

Targets:
- `00. Inbox/03. AI Agent/**/*` — pending artifacts
- `30. Permanent Notes/*.md` where `CMDS:` matches `[[📚 6` (600 series specialties)
- `50. Assets/51. Prompt/*.md` — reusable prompts

Checks:

1. **Stale code in inbox**: Code files in `03-1. Claude Code (MBP)/` unchanged > 30 days, status `inProgress`. Propose: review/test/promote or delete.
2. **Untested prompts**: `492 Prompts` with no usage log / no example output. Propose: test before adding to prompt library.
3. **Stale specialty notes**: 600 notes unchanged > 180 days. Propose: refresh from recent 200 Literature.
4. **Missing `developSources:`**: artifacts without source linkage. Propose: backfill.
5. **Code without README**: project folders in inbox with > 3 files but no README/index. Propose: add README pointing to vault tracking note.

---

### Scope: `share` (700-800)

Targets: `70. Outputs/**/*.md`, notes with `CMDS:` matching `[[📚 7` (Creatives) or `[[📚 8` (Outputs).

Checks:

1. **Broken outbound links**: published notes with `[[wikilinks]]` to deleted/renamed sources.
2. **Draft vs published mismatch**: notes with `status: draft` but in `71. Published/` folder, or vice versa.
3. **Missing `shareSourceNotes:`**: post-2026-04-14 share outputs without source linkage.
4. **Format ↔ destination mismatch**: e.g., a slide deck note in `802 Articles` (should be in `840 Lectures`).
5. **Orphan outputs**: published with no back-link from any source synthesis. Propose: add back-link.

---

### Scope: `all`

Run all 5 scopes sequentially. Output one summary section per scope. At the end, a global priority list:

```
🔝 Top fix priority (across all scopes):
  1. {scope}: {issue} — {n} files affected
  2. ...
```

### Step 2: Frontmatter v2 Coverage (always reported)

Across the resolved scope, compute:
- % of files with all 7 required properties
- % with English `description` (heuristic: contains ASCII alphabetic and ends with period)
- % with 2026-04-14+ properties (`description` field)
- Stale 5 system files: any of CLAUDE.md/AGENTS.md/CMDS.md/🏛 CMDS Guide.md/🏛 CMDS Head Quarter.md unchanged > 30 days

### Step 3: Report

```
🩺 /lint — Report
─────────────────────────────────
Scope:        {scope}
Files scanned: {n}
Issues found: {total}

[Per-check details with file lists]

📊 Frontmatter v2 coverage:
  All 7 required:     {p}% ({m}/{n})
  English description:{p}% ({m}/{n})

🔝 Recommended actions (top 3):
  1. {action} → run {command}
  2. ...

Next:
  - 특정 fix를 적용하려면 → "fix #{n}" 또는 "{검사 종류} 자동 적용해줘"
  - 다른 scope 점검 → /lint {scope}
```

### Step 4: Dialog (only if user wants to fix)

If the user follows up with "fix #N" or similar:

```
AskUserQuestion (single):
  Q: "{check name}을 어떻게 처리할까요?"
  Header: "Fix mode"
  Options:
    - "한 파일씩 검토 후 적용 (Recommended)"
    - "전체 자동 적용"
    - "자동 적용 + 사용자 확인 없이"
    - "취소"
```

Then apply per chosen mode using Edit.

## Anti-patterns

- ❌ Auto-fixing without user confirmation. Lint surfaces; fix is opt-in.
- ❌ Running `all` scope for casual checks. Default to specific scope.
- ❌ Reading every file fully — use Glob + frontmatter-only Read for speed.
- ❌ Flagging orphans on notes that are intentionally orphan (e.g., daily notes). Skip files in `00. Inbox/01. Daily Notes/` for orphan checks.

## Notes

- `lint inbox` is the most useful weekly habit — surfaces what to `/connect` or `/merge` next.
- `lint merge` is the highest-quality check for synthesis health; run before `/share` to avoid sharing weakly-backed claims.
- `lint all` is monthly hygiene — schedule via `/loop 30d /lint all` if desired.
- For any "fix" that requires content rewriting (e.g., regenerate English description), fall back to `/connect` or `/merge` rather than doing it inside `/lint`.
