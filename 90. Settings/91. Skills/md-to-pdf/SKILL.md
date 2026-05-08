---
name: md-to-pdf
description: Convert Obsidian markdown documents (with Mermaid diagrams, tables, wiki links) to professional A4 PDF using Playwright. Use when user requests PDF export of markdown files.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
license: MIT
---

# Markdown to PDF Skill

Convert Obsidian markdown files to styled A4 PDF documents with full support for Mermaid diagrams, tables, wiki links, embedded images (`![[image.png]]`), and Korean text.

## When to Use This Skill

Activate when the user:
- Asks to convert a markdown file to PDF
- Wants to export a document as PDF
- Needs a printable version of a markdown document
- Requests PDF generation with Mermaid diagram support

## Dependencies

- **Python packages**: `markdown`, `playwright`
- **Playwright browser**: Chromium (install via `playwright install chromium`)
- Install check: `python3 -c "import markdown; from playwright.sync_api import sync_playwright"`
- If missing: `pip3 install markdown playwright && python3 -m playwright install chromium`

## Pipeline

1. **Strip YAML frontmatter** — remove `---` blocks
2. **Convert checkboxes** — `- [ ]` → ☐, `- [x]` → ☑
3. **Fix list breaks** — ensure blank line before bullet lists that follow inline text (see List Break Fix section)
4. **Extract & embed images** — convert `![[image.png]]` to base64 `<img>` tags (placeholder swap)
5. **Convert wiki links** — `[[link|display]]` → display text, `[[link]]` → link text
6. **Convert markdown to HTML** — using `markdown` library with `tables`, `fenced_code`, `attr_list` extensions
7. **Restore image placeholders** — swap placeholders back to `<img>` tags
8. **Wrap Mermaid blocks** — detect ```` ```mermaid ```` code blocks and convert to `<div class="mermaid">` with type-specific CSS classes
9. **Render with Playwright** — load HTML in headless Chromium, wait for Mermaid JS to render SVGs, export PDF

## Script Generation

Generate a self-contained Python script at `/tmp/md_to_pdf.py` with the following parameters extracted from user request:

```python
INPUT = "<source markdown file path>"
OUTPUT = "_Outbox_/PDF/<filename>.pdf"  # always output to _Outbox_/PDF/
TITLE = "<document title>"    # extracted from H1 or filename
AUTHOR = "<author name>"      # from frontmatter or user request
DATE = "<YYYY-MM-DD>"         # from frontmatter or today
```

## HTML Template Structure

```
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8">
  <style>/* see CSS Rules below */</style>
  <script src="mermaid CDN"></script>
</head>
<body>
  <div class="doc-meta">AUTHOR | DATE</div>
  <h1>TITLE</h1>
  {converted HTML body}
  <script>mermaid.initialize({...})</script>
</body>
</html>
```

## CSS Rules

### Page Layout
```css
@page { size: A4; margin: 20mm 18mm 25mm 18mm; }
body { font-family: 'Apple SD Gothic Neo', 'Noto Sans KR', sans-serif; font-size: 11pt; line-height: 1.6; }
```

### Typography
- H1: 22pt, border-bottom 2px solid
- H2: 16pt, color #2c3e50, border-bottom 1px solid #ddd
- H3: 13pt, color #34495e
- Tables: 10pt font, collapsed borders, striped rows
- Blockquotes: left blue border, italic, light background
- Code: 9.5pt, light gray background

### Mermaid Diagrams — Critical Lessons

**Container sizing by diagram type:**
- **Default** (`.mermaid`): `max-width: 100%` — timeline, gantt, sequence, `graph LR` diagrams use full page width
- **Vertical flowcharts** (`.mermaid-flowchart`): `max-width: 420px` — only `flowchart TB`, `flowchart TD`, `graph TB`, `graph TD` get constrained to prevent oversized rendering
- All diagrams: `text-align: center; margin: 16px auto; overflow: visible`
- SVGs inside: `max-width: 100% !important; height: auto !important`

**Type detection logic** (in `wrap_mermaid_blocks`):
```python
stripped = code.strip().lower()
if stripped.startswith(('flowchart tb', 'flowchart td', 'graph tb', 'graph td')):
    cls = 'mermaid mermaid-flowchart'  # constrained width
else:
    cls = 'mermaid'  # full width
