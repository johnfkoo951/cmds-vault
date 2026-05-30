---
name: create-gobi-homepage
description: Generate or modify a Gobi Brain homepage (home.html) using one of 4 style templates (neon-terminal, minimal-editorial, magazine, brutalist) with an interview that customizes hero links, gobi.* features to include, accent color, and fonts. Use when asked to create a Brain homepage, redesign home.html, build a Gobi vault landing page, or apply a different style to an existing Brain page.
metadata:
  version: 1.0.0
  author: jyk
allowed-tools: [Read, Write, Edit, Bash, Glob, Grep]
---

# Create Gobi Homepage

Generate or rewrite the `home.html` rendered by Gobi Desktop for a Brain page. The skill ships four distinct style templates and an interactive interview so each homepage can match the user's intent without rebuilding from scratch every time.

## Templates

| Slug | Aesthetic | Background | Accent | Display font | Body font |
|------|-----------|-----------|--------|--------------|-----------|
| `neon-terminal` | Cyberpunk / terminal | `#000000` | `#ccff00` neon lime | Space Grotesk | Inter |
| `minimal-editorial` | Quiet, refined, blog-like | `#fafaf7` warm cream | `#c8553d` terracotta | Inter | Crimson Pro (serif) |
| `magazine` | Editorial / NYT-style | `#f5f1ea` paper | `#1a1a1a` + `#b8860b` gold rule | Playfair Display | Inter |
| `brutalist` | Raw, high-contrast | `#ffffff` | `#ff3300` red | Inter Black (uppercase) | Inter |
| `book` | Magazine variant tuned for a single book / living-book project | `#f5f1ea` paper | `#1a1a1a` + `#b8860b` gold rule | Playfair Display | Inter |

The first four implement the same gobi.* surface (hero, Brain Updates grid, Knowledge Graph, file viewer overlay, streaming chat, footer). `book` rearranges that surface for book-publishing context — see "Book template specifics" below. Style is the variable; functionality is constant across all five.

### Style preview

Full-page renders with 8 stub Brain Updates (1440×1024 viewport @2x, Playwright). Open the JPG to see the hero + KGraph, BU grid, chat section, and footer for each style.

| | |
|---|---|
| ![[examples/neon-terminal.jpg\|320]] | ![[examples/minimal-editorial.jpg\|320]] |
| **neon-terminal** | **minimal-editorial** |
| ![[examples/magazine.jpg\|320]] | ![[examples/brutalist.jpg\|320]] |
| **magazine** | **brutalist** |

Regenerate after editing any template: `python examples/_render_screenshots.py` (requires `pip install playwright && playwright install chromium`).

## Input

- Optional `--style=<slug>` — skip Q1 interview question.
- Optional `--features=<list>` — comma-separated set of `kgraph,chat,file_viewer,infoviz,pagination`. Default = all.
- Optional `--from-scratch` — generate without using a template (pure interview-driven).
- Optional `--output=<path>` — default `_Gobi_/app/home.html`.
- Existing `_Gobi_/app/home.html` — used as the live reference if modifying in place.

## Output

- A single self-contained HTML file at the output path. All CSS/JS inline. CDN dependencies allowed for fonts, marked, d3 only.
- Append a row to `_Settings_/Skills/skill_usage_logs.md`: `| YYYY-MM-DD | HH:MM | create-gobi-homepage | <style> + <features> |`.

## Interview

Run sequentially. Skip a question if the user has already answered it (CLI args, prior turn, or explicit "use defaults"). Batch Q1+Q2 then Q3+Q4+Q5 to keep momentum.

**Q1 — Style** (skip if `--style` provided):
> Which look should the homepage have?
> 1. **neon-terminal** — current style (dark, neon lime, terminal/cyberpunk)
> 2. **minimal-editorial** — light, serif-bodied, calm blog feel
> 3. **magazine** — editorial paper, drop caps, gold-rule
> 4. **brutalist** — white + red, thick black borders, raw type
> 5. **book** — magazine variant for a single-book / living-book site (full-width hero + pitch, single-column "Book Updates" feed, KGraph + Chat side-by-side below the feed). Recommend when the vault publishes one book project. Pre-tuned hero links: Outline + Prior Edition.
> 6. **custom-blend** — start from one of the above and override colors/fonts

