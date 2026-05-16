#!/usr/bin/env python3
"""
Obsidian Canvas to JPG renderer.
Usage: python3 render_canvas.py <input.canvas> [output.jpg] [--light]
"""

import argparse, json, re, math, os
import html as html_mod
from playwright.sync_api import sync_playwright

# --- Config ---
SCALE_FACTOR = 2
JPEG_QUALITY = 92
PADDING = 40

THEMES = {
    "dark": {
        "bg": "#1a1a2e",
        "default": {"bg": "#262626", "border": "#404040", "text": "#ddd"},
        "colors": {
            "1": {"bg": "#fb464c", "border": "#e03e43", "text": "#fff"},
            "2": {"bg": "#e9973f", "border": "#d08636", "text": "#fff"},
            "3": {"bg": "#e0de71", "border": "#c8c664", "text": "#1a1a1a"},
            "4": {"bg": "#44cf6e", "border": "#3cb862", "text": "#fff"},
            "5": {"bg": "#a882ff", "border": "#9674e0", "text": "#fff"},
            "6": {"bg": "#53dfdd", "border": "#4ac8c6", "text": "#1a1a1a"},
        },
        "edge_colors": {
            "1": "#fb464c", "2": "#e9973f", "3": "#e0de71",
            "4": "#44cf6e", "5": "#a882ff", "6": "#53dfdd",
        },
        "edge_default": "#666",
        "edge_opacity": 0.7,
        "code_bg": "rgba(0,0,0,0.25)",
        "link_color": "#7db8f5",
        "quote_border": "rgba(255,255,255,0.3)",
        "table_border": "rgba(255,255,255,0.3)",
        "table_header_bg": "rgba(0,0,0,0.2)",
        "border_width": "2px",
        "box_shadow": "0 2px 8px rgba(0,0,0,0.3)",
    },
    "light": {
        "bg": "#fafafa",
        "default": {"bg": "#f4f4f6", "border": "#d8d8de", "text": "#1f2937"},
        "colors": {
            "1": {"bg": "#fde8e9", "border": "#f4b9bc", "text": "#1f2937"},
            "2": {"bg": "#fde9d2", "border": "#f3c994", "text": "#1f2937"},
            "3": {"bg": "#fdf6c2", "border": "#e8de7b", "text": "#1f2937"},
            "4": {"bg": "#dff0e3", "border": "#a3d5b1", "text": "#1f2937"},
            "5": {"bg": "#e9e0ff", "border": "#bfa9f2", "text": "#1f2937"},
            "6": {"bg": "#d8f1f0", "border": "#8fd5d3", "text": "#1f2937"},
        },
        "edge_colors": {
            "1": "#d14a50", "2": "#c97a26", "3": "#b3a82a",
            "4": "#2f9c54", "5": "#7a5cd4", "6": "#3aa8a6",
        },
        "edge_default": "#8a8a92",
        "edge_opacity": 0.8,
        "code_bg": "rgba(0,0,0,0.06)",
        "link_color": "#2563eb",
        "quote_border": "rgba(0,0,0,0.2)",
        "table_border": "rgba(0,0,0,0.15)",
        "table_header_bg": "rgba(0,0,0,0.04)",
        "border_width": "1.5px",
        "box_shadow": "0 1px 4px rgba(0,0,0,0.06)",
    },
}

FONT_STACK = "'Apple SD Gothic Neo','Noto Sans KR',system-ui,sans-serif"


# --- Inline markdown formatting ---
def inline_fmt(text, theme):
    t = html_mod.escape(text)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(
        r'`(.+?)`',
        rf'<code style="background:{theme["code_bg"]};padding:1px 4px;border-radius:3px;font-size:12px">\1</code>',
        t,
    )
    link_color = theme["link_color"]
    t = re.sub(
        r'\[\[(.+?)\|(.+?)\]\]',
        rf'<span style="color:{link_color};text-decoration:underline">\2</span>',
        t,
    )
    t = re.sub(
        r'\[\[(.+?)\]\]',
        rf'<span style="color:{link_color};text-decoration:underline">\1</span>',
        t,
    )
    return t


