---
name: canvas-to-jpg
description: Export Obsidian Canvas (.canvas) files to JPG images using Playwright. Use when user asks to export, screenshot, or convert a canvas to an image.
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
license: MIT
---

# Canvas to JPG Skill

Export Obsidian Canvas files to high-resolution JPG images via Playwright headless browser.

## When to Use

- User asks to export a canvas to JPG/image
- User wants to share a canvas as a static image
- User asks to screenshot or render a canvas

## Prerequisites

- Python 3 with `playwright` package installed
- Chromium browser installed for Playwright

## How to Export

### Step 1: Read the canvas file

Read the `.canvas` file (JSON format) to get nodes and edges.

**CRITICAL**: Obsidian may strip nodes when a canvas is open. If the canvas is currently open in Obsidian, ask the user to close it first, or use the canvas data from memory/inline rather than reading the file.

### Step 2: Run the renderer script

Use the Python renderer below. Pass the canvas file path as argument.

```bash
python3 "90. Settings/91. Skills/canvas-to-jpg/render_canvas.py" "<input_canvas_path>" "<output_jpg_path>" [--light]
```

- If `<output_jpg_path>` is omitted, the JPG is saved alongside the canvas file with the same name.
- Default theme is **dark** (matches Obsidian dark mode). Pass `--light` for a white background with pastel boxes — good for sharing or printing.
- Device scale factor is 2x (Retina quality).

### Step 3: Open the result

```bash
open "<output_jpg_path>"
```

## Color Scheme

### Dark theme (default — matches Obsidian dark mode)

| Color ID | Name | Hex |
|----------|------|-----|
| 1 | Red | #fb464c |
| 2 | Orange | #e9973f |
| 3 | Yellow | #e0de71 |
| 4 | Green | #44cf6e |
| 5 | Purple | #a882ff |
| 6 | Cyan | #53dfdd |

### Light theme (`--light` — pastel boxes, dark text on white)

| Color ID | Name | Box Hex |
|----------|------|---------|
| 1 | Red pastel | #fde8e9 |
| 2 | Orange pastel | #fde9d2 |
| 3 | Yellow pastel | #fdf6c2 |
| 4 | Green pastel | #dff0e3 |
| 5 | Purple pastel | #e9e0ff |
| 6 | Cyan pastel | #d8f1f0 |

## Supported Markdown in Nodes

- `# H1`, `## H2` headings
- `**bold**` text
- `- bullet` lists
- `> blockquote`
- `` `code` `` inline
- `[[wiki|alias]]` links (rendered as styled text)
- Markdown tables with `|` delimiters

## Limitations

- File nodes (`type: "file"`) render as text with the file path
- Group nodes render as colored boxes (no containment visual)
- Edge labels are positioned at midpoint of the curve
- Complex nested markdown (code blocks, nested lists) not supported

## Troubleshooting

- **Missing nodes in output**: Obsidian may have reformatted the canvas. Close the canvas in Obsidian and rewrite the file.
- **Font rendering**: Uses Apple SD Gothic Neo / Noto Sans KR for Korean text support.
- **Playwright not found**: Run `pip install playwright && playwright install chromium`
