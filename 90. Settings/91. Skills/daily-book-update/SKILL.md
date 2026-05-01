---
name: daily-book-update
description: Daily automated update of the student's Living Book chapters — scans vault for new memos/imports, enriches relevant chapter sections, folds in critique inbox items, and writes a daily diff log. Activate when scheduled (cron / launchd / Task Scheduler) or when the user says "update my book", "오늘 책 업데이트", "daily book update".
metadata:
  version: "0.1"
  author: jykim
  created: 2026-05-02
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
   - 70. Outputs/Book/<chapter>.md 파일 목록 수집

1. SCAN RECENT ACTIVITY
   - 00. Inbox/01. Daily Notes/ 에서 최근 24h 내 modified 파일 수집
   - 20. Literature Notes/ 에서 최근 24h 내 modified 파일 수집
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

- **Read-only 영역**: Author Voice / Reflection 섹션, frontmatter, 사람이 작성한 본문
- **Append-only 영역**: section 본문 끝, Critique Received, Daily Update Log
- **Idempotent**: 같은 entry 를 이중 인용하지 않는다 (Daily Update Log 또는 chapter 본문에서 wikilink 검색으로 dedupe)
- **Small steps**: 한 실행에서 chapter 당 최대 3 sentences 추가. 폭주 방지.

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