# --- Markdown to HTML ---
def md_to_html(text, theme):
    lines = text.split("\n")
    result = []
    in_table = False
    header_done = False

    for line in lines:
        s = line.strip()

        # Table separator row
        if re.match(r'^\|[\s\-:|]+\|$', s):
            continue

        # Table row
        if '|' in s and s.startswith('|') and s.endswith('|'):
            cells = [c.strip() for c in s.split('|')[1:-1]]
            if not in_table:
                result.append(
                    '<table style="width:100%;border-collapse:collapse;font-size:14px;margin:6px 0">')
                in_table = True
                header_done = False
            if not header_done:
                tag = "th"
                header_done = True
            else:
                tag = "td"
            sty = f"border:1px solid {theme['table_border']};padding:6px 10px;"
            if tag == "th":
                sty += f"font-weight:700;background:{theme['table_header_bg']};"
            row = ''.join(
                f'<{tag} style="{sty}">{inline_fmt(c, theme)}</{tag}>' for c in cells)
            result.append(f'<tr>{row}</tr>')
            continue

        # Close table
        if in_table:
            result.append('</table>')
            in_table = False
            header_done = False

        # Headings
        if s.startswith('# '):
            result.append(
                f'<div style="font-size:19px;font-weight:700;margin-bottom:6px">{inline_fmt(s[2:], theme)}</div>')
        elif s.startswith('## '):
            result.append(
                f'<div style="font-size:16px;font-weight:700;margin-bottom:5px">{inline_fmt(s[3:], theme)}</div>')
        elif s.startswith('### '):
            result.append(
                f'<div style="font-size:14px;font-weight:700;margin-bottom:4px">{inline_fmt(s[4:], theme)}</div>')
        # Blockquote
        elif s.startswith('> '):
            result.append(
                f'<div style="font-style:italic;opacity:0.9;font-size:13px;'
                f'border-left:3px solid {theme["quote_border"]};padding-left:8px;margin:4px 0">'
                f'{inline_fmt(s[2:], theme)}</div>')
        # Bullet
        elif s.startswith('- '):
            result.append(
                f'<div style="padding-left:14px;text-indent:-12px;margin:3px 0">• {inline_fmt(s[2:], theme)}</div>')
        # Plain text
        elif s:
            result.append(f'<div style="margin:3px 0">{inline_fmt(s, theme)}</div>')

    if in_table:
        result.append('</table>')
    return '\n'.join(result)


# --- Edge geometry ---
def side_point(node, side, offset_x, offset_y):
    cx = node["x"] + node["width"] / 2 - offset_x
    cy = node["y"] + node["height"] / 2 - offset_y
    if side == "top":
        return (cx, node["y"] - offset_y)
    if side == "bottom":
        return (cx, node["y"] + node["height"] - offset_y)
    if side == "left":
        return (node["x"] - offset_x, cy)
    if side == "right":
        return (node["x"] + node["width"] - offset_x, cy)
    return (cx, cy)


def render_edges(edges, node_lookup, offset_x, offset_y, theme):
    svgs = []
    for edge in edges:
        fn = node_lookup.get(edge.get("fromNode"))
        tn = node_lookup.get(edge.get("toNode"))
        if not fn or not tn:
            continue

        fs = edge.get("fromSide", "bottom")
        ts = edge.get("toSide", "top")
        fp = side_point(fn, fs, offset_x, offset_y)
        tp = side_point(tn, ts, offset_x, offset_y)

        color_id = edge.get("color", "")
        stroke = theme["edge_colors"].get(color_id, theme["edge_default"])
        opacity = theme["edge_opacity"]

        mx, my = (fp[0] + tp[0]) / 2, (fp[1] + tp[1]) / 2

        # Control points for bezier curve
        if fs in ("left", "right") and ts in ("left", "right"):
            c1, c2 = (mx, fp[1]), (mx, tp[1])
        elif fs == "bottom" and ts == "bottom":
            low = max(fp[1], tp[1]) + 60
            c1, c2 = (fp[0], low), (tp[0], low)
        else:
            c1, c2 = (fp[0], my), (tp[0], my)

        path = f"M {fp[0]} {fp[1]} C {c1[0]} {c1[1]}, {c2[0]} {c2[1]}, {tp[0]} {tp[1]}"

        # Arrowhead
        angle = math.atan2(tp[1] - c2[1], tp[0] - c2[0])
        a1 = (tp[0] - 12 * math.cos(angle - 0.4),
              tp[1] - 12 * math.sin(angle - 0.4))
        a2 = (tp[0] - 12 * math.cos(angle + 0.4),
              tp[1] - 12 * math.sin(angle + 0.4))

        svgs.append(
            f'<path d="{path}" fill="none" stroke="{stroke}" '
            f'stroke-width="2.5" stroke-opacity="{opacity}"/>')
        svgs.append(
            f'<polygon points="{tp[0]},{tp[1]} {a1[0]},{a1[1]} {a2[0]},{a2[1]}" '
            f'fill="{stroke}" fill-opacity="{opacity}"/>')

        # Edge label
        label = edge.get("label", "")
        if label:
            svgs.append(
                f'<text x="{mx}" y="{my + 30}" font-size="13" fill="{stroke}" '
                f'text-anchor="middle" font-family="system-ui">'
                f'{html_mod.escape(label)}</text>')

    return '\n'.join(svgs)


