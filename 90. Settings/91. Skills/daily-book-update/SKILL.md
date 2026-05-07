---
name: daily-book-update
description: Daily automated update of the student's Living Book chapters — scans vault for new memos/imports, bootstraps an empty outline from staging notes, mirrors changes into the matching .canvas, enriches relevant chapter sections, folds in critique inbox items, and writes a daily diff log. Activate when scheduled (cron / launchd / Task Scheduler) or when the user says "update my book", "오늘 책 업데이트", "daily book update".
metadata:
  version: "0.3"
  author: jykim
  created: 2026-05-02
  updated: 2026-05-07
  base: "https://github.com/johnfkoo951/cmds-vault — Living Book scaffolding"
---

# daily-book-update

Living Book 의 첫 번째 메커니즘 ("매일 자라는 책") 을 구현하는 스킬. 학생이 매일 손대지 않아도 매일 한 번씩 본인 책 챕터가 보강된다.

## When to Use

다음 중 어느 하나에 해당하면 활성화:
- 스케줄러 (cron / launchd / Task Scheduler) 가 주기적으로 호출
- 사용자가 "update my book", "오늘 책 업데이트", "daily book update", "매일 갱신" 등을 말함
- W3 (Session 3) 이후 학생이 워크플로우 가동 검증을 위해 수동 실행

## Pipeline

각 실행은 작다 — 한 두 단락 수준 변경. 14일 누적되면 챕터가 눈에 띄게 자란다.

