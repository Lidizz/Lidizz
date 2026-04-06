import sys

def make_terminal(theme, temp="--°C", condition="Loading...", emoji="🌡️", timestamp="--:-- UTC"):
    dark = theme == "dark"

    # colours
    bg_outer  = "#0d1117" if dark else "#ffffff"
    bg_bar    = "#161b22" if dark else "#e8e8e8"
    bg_term   = "#0d1117" if dark else "#f6f8fa"
    bdr       = "#30363d" if dark else "#d0d7de"
    prompt    = "#39d353" if dark else "#2da44e"
    path_c    = "#e6db74" if dark else "#9a6700"
    cmd_c     = "#58a6ff" if dark else "#0969da"
    out_c     = "#8b949e" if dark else "#57606a"
    hl_c      = "#e6edf3" if dark else "#1f2328"
    green_c   = "#39d353" if dark else "#2da44e"
    blue_c    = "#58a6ff" if dark else "#0969da"
    purple_c  = "#bc8cff" if dark else "#8250df"
    orange_c  = "#ffa657" if dark else "#bc4c00"
    key_c     = "#79c0ff" if dark else "#0550ae"
    val_c     = "#a5d6ff" if dark else "#0a3069"
    dim_c     = "#484f58" if dark else "#afb8c1"
    cursor_c  = "#39d353" if dark else "#2da44e"
    dot1      = "#ff5f57"
    dot2      = "#febc2e"
    dot3      = "#28c840"

    W   = 640
    BAR = 36
    PAD = 20
    LH  = 22   # line height
    FS  = 12   # font size

    # lines of content
    LINES = [
        # (type, segments)
        # types: prompt, blank, out
        ("prompt", [("prompt", "lidizz@github"), ("dim", ":"), ("path", "~"), ("dim", "$ "), ("cmd", "cat about.txt")]),
        ("out",    [("out", "Systems Developer "), ("out", "@ "), ("orange", "Statens vegvesen")]),
        ("out",    [("out", "IT & IS student "), ("out", "@ "), ("purple", "USN"), ("out", ", Norway")]),
        ("out",    [("out", "Experimenting with "), ("out", "AI/ML"), ("out", " in my free time")]),
        ("blank",  []),
        ("prompt", [("prompt", "lidizz@github"), ("dim", ":"), ("path", "~"), ("dim", "$ "), ("cmd", "cat status.json")]),
        ("out",    [("out", "{")]),
        ("out",    [("out", "  "), ("key", '"weather"'), ("out", ":  "), ("val", f'"{emoji} {temp} \u00b7 {condition} \u00b7 last updated: {timestamp}"'), ("out", ",")]),
        ("out",    [("out", "  "), ("key", '"status"'),  ("out", ":   "), ("out", '"open to interesting conversations"')]),
        ("out",    [("out", "}")]),
        ("blank",  []),
        ("prompt", [("prompt", "lidizz@github"), ("dim", ":"), ("path", "~"), ("dim", "$ "), ("cursor", "")]),
    ]

    content_h = len(LINES) * LH + PAD
    H = BAR + content_h + PAD

    COLOR = {
        "prompt": prompt, "path": path_c, "cmd": cmd_c,
        "out": out_c, "hl": hl_c, "green": green_c,
        "blue": blue_c, "purple": purple_c, "orange": orange_c,
        "key": key_c, "val": val_c, "dim": dim_c,
    }

    def escape(s):
        return s.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;").replace('"','&quot;')

    def render_line(segments, y):
        """Render a line using SVG tspan elements inside one text element."""
        parts = [f'<text y="{y}" font-family="monospace" font-size="{FS}" x="{PAD}">']
        for seg_type, seg_text in segments:
            if seg_type == "cursor":
                # blinking cursor rect — separate element, added after
                parts.append(f'</text>')
                return "".join(parts), True  # signal cursor needed
            color = COLOR.get(seg_type, out_c)
            parts.append(f'<tspan fill="{color}">{escape(seg_text)}</tspan>')
        parts.append('</text>')
        return "".join(parts), False

    svg_parts = [
        f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">',
        # outer rounded rect
        f'<rect width="{W}" height="{H}" rx="10" fill="{bg_outer}" stroke="{bdr}" stroke-width="0.5"/>',
        # title bar
        f'<rect width="{W}" height="{BAR}" rx="10" fill="{bg_bar}"/>',
        f'<rect y="{BAR-4}" width="{W}" height="4" fill="{bg_bar}"/>',  # square bottom of bar
        f'<line x1="0" y1="{BAR}" x2="{W}" y2="{BAR}" stroke="{bdr}" stroke-width="0.5"/>',
        # traffic dots
        f'<circle cx="16" cy="{BAR//2}" r="5.5" fill="{dot1}"/>',
        f'<circle cx="32" cy="{BAR//2}" r="5.5" fill="{dot2}"/>',
        f'<circle cx="48" cy="{BAR//2}" r="5.5" fill="{dot3}"/>',
        # title text
        f'<text x="{W//2}" y="{BAR//2+4}" font-family="monospace" font-size="11" '
        f'fill="{dim_c}" text-anchor="middle">lidizz@github \u2014 bash</text>',
        # terminal body bg
        f'<rect y="{BAR}" width="{W}" height="{H-BAR}" fill="{bg_term}"/>',
        f'<rect y="{H-10}" width="{W}" height="10" rx="0" fill="{bg_term}"/>',  # keep corners square at bottom
        f'<rect y="{H-10}" width="{W}" height="10" rx="10" fill="{bg_outer}"/>',
        f'<rect y="{H-20}" width="{W}" height="10" fill="{bg_term}"/>',
    ]

    cursor_x_approx = PAD  # fallback
    cursor_y_approx = BAR + PAD + LH

    y = BAR + PAD + LH
    for line_type, segments in LINES:
        if line_type == "blank":
            y += LH // 2
            continue
        line_svg, has_cursor = render_line(segments, y)
        svg_parts.append(line_svg)
        if has_cursor:
            # estimate cursor x by counting chars in prompt
            prompt_text = "lidizz@github:~$ "
            cursor_x_approx = PAD + len(prompt_text) * 7  # ~7px per mono char at fs12
            cursor_y_approx = y - FS + 2
        y += LH

    # blinking cursor rect
    svg_parts.append(
        f'<rect x="{cursor_x_approx}" y="{cursor_y_approx}" width="7" height="{FS+1}" fill="{cursor_c}">'
        f'<animate attributeName="opacity" values="1;1;0;0" dur="1.2s" repeatCount="indefinite"/>'
        f'</rect>'
    )

    svg_parts.append('</svg>')
    return "\n".join(svg_parts)


if __name__ == "__main__":
    if len(sys.argv) >= 6:
        theme, temp, condition, emoji, timestamp = sys.argv[1:6]
        print(make_terminal(theme, temp, condition, emoji, timestamp))
    elif len(sys.argv) >= 5:
        theme, temp, condition, emoji = sys.argv[1:5]
        print(make_terminal(theme, temp, condition, emoji))
    else:
        for theme in ["dark", "light"]:
            svg = make_terminal(theme)
            path = f"/mnt/user-data/outputs/terminal-{theme}.svg"
            with open(path, "w", encoding="utf-8") as f:
                f.write(svg)
            print(f"Written: {path}")
