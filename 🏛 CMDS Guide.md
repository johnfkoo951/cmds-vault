---
type: CMDS
aliases:
  - CMDS Guide
  - guide
description: "Operational standards guide for the CMDS vault. Defines the 7 required Properties, standard note types, file naming conventions, folder structure, citation styles, and template examples. Reference when creating new notes or validating existing ones."
author:
  - "[[Me]]"
date created: 2025-09-15T23:39
date modified: 2026-04-28
tags:
  - CMDS
  - system
  - guideline
  - index
  - NoteClass
  - operation
  - maps
  - example
  - service
audience: User + AI
scope: operational-standards
precedence: 4
memory-type: reference
required-for:
  - file-creation
  - standards-compliance
optional-for:
  - search
  - analysis
token-estimate: 4800
links: []
index: "[[🏛 CMDS Head Quarter]]"
version: "2.3"
status: completed
changelog:
  - "2.3 (2026-04-07): 필수 프로퍼티 7개로 확장 (description 추가, English required for LLMs)"
  - "2.2 (2026-04-01): precedence/memory-type/token-estimate 추가, tags 정리"
  - "2.1 (2026-03-15): 폴더 구조 현행화, 새 type 추가"
---

> **🔄 Last Updated: 2026-04-28** | Upstream reference: [system.cmdspace.work](https://system.cmdspace.work) (canonical CMDS conventions by 구요한 / Yohan Koo)
>
> 📌 **Version 2.3** — Properties 표준화 및 체계 개선판

# CMDS Guide

이 문서는 CMDS 볼트에서 노트를 만들고 관리할 때 따르는 **표준 규칙**을 정의합니다. 새 노트를 만들 때마다 여기를 참조하세요.

> **저자 표기 규칙**: 시스템 파일과 새 노트의 `author` 필드는 기본적으로 `[[Me]]` placeholder로 시작합니다. 온보딩 후에 본인 이름으로 일괄 치환하세요. 자세한 절차는 [[WELCOME]] 참조.

## Properties

### 필수 Properties (Required)

모든 노트는 다음 7개의 필수 properties를 포함해야 합니다:

```yaml
---
type:           # 노트 유형 (아래 표준 type 참조)
aliases: []     # 별칭 (배열 형식)
description: "" # 1-2 문장 영어 요약 (LLM용, 아래 규칙 참조)
author:
  - "[[Me]]"  # 작성자 (wikilink 형식, 온보딩 후 본인 이름으로 일괄 치환)
date created:   # 생성일 (YYYY-MM-DDTHH:mm:ss)
date modified:  # 수정일 (YYYY-MM-DDTHH:mm:ss)
tags: []        # 태그 (배열 형식)
---
```

> ⚠️ **`description` 작성 규칙**
> - **반드시 영어로 작성**. LLM(Claude Code, Gemini CLI, ChatGPT 등)이 이 노트의 관련성을 판단할 때 사용하는 기계 가독 힌트입니다.
> - **1-2 문장**, skill/tool description처럼 구체적이고 action-oriented하게.
> - 노트의 내용 + 언제 참조해야 하는지를 함께 제공.
> - **항상 큰따옴표(`"..."`)로 감쌀 것.** 안에 `: ` 또는 ` #` 들어가면 YAML plain scalar 파서가 깨져 Obsidian Properties 패널 렌더가 손상됩니다.
> - ✅ 좋음: `"Synthesized analysis of X. Reference when planning Y."`
> - ❌ 나쁨: `"이건 노트에요"` (한국어, 무정보)
> - ❌ 나쁨: `"This is a note"` (관련성 신호 없음)

### 표준 Properties 정의

#### 날짜 관련
- `date created` - 생성일 (YYYY-MM-DDTHH:mm:ss)
- `date modified` - 수정일 (YYYY-MM-DDTHH:mm:ss)
- `date` - 이벤트/미팅 날짜 (YYYY-MM-DD)
- `publish_date` - 발행일 (YYYY-MM-DD)
- `year` - 연도 (YYYY)

> ⚠️ **통일 규칙**: 모든 날짜는 ISO 8601 형식 (YYYY-MM-DD) 사용

#### 작성자 및 관계
- `author: [[Me]]` - 항상 wikilink 형식 사용 (온보딩 시 본인 이름으로 치환)
- `attendees: []` - 참석자 목록 (wikilink 배열)
- `organization: [[조직명]]` - 조직 (wikilink)

#### 분류 및 상태
- `type` - 노트 유형 (아래 표준 type 목록 참조)
- `CMDS` - CMDS 카테고리 연결 (예: `[[📚 620 Generative AI]]`) — 반드시 📚 2nd-level 가리킴
- `index` - 인덱스 참조 (예: `[[🏷 Meeting Notes]]`) — 반드시 🏷 Index 가리킴
- `status` - 상태값
	- ✅ 표준값: `unread` | `reading` | `inProgress` | `completed` | `archived`

#### 평가 및 측정
- `myRate` - 평점 (1-5 scale, 숫자)
- `totalPage` - 총 페이지 수 (camelCase)
- `views` - 조회수

#### 연결 및 참조
- `aliases: []` - 별칭 (배열 형식으로 통일)
- `tags: []` - 태그 (배열 형식으로 통일)
- `links` - 관련 링크
- `source` - 출처
- `source_url` - 출처 URL

#### CMDS Process Command Fields (v2.2, 2026-04-14+)

CMDS Process 슬래시 커맨드 (`/connect`, `/merge`, `/develop`, `/share`, `/query`) 가 자동으로 기록하는 프로퍼티. 모두 **camelCase**, 배열 필드는 quoted wikilink.

| 필드 | 기록하는 커맨드 | 용도 |
|------|---------------|------|
| `sourceInbox: []` | `/connect` | Theme stub 이 어느 inbox 파일에서 캡처됐는지 배열로 기록 |
| `mergePurpose: ""` | `/merge` | 합성 목적 (한 줄 맥락). 다운스트림 `/share` 의 format 자동 추천에 사용 |
| `sourceNotes: []` | `/merge` | 합성에 쓰인 후보 노트들의 wikilink 배열 (N→1 traceability) |
| `mainVaultRelated: []` | `/merge`, `/query` | 위성 볼트 페이지 참조 (text ref 형식: `"→ Other Vault: {page name}"`) |
| `developSources: []` | `/develop` | artifact 가 참조한 method/data/specialty 노트들 |
| `shareSourceNotes: []` | `/share` | 산출물이 어느 합성 노트에서 나왔는지 |
| `shareFormat: ""` | `/share` | newsletter / slides / video / social / article / proposal 등 |
| `sharePurpose: ""` | `/share` | 왜 이 share 가 일어났는지 (예: "월간 팀 공유용") |
| `queryOrigin: ""` | `/query` | 원 질문 verbatim (file-back 된 답변 노트에 기록) |
| `querySources: []` | `/query` | 답변 합성에 쓰인 노트 배열 |

사용 예시 (merge 된 Literature 노트):

```yaml
---
type: note
aliases: []
description: "Synthesized analysis comparing RAG and Compiled Wiki patterns for team research sharing workflows. Reference when deciding between retrieval-based vs pre-compiled knowledge architectures."
author:
  - "[[Me]]"
date created: 2026-04-14
date modified: 2026-04-14
tags:
  - merged
  - rag
  - knowledge-management
  - literature-review
CMDS: "[[📚 210 Literature Reviews]]"
index: "[[🏷 Research Notes]]"
status: completed
mergePurpose: "주간 팀 리서치 공유 워크플로 재설계"
sourceNotes:
  - "[[RAG 한계 분석]]"
  - "[[Compiled Wiki 운영 경험]]"
related:
  - "[[📚 601 Knowledge Management]]"
---
```

> **구현 위치**: 커맨드 정의는 `.claude/commands/` 또는 `90. Settings/94. Agent Settings/claude/commands/`. 전체 커맨드 사용법은 [[CLAUDE]] "CMDS Process Command Suite" 섹션 참조.

### 표준 Type 목록

#### 주요 노트 타입
- `note` - 일반 노트
- `terminology` - 용어 정의
- `meeting` - 회의록
- `people` - 인물 정보
- `curriculum` - 강의 커리큘럼
- `memo` - 메모
- `class` - 수업 관련
- `manuscript` - 원고/초안
- `daily-note` - 일일 노트
- `article` - 글/기사
- `sermon` - 설교
- `review` - 리뷰/연구평론
- `project` - 프로젝트
- `zettel` - 제텔카스텐 노트

#### 구조/조직 타입
- `CMDS` - 커맨드스페이스 인덱스 (전통 MOC 개념 대체)
- `organization` - 조직/기관
- `portal` - 포털 페이지
- `documentation` - 문서화/가이드
- `index` - 색인
- `moc` - Map of Content

#### 콘텐츠 타입
- `books` - 도서
- `research-review` - 연구 리뷰
- `research-pipeline` - 연구 파이프라인
- `api` - API 문서
- `idea` - 아이디어
- `resource` - 리소스
- `product` - 제품/서비스
- `channel` - YouTube/Blog/Newsletter 채널 프로필

### Tags

- 태그는 자유롭게 작성하되 일관성 유지
- Nested tags 예시:
	- `#Author/Koo`
	- `#가이드/태그작성법`
	- `#가이드/목차작성법`

## Collections

### CMDS

- [[🏛 CMDS Head Quarter]]
- [[🏛 CMDS Guide]]

### Index (예시 — 본인 볼트 운영하면서 채워나갈 것)

#index #NoteClass #maps

- [[🏷 Guideline]]
- [[🏷 Daily Notes]]
- [[🏷 Research Notes]]
- [[🏷 Project Notes]]
- [[🏷 Lecture Notes]]
- [[🏷 Review Notes]]
- [[🏷 Draft Article]]
- [[🏷 Web Clips]]
- [[🏷 Waypoint]]
- [[🏷 Meeting Notes]]
- [[🏷 People]]
- [[🏷 Organization]]
- [[🏷 Prompts]]
- [[🏷 Syntax and Codes]]
- [[🏷 Recordings]]

> 💡 Index 노트는 학생 본인이 사용하면서 만들어 가는 것. 처음에는 위 wikilink 들이 모두 비어있고, 첫 노트가 생기는 순간 자동으로 의미를 갖습니다.

### Backlinks

- 백링크는 본인 인지범위가 허락하는 선까지 `[[]]`
- 한 번에 다 할 필요는 없음
- AI 보조로 자동 연결 가능
	- Smart Composer (Obsidian 플러그인) - YAML, In-line
	- Claude Code (`/connect` 등 슬래시 커맨드)

## CMDS Levels

### 계층 구조

- 🏛 - Home, Guide (최상위)
- 📖 - 1st level CMDS (100-900 시리즈)
	- Space Collection
	- 1 digit (100-900)
- 📚 - 2nd level CMDS (N01-N99)
	- Spaces
	- 2 digit (N01-N99)
- (No Icon) - 3rd level CMDS
	- 상세 주제는 3rd level CMDS로 분류

### CMDS Level Example

```
📚 840 Lectures
├── 840.01 University Courses
│   ├── 840.01-A {대학명}
│   │   ├── 840.01-A1 2026-1
│   │   │   └── [[수업명]]
│   │   └── 840.01-A2 2026-2
│   │       └── [[다른 수업명]]
│   └── 840.01-B {다른 대학}
```

## Filename Conventions

### 접두사 (Prefix)

#### Input
- 📎 - Web Clips
- 🌿 - Readwise
- 📘 - Books, Reference (`#📚Book`)

#### Process
- 🏷 - Index
- 📦 - Review

#### Output
- 🔖 - Personal Idea Output
- 📜 - Other's Idea Output
- 📈 - Code and Syntax
- 🎹 - Music
- 🏙 - Canvas

#### References
- 📕 - Bible

### 접미사 (Suffix)

#### Service에 따라
- `.obsidian`
- `.python`
- `.chatgpt`
- `.claude`
- `.midjourney`

#### Purpose에 따라
- `.meeting`
- `.portal`

## Folder Structure

> 자세한 폴더 구조는 [[CLAUDE]] 의 Directory Structure 섹션과 `.claude/rules/directory-structure.md` 참조.

```
00. Inbox/                      # 임시 저장 및 처리 공간
├── 01. Daily Notes/            # 데일리 노트
├── 02. Clippings/              # 웹 클리핑
├── 03. AI Agent/               # ⭐ AI 코드 작업 전용 (PRIMARY)
├── 04. Excalidraw/             # 다이어그램
├── 05. Canvas/                 # Canvas 노트
├── 06. Automation/             # 자동화
├── 07. App Sync/               # 외부 앱 연동
├── 08. Unlisted/               # 미분류
└── 09. Legacy/                 # 레거시 컨텐츠

10. CMDS Process/               # CMDS 프로세스 워크플로우
20. Literature Notes/           # 문헌 노트 및 리뷰
30. Permanent Notes/            # 영구 노트 (Evergreen)
40. Docs/                       # 기술 문서 (Technical Documentation)
50. Assets/                     # 미디어 및 자산
60. Collections/                # 엔티티 관리 컬렉션
70. Outputs/                    # 최종 산출물
80. References/                 # 참고 자료 및 출처
90. Settings/                   # 시스템 설정 및 관리
├── 91. Skills/                 # Skills (gobi-cli, gobi-onboarding 등)
├── 92. Prompts/                # Prompt assets (CBH 등)
└── 94. Agent Settings/         # AI 에이전트 설정 (claude/{commands,rules,skills,agents})
```

## Properties Template Examples

### 기본 노트 템플릿

```yaml
---
type: note
aliases: []
description: ""
author:
  - "[[Me]]"
date created: 2026-04-28T14:30
date modified: 2026-04-28T14:30
tags: []
CMDS: 
index: 
status: 
---
```

### 회의록 템플릿

```yaml
---
type: meeting
aliases: []
description: ""
author:
  - "[[Me]]"
date created: 2026-04-28T09:00
date: 2026-04-28
attendees:
  - "[[참석자1]]"
  - "[[참석자2]]"
organization: "[[조직명]]"
CMDS: "[[📚 831 Consulting]]"
index: "[[🏷 Meeting Notes]]"
status: inProgress
tags: [meeting]
---
```

### 연구 노트 템플릿

```yaml
---
type: research-review
aliases: []
description: ""
author:
  - "[[Me]]"
date created: 2026-04-28T16:45
title: 
source: 
source_url: 
doi: 
keywords: []
CMDS: "[[📚 820 Research]]"
index: "[[🏷 Research Notes]]"
status: reading
tags: [research]
---
```

### 도서 노트 템플릿

```yaml
---
type: books
aliases: []
description: ""
author:
  - "[[Me]]"
date created: 2026-04-28T11:20
title: 
subtitle: 
isbn: 
publisher: 
publish_date: 
totalPage: 
myRate: 
status: unread
CMDS: "[[📚 240 Books]]"
index: "[[🏷 Books]]"
tags: [📚Book]
---
```

### 인물 노트 템플릿

```yaml
---
type: people
aliases: []
description: ""
author:
  - "[[Me]]"
date created: 2026-04-28T10:15
email: 
mobile: 
organization: "[[조직명]]"
group: 
CMDS: 
index: "[[🏷 People]]"
status: 
tags: [people]
---
```

## Property 네이밍 규칙 (Naming Convention)

CMDS 볼트에서 YAML 프로퍼티 이름을 지을 때 따르는 규칙입니다.

### camelCase (카멜케이스) — 복합 단어 프로퍼티의 기본 규칙

두 단어 이상을 조합할 때, **첫 단어는 소문자**, **이후 단어의 첫 글자만 대문자**로 쓰는 방식입니다.

```yaml
# ✅ camelCase (CMDS 표준)
myRate: 5
totalPage: 320
startReadDate: 2026-03-30
channelUrl: "https://youtube.com/@example"
updateFrequency: weekly

# ❌ 잘못된 예시
my_rate: 5        # snake_case — 사용 금지
my-rate: 5        # kebab-case — YAML에서 문제 가능
MyRate: 5         # PascalCase — 사용 금지
```

### snake_case (스네이크케이스) — 레거시 호환

단어 사이를 밑줄(`_`)로 연결하는 방식입니다. CMDS에서는 **기존에 이미 대량으로 사용 중인 프로퍼티**에 한해 유지합니다.

```yaml
# ⚠️ snake_case (레거시 유지 — 신규 사용 금지)
source_url: "https://example.com"
publish_date: 2026-01-15
recommended_by:
  - "[[추천인]]"
```

### 단일 단어 — 그대로 소문자

한 단어로 된 프로퍼티는 그냥 소문자입니다.

```yaml
type: note
platform: YouTube
language: Korean
status: completed
```

### Obsidian 기본값 — 공백 허용

Obsidian이 자동 생성하는 프로퍼티는 공백 형태를 유지합니다.

```yaml
date created: 2026-03-30
date modified: 2026-03-30
```

### 요약 표

| 패턴 | 사용 시점 | 예시 |
|------|----------|------|
| **camelCase** | 새로운 복합 단어 프로퍼티 (기본) | `myRate`, `totalPage`, `channelUrl` |
| **snake_case** | 기존 대량 사용 중인 레거시만 유지 | `source_url`, `publish_date` |
| **소문자** | 단일 단어 프로퍼티 | `type`, `platform`, `status` |
| **공백** | Obsidian 기본값 | `date created`, `date modified` |

> **원칙**: 새 프로퍼티를 만들 때는 반드시 **camelCase**를 사용하세요. `rating` 대신 `myRate`, `channel_url` 대신 `channelUrl`입니다.

---

## Note-taking Guidelines

### Citation Style

#### 책 인용
> [!TIP] _책 제목_
> 책의 내용 원본^[저자명. (출판년도). _책 제목._ 출판사. p.페이지.]

#### 논문 인용
> [!ABSTRACT] 논문 제목
> 핵심 주장^[저자명. (출판년도). 논문 제목. _저널명_, 권(호), 페이지범위.]

#### 명언 / 직접 인용
> [!QUOTE]
> "인용문"
> — 화자

---

## Sync Settings (선택)

<!-- TODO: 본인 환경에 맞춰 채울 것
이 볼트가 단일 머신용인지, 여러 Mac/PC 간 Obsidian Sync로 동기화하는지 기록.
예시:

| 환경 | 기기 | Base Path |
|------|------|-----------|
| Primary | (your machine) | `~/Documents/cmds-vault` |

다중 환경이라면 `00. Inbox/03. AI Agent/` 하위에 머신/에이전트별 서브폴더를 두어 출처를 추적할 수 있음.
-->

## Version History

- **v2.3** (2026-04-07): description 필드 영어 + double-quote 강제 규칙 도입
- **v2.2** (2026-04-01): precedence/memory-type/token-estimate 메타필드 추가
- **v2.1** (2025-10-23): 폴더 구조 현행화, 새 type 추가
- **v2.0** (2025-09-15): Properties 표준화 및 체계 개선
- **v1.0** (2022-05-25): 초기 버전

## 추가 참고사항

### Graph View 활용

Obsidian Graph View 필터 예시:
- `-tag:Waypoint`
- `-path:"01. Daily Notes"`
- `-path:"study" -path:"reading"`
- `-file:"00. Inbox" -tag:waypoint`
- `["type":curriculum]`

### 추천 플러그인 (CMDS 워크플로 친화)

#### Supercharged Links
- People, Organization, Curriculum 노트 시각 강조

#### 그 외 자주 쓰는 것
- Dataview — 동적 쿼리, 데이터 집계
- Smart Connections — AI 기반 노트 연결 추천
- Excalidraw / Excalibrain — 시각적 사고
- Calendar / Chronology — 시간 축 정렬

### Citation Callout 추가 예시

#### 웹 아티클
> [!LINK] How to Take Smart Notes
> Zettelkasten 방법론 가이드^[Ahrens, S. (2022, March 15). _The Complete Guide to the Zettelkasten Method._ Retrieved from https://zettelkasten.de/posts/overview/]

#### INFO/EXAMPLE Callout
> [!INFO] _Deep Work_
> 몰입의 기술^[Newport, C. (2016). _Deep Work: Rules for Focused Success in a Distracted World._ Grand Central Publishing.]

> [!EXAMPLE] _Atomic Habits_
> "You do not rise to the level of your goals. You fall to the level of your systems."^[Clear, J. (2018). _Atomic Habits._ Avery. p.27.]

---

*이 가이드는 CMDS 볼트의 표준 Properties 체계를 정의합니다. 모든 새로운 노트는 이 규칙을 따라 작성되어야 합니다.*

*상위 캐노니컬 버전: 구요한(Yohan Koo)이 운영하는 메인 볼트 — [system.cmdspace.work](https://system.cmdspace.work) 참조.*