# --- Main ---
def main():
    parser = argparse.ArgumentParser(
        description="Render an Obsidian Canvas file to a JPG image.")
    parser.add_argument("input", help="Input .canvas file path")
    parser.add_argument("output", nargs="?",
                        help="Output .jpg path (defaults to input with .jpg extension)")
    parser.add_argument("--light", action="store_true",
                        help="Use light theme (white bg, pastel boxes). Default is dark.")
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output or os.path.splitext(input_path)[0] + ".jpg"
    theme = THEMES["light" if args.light else "dark"]

    with open(input_path, "r", encoding="utf-8") as f:
        canvas = json.load(f)

    nodes = canvas.get("nodes", [])
    edges = canvas.get("edges", [])

    if not nodes:
        print("Error: No nodes found in canvas")
        raise SystemExit(1)

    # Bounding box
    min_x = min(n["x"] for n in nodes) - PADDING
    min_y = min(n["y"] for n in nodes) - PADDING
    max_x = max(n["x"] + n["width"] for n in nodes) + PADDING
    max_y = max(n["y"] + n["height"] for n in nodes) + PADDING
    canvas_w = max_x - min_x
    canvas_h = max_y - min_y

    node_lookup = {n["id"]: n for n in nodes}

    # Render edges
    edge_svg = render_edges(edges, node_lookup, min_x, min_y, theme)

    # Render nodes
    node_divs = []
    for n in nodes:
        c = theme["colors"].get(n.get("color", ""), theme["default"])
        x = n["x"] - min_x
        y = n["y"] - min_y
        w, h = n["width"], n["height"]
        content = md_to_html(n.get("text", ""), theme)

        node_divs.append(f'''<div style="
            position:absolute;left:{x}px;top:{y}px;width:{w}px;min-height:{h}px;
            background:{c['bg']};color:{c['text']};border:{theme['border_width']} solid {c['border']};
            border-radius:8px;padding:14px 16px;box-sizing:border-box;
            font-family:{FONT_STACK};
            font-size:14px;line-height:1.6;overflow:hidden;
            box-shadow:{theme['box_shadow']};
        ">{content}</div>''')

    # Assemble HTML
    page_html = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:{theme['bg']};">
<div style="position:relative;width:{canvas_w}px;height:{canvas_h}px;">
<svg style="position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none;">
{edge_svg}
</svg>
{''.join(node_divs)}
</div>
</body></html>'''

    # Screenshot
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(
            viewport={"width": int(canvas_w), "height": int(canvas_h)},
            device_scale_factor=SCALE_FACTOR
        )
        page.set_content(page_html)
        page.wait_for_timeout(500)
        page.screenshot(path=output_path, type="jpeg",
                        quality=JPEG_QUALITY, full_page=True)
        browser.close()

    print(f"Saved: {output_path} ({int(canvas_w * SCALE_FACTOR)}x{int(canvas_h * SCALE_FACTOR)}px)")


if __name__ == "__main__":
    main()