**Q2 — Hero links** (always ask unless regenerating with `--reuse-links`):
> What buttons should sit in the hero next to the title? Provide a list of `{label, url}` pairs. Defaults if you skip: existing entries from current home.html (RESEARCH → github.io, LINKS → linktr.ee). Set to empty list to remove external links entirely.

**Q3 — gobi.* features to include** (multi-select, default = all):
> Which Brain page features should be present? Toggle any off to slim the page.
> - **Knowledge Graph** — D3 topic graph in hero RHS + full-screen overlay (heavyweight; remove if BU count is small)
> - **Chat** — streaming brain chat section + hero CHAT button
> - **File Viewer** — inline overlay for opening BU and vault files when a wiki/relative link is clicked
> - **INFOVIZ filter** — hero button filtering BUs to viz/HTML artifacts
> - **More Updates pagination** — "More Updates" button under the BU grid

Topic-badge filtering on cards is always on (it's part of the card markup; opt-out requires hand-editing).

**Q4 — Brand overrides** (optional, default to template values):
> Any tweaks to the chosen style? You can override:
> - Accent color (hex; replaces template's `--accent`)
> - Display font (Google Fonts family; replaces template's display font)
> - Profile fallback emoji (used if `vault.thumbnailPath` is empty; default `🧠`)
> - Page title prefix (replaces `vault.title` in `<title>`; useful for custom branding)

**Q5 — Output path** (skip if `--output` provided):
> Where should the file land? Default `_Gobi_/app/home.html`. Suggest `_Gobi_/app/home-<style>.html` if previewing alternates side-by-side.

After collecting answers, summarize in 4-6 bullets and proceed unless the user pushes back.

## Workflow

1. **ANALYZE REQUEST**
   - If modifying in place, read current `_Gobi_/app/home.html` to pull existing hero links / accent / title.
   - Run Interview (skip if all args provided).
   - Confirm summary if any answer materially changes the result (style switch, KGRAPH off, etc).

2. **LOAD TEMPLATE**
   - Read `templates/{style}.html` (or merge with current home.html for in-place mods).
   - For `custom-blend`, pick the closest base template and queue Q4 overrides.

3. **STRIP DISABLED FEATURES**
   - For each feature in `{kgraph, chat, file_viewer, infoviz, pagination}` that is OFF, remove every `<!-- FEATURE:NAME -->…<!-- /FEATURE:NAME -->` block (HTML markers are present in all 4 templates).
   - JS functions for removed features can stay — they're dormant if their DOM targets are gone. Don't touch the script block.
   - If KGRAPH is off, also change `.hero-grid` `grid-template-columns: 3fr 2fr` → `1fr` so the hero collapses to single column.

4. **APPLY HERO LINKS**
   - Replace contents of the `<!-- HERO_LINKS:START -->…<!-- HERO_LINKS:END -->` block with one `<a>` per `{label, url}` pair from Q2. Match the template's button class (e.g. `btn outline`).

5. **APPLY BRAND OVERRIDES**
   - Q4 accent → patch `--accent` and `--accent-dim` in `:root`.
   - Q4 display font → patch the Google Fonts `<link>` and the relevant `font-family` declarations (`h1`, `section h2`, `.update-card h3`).
   - Q4 emoji → patch `<div class="profile-pic" id="profilePic">🧠</div>` default.
   - Q4 title prefix → patch `<title>` and the `vault.title` fallback in `updateHeroSection()`.

6. **VERIFY**
   - `grep "listBrainUpdates\|brainUpdateId"` → must be zero hits (use new API names).
   - `grep "<!-- FEATURE:"` → must be zero hits for any feature the user toggled OFF.
   - Open the file in a browser if possible (or report "manual visual check needed").
   - Confirm responsive `@media (max-width: 768px)` rules survived edits.

7. **WRITE & LOG**
   - Write to output path.
   - Append usage log row.
   - Tell the user: file written, what changed, how to preview (drop into `_Gobi_/app/home.html` for Gobi Desktop to render).

## Latest gobi-cli API (post v1.3.x)

Use these names in any newly written or modified JS. Full reference: [[reference/gobi-api]].

| Method | Sync? | Returns | Notes |
|--------|-------|---------|-------|
| `gobi.vault` | sync | `{vaultId, title, description, thumbnailPath, tags, ownerName, ownerProfilePictureUrl, webdriveUrl, slug}` | New props: `tags`, `slug`, `ownerProfilePictureUrl`. |
| `gobi.listPersonalPosts({limit, cursor})` | async | `{data, pagination: {nextCursor, hasMore}}` | Was `listBrainUpdates` — that name still works as alias but is deprecated. |
| `gobi.getSessions({limit})` | async | `{data}` | Chat session list. |
| `gobi.loadMessages(sessionId, {limit})` | async | `{messages}` | |
| `gobi.sendMessage(sessionId, text, options?, onDelta)` | async stream | Promise | New `options.context: {postId?, postTitle?, filePath?}` — pass current viewed post so AI is context-aware. |
| `gobi.readFile(path)` | async | `Promise<string>` | Throws on not found. |
| `gobi.listFiles(folderPath)` | async | `[{name, type}]` | NEW. |
| `gobi.fileExists(path)` | async | `boolean` | NEW. |

**URL params changed**: GobiSpace post links use `?postId=<id>` (no longer `?brainUpdateId=`). Footer "POWERED BY GOBI" still uses `?og=1` to surface OG meta.

**CDN whitelist**:
- Fonts: `https://fonts.googleapis.com` / `https://fonts.gstatic.com`
- Markdown: `https://cdn.jsdelivr.net/npm/marked/marked.min.js`
- Graph: `https://cdn.jsdelivr.net/npm/d3@7/dist/d3.min.js`
- Editorial templates may also load: `https://fonts.googleapis.com/css2?family=Playfair+Display`, `family=Crimson+Pro`.

## Caveats

### Single-file rule
Every template stays a single HTML file with inline CSS and JS. Never split into external files. CDNs OK only for the whitelist above.

### Markdown rendering (shared across templates)
- Custom `marked.Renderer`:
  - GobiSpace file links (`gobispace.com/@slug?file=path`) → intercept, call `openFileViewer(path)` for inline popup.
  - Relative-path links (no `http`) → also route through `openFileViewer`.
  - All other external links → `target="_blank" rel="noopener"`.
- Images:
  - Relative-path image (`_files_/img.png`) → resolved via `getFileUrl(path)` to webdrive URL.
- BU full view uses `marked.parse(processed)` after `resolveWikiLinks` + `resolveWikiImages`.
- BU preview uses `marked.parse(escapeHtml(content.substring(0,300)))`.
- Chat assistant messages: `marked.parse(content)` (markdown allowed).
- Chat human messages: `escapeHtml(content)` only (plain text, XSS safe).
- Streaming: each delta appended to a buffer, then `loadingMsg.innerHTML = marked.parse(buffer)`.

### File / visualization viewer (`openFileViewer`)
- Normalize path: strip query params + decode `%20` / `+`.
- If extension is `.html`: render inside `<iframe>` with white background and zero padding (full-bleed effect).
- Otherwise: `gobi.readFile(path)` → strip YAML frontmatter → `marked.parse`.
- On init, paginate `listPersonalPosts` ~10 extra pages so older HTML artifacts are reachable via the file viewer.

### Knowledge Graph (D3)
- Top 30 topics from BU `topics[]` become labeled nodes; BUs that touch any of those topics become small grey dots.
- Mini view (hero RHS): `distance: 60`, `charge: -80`.
- Full view (overlay): `distance: 180`, `charge: -600`.
- Topic click → `showTopicBUs(topicName)` → list overlay. BU click → `openBUInline(id)` → reader overlay with `?postId=...` permalink button.
- Topic↔topic links hidden; only BU↔topic edges drawn (reduces noise).

### Filter system
- `setTopicFilter(name)` and `setInfoVizFilter()` are additive; combine freely. `clearFilters()` resets both.
- INFOVIZ test: post content includes `.html` OR a topic name matches `/viz/i` or `/인포/`.

### BU card interactions
- Click toggles preview ↔ full (`toggleUpdateDetail`); link clicks bail via `event.target.closest('a')` guard.
- Display max 3 topic badges per card (`topics.slice(0, 3)`).
- Full body uses a slightly brighter text (`#c0c0c0` in dark templates, `#3a3a3a` in light templates) for hierarchy.

### Layout (logical sections, in order)
```
Hero (hero-grid)
├── LHS: profile-pic + h1 + hero-actions ({HERO_LINKS} + [INFOVIZ?] + [CHAT?])
└── RHS: [KGRAPH mini?]
Overlays (z-index 1000): [KGRAPH full?], [FILE_VIEWER?]
Brain Updates (updates-grid 2-col, 1-col on mobile)
[Pagination? "More Updates"]
[Chat section?]
Footer (POWERED BY GOBI → gobispace.com/@slug?og=1)
```

### Mobile
- `@media (max-width: 768px)`: hero collapses to 1 column, hero-actions full-width-stacked, updates-grid → 1 column, chat container 400px tall.

### XSS / security
- `escapeHtml(text)` on every user-supplied or BU-derived value rendered as text (titles, topic names, chat human messages).
- Never inject raw `update.content` without going through `marked.parse(resolveWikiLinks(resolveWikiImages(content)))`.

## Custom blend (Q1 option 6)

If the user picks `custom-blend`:
- Ask which base template to start from (Q1 again, options 1-5).
- Skip Q3 default (let user re-pick features knowing this is a custom).
- Drive Q4 aggressively (accent + display font + body font + border thickness + hover style).
- Save the resulting file with a `-custom` suffix so it's clearly not one of the canon templates.

## Book template specifics (Q1 option 5)

The `book` template is a magazine-derivative tuned for vaults whose primary output is a single book. Layout and naming changes vs. `magazine`:

**Layout differences**:
- **Hero is full-width** — no 2-column hero-grid. Profile + title + actions are a single row, hero description follows as a full-width block below with a gold border-top separator.
- **Hero description is the book pitch**, not a vault description. Hard-coded as inline HTML in `updateHeroSection()` so it can carry `<em>`/`<strong>` formatting. Look for the `BOOK_DESC:` comment marker in the JS — that's the block to edit.
- **"Book Updates" replaces "Brain Updates"** in: section heading, CSS comments, chat prompt buttons, KGraph tooltip text, topic-filter overlay text.
- **Book Updates feed is single-column full-width** (not 2-col grid). `.updates-grid` uses `grid-template-columns: 1fr`. Update cards stretch horizontally with top-border separators.
- **Knowledge Graph + Chat are side-by-side below the feed**, not in hero RHS. The `kchat-grid` 2-col container places both at equal height (520px desktop, stacked on mobile). Click KGraph mini → existing full-screen overlay still works.
- **INFOVIZ button removed by default** — book grids don't filter to viz/HTML artifacts. JS function stays dormant.

**Interview adjustments**:
- Q2 default hero links: `Outline` (linking to the book outline post on GobiSpace) + `Prior Edition` (linking to a bookstore page or previous edition URL). Replace `OUTLINE_POST_ID` and `your-slug` in the template with real values.
- Q3 default features: KGraph ON, Chat ON, File Viewer ON, INFOVIZ OFF (already stripped), Pagination ON.
- Q4 description override: instead of patching `vault.description`, hand-edit the `vaultDesc.innerHTML` block in `updateHeroSection()` (search for the `BOOK_DESC:` comment marker). Use `<em>` for italics, `<strong>` for non-italic bold emphasis.

**When to pick `book` over `magazine`**:
- Vault's primary published artifact is one book (or one living-book project).
- You want the book pitch on the hero, not a generic vault description.
- Book Updates feed will be a chronological narrative of chapter drafts / daily progress, not a topic-diverse stream where 2-col makes sense.
- KGraph is still useful (topic clustering across chapter posts), but not at hero-RHS prominence.

**When `magazine` is better**:
- Vault publishes multiple ongoing projects, not one book.
- Hero RHS KGraph is a visual identity element you want preserved.
- Update grid benefits from 2-col density (many short posts).

## Related skills / docs

- `_Claw_/skills/gobi-cli/skills/gobi-homepage/SKILL.md` — gobi-cli's own homepage skill; canonical source of the API. Read it if you suspect this skill's API table has drifted.
- `_Settings_/Skills/road-trip-planning/SKILL.md` — pattern for HTML-template + interview skills (reference for the interview cadence).
- `_Settings_/Prompts/Create Brain Homepage (CBH).md` — legacy single-shot prompt; now a pointer to this skill.

## When NOT to use

- For BU drafting / publishing → use the gobi-cli `global create-post` workflow (see [[feedback_gobi_cli_publish_command]]).
- For the GobiSpace community web UI → not configurable from this skill; that's an upstream Gobi product surface.
- For generating BU summary GIFs → use `create-gif-slides` skill.
