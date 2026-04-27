---
title: "Create Brain Homepage (CBH)"
abbreviation: CBH
category: creation
created: "2026-04-10"
---
Gobi Brain 페이지용 커스텀 홈페이지(home.html)를 생성하거나 수정한다. 레퍼런스 구현체(`app/home.html`)를 기반으로 사용자 요구에 맞게 조정.

## Input
- **Optional**: 커스터마이징 요청 (레이아웃 변경, 색상, 섹션 추가/제거 등)
- **Optional**: 외부 링크 목록 (RESEARCH, LINKS 등 hero 버튼)
- **Optional**: `--from-scratch` (레퍼런스 없이 새로 생성)
- **Reference**: `app/home.html` (현재 구현체)

## Output
- `app/home.html` — 단일 HTML 파일 (모든 CSS/JS 인라인)
- Gobi Desktop에서 Brain 페이지로 렌더링됨

## Main Process
```
1. ANALYZE REQUEST
   - 기존 app/home.html 읽기
   - 사용자 요청 분석 (레이아웃, 기능, 스타일 변경)
   - 변경 범위 결정

2. IMPLEMENT CHANGES
   - 디자인 시스템 유지하며 수정 (아래 Caveats 참조)
   - 섹션 순서: Hero → Brain Updates → Chat → Footer
   - 모바일 반응형 확인

3. VERIFY
   - HTML 문법 확인
   - API 호출 패턴 확인 (gobi.* 메서드)
   - 반응형 breakpoint (768px) 확인
```

## Caveats

### Gobi Brain Page API (window.gobi)
Brain 페이지에서 사용 가능한 API (HTML App API와 다름):

| Method | Return | 용도 |
|--------|--------|------|
| `gobi.vault` | Object (sync) | vault 메타데이터 (title, description, thumbnailPath, vaultId, webdriveUrl) |
| `gobi.listBrainUpdates({limit, cursor})` | `{data, pagination}` | Brain Update 목록 |
| `gobi.getSessions({limit})` | `{data}` | 채팅 세션 목록 |
| `gobi.loadMessages(sessionId, {limit})` | `{messages}` | 세션 메시지 로드 |
| `gobi.sendMessage(sessionId, text, deltaCallback)` | Promise | 스트리밍 채팅 전송 |

- `gobi.vault.thumbnailPath` → CDN URL: `https://d16t3dioqz0xo9.cloudfront.net/${path}@128x128.webp`
- BU 데이터에 `topics` 배열 포함: `[{name: "Topic Name"}, ...]`
- 페이지네이션: `result.pagination?.nextCursor`를 다음 호출의 cursor로 전달

### 디자인 시스템
```css
:root {
    --bg: #000000;
    --fg: #ffffff;
    --accent: #ccff00;        /* 주 강조색 */
    --accent-dim: #99cc00;
    --grey-900: #111111;      /* 카드 배경 */
    --grey-800: #1a1a1a;      /* 보더 */
    --grey-700: #2a2a2a;      /* 보더 (밝은) */
    --grey-600: #404040;
    --grey-500: #606060;      /* 보조 텍스트 */
    --border: 2px;
    --transition: 0.15s ease;
}
```
- **폰트**: Space Grotesk (제목), IBM Plex Mono (메타/코드), Inter (본문)
- **카드 호버**: `translate(-4px, -4px)` + box-shadow 효과
- **버튼**: `.btn` (filled) / `.btn.outline` (outlined), uppercase, monospace
- **Hero 배경**: CSS grid 패턴 (linear-gradient)
- **노이즈 오버레이**: `body::before`로 SVG 노이즈 텍스처

### 마크다운 렌더링
- **CDN**: `https://cdn.jsdelivr.net/npm/marked/marked.min.js`
- **링크 설정**: marked renderer를 커스텀하여 모든 `<a>`에 `target="_blank" rel="noopener"` 추가
- **BU 전체 보기**: `marked.parse(resolveWikiImages(content))` 사용
- **BU 프리뷰**: `escapeHtml(content.substring(0, 200))` (plain text)
- **채팅 assistant 메시지**: `marked.parse(content)` (마크다운)
- **채팅 human 메시지**: `escapeHtml(content)` (plain text)
- **스트리밍**: `loadingMsg.innerHTML = marked.parse(response)` (delta 누적)

### Wiki 이미지 해석
```javascript
function resolveWikiImages(markdown) {
    return markdown.replace(/!\[\[([^\]|]+)(?:\|(\d+))?\]\]/g, (_, path, width) => {
        const url = getFileUrl(path.trim());
        return width
            ? `<img src="${url}" alt="${path.trim()}" width="${width}" style="max-width:100%">`
            : `<img src="${url}" alt="${path.trim()}" style="max-width:100%">`;
    });
}

function getFileUrl(path) {
    const { vaultId, webdriveUrl } = vault;
    const encoded = path.split('/').map(encodeURIComponent).join('/');
    return `${webdriveUrl}/api/v1/file/raw/${vaultId}/${encoded}`;
}
```

