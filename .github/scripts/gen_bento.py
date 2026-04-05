import sys

# ── EMOJI MAP ─────────────────────────────────────────────────
# Single emojis only — no doubles
# Condition text comes separately so emoji doesn't need to carry full meaning
EMOJI_MAP = {
    "clearsky_day":            "☀️",
    "clearsky_night":          "🌙",
    "clearsky_polartwilight":  "🌅",
    "fair_day":                "🌤️",
    "fair_night":              "🌙",
    "partlycloudy_day":        "⛅",
    "partlycloudy_night":      "🌙",
    "cloudy":                  "☁️",
    "fog":                     "🌫️",
    "lightfog":                "🌫️",
    "lightrainshowers_day":    "🌦️",
    "lightrainshowers_night":  "🌧️",
    "rainshowers_day":         "🌧️",
    "rainshowers_night":       "🌧️",
    "heavyrainshowers_day":    "🌧️",
    "heavyrainshowers_night":  "🌧️",
    "lightrain":               "🌦️",
    "rain":                    "🌧️",
    "heavyrain":               "🌧️",
    "lightsleetshowers_day":   "🌨️",
    "lightsleetshowers_night": "🌨️",
    "sleetshowers_day":        "🌨️",
    "sleetshowers_night":      "🌨️",
    "lightsleet":              "🌨️",
    "sleet":                   "🌨️",
    "lightsnowshowers_day":    "🌨️",
    "lightsnowshowers_night":  "❄️",
    "snowshowers_day":         "🌨️",
    "snowshowers_night":       "❄️",
    "lightsnow":               "❄️",
    "snow":                    "❄️",
    "heavysnow":               "❄️",
    "thunder":                 "⛈️",
    "rainandthunder":          "⛈️",
    "lightrainandthunder":     "⛈️",
    "heavyrainandthunder":     "⛈️",
    "sleetandthunder":         "⛈️",
    "snowandthunder":          "⛈️",
    "lightrainshowersandthunder_day":   "⛈️",
    "lightrainshowersandthunder_night": "⛈️",
}

def symbol_to_emoji(symbol):
    emoji = EMOJI_MAP.get(symbol)
    if not emoji:
        # strip _day/_night/_polartwilight and try base
        base = symbol.replace("_day","").replace("_night","").replace("_polartwilight","")
        emoji = EMOJI_MAP.get(base, "🌡️")
    return emoji

def symbol_to_condition(symbol):
    """Convert symbol_code to readable condition with proper spacing."""
    base = symbol.replace("_day","").replace("_night","").replace("_polartwilight","")
    # insert spaces before capitals isn't needed — use replacement dict
    COND_MAP = {
        "clearsky":        "Clear sky",
        "fair":            "Fair",
        "partlycloudy":    "Partly cloudy",
        "cloudy":          "Cloudy",
        "fog":             "Fog",
        "lightfog":        "Light fog",
        "lightrain":       "Light rain",
        "rain":            "Rain",
        "heavyrain":       "Heavy rain",
        "lightrainshowers":"Light showers",
        "rainshowers":     "Showers",
        "heavyrainshowers":"Heavy showers",
        "lightsleet":      "Light sleet",
        "sleet":           "Sleet",
        "lightsleetshowers":"Light sleet showers",
        "sleetshowers":    "Sleet showers",
        "lightsnow":       "Light snow",
        "snow":            "Snow",
        "heavysnow":       "Heavy snow",
        "lightsnowshowers":"Light snow showers",
        "snowshowers":     "Snow showers",
        "thunder":         "Thunder",
        "rainandthunder":  "Rain and thunder",
        "lightrainandthunder": "Light rain, thunder",
        "heavyrainandthunder": "Heavy rain, thunder",
        "sleetandthunder": "Sleet and thunder",
        "snowandthunder":  "Snow and thunder",
        "lightrainshowersandthunder": "Showers and thunder",
    }
    return COND_MAP.get(base, base.replace("and"," and ").capitalize())

