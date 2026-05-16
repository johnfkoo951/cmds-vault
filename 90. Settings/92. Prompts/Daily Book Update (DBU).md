---
title: "Daily Book Update (DBU)"
abbreviation: DBU
category: batch
created: "2026-05-15"
tags:
  - prompt
  - book
  - daily
  - automation
when_to_use: "Living Book의 'every-day-grows' 메커니즘. 매일 한 번 vault의 새 메모/임포트를 스캔해 책 챕터에 1-2 문장씩 자라게 한다."
---

매일 오전 한 번, vault 의 최근 24h 활동을 스캔해서 `70. Outputs/Book/` 의 챕터들에 1–2 문장씩 자라게 하는 배치. 본 프롬프트는 [[daily-book-update]] 스킬을 cron 으로 트리거하는 thin wrapper — 실제 파이프라인은 스킬 안에 정의되어 있다.

## Input

- **Driven by skill**: 이 프롬프트는 [`daily-book-update`](../91.%20Skills/daily-book-update/SKILL.md) 스킬을 호출한다. 입력 스캔 범위/규칙은 스킬의 "Pipeline" 섹션 (`1. SCAN RECENT ACTIVITY`) 참조.
- **기본 스캔 범위** (스킬 정의 그대로):
	- `00. Inbox/` (Daily Notes, Clippings, AI Agent outputs)
	- `10. CMDS Process/`
	- `20. Literature Notes/`
	- `30. Permanent Notes/`
- **제외**: `00. Inbox/09. Legacy/`, `00. Inbox/03. AI Agent/` 의 비-md 산출물

## Output

- **In-place edits** to `70. Outputs/Book/Ch*/*.md` — 매칭된 챕터 본문 끝에 1–2 문장 + `[[wikilink]]` append
- **Critique inbox folded in**: `70. Outputs/Book/Critique Inbox/` 의 미처리 비평을 대상 챕터의 `## Critique Received` 섹션에 append, 원본은 `_processed/` 로 이동
- **Diff log**: `70. Outputs/Book/Daily Update Log.md` 에 한 줄 append
	- 예: `2026-05-15: Ch1 +2 sentences from [[2026-05-14 …]] · Ch3 empty section seeded · 1 critique queued`
	- 빈 날도 기록 (`no changes (vault idle)` 또는 `waiting for W2: chapter stubs`)
- **Canvas mirror** (변경 있을 때): `My Book Outline.canvas` 가 outline 변경을 반영하도록 재생성. manual-edited canvas 는 보존.
- **Bootstrap (first-run only)**: `My Book Outline.md` 가 template 상태이면 staging note 로부터 자동 합성 (스킬의 `0.5 BOOTSTRAP` 참조)

## Main Process

```
1. INVOKE skill: daily-book-update
   - 스킬이 PREP → SCAN → MATCH → ENRICH → CRITIQUE → LOG → (CANVAS SYNC) 순으로 실행
2. RETURN summary (log line)
```

전체 파이프라인은 [[daily-book-update]] SKILL.md 의 "Pipeline" 섹션에 정의. 본 프롬프트는 진입점일 뿐.

## Constraints

스킬 정의에서 가져온 핵심 제약 — 한눈에 보기 위해 재게시:

- **Read-only 영역**: `## Author Voice / Reflection`, frontmatter (type/created/parent), 사람이 작성한 본문
- **Append-only 영역**: section 본문 끝, `## Critique Received`, `Daily Update Log.md`
- **Idempotent**: 같은 entry 를 이중 인용하지 않는다 (Daily Update Log + chapter 본문 wikilink 검색으로 dedupe). 채워진 outline 에 BOOTSTRAP 재실행하지 않는다.
- **Small steps**: 한 실행에서 chapter 당 최대 3 sentences 추가
- **Wikilink safety**: 모든 `[[wikilink]]` 는 작성 전 filesystem 검증. 미존재 target 은 drop. 이유: broken wikilink 클릭 시 `00. Inbox/` 에 빈 placeholder 가 생성되어 인박스 오염. emoji prefix (📜/📚/🏛/…) 포함해서 검증 (`.claude/rules/wikilink-rules.md`).
- **Status logging when waiting**: outline 채워졌으나 chapter 파일 없으면 매 run 마다 `"waiting for W2: chapter stubs"` 라벨로 로그 (silent no-op 금지)

## Configuration

```yaml
# orchestrator.yaml 예시 — daily cron
- type: agent
	name: Daily Book Update (DBU)
	cron: 0 8 * * *  # 매일 오전 8시
	output_path: "70. Outputs/Book"
	enabled: false   # 처음에는 opt-in. 셋업 검증 후 true 로
```

`enabled: false` 로 시작하는 이유: BOOTSTRAP 이 outline 을 자동 합성하기 때문에, 학생이 W2 (chapter stubs) 단계 진입을 확인한 뒤 flip 하는 것이 안전하다. 수동 검증 절차는 [[daily-book-update]] SKILL.md "Verification (first run)" 섹션 참조.

## Post-processing (사람이 한다)

매일 한 번 (또는 주말에 몰아서):

1. `Daily Update Log.md` 의 한 줄 보고 → 어디가 자랐는지 확인
2. 자란 챕터 열어서 새로 append 된 문장 검토 — keep / rewrite / drop
3. `## Critique Received` 의 새 비평 → 본문에 반영 여부 결정
4. 부족한 챕터가 있으면 [[Outline → Paragraph (OTP)]] / [[Add-Author-Voice (AAV)]] 수동 호출로 보강

## Differences from DRB

[[Daily Research Briefing (DRB)]] 와의 관계:

| 항목 | DRB | DBU |
|------|-----|-----|
| 시간 | 07:00 | 08:00 |
| 소스 | 외부 웹 (논문/뉴스/블로그) | 내부 vault (Inbox/Permanent Notes 등) |
| 출력 | `03. AI Agent/` 의 새 브리핑 파일 (inbox 자료) | `70. Outputs/Book/` 챕터에 in-place edit + log |
| 자동 머지 | X — 사용자가 결정 | O (제한적) — 챕터 본문 append, critique 는 queue만 |
| 모드 | scope (topics / book / project / paths) | 단일 (Living Book 전용) |
| 페어 | [[Generate Daily Roundup (GDR)]] (내부 활동 정리) | (이 프롬프트 자체가 책 갱신) |

DRB 는 *외부 자료를 가져오는* 채집 단계, DBU 는 *vault 안의 자료를 책으로 모으는* 가공 단계. 두 cron 이 하루 시작에 30분 간격으로 도는 그림이 권장 셋업.

## Related

- 스킬: [[daily-book-update]] — 실제 파이프라인 정의
- 짝: [[Daily Research Briefing (DRB)]] — 외부 자료 채집 (07:00)
- 사후 가공 프롬프트: [[Outline → Paragraph (OTP)]], [[Add-Author-Voice (AAV)]]
- 책 구조: `70. Outputs/Book/My Book Outline.md`, `My Book Outline.canvas`
- 비평 inbox: `70. Outputs/Book/Critique Inbox/`