### Knowledge Graph (K-Graph)
- **CDN**: `https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js`
- **데이터**: BU의 topics 배열에서 추출. 토픽 = 노드, 같은 BU에 공존 = 엣지
- **Top N 필터**: 빈도 상위 20개 토픽만 유지
- **고아 노드 제거**: 엣지가 없는 노드는 숨김
- **풍부한 데이터**: 초기 8개 BU 외 추가 3회 페이지네이션 (최대 32개 BU)
- **노드 크기**: `d3.scaleSqrt()` — 빈도에 비례
- **노드 색상**: accent 색상, opacity = 0.3 + (count/maxCount) * 0.7
- **드래그**: `d3.drag()` 적용
- **경계**: tick에서 `Math.max(20, Math.min(width-20, x))` 클램핑

### K-Graph 아키텍처
- **데이터/렌더링 분리**: `buildGraphData(updates)` → 데이터 구조 반환, `drawGraph(containerId, w, h, data, opts)` → 렌더링
- **그래프 데이터 캐싱**: `kgraphData` 전역 변수에 저장하여 full-scale 뷰에서 재사용
- **drawGraph opts**: `{ nodeRange, fontSize, distance, charge }` — 미니/풀 뷰 파라미터 분리
  - 미니 (hero): `nodeRange=[4,16]`, `fontSize='9px'`, `distance=60`, `charge=-80`
  - 풀스케일: `nodeRange=[8,32]`, `fontSize='12px'`, `distance=120`, `charge=-200`

### K-Graph 풀스케일 오버레이
- **클릭 → 오버레이**: hero의 kgraph-container 클릭 시 전체 화면 오버레이 표시
- **오버레이 구조**: `position: fixed`, `100vw x 100vh`, 반투명 검정 배경 (`rgba(0,0,0,0.95)`)
- **닫기**: ESC 키 또는 CLOSE 버튼
- **body overflow hidden**: 오버레이 열릴 때 스크롤 방지, 닫힐 때 복원
- **독립 시뮬레이션**: 풀스케일은 새 노드/링크 복사본으로 별도 시뮬레이션 실행

### BU 카드 인터랙션
- **클릭 토글**: preview ↔ full 전환 (`toggleUpdateDetail`)
- **링크 클릭 가드**: `if (event.target.closest('a')) return;` — 링크 클릭 시 토글 방지
- **확장 텍스트 색상**: `#c0c0c0` (preview의 grey-500보다 밝게)
- **em 텍스트**: `#a0a0a0`

### 채팅 예시 프롬프트
- 세션 로드 후 빈 채팅에 clickable suggestion chips 표시
- 클릭 시 input 필드에 텍스트 채움 (`fillPrompt`) + chips 숨김
- 스타일: `.chat-prompt-btn` — 투명 배경, grey-700 보더, hover 시 accent 색상
- `showChatUI()`에서 prompts DOM 동적 생성

### 레이아웃 구조
```
Hero Section (hero-grid: 3fr 2fr)
├── LHS: profile-pic + title + action buttons + description
└── RHS: Knowledge Graph (D3 force-directed, 클릭 → 풀스케일 오버레이)

K-Graph Full Overlay (fixed, 100vw x 100vh)
├── Title (top-left)
├── Close button (top-right, ESC 키 지원)
└── Full-scale graph (bigger nodes/labels, more spacing)

Brain Updates (updates-grid: 1fr 1fr)
├── Card 1 (toggle preview/full)
├── Card 2
└── ... (paginated, 8 per load)

Chat Section
├── Header
├── Messages (scrollable) + Example Prompt Chips
└── Input area (hidden until session exists)

Footer
└── "POWERED BY GOBI" link → gobispace.com/@slug?og=1
```

### 모바일 반응형 (max-width: 768px)
- `hero-grid` → 1 column
- `updates-grid` → 1 column
- hero-content → column direction
- 버튼 full-width
- chat container height 400px (desktop 500px)

### 주의사항
- **단일 파일**: 모든 CSS/JS를 HTML 내 인라인으로 유지 (외부 파일 분리 금지)
- **CDN만 허용**: Google Fonts, marked.js, d3.js는 CDN 로드
- **gobi.vault은 동기**: await 불필요, 즉시 접근 가능
- **escapeHtml 필수**: 사용자 입력/BU 제목 등 XSS 방지
- **Footer 링크**: `https://www.gobispace.com/@{slug}?og=1` 형식 (og=1로 오픈그래프 메타 포함)