# ── SVG GENERATOR ─────────────────────────────────────────────
def make_svg(theme, temp="--°C", condition="Loading...", emoji="🌡️", timestamp="--:-- UTC"):
    dark  = theme == "dark"
    bg    = "#0d1117" if dark else "#ffffff"
    bg2   = "#161b22" if dark else "#f6f8fa"
    bg3   = "#21262d" if dark else "#eaeef2"
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
    H1  = 80   # weather cell
    H2  = 80   # focus cell
    TH  = PAD + H1 + PAD

    # Emoji width detection — some emoji are wider (flag, double-width)
    # We use a fixed offset approach: emoji x=PAD, temp starts at PAD+34
    EMOJI_X   = PAD
    TEMP_X    = PAD + 34   # consistent gap after emoji regardless of width

    def rect(x, y, w, h, fill=bg2, stroke=bdr, rx=8):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="0.5"/>'

    def txt(x, y, content, fill, size=10, weight="normal", spacing="0", anchor="start"):
        return (f'<text x="{x}" y="{y}" font-family="monospace" font-size="{size}" '
                f'fill="{fill}" font-weight="{weight}" letter-spacing="{spacing}" '
                f'text-anchor="{anchor}">{content}</text>')

    def bar(x, y, total, filled, fill):
        return (
            f'<rect x="{x}" y="{y}" width="{total}" height="4" rx="2" fill="{bg3}"/>'
            f'<rect x="{x}" y="{y}" width="{filled}" height="4" rx="2" fill="{fill}"/>'
        )

    BW = CW - PAD*2 - 50   # bar track width

    # Row y positions
    ry = PAD

    parts = [
        f'<svg width="{W}" height="{TH}" viewBox="0 0 {W} {TH}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{W}" height="{TH}" rx="10" fill="{bg}"/>',

        # ── WEATHER CELL (left) ───────────────────────────────
        rect(0, ry, CW, H1),
        txt(PAD, ry+18, "WEATHER  ·  OSLO", t3, size=9, spacing="2"),
        # emoji — fixed position
        txt(EMOJI_X, ry+50, emoji, t1, size=20),
        # temp — fixed offset from emoji
        txt(TEMP_X, ry+50, temp, amber, size=19, weight="600"),
        # condition on second line
        txt(PAD, ry+H1-10, condition, t2, size=10),

        # ── FOCUS CELL (right) ───────────────────────────────
        rect(CW+GAP, ry, CW, H2),
        txt(CW+GAP+PAD, ry+18, "FOCUS", t3, size=9, spacing="2"),
        txt(CW+GAP+PAD, ry+34, "backend", t2, size=9),
        bar(CW+GAP+PAD+50, ry+29, BW, int(BW*.88), green),
        txt(CW+GAP+PAD, ry+50, "infra", t2, size=9),
        bar(CW+GAP+PAD+50, ry+45, BW, int(BW*.75), blue),
        txt(CW+GAP+PAD, ry+66, "AI/ML", t2, size=9),
        bar(CW+GAP+PAD+50, ry+61, BW, int(BW*.55), purp),

        # timestamp bottom-right of weather cell
        txt(CW-PAD, ry+H1-10, f"updated {timestamp}", t3, size=9, anchor="end"),

        '</svg>'
    ]
    return "\n".join(parts)


if __name__ == "__main__":
    if len(sys.argv) >= 6:
        # Called by Action: theme temp condition emoji timestamp
        theme, temp, condition, emoji, timestamp = sys.argv[1:6]
        print(make_svg(theme, temp, condition, emoji, timestamp))
    elif len(sys.argv) >= 5:
        # Called by Action without timestamp (backwards compat)
        theme, temp, condition, emoji = sys.argv[1:5]
        print(make_svg(theme, temp, condition, emoji))
    else:
        # Local placeholder generation
        for theme in ["dark","light"]:
            svg = make_svg(theme)
            with open(f"/mnt/user-data/outputs/bento-{theme}.svg","w",encoding="utf-8") as f:
                f.write(svg)
            print(f"Written: bento-{theme}.svg")

