"""
.github/scripts/gen_bento.py

Generates bento-dark.svg or bento-light.svg with live weather data.

Usage (called by GitHub Action):
    python3 gen_bento.py <theme> <temp> <condition> <emoji> > bento-<theme>.svg

Usage (local placeholder generation):
    python3 gen_bento.py
    → writes bento-dark.svg and bento-light.svg with placeholder data
"""

import sys


def make_svg(theme, temp="--°C", condition="Loading...", emoji="🌡️"):
    dark  = theme == "dark"
    bg    = "#0d1117" if dark else "#ffffff"
    bg2   = "#161b22" if dark else "#f6f8fa"
    bg3   = "#1c2128" if dark else "#eaeef2"
    bdr   = "#30363d" if dark else "#d0d7de"
    t1    = "#e6edf3" if dark else "#1f2328"
    t2    = "#8b949e" if dark else "#57606a"
    t3    = "#484f58" if dark else "#afb8c1"
    green = "#39d353" if dark else "#2da44e"
    blue  = "#58a6ff" if dark else "#0969da"
    purp  = "#bc8cff" if dark else "#8250df"
    amber = "#e6db74" if dark else "#9a6700"

    W, GAP, PAD = 640, 10, 14
    CW  = (W - GAP) // 2
    H1  = 92   # top row
    H2  = 82   # middle row
    H3  = 56   # weather row
    TH  = PAD + H1 + GAP + H2 + GAP + H3 + PAD

    def rect(x, y, w, h, fill=bg2, stroke=bdr, rx=8):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="0.5"/>'

    def txt(x, y, content, fill, size=10, weight="normal", spacing="0"):
        return f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" fill="{fill}" font-weight="{weight}" letter-spacing="{spacing}">{content}</text>'

    def bar(x, y, total, filled, fill):
        return (
            f'<rect x="{x}" y="{y}" width="{total}" height="4" rx="2" fill="{bg3}"/>'
            f'<rect x="{x}" y="{y}" width="{filled}" height="4" rx="2" fill="{fill}"/>'
        )

    r1y = PAD
    r2y = PAD + H1 + GAP
    r3y = PAD + H1 + GAP + H2 + GAP
    BW  = CW - PAD*2 - 52

    # vertical separator x position in weather cell
    SEP_X = PAD + 140

    parts = [
        f'<svg width="{W}" height="{TH}" viewBox="0 0 {W} {TH}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{W}" height="{TH}" rx="12" fill="{bg}"/>',

        # ── Cell 1: ROLE ─────────────────────────────────────
        rect(0, r1y, CW, H1),
        txt(PAD, r1y+20, "ROLE", t3, size=9, spacing="2"),
        f'<circle cx="{CW-PAD}" cy="{r1y+16}" r="4" fill="{green}"/>',
        txt(PAD, r1y+42, "Systems", t1, size=14, weight="600"),
        txt(PAD, r1y+60, "Developer", green, size=14, weight="600"),
        txt(PAD, r1y+H1-10, "@ Statens vegvesen", t2, size=10),

        # ── Cell 2: LOCATION ─────────────────────────────────
        rect(CW+GAP, r1y, CW, H1),
        txt(CW+GAP+PAD, r1y+20, "LOCATION", t3, size=9, spacing="2"),
        txt(CW+GAP+PAD, r1y+52, "Norway", t1, size=16, weight="600"),
        txt(CW+GAP+PAD, r1y+H1-10, "59.9 N  ·  UTC+1", t2, size=10),

        # ── Cell 3: STUDYING ─────────────────────────────────
        rect(0, r2y, CW, H2),
        txt(PAD, r2y+20, "STUDYING", t3, size=9, spacing="2"),
        txt(PAD, r2y+42, "BSc IT &amp; IS", blue, size=13, weight="600"),
        txt(PAD, r2y+H2-10, "@ USN, Norway", t2, size=10),

        # ── Cell 4: FOCUS ────────────────────────────────────
        rect(CW+GAP, r2y, CW, H2),
        txt(CW+GAP+PAD, r2y+20, "FOCUS", t3, size=9, spacing="2"),
        txt(CW+GAP+PAD, r2y+36, "backend", t2, size=9),
        bar(CW+GAP+PAD+52, r2y+31, BW, int(BW*.88), green),
        txt(CW+GAP+PAD, r2y+52, "infra", t2, size=9),
        bar(CW+GAP+PAD+52, r2y+47, BW, int(BW*.75), blue),
        txt(CW+GAP+PAD, r2y+68, "AI/ML", t2, size=9),
        bar(CW+GAP+PAD+52, r2y+63, BW, int(BW*.55), purp),

        # ── Cell 5: WEATHER (full width) ─────────────────────
        rect(0, r3y, W, H3),
        txt(PAD, r3y+20, "WEATHER", t3, size=9, spacing="2"),
        # emoji
        txt(PAD, r3y+46, emoji, t1, size=22),
        # temperature
        txt(PAD+38, r3y+46, temp, amber, size=20, weight="600"),
        # vertical separator
        f'<line x1="{SEP_X}" y1="{r3y+14}" x2="{SEP_X}" y2="{r3y+H3-8}" '
        f'stroke="{bdr}" stroke-width="0.5"/>',
        # condition
        txt(SEP_X+14, r3y+34, condition, t1, size=12, weight="600"),
        # location + update cadence
        txt(SEP_X+14, r3y+50, "Oslo, Norway  ·  updated hourly", t2, size=10),

        '</svg>'
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    if len(sys.argv) >= 5:
        # Called by GitHub Action: theme temp condition emoji
        print(make_svg(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]))
    else:
        # Local: generate placeholder SVGs for both themes
        for theme in ["dark", "light"]:
            svg = make_svg(theme)
            path = f"bento-{theme}.svg"
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"Written: {path}")