```
0. PREP
   - vault 루트 확인: CMDS.md / 70. Outputs/Book/ 존재
   - 70. Outputs/Book/My Book Outline.md 읽기 → core_question, chapter list 추출
   - 70. Outputs/Book/My Book Outline.canvas 존재·내용 읽기 (있으면 — JSON 파싱)
   - 70. Outputs/Book/<chapter>.md 파일 목록 수집
   - 70. Outputs/Book/assets/ 의 cover 후보 이미지 감지 (jpg/png/webp)
   - outline template 상태 감지:
     - core_question 또는 chapter 행에 "<...>" 플레이스홀더가 남아 있으면 → 0.5 BOOTSTRAP 으로 분기
     - 채워져 있으면 → 0.6 CANVAS SYNC (필요 시) → 1. SCAN 으로 진행

0.5 BOOTSTRAP (first-run only — outline 이 template 상태일 때만 실행)
   - 1. SCAN 을 먼저 실행해 최근 24h 자료 수집
   - 추가로 70. Outputs/Book/ 외부의 가까운 staging note 도 함께 읽음
     (e.g. CMDS=📚 101 Interests / 📚 102 Topics 의 inProgress 노트 — book 의도가 명시된 hub note)

   a. **CONCEPT INFERENCE** — staging note 가 ingested 책 (예: `10. Raw Sources/13. Books/` 의 prior-art 책) 을 5건 이상 참조하면 → "prior-art tracking" 컨셉 채택. 그 책의 챕터 구조를 1:1 골조로 사용. 그 외에는 opportunity-gap 또는 hub-theme 기반으로 자율 합성.

   b. **합성**:
     - core_question (1–3 줄) — staging note 의 mission/intent 진술에서 추출 (concept 에 따라 phrasing 조정)
     - target_reader — staging note 또는 관련 미팅·경험 기록에서 추출
     - chapter candidates 5–7개 — concept 에 따라:
       · prior-art tracking → 원작 N장 spine 그대로 + 각 장에 "← spine, → 갱신" annotation
       · opportunity-gap → 식별된 gap 들을 챕터로
       · hub-theme → staging note 의 sub-theme 들을 챕터로
     - Source Materials — 합성에 사용한 노트들의 [[wikilink]] 목록 (그룹별: prior-art ingest / Permanent / Literature / Synthesis)
     - Notes — staging note 의 "왜 이 책을 쓰는가" 단락을 발췌
     - Cover (있으면) — `70. Outputs/Book/assets/` 의 후보 이미지를 `![[<filename>]]` embed 로

   c. **WIKILINK VERIFICATION** (필수): 합성 결과에 들어갈 모든 [[wikilink]] 는 작성 전 filesystem 검증.
     - 존재하지 않는 target 은 drop (또는 텍스트 인용으로 demote)
     - 이유: `wikilink-rules.md` 에 따라 broken wikilink 클릭 시 `00. Inbox/` 에 빈 placeholder 파일 생성됨 → 인박스 오염
     - emoji-prefixed target (📜/📚/🏛/...) 는 정확한 prefix 포함해서 검증

   d. **OUTLINE WRITE** — My Book Outline.md 의 해당 섹션만 in-place 치환:
     - frontmatter 형식과 다른 섹션은 보존 (refactor 금지)
     - YAML 규칙 준수: 2 spaces, 위키링크는 큰따옴표 (CLAUDE.md 참조)
     - 추가 섹션 (Concept, Cover) 은 outline 시작부에 삽입 가능

   e. **CANVAS SYNC** — `0.6 CANVAS SYNC` 호출하여 outline 변경을 canvas 에도 반영

   f. **LOG** — Daily Update Log 에 "bootstrap" 라벨로 한 줄 기록 후 종료
     (이번 실행에서 ENRICH/CRITIQUE 는 건너뜀 — chapter 파일 없음)

0.6 CANVAS SYNC (outline ↔ canvas 미러 — BOOTSTRAP 후 또는 수동 호출)
   - 70. Outputs/Book/My Book Outline.canvas 가 존재하면 outline 의 변화를 반영하도록 재생성
   - 기본 layout (vertical scan):
     - cover (`type:file` 노드, 있으면) — far-left anchor
     - cover_caption — 표지 출처 메모
     - reader / core / sources — header row
     - concept (`color:5`) — full-width row, "변하지 않는 본질 vs 새로 필요한 판단력" 같은 high-level framing (prior-art tracking 컨셉일 때 권장)
     - chapters (color:4) — single column, top-to-bottom (vertical scan)
     - chapter ideas (color:1) — RHS, 1:1 aligned with chapters
   - edges:
     - cover → concept, reader → core, core → sources
     - core → concept → ch1 → ch2 → ... → chN (체인)
     - 각 chapter → 해당 ideas 카드 (right side)
   - 색상 일관성 규칙:
     - 동일한 처리(treatment) 받는 챕터는 같은 색
     - reboot/gap 등 의미 카테고리 구분 시에만 색 다양화
   - 수동 customization 보존 — 기존 canvas 에 사용자 추가 노드 (예: 연표·인용·메모) 가 있으면 합성 대신 LOG 에 "manual canvas detected, skipping auto-sync" 기록

1. SCAN RECENT ACTIVITY
   - 다음 폴더에서 최근 24h 내 modified .md 파일 수집:
     - 00. Inbox/                (Daily Notes, Clippings, AI Agent outputs 등)
     - 10. CMDS Process/         (Connect/Merge/Develop/Share 작업물)
     - 20. Literature Notes/     (외부 자료 임포트)
     - 30. Permanent Notes/      (정제된 개인 지식)
   - 제외: 00. Inbox/09. Legacy/, 00. Inbox/03. AI Agent/ 의 비-md 산출물 (이미지/영상/코드)
   - 빈 결과면 → 4. PROCESS CRITIQUE INBOX 로 점프

2. MATCH TO CHAPTER
   - 각 새 entry 마다, chapter list 의 어느 섹션과 가장 관련 있는지 추론
     - chapter file 의 헤더 + core_question 을 컨텍스트로
     - 매칭 신뢰도 낮으면 (e.g. < 0.6) 스킵하고 로그에 unmatched 로 기록
   - 매칭된 entry 별로 1–2 문장 요약 + [[wikilink]] 인용 생성

3. ENRICH SECTION
   - 매칭된 chapter 의 해당 섹션 끝에 1–2 문장 append
     - 형식: "<요약 문장>. → [[<wikilink>]]"
   - 섹션이 비어 있으면: 90. Settings/92. Prompts/Book/Outline-to-Paragraph (OTP).md 호출하여 첫 단락 생성
   - **NEVER touch**:
     - "## Author Voice / Reflection" 섹션 (read-only)
     - "## Critique Received" 의 사람이 추가한 응답 부분
     - chapter frontmatter

4. PROCESS CRITIQUE INBOX
   - 70. Outputs/Book/Critique Inbox/ 에서 처리되지 않은 .md 파일 수집
   - 각 비평 파일에서 대상 chapter 추출 (frontmatter target_chapter 또는 wikilink)
   - 대상 chapter 의 "## Critique Received" 섹션에 비평을 timestamp + 출처와 함께 append
   - **자동 반영하지 않음** — 사람이 읽고 본문에 반영. 비평은 보관 + 표시만.
   - 처리한 비평 파일을 70. Outputs/Book/Critique Inbox/_processed/ 로 이동

5. LOG
   - 70. Outputs/Book/Daily Update Log.md 에 한 줄 append:
     - "YYYY-MM-DD: <chapter A> +2 sentences from [[<source>]] · <chapter B> empty section seeded · 1 critique queued"
   - 빈 날도 기록: "YYYY-MM-DD: no changes (vault idle)"
```

## Constraints

