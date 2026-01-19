#!/usr/bin/env python3
"""
Generate an SVG file with colored ASCII-style text for README.

Usage:
  python tools/gen_readme_svg.py --out resources/readme_ascii.svg

You can also provide a JSON file describing `lines` (list of list of spans),
where each span is {"fill": "#RRGGBB", "text": "..."}.
If no input JSON is provided, a default template matching the README block is used.
"""
from __future__ import annotations
import argparse
import json
import os
import html
from typing import List, Dict


DEFAULT_WIDTH = 900
DEFAULT_HEIGHT = 460
DEFAULT_FONT = "DejaVu Sans Mono, monospace"
DEFAULT_FONT_SIZE = 14


DEFAULT_TEMPLATE = [
    [{"fill": "#800020", "text": "Profile Configuration:"}],
    [
        {"fill": "#800020", "text": "├── "},
        {"fill": "#FF0000", "text": "User:"},
        {"fill": "#FF6347", "text": "  Gr00ss"},
    ],
    [
        {"fill": "#800020", "text": "├── "},
        {"fill": "#FF0000", "text": "Location:"},
        {"fill": "#FF6347", "text": "  /home/revenant/github/Gr00ss"},
    ],
    [
        {"fill": "#800020", "text": "├── "},
        {"fill": "#FF0000", "text": "Shell:"},
        {"fill": "#FF8C00", "text": "  /bin/bash"},
    ],
    [
        {"fill": "#800020", "text": "├── "},
        {"fill": "#FF0000", "text": "Theme:"},
        {"fill": "#FF6347", "text": "  linux-terminal (dark mode)"},
    ],
    [{"fill": "#800020", "text": "├── "}, {"fill": "#FF0000", "text": "Color Scheme:"}],
    [
        {"fill": "#800020", "text": "│   ├── "},
        {"fill": "#800020", "text": "Border:"},
        {"fill": "#800020", "text": " burgundy (#800020)"},
    ],
    [
        {"fill": "#8B0000", "text": "│   ├── "},
        {"fill": "#8B0000", "text": "Dark-Red:"},
        {"fill": "#8B0000", "text": " dark-red (#8B0000)"},
    ],
    [
        {"fill": "#FF0000", "text": "│   ├── "},
        {"fill": "#FF0000", "text": "Header / Red:"},
        {"fill": "#FF0000", "text": " red (#FF0000)"},
    ],
    [
        {"fill": "#FF6347", "text": "│   ├── "},
        {"fill": "#FF6347", "text": "Text (Light-Red):"},
        {"fill": "#FF6347", "text": " light-red (#FF6347)"},
    ],
    [
        {"fill": "#FFFFFF", "text": "│   └── "},
        {"fill": "#FFFFFF", "text": "Normal (White):"},
        {"fill": "#FFFFFF", "text": " white (#FFFFFF)"},
    ],
    [
        {"fill": "#800020", "text": "└── Status: "},
        {"fill": "#00FF00", "text": "ACTIVE"},
    ],
]


def escape_tspan_text(s: str) -> str:
    return html.escape(s)


def build_svg(lines: List[List[Dict[str, str]]], width: int, height: int, font_family: str, font_size: int) -> str:
    line_h = int(font_size * 1.6)
    x = 12
    y_start = 28
    parts = []
    parts.append(f'<?xml version="1.0" encoding="UTF-8"?>')
    parts.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">')
    parts.append(f'<rect width="100%" height="100%" fill="#070607"/>')
    parts.append(f'<style>text{{font-family: {font_family}; font-size:{font_size}px; white-space:pre;}}</style>')

    for i, spans in enumerate(lines):
        y = y_start + i * line_h
        parts.append(f'<text x="{x}" y="{y}">')
        for span in spans:
            fill = span.get("fill", "#FFFFFF")
            text = escape_tspan_text(span.get("text", ""))
            parts.append(f'<tspan fill="{fill}">{text}</tspan>')
        parts.append('</text>')

    parts.append('</svg>')
    return "\n".join(parts)


def main() -> None:
    p = argparse.ArgumentParser(description="Generate README ASCII SVG with colors")
    p.add_argument("--in", dest="infile", help="Optional JSON file describing lines/spans")
    p.add_argument("--md", dest="mdfile", default="tools/readme_ascii.md", help="Optional markdown file with ASCII text (default: tools/readme_ascii.md)")
    p.add_argument("--out", dest="outfile", default="resources/readme_ascii.svg", help="Output SVG path")
    p.add_argument("--width", type=int, default=DEFAULT_WIDTH)
    p.add_argument("--height", type=int, default=DEFAULT_HEIGHT)
    p.add_argument("--font-size", type=int, default=DEFAULT_FONT_SIZE)
    p.add_argument("--font-family", default=DEFAULT_FONT)
    args = p.parse_args()

    lines = DEFAULT_TEMPLATE
    # If an input JSON is provided, use that template (same as before)
    if args.infile:
        if not os.path.exists(args.infile):
            raise SystemExit(f"Input file not found: {args.infile}")
        with open(args.infile, "r", encoding="utf-8") as fh:
            data = json.load(fh)
            lines = data.get("lines", DEFAULT_TEMPLATE)
    # Otherwise, if a markdown file is provided (or default exists), parse it
    elif args.mdfile and os.path.exists(args.mdfile):
        with open(args.mdfile, "r", encoding="utf-8") as fh:
            md_lines = [ln.rstrip("\n") for ln in fh.readlines() if ln.strip()]
        # Convert each text line into spans: box-drawing prefix (burgundy) + rest (light-red)
        parsed: List[List[Dict[str, str]]] = []
        for ln in md_lines:
            # detect leading box chars
            prefix = ""
            rest = ln
            if ln and ln[0] in "┌┐└┘├┤│─":
                # capture continuous leading box chars/spaces
                i = 0
                while i < len(ln) and ln[i] in "┌┐└┘├┤│─ ─":
                    prefix += ln[i]
                    i += 1
                rest = ln[i:]
            spans = []
            if prefix:
                spans.append({"fill": "#800020", "text": prefix})
            # default rest color: light-red
            if rest:
                spans.append({"fill": "#FF6347", "text": rest})
            parsed.append(spans)
        if parsed:
            lines = parsed

    svg = build_svg(lines, args.width, args.height, args.font_family, args.font_size)
    os.makedirs(os.path.dirname(args.outfile) or ".", exist_ok=True)
    with open(args.outfile, "w", encoding="utf-8") as fh:
        fh.write(svg)
    print(f"Wrote SVG to {args.outfile}")


if __name__ == "__main__":
    main()