```

**Mermaid initialization:**
```javascript
mermaid.initialize({
    startOnLoad: true,
    theme: 'default',
    flowchart: { useMaxWidth: true, htmlLabels: true },
    sequence: { useMaxWidth: true },
    themeVariables: { fontSize: '13px' }
});
```

**Key lessons:**
- Do NOT set `fontSize` per diagram type config (e.g., `flowchart.fontSize`) — it makes non-flowchart diagrams too small
- Use `themeVariables.fontSize` as the single global font size control
- Constrain oversized diagrams via CSS `max-width` on the container, not font size reduction
- `graph LR` is a horizontal layout and should NOT be constrained — only TB/TD directions overflow

### Footer (Page Numbers)

Use Playwright's `display_header_footer` — do NOT also use CSS `@page @bottom-center` (causes duplication).

```python
await page.pdf(
    ...,
    display_header_footer=True,
    header_template='<span></span>',
    footer_template='<div style="width:100%;text-align:center;font-size:8pt;color:#888;font-family:Apple SD Gothic Neo,sans-serif;">TITLE &nbsp;|&nbsp; p. <span class="pageNumber"></span></div>'
)
```

### Author/Date Header

Place above H1 as right-aligned metadata:
```html
<div class="doc-meta">AUTHOR &nbsp;|&nbsp; DATE</div>
```
```css
.doc-meta { text-align: right; color: #666; font-size: 10pt; margin-bottom: 4px; }
```

## List Break Fix — Critical for Bullet Rendering

**Problem**: Python's `markdown` library requires a blank line between a paragraph and a bullet list. Without it, list items render as inline text inside a `<p>` tag instead of proper `<ul><li>` elements.

**Example of broken markdown:**
```markdown
**논의 포인트**:
- 항목 1
- 항목 2
```
This renders as `<p><strong>논의 포인트</strong>:\n- 항목 1\n- 항목 2</p>` — all one paragraph, no bullets.

**Fix**: Two transformations needed:
1. Insert a blank line before top-level `- ` that follows non-list text
2. Convert 2-space indent to 4-space (Python markdown requires 4-space for nested lists)

```python
def fix_list_breaks(md_text):
    lines = md_text.split('\n')
    result = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        is_top_level_bullet = stripped.startswith('- ') and not line.startswith(' ')
        # Insert blank line before top-level bullets following paragraph text
        if (is_top_level_bullet and
            i > 0 and
            not lines[i-1].strip().startswith('- ') and
            not lines[i-1].strip().startswith('  - ') and
            lines[i-1].strip() != ''):
            result.append('')
        # Convert 2-space indent to 4-space for proper nesting
        if line.startswith('  - ') and not line.startswith('    - '):
            line = '    ' + line.lstrip(' ')
        result.append(line)
    return '\n'.join(result)
```

**Key lesson**: Obsidian uses 2-space indentation for sub-lists, but Python `markdown` library requires 4-space. Always normalize indentation before conversion.

**Processing order** — must run BEFORE markdown conversion:
```python
md_text = strip_frontmatter(md_text)
md_text = convert_checkboxes(md_text)
md_text = fix_list_breaks(md_text)                    # NEW: ensure proper list parsing
md_text = extract_images_to_placeholders(md_text)
md_text = convert_wiki_links(md_text)
html = markdown.markdown(md_text, ...)
html = restore_placeholders(html)
```

## Image Embedding — Critical Ordering

**CRITICAL**: Image extraction (`![[...]]`) MUST happen BEFORE wiki link conversion (`[[...]]`).

`convert_wiki_links` uses `r'\[\[([^\]]+)\]\]'` which also matches the inner `[[...]]` of `![[image.png]]`, stripping the image embed. Always extract images first, replace with text placeholders, then convert wiki links.

**Processing order:**
```python
md_text = strip_frontmatter(md_text)
md_text = convert_checkboxes(md_text)
md_text = extract_images_to_placeholders(md_text)  # ![[img]] → PLACEHOLDER
md_text = convert_wiki_links(md_text)               # [[link]] → text
html = markdown.markdown(md_text, ...)
html = restore_placeholders(html)                    # PLACEHOLDER → <img base64>
```

**Image search paths** (tried in order):
1. `_files_/` subdirectory relative to the markdown file's parent
2. Same directory as the markdown file
3. Explicit `IMG_DIR` if set

**CSS for embedded images:**
```css
.embedded-img {
    display: block;
    max-width: 100%;
    height: auto;
    margin: 16px auto;
    border-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
```

## Wiki Link Conversion

Obsidian wiki links are not valid HTML. Convert before markdown processing:
- `[[Page|Display Text]]` → `Display Text`
- `[[Page Name]]` → `Page Name`

## Execution

```bash
python3 /tmp/md_to_pdf.py
```

The script:
1. Saves intermediate HTML to `/tmp/<name>.html` for debugging
2. Prints count of rendered Mermaid diagrams
3. Saves PDF to output path
4. Open PDF after generation: `open "<output path>"`

## Output

- **PDF file**: `_Outbox_/PDF/<filename>.pdf` (ensure directory exists with `mkdir -p`)
- **Debug HTML**: `/tmp/<name>.html`
- Always open the PDF in default viewer after generation
