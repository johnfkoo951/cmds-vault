# Vault Directory Structure

```
00. Inbox/                      # Temporary storage and processing
├── 01. Daily Notes/            # Daily journal (01-1. Planners, 01-2. Weekly Notes)
├── 02. Clippings/              # Web clippings (02-1. Literature Notes)
├── 03. AI Agent/               # Code outputs (PRIMARY)
│   ├── 03-1. Claude Code (MBP)/
│   ├── 03-2. Claude Code (Studio)/
│   ├── 03-3. OpenClaw (MBP)/
│   └── 03-4. OpenClaw (Studio)/
├── 04. Excalidraw/             # Visual diagrams
├── 05. Canvas/                 # Canvas notes
├── 06. Automation/             # Automation (Make.com, n8n)
├── 06. GenAI Chats/            # GenAI conversation logs
├── 07. App Sync/               # External apps (Claude, Antigravity, Bear Notes)
├── 08. Transcripts/            # Raw transcript landing lanes (08-1. Plaud, 08-2. STT, 08-3. Manual)
└── 09. Legacy/                 # Legacy content

10. CMDS Process/               # Connect→Merge→Develop→Share
20. Literature Notes/           # Reading notes (외부 지식 내재화)
30. Permanent Notes/            # Evergreen content (정제된 개인 지식)
40. Docs/                       # Technical documentation (업무 문서/기록)
50. Assets/                     # Reusable resources (재사용 자원)
60. Collections/                # Entity management (People, Meetings, Preferences)
70. Outputs/                    # Final deliverables (최종 산출물)
80. References/                 # Reference materials (참조 자료)
90. Settings/                   # System settings and templates
├── 94. Agent Settings/         # AI agent configs (원본, Obsidian Sync 동기화)
│   └── claude/                 # .claude/ 원본 → symlink로 연결
│       ├── agents/
│       ├── commands/
│       ├── rules/
│       └── skills/
```

## Symbolic Link: .claude/ ↔ 94. Agent Settings/

`.claude/`는 숨김 폴더라 Obsidian Sync 대상이 아닙니다.
원본 파일은 `90. Settings/94. Agent Settings/claude/`에 두고, `.claude/`에서 상대경로 symbolic link로 연결합니다. 이 스타터킷은 v1.3.0 부터 이 구조로 배포됩니다.

### 왜 이렇게 하나 — 점폴더 동기화 정책
Obsidian Sync 는 `.obsidian` 을 뺀 점폴더(`.claude`, `.codex`, `.agents`, `.git` 등)를 동기화하지 않는다. 그렇다고 점폴더를 다른 도구로 실시간 동기화하면 아래 사고가 난다.
- `.git` 이 두 머신에서 동시에 바뀌면 저장소가 깨진다.
- `settings.local.json`·`sessions/` 에 든 토큰·개인 기록이 다른 머신으로 퍼진다.
- 훅 스크립트의 머신 전용 경로가 다른 머신에서 그대로 실행된다.
- symlink 가 실제 폴더로 복제되어 두 사본이 따로 놀기 시작한다.
- 캐시 폴더가 계속 바뀌어 충돌과 쓸데없는 전송이 늘고, JSON 설정이 병합 충돌을 일으킨다.

그래서 규칙은 이렇다.
1. **공유할 에이전트 설정은 일반 폴더에 둔다** — `90. Settings/94. Agent Settings/` 아래가 정본이고 Obsidian Sync·git 으로 머신 사이를 오간다.
2. **각 머신에서 점폴더 symlink 를 한 번만 만든다** — 상대경로(`../90. Settings/...`)로 만들어 볼트 경로가 달라도 그대로 동작하게 한다.
3. **머신 전용 설정은 동기화하지 않는다** — `settings.json`, `settings.local.json`, `sessions/` 는 각 머신의 점폴더 안에 실제 파일로 둔다.
4. **`.git` 은 git 으로만 옮긴다** — Sync·rsync 로 복사하지 않는다.
5. osync·rsync 를 쓸 일이 생기면 `.git .claude .codex .agents .smart-env .trash node_modules` 를 제외한다.

```
.claude/
├── agents   → symlink → ../90. Settings/94. Agent Settings/claude/agents
├── commands → symlink → ../90. Settings/94. Agent Settings/claude/commands
├── rules    → symlink → ../90. Settings/94. Agent Settings/claude/rules
├── skills   → symlink → ../90. Settings/94. Agent Settings/claude/skills
├── sessions/          (로컬 전용, 링크 안 함)
├── settings.json      (로컬 전용, 링크 안 함)
└── settings.local.json (로컬 전용, 링크 안 함)
```

### 새 머신에서 설정
볼트 루트에서 setup 스크립트를 한 번 실행한다. 링크가 이미 맞으면 `ok` 만 출력하고, 풀린 링크(ZIP·Windows·Sync 복사본)는 다시 만든다. 점폴더 안에 실제 폴더가 있으면 정본으로 옮기거나 `*_backup-<시각>` 으로 보존한다.

```bash
bash "90. Settings/94. Agent Settings/setup-agent-links.sh"          # 링크 생성·복구
bash "90. Settings/94. Agent Settings/setup-agent-links.sh" --check  # 확인만
```

Windows: `powershell -ExecutionPolicy Bypass -File "90. Settings\94. Agent Settings\setup-agent-links.ps1"`. symlink 에는 개발자 모드(설정 → 시스템 → 개발자용) 또는 관리자 권한이 필요하며, 없으면 스크립트가 디렉터리 junction 으로 대신 연결한다.

수동으로 할 때:

```bash
cd <vault-path>/.claude
for d in agents commands rules skills; do
  [ -e "$d" ] && ! [ -L "$d" ] && mv "$d" "${d}_backup"
  ln -s "../90. Settings/94. Agent Settings/claude/$d" "$d"
done
ls -l  # l로 시작하면 symlink — 확인 후 *_backup 내용을 정본에 합치고 삭제
```

- 훅(`hooks/`)을 쓰기 시작하면 정본 `claude/hooks/` 를 만들고 같은 방식으로 링크한다. Obsidian Sync 는 실행 권한을 떨어뜨리므로 머신마다 `chmod +x` 가 필요하고, `.sh` 는 Sync 설정의 **"기타 파일 유형(other file types)"** 을 켜야 넘어온다.

## CMDS Categories (100-900)

| Category | Name | Purpose |
|----------|------|---------|
| 📖 100 | Themes | Interests, topics, variables, terminologies |
| 📖 200 | Literature | Concepts, frameworks, theories, reviews |
| 📖 300 | Data | Data management, surveys, databases |
| 📖 400 | Methodologies | Research methods, statistics, ML, codes |
| 📖 500 | Products | Tools (Obsidian, ChatGPT, Claude, etc.) |
| 📖 600 | Specialties | KM, Second Brain, Gen AI, productivity |
| 📖 700 | Creatives | YouTube, SNS, music, digital art |
| 📖 800 | Outputs | PhD, articles, lectures, consulting |
| 📖 900 | Divisions | 9 operational divisions |

## Hierarchy System

- 🏛 — Home/Guide (top level)
- 📖 — 1st level CMDS (100-900 series)
- 📚 — 2nd level CMDS (N01-N99)
- (No icon) — 3rd level (detailed topics)
