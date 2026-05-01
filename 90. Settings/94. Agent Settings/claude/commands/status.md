---
description: Snapshot of vault health by CMDS Process stage — counts per stage, recent activity, inbox size, lint hotspots. Read-only one-screen summary. Use as a weekly/daily check-in before deciding what to /connect or /merge.
allowed-tools: Read, Glob, Grep, Bash
---

# /status — CMDS Vault Stage Snapshot

One-screen overview of the vault's CMDS Process state. **Read-only**, fast, no dialogs. Designed to be the first command of a working session.

> **🧭 Prerequisite**: `CMDS.md` for stage definitions.

## Input

`$ARGUMENTS`

- Blank: full snapshot
- `inbox` — only inbox section
- `outputs` — only 700-800 section
- `recent` — only recent activity (last 7 days)

## Process

### Step 1: Inbox Counts

Glob `00. Inbox/**/*.md`, count by subfolder. Identify oldest 3 files per top-3 largest subfolders.

### Step 2: CMDS Stage Counts

For each stage, count notes via Grep on `CMDS:` frontmatter. Per 🏛 CMDS Guide, `CMDS:` values point to 📚 subcategories (not 📖 top-levels), so match by the leading digit of the 📚 number:

```
Grep(pattern="CMDS:.*\[\[📚 1", path=".", glob="*.md", output_mode="count")   # 100 Themes
Grep(pattern="CMDS:.*\[\[📚 2", ...)   # 200 Literature
Grep(pattern="CMDS:.*\[\[📚 3", ...)   # 300 Data
Grep(pattern="CMDS:.*\[\[📚 4", ...)   # 400 Methodologies
Grep(pattern="CMDS:.*\[\[📚 5", ...)   # 500 Products
Grep(pattern="CMDS:.*\[\[📚 6", ...)   # 600 Specialties
Grep(pattern="CMDS:.*\[\[📚 7", ...)   # 700 Creatives
Grep(pattern="CMDS:.*\[\[📚 8", ...)   # 800 Outputs
Grep(pattern="CMDS:.*\[\[📚 9", ...)   # 900 Divisions
```

(Use `head_limit=0` for full count if needed; for speed, just use count mode. Display labels below still use the conceptual 📖 top-level names for clarity.)

### Step 3: Recent Activity

`Bash`:
```
find "{vault root}" -name "*.md" -mtime -7 -type f -not -path "*/node_modules/*" -not -path "*/.obsidian/*" | wc -l
```

Then identify which folders received the most updates:
```
find "{vault root}" -name "*.md" -mtime -7 -type f | awk -F'/' '{print $NF}' | head -10  # last 10 modified
```

### Step 4: System File Freshness

Check `date modified` on the 5 system files:
- CLAUDE.md, AGENTS.md, CMDS.md, 🏛 CMDS Guide.md, 🏛 CMDS Head Quarter.md

Flag any unchanged > 30 days.

### Step 5: Output Snapshot

```
🩺 CMDS Vault Status — {today}
═══════════════════════════════════════════════

📥 Inbox
   01. Daily Notes      {n} files
   02. Clippings        {n} files  ← largest
   03. AI Agent         {n} files
   06. GenAI Chats      {n} files
   ...
   Total inbox          {N} files

   Aging hotspot: 02. Clippings — {oldest} ({age}d)

🧭 CMDS Process Stage Counts
   📖 100 Themes        {n} notes
   📖 200 Literature    {n} notes
   📖 300 Data          {n} notes
   📖 400 Methodologies {n} notes
   📖 500 Products      {n} notes
   📖 600 Specialties   {n} notes
   📖 700 Creatives     {n} notes
   📖 800 Outputs       {n} notes
   📖 900 Divisions     {n} notes

📈 Recent Activity (last 7 days)
   Notes touched:       {N}
   Top folders:
     30. Permanent Notes  {n} updates
     00. Inbox/02         {n} updates
     ...

🛠 System File Freshness
   CLAUDE.md            {date}  ({age}d)
   CMDS.md              {date}  ({age}d)
   ...
   ⚠ {file} — {age}d (consider /refresh-context)

💡 Suggested next action
   • Inbox 02. Clippings 적체 → /inbox 02. Clippings → /merge
   • 200 Literature 정체 (지난 14일 0개 추가) → /merge 활성화
   • 시스템 파일 X.md 30일+ → 업데이트 검토
```

### Step 6: One-Line Recommendation

Based on counts/activity, surface the single highest-leverage action:

- Inbox 큰 폴더 + 합성 정체 → `/merge {topic}` 우선
- Inbox 작음 + Theme 정체 → `/connect`로 capture 활성화
- 200 Literature 풍부 + Output 정체 → `/share {topic}`로 분배
- 모든 게 균형 → `/lint inbox`로 위생 점검

## Anti-patterns

- ❌ **Reading file contents** — only count and timestamp. /status must be fast.
- ❌ **Adding dialogs** — /status is informational, not interactive.
- ❌ **Recomputing from scratch every time** — if a status cache exists in future, prefer it. (Not implemented yet.)

## Notes

- Run `/status` as the **first command** of a session to ground decisions.
- Pair with `/lint inbox` for a fuller picture (status = quantity, lint = quality).
- The "Suggested next action" line is the most useful output — don't skip it.
- Future enhancement: track stage transitions (how many Themes became Literature this month) — needs a log file or git diff.
