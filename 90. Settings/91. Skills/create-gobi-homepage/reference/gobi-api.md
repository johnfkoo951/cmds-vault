---
title: Gobi Brain Page API reference (window.gobi)
created: 2026-05-13
updated: 2026-05-13
---

# `window.gobi` — Brain page API

This reference documents the `window.gobi.*` surface available **inside** the Brain homepage iframe rendered by Gobi Desktop. It is distinct from the gobi-cli command-line tool and the public Gobi Web SDK.

The canonical upstream source is `_Claw_/skills/gobi-cli/skills/gobi-homepage/SKILL.md` (shipped by gobi-cli). When in doubt, cross-check there.

## Vault metadata (sync)

```js
const v = gobi.vault;  // available immediately, no await
```

| Property | Type | Notes |
|----------|------|-------|
| `vaultId` | string | Internal vault UUID. |
| `title` | string | Display name. Use as `<title>` and h1 fallback. |
| `description` | string | One-liner shown in hero. |
| `thumbnailPath` | string \| null | Vault avatar; render via CDN `https://d16t3dioqz0xo9.cloudfront.net/${thumbnailPath}@128x128.webp`. |
| `tags` | string[] | Vault-level tags (added v1.3). |
| `ownerName` | string | Display name of vault owner. |
| `ownerProfilePictureUrl` | string \| null | Owner avatar URL (added v1.3). |
| `webdriveUrl` | string | Base for `getFileUrl()` — reads files via `${webdriveUrl}/api/v1/file/raw/${vaultId}/${encodedPath}`. |
| `slug` | string | URL slug; use in `gobispace.com/@${slug}?og=1` (footer) and `?postId=` deep links. |

## Posts (formerly "Brain Updates")

```js
const { data, pagination } = await gobi.listPersonalPosts({ limit: 8, cursor: null });
// data: [{ id, title, content, topics: [{name, slug, id}], createdAt }, ...]
// pagination: { nextCursor: string|null, hasMore: boolean }
```

| Property | Notes |
|----------|-------|
| `id` | Post ID (number). Use in `?postId=${id}` deep link. |
| `title` | Display title (escape with `escapeHtml`). |
| `content` | Markdown body. Pass through `resolveWikiLinks` + `resolveWikiImages` before `marked.parse`. |
| `topics` | Array of `{name, slug, id}`. Limit to top 3 on card preview (`topics.slice(0, 3)`). |
| `createdAt` | ISO 8601 string. |

**Deprecated alias**: `gobi.listBrainUpdates(...)` still works for now but emits a console warning. All new code should call `listPersonalPosts`.

**URL parameter change**: GobiSpace deep links use `?postId=<id>` (no longer `?brainUpdateId=`).

## Chat sessions

```js
const sessions = await gobi.getSessions({ limit: 1 });
// sessions.data: [{ sessionId, messageCount, lastMessageAt }, ...]

const history = await gobi.loadMessages(sessionId, { limit: 10 });
// history.messages: [{ id, role: 'human' | 'assistant', content, createdAt }]
```

## Streaming chat

```js
let buf = '';
await gobi.sendMessage(
    sessionId,
    userText,
    { context: { postId: 1234, postTitle: '...', filePath: '_Outbox_/...' } },  // optional (v1.3)
    (delta) => {
        buf += delta;
        loadingMsg.innerHTML = marked.parse(buf);
        scrollChatBottom();
    }
);
```

The `options.context` object lets the AI see what the user is looking at right now — useful when the chat is launched from a BU or file viewer. Omit `options` entirely for plain chat.

## Vault filesystem

```js
const text = await gobi.readFile('_Outbox_/path/to/file.md');  // throws if missing
const items = await gobi.listFiles('_Outbox_/folder');          // [{name, type: 'file'|'folder'}]
const exists = await gobi.fileExists('_Outbox_/path/file.md');  // boolean (v1.3)
```

Path semantics: relative to the vault root. Do NOT include a leading slash. Encode each segment via `encodeURIComponent` when building a raw webdrive URL.

## Helpers used by all 4 templates

These are not part of `window.gobi` — they're conventions the templates share. Keep their signatures identical across templates so users can swap stylesheets without breaking JS.

```js
function getFileUrl(path) {
    const { vaultId, webdriveUrl } = vault;
    const cleanPath = decodeURIComponent(path.replace(/\+/g, ' '));
    const encoded = cleanPath.split('/').map(encodeURIComponent).join('/');
    return `${webdriveUrl}/api/v1/file/raw/${vaultId}/${encoded}`;
}

function resolveWikiImages(md) { /* ![[path|width]] -> <img> */ }
function resolveWikiLinks(md)  { /* [[path|label]] -> openFileViewer link */ }
function escapeHtml(text)      { /* &<>"' */ }
function formatDate(iso)       { /* ko-KR locale */ }
```

## URL endpoints used (for grep checklist)

| URL pattern | Where | Modernization |
|-------------|-------|---------------|
| `gobispace.com/@${slug}?og=1` | Footer | unchanged |
| `gobispace.com/@${slug}?postId=${id}` | BU permalinks | was `?brainUpdateId=` |
| `https://d16t3dioqz0xo9.cloudfront.net/${path}@128x128.webp` | Profile picture | unchanged |
| `${webdriveUrl}/api/v1/file/raw/${vaultId}/${encodedPath}` | File reads | unchanged |

## What's NOT available

Things the Brain homepage cannot do (must be done via gobi-cli or Gobi Desktop UI):

- Create / edit / delete posts
- Sync vault files
- Authenticate or switch accounts
- Cross-vault navigation
- Push to GobiSpace community

The Brain page is read-and-chat only.