- **Read-only 영역**: Author Voice / Reflection 섹션, frontmatter (type/created/parent), 사람이 작성한 본문
- **Append-only 영역**: section 본문 끝, Critique Received, Daily Update Log
- **Idempotent**:
  - 같은 entry 를 이중 인용하지 않는다 (Daily Update Log 또는 chapter 본문에서 wikilink 검색으로 dedupe)
  - 채워진 outline 에 BOOTSTRAP 재실행하지 않는다 (template-state 만 트리거; 사용자가 명시적으로 "re-bootstrap" 요청 시 예외)
  - 사용자 manual edit 이 들어온 canvas 는 auto-sync 하지 않는다
- **Small steps**: 한 실행에서 chapter 당 최대 3 sentences 추가. 폭주 방지.
- **Wikilink safety**: 모든 [[wikilink]] 는 작성 전 filesystem 검증. 미존재 target 은 drop. 이유: `wikilink-rules.md` 에 따라 broken link 클릭 시 인박스에 빈 placeholder 파일 생성 → 인박스 오염.
- **Status when waiting**: outline 채워졌으나 chapter 파일 없음 → 매 run 마다 "waiting for W2: chapter stubs" 라벨로 명시 로그 (silent no-op 금지).

## Setup

각 OS 별 스케줄러 등록 — 학생이 W3 실습 단계 2에서 1번 셋업하면 끝.

### macOS (launchd, 권장)

```bash
# Save as ~/Library/LaunchAgents/com.cmds.daily-book-update.plist
# Trigger: 매일 07:00
launchctl load ~/Library/LaunchAgents/com.cmds.daily-book-update.plist
```

`.plist` 템플릿은 `references/launchd.plist.template` 참조 (TODO: 추가 예정).

### macOS / Linux (cron)

```bash
crontab -e
# Add:
0 7 * * * cd ~/Documents/cmds-vault && claude run "use the daily-book-update skill" >> /tmp/daily-book-update.log 2>&1
```

### Windows (Task Scheduler)

- Trigger: Daily 07:00
- Action: Start a program
- Program: `C:\path\to\claude.exe`
- Arguments: `run "use the daily-book-update skill"`
- Start in: `C:\Users\<you>\Documents\cmds-vault`

## Verification (first run)

```
1. Drop dummy memo: 00. Inbox/01. Daily Notes/2026-MM-DD.md
   - content 에 본인 챕터 핵심 키워드 1개 포함
2. Manual run: claude run "use the daily-book-update skill"
3. Check:
   - 매칭된 chapter 에 1-2 문장 + [[wikilink]] append 됨
   - 70. Outputs/Book/Daily Update Log.md 에 한 줄 append 됨
4. Re-run immediately:
   - 같은 entry 가 두 번 인용되지 않음 (idempotency check)
```

## Cohort Context

W3 (Session 3) 의 핵심 가동 메커니즘. → [Session 3 docs in jykim's GOBI vault]

## TODO (PR welcome)

- [ ] `references/launchd.plist.template`
- [ ] `references/cron.example`
- [ ] `references/task-scheduler.xml.template`
- [ ] `scripts/install-scheduler.sh` (OS 자동 감지 + 등록)
- [ ] Matching score 임계값 튜닝 (현재 0.6, 데이터 모이면 조정)

## Changelog

- **0.3 (2026-05-07)**: 첫 가동 후 lessons-learned 반영.
  - BOOTSTRAP 에 **CONCEPT INFERENCE** 추가 — staging note 가 ingested 책을 다수 참조하면 prior-art tracking 컨셉 자동 채택 (해당 책의 챕터 spine 1:1 사용; 예: HelloDS-Reboot 7-chapter ingest → DS 책 7장 spine).
  - **WIKILINK VERIFICATION** 의무화 — 모든 wikilink 작성 전 filesystem 검증 (인박스 오염 방지). 미존재 target 은 drop 또는 텍스트 인용으로 demote.
  - 신규 step **0.6 CANVAS SYNC** — outline ↔ canvas 미러; 기본 vertical-scan 레이아웃 (cover 노드 anchor, concept card, chapter chain, RHS ideas cards) 정의. manual-edited canvas 는 보존.
  - **Cover asset detection** — `70. Outputs/Book/assets/` 의 표지 후보 자동 embed (outline + canvas).
  - **Status logging** 강화 — outline 은 채워졌으나 chapter 파일 없는 단계도 명시 로그 ("waiting for W2: chapter stubs"). silent no-op 금지.
  - Idempotency 명문화 — filled outline 에 BOOTSTRAP 재실행 금지 (사용자 명시 요청 시 예외); manual-edited canvas 는 auto-sync 스킵.
- **0.2 (2026-05-07)**: SCAN scope 를 `00. Inbox/` ~ `30. Permanent Notes/` 전체로 확장 (이전: Daily Notes + Literature Notes 만). first-run BOOTSTRAP 단계 추가 — outline 이 template 상태면 SCAN 결과 + staging note 로 outline 자동 채움.
- **0.1 (2026-05-02)**: 초기 구현.
