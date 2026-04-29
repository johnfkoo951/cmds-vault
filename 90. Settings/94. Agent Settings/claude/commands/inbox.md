---
description: Scan 00. Inbox/ subfolders, present a count snapshot, then use AskUserQuestion to route the user to the appropriate CMDS Process command (/connect, /merge, /develop, /share).
allowed-tools: Read, Glob, Bash, AskUserQuestion, mcp__qmd__query
---

# /inbox — CMDS Inbox Scanner & Router

Scan the mothership inbox, summarize its state, and route the user into the right CMDS Process stage command. **This command itself does not write to the vault** — it only reads, summarizes, and routes.

> **🧭 Prerequisite**: Familiarity with the CMDS Process (Connect → Merge → Develop → Share) — see `CMDS.md`.

## Input

`$ARGUMENTS`

- If blank: scan **all** subfolders + root
- If a subfolder name (e.g. `02. Clippings`, `clippings`): scan only that subfolder
- If `count` or `status`: just emit the count table, skip routing

## Process

### Step 1: Scan

Inspect the following paths under `00. Inbox/`. Use `Glob` for each, count `*.md` files (exclude `.gitkeep`, hidden files):

| Subfolder | Typical content |
|-----------|----------------|
| `01. Daily Notes/` | Daily journals, planners, weekly notes |
| `02. Clippings/` | Web clippings, literature notes |
| `03. AI Agent/` | Code outputs from Claude Code / OpenClaw |
| `04. Excalidraw/` | Visual diagrams |
| `05. Canvas/` | Canvas notes |
| `06. Automation/` | n8n / Make.com workflow notes |
| `06. GenAI Chats/` | ChatGPT / Claude conversation logs |
| `07. App Sync/` | External app sync (Bear, Antigravity, etc.) |
| `08. Unlisted/` | Unlisted items |
| `09. Legacy/` | Archived legacy content |
| `_Gobi_Captures/` | Gobi Desktop captures |
| `(root)` | Uncategorized loose files |

Also compute **age buckets** for the largest 1~2 subfolders (using `Bash` `find ... -mtime`):
- `< 7 days`, `7~30 days`, `30~90 days`, `> 90 days`

### Step 2: Present Snapshot

Output a table:

```
📥 Mothership Inbox — Snapshot ({today})
────────────────────────────────────────────
01. Daily Notes      {n} files  (last: {YYYY-MM-DD})
02. Clippings        {n} files  (last: {YYYY-MM-DD})
03. AI Agent         {n} files  (last: {YYYY-MM-DD})
04. Excalidraw       {n} files
05. Canvas           {n} files
06. Automation       {n} files
06. GenAI Chats      {n} files
07. App Sync         {n} files
08. Unlisted         {n} files
09. Legacy           {n} files
_Gobi_Captures       {n} files
(root, uncategorized){n} files
────────────────────────────────────────────
Total                {N} files

Aging hotspot: {subfolder with most >90-day files} → {n} stale files
```

If a subfolder has > 50 files OR > 20 files older than 90 days, mark it with `⚠`.

### Step 3: Ask Scope (AskUserQuestion)

Use the `AskUserQuestion` tool with **multiSelect: true** to let the user pick which subfolders to work on:

```
Question: "어느 inbox 영역을 작업할까요? (복수 선택 가능)"
Header: "Inbox scope"
multiSelect: true
Options:
  - "02. Clippings (Recommended)" — 웹 기사·논문 클리핑. /connect 또는 /merge에 적합
  - "06. GenAI Chats" — AI 대화 로그. /merge로 정수만 추출하기 좋음
  - "01. Daily Notes" — 회고에서 Theme 발굴. /connect에 적합
  - "Root (uncategorized)" — 미분류 루트 파일. /connect로 분류부터
```

(Recommendation 순서는 위 snapshot에서 가장 활동이 많은 폴더 기준으로 동적 결정. ⚠ 마크된 영역이 있으면 그것을 첫 옵션으로.)

If the user picks `Other`, accept free-text (e.g., "07. App Sync 일주일치만").

### Step 4: Ask Stage (AskUserQuestion)

After scope is determined, recommend the most appropriate CMDS Process stage command based on selected subfolders' content type:

| Selected scope | Default recommendation |
|----------------|------------------------|
| 02. Clippings (rich literature) | `/merge` — N→1 합성 |
| 02. Clippings (light snippets) | `/connect` — Theme stub 빠르게 |
| 06. GenAI Chats | `/merge` — 대화에서 정수 추출 |
| 01. Daily Notes | `/connect` — 회고에서 Theme 발굴 |
| 03. AI Agent | `/develop` 또는 `/share` (이미 코드/초안) |
| Root uncategorized | `/connect` — 분류 + Theme 등록 |
| Mixed selection | `/connect` 부터 권장 (low-friction) |

Then ask:

```
Question: "어떤 단계로 진행할까요?"
Header: "CMDS stage"
multiSelect: false
Options:
  - "{Recommended stage} (Recommended)" — {one-line description}
  - "/connect" — Capture & triage to 100 Themes
  - "/merge" — Synthesize multiple notes into 200 Literature
  - "/develop" — Apply method, build artifact (300-600)
  - "/share" — Format for output (700-800)
```

If user picks `Other`: accept free-text like "그냥 보기만" → emit a deeper preview of selected subfolder and stop.

### Step 5: Hand-off

Output a clear hand-off message:

```
🔀 Routing
  Scope:  {selected subfolders}
  Stage:  {chosen command}
  Files:  {N} candidates in scope

다음 명령을 실행하세요:
  {command} {scope-arg}

또는 자동 실행을 원하시면 "고고" 라고 답해주세요 — 곧바로 {command}을 실행합니다.
```

If user replies "고고" or equivalent, immediately invoke the chosen command in the same session. Pass the selected subfolder paths as the argument.

## Notes

- This command is **read-only**. It never moves, renames, or deletes inbox files.
- For batch routing across multiple stages (e.g., "02. Clippings로는 merge, 03. AI Agent로는 share"), run `/inbox` twice.
- The age bucket computation helps surface stale/forgotten content — useful for periodic inbox cleanup.
- If `mcp__qmd__query` is available, optionally surface 2~3 inbox files that semantically match a recent topic the user has been working on (use the latest entry in `01. Daily Notes/` as the seed query).

## Anti-patterns

- ❌ Reading file contents in full during scan (slow + token-expensive). Stick to titles + frontmatter only.
- ❌ Suggesting `/develop` or `/share` for raw clippings (they belong in `/connect` or `/merge` first).
- ❌ Skipping AskUserQuestion and assuming the user wants "all" — the inbox is too vast for blind defaults.
