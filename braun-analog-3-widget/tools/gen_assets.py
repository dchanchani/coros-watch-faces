"""Generate the Braun Analog 3-widget artwork (PNG) from spec.py via SVG + rsvg-convert.

Needs Python 3 with Pillow, rsvg-convert (librsvg), and Barlow installed for fontconfig
(e.g. Barlow-Medium.ttf in ~/.fonts, then fc-cache -f). Writes everything to ./out/.
See ../BUILD.md for which output file goes where in the repo.
"""
import math, os, subprocess, json
from spec import *

OUT = os.path.join(os.path.dirname(__file__), "out")
os.makedirs(OUT, exist_ok=True)

def svg_doc(body, size=MASTER, bg=None):
    rect = f'<rect width="{size}" height="{size}" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
            f'viewBox="0 0 {size} {size}">{rect}{body}</svg>')

def _require_font(family="Barlow"):
    """rsvg silently falls back (to Liberation Sans/Arial) when a family is missing; refuse to render instead."""
    got = subprocess.run(["fc-match", "-f", "%{family}", f"{family}:weight=100"], capture_output=True, text=True).stdout
    if family not in got.split(","):
        raise SystemExit(f"{family} is not installed for fontconfig (fc-match gave {got!r}); put Barlow-*.ttf in ~/.fonts and run fc-cache -f")

def write_png(name, svg, size=MASTER):
    _require_font()
    sub = os.path.dirname(name)
    if sub:
        os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    svg_path = os.path.join(OUT, name + ".svg")
    png_path = os.path.join(OUT, name + ".png")
    with open(svg_path, "w") as f:
        f.write(svg)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size), "-o", png_path, svg_path], check=True)
    os.remove(svg_path)
    return png_path

# ---------- dial pieces (shared with the review page) ----------
def ticks_svg(hour_only=False, aod=False):
    out = []
    for i in range(60):
        is_hour = i % 5 == 0
        if hour_only and not is_hour:
            continue
        a = math.radians(i * 6 - 90)
        r1 = DIAL["tick_outer_r"]
        ln = DIAL["tick_hour_len"] if is_hour else DIAL["tick_minute_len"]
        w = DIAL["tick_hour_w"] if is_hour else DIAL["tick_minute_w"]
        col = COLORS["aod_tick"] if aod else (COLORS["tick_hour"] if is_hour else COLORS["tick_minute"])
        x1, y1 = C + r1 * math.cos(a), C + r1 * math.sin(a)
        x2, y2 = C + (r1 - ln) * math.cos(a), C + (r1 - ln) * math.sin(a)
        out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                   f'stroke="{col}" stroke-width="{w}" stroke-linecap="butt"/>')
    return "".join(out)

def _digit_half_height(size, weight):
    """Half the visible height of a digit at this size, from the real font file (for true vertical centering)."""
    from PIL import ImageFont
    import glob
    names = {400: "Regular", 500: "Medium", 600: "SemiBold", 700: "Bold"}
    path = os.path.expanduser(f"~/.fonts/Barlow-{names[weight]}.ttf")
    font = ImageFont.truetype(path, size)  # fails loudly if Barlow isn't installed
    x0, y0, x1, y1 = font.getbbox("0", anchor="ls")  # relative to the baseline
    return (y1 - y0) / 2 - y1  # distance from baseline up to the digit's vertical middle

def numerals_svg():
    """Numerals optically centered on the numeral ring. The baseline is placed explicitly because
    rsvg ignores dominant-baseline, which would shift every numeral up by half its height."""
    out = []
    half = _digit_half_height(DIAL["numeral_size"], DIAL["numeral_weight"])
    for h in range(1, 13):
        a = math.radians(h * 30 - 90)
        x, y = C + DIAL["numeral_r"] * math.cos(a), C + DIAL["numeral_r"] * math.sin(a)
        out.append(f'<text x="{x:.1f}" y="{y + half:.1f}" font-family="{DIAL["numeral_font"]}, Helvetica Neue, Arial, sans-serif" '
                   f'font-weight="{DIAL["numeral_weight"]}" font-size="{DIAL["numeral_size"]}" fill="{COLORS["numeral"]}" '
                   f'text-anchor="middle">{h}</text>')
    return "".join(out)

def inner_ring_svg():
    return (f'<circle cx="{C}" cy="{C}" r="{DIAL["inner_ring_r"]}" fill="none" '
            f'stroke="{COLORS["inner_ring"]}" stroke-width="{DIAL["inner_ring_w"]}"/>')

# ---------- hands (pivot at canvas center, pointing to 12) ----------
def _bar(x0, y0, x1, y1, r, col):
    """Axis-aligned rounded rectangle (tiny radius = squared-off look)."""
    return (f'<rect x="{x0:.2f}" y="{y0:.2f}" width="{x1-x0:.2f}" height="{y1-y0:.2f}" rx="{r}" ry="{r}" fill="{col}"/>')

def hour_hand_svg(aod=False):
    h = HANDS["hour"]; hw = h["w_base"] / 2; tw = h["w_tip"] / 2
    top = C - h["len"]; tip_bottom = top + h["tip_len"]
    body_col = COLORS["aod_hour"] if aod else COLORS["hour"]
    tip_col = COLORS["aod_hour_tip"] if aod else COLORS["hour_tip"]
    # slightly tapered body as a polygon with squared ends, then a square tip block
    body = (f'<polygon points="{C-hw},{C} {C-tw},{top} {C+tw},{top} {C+hw},{C}" fill="{body_col}" '
            f'stroke="{body_col}" stroke-width="{h["corner"]}" stroke-linejoin="round"/>')
    tip = _bar(C - tw - h["corner"]/2, top - h["corner"]/2, C + tw + h["corner"]/2, tip_bottom, h["corner"]/2, tip_col)
    return body + tip

def minute_hand_svg(aod=False):
    m = HANDS["minute"]; b = m["w_base"] / 2; t = m["w_tip"] / 2
    top = C - m["len"]
    col = COLORS["aod_minute"] if aod else COLORS["minute"]
    return (f'<polygon points="{C-b},{C} {C-t},{top} {C+t},{top} {C+b},{C}" fill="{col}" '
            f'stroke="{col}" stroke-width="{m["corner"]}" stroke-linejoin="round"/>')

def second_hand_svg():
    s = HANDS["second"]
    # thin needle with a squared tip, a round hub that rings the cap, and a fat pill counterweight
    main = _bar(C - s["w"] / 2, C - s["len"], C + s["w"] / 2, C, 1, COLORS["second"])
    tail = (f'<line x1="{C}" y1="{C}" x2="{C}" y2="{C + s["tail_len"] - s["tail_w"] / 2}" '
            f'stroke="{COLORS["second"]}" stroke-width="{s["tail_w"]}" stroke-linecap="round"/>')
    hub = f'<circle cx="{C}" cy="{C}" r="{s["hub_r"]}" fill="{COLORS["second"]}"/>'
    return tail + main + hub

def cap_svg(aod=False):
    r = HANDS["cap_r"]; sw = HANDS["cap_stroke"]
    col = COLORS["aod_cap"] if aod else COLORS["cap"]
    # plain disc with a black outline so it separates from the yellow hub behind it
    return (f'<circle cx="{C}" cy="{C}" r="{r + sw}" fill="#000000"/>'
            f'<circle cx="{C}" cy="{C}" r="{r}" fill="{col}"/>')

def tight(body, w, h):
    """Re-frame a center-pivot drawing from the 800 canvas into a tight w x h canvas (pivot at its center)."""
    w = int(math.ceil(w)); h = int(math.ceil(h))
    if w % 2: w += 1
    if h % 2: h += 1
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<g transform="translate({w/2 - C},{h/2 - C})">{body}</g></svg>')

def write_png_wh(name, svg, w, h):
    sub = os.path.dirname(name)
    if sub: os.makedirs(os.path.join(OUT, sub), exist_ok=True)
    svg_path = os.path.join(OUT, name + ".svg"); png_path = os.path.join(OUT, name + ".png")
    open(svg_path, "w").write(svg)
    subprocess.run(["rsvg-convert", "-w", str(w), "-h", str(h), "-o", png_path, svg_path], check=True)
    os.remove(svg_path); return png_path

def _even(w, h):
    w = int(math.ceil(w)); h = int(math.ceil(h))
    return w + (w % 2), h + (h % 2)

def hand_canvas(kind):
    return _even(*_hand_canvas(kind))

def _hand_canvas(kind):
    pad = 4
    if kind == "hour":
        h = HANDS["hour"]; return h["w_base"] + pad, 2 * (h["len"] + pad)
    if kind == "minute":
        m = HANDS["minute"]; return m["w_base"] + pad, 2 * (m["len"] + pad)
    if kind == "second":
        s = HANDS["second"]; return max(s["w"], s["tail_w"], 2 * s["hub_r"]) + pad, 2 * (max(s["len"], s["tail_len"], s["hub_r"]) + pad)
    if kind == "cap":
        d = (HANDS["cap_r"] + HANDS["cap_stroke"]) * 2 + pad; return d, d

def battery_level_color(i):
    """Fill color by COROS state index: 0 charging, 1 empty, 2..11 = 10%..100%."""
    if i == 0: return ICON_COLORS["battery"]          # charging: green
    pct = (i - 1) * 10
    if pct >= 50: return ICON_COLORS["battery"]       # green
    if pct >= 30: return ICON_COLORS["calories"]      # orange
    return ICON_COLORS["heart_rate"]                  # red (10-20%)

def battery_frame_svg(i):
    """Battery state frame. The template's control-battery slot is 69x54 master px and the firmware
    stretches the image into it, so the canvas uses that aspect (138x108) and the gauge is drawn
    as large as possible inside it with a little breathing room."""
    outline = COLORS["label"]; fill = battery_level_color(i)
    W, H = 138, 108
    bx, by, bw, bh, r = 6, 24, 112, 60, 12          # body
    nub = f'<rect x="{bx+bw+4}" y="{by+bh/2-12}" width="12" height="24" rx="4" fill="{outline}"/>'
    body = f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="{r}" fill="none" stroke="{outline}" stroke-width="8"/>'
    ix, iy, iw, ih = bx + 10, by + 10, bw - 20, bh - 20   # inner fill box
    if i == 0:
        cx, cy = ix + iw / 2, iy + ih / 2
        inner = f'<path d="M{cx+4},{cy-18} L{cx-12},{cy+4} L{cx-1},{cy+4} L{cx-5},{cy+18} L{cx+12},{cy-4} L{cx+1},{cy-4} Z" fill="{fill}"/>'
    else:
        level = 0 if i == 1 else (i - 1) / 10
        w = iw * level
        inner = f'<rect x="{ix}" y="{iy}" width="{w:.1f}" height="{ih}" rx="5" fill="{fill}"/>' if w > 0 else ''
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{body}{nub}{inner}</svg>'

# ---------- icons (96 px source, placed at 64 px master) ----------
ICON_COL = COLORS["label"]
ICONS = {
    "heart_rate": '<path d="M48 84 C20 62 10 48 10 32 A18 18 0 0 1 48 24 A18 18 0 0 1 86 32 C86 48 76 62 48 84 Z" fill="{c}"/>',
    "battery": ('<rect x="8" y="28" width="70" height="40" rx="8" fill="none" stroke="{c}" stroke-width="7"/>'
                '<rect x="82" y="40" width="8" height="16" rx="2" fill="{c}"/>'
                '<rect x="18" y="38" width="36" height="20" rx="3" fill="{c}"/>'),
    "steps": ('<ellipse cx="34" cy="30" rx="13" ry="20" fill="{c}" transform="rotate(-12 34 30)"/>'
              '<rect x="22" y="52" width="22" height="13" rx="6" fill="{c}" transform="rotate(-12 33 58)"/>'
              '<ellipse cx="64" cy="52" rx="13" ry="20" fill="{c}" transform="rotate(-12 64 52)"/>'
              '<rect x="52" y="74" width="22" height="13" rx="6" fill="{c}" transform="rotate(-12 63 80)"/>'),
    "calories": ('<path d="M50 8 C52 30 70 36 70 58 A22 22 0 0 1 26 58 C26 46 34 40 36 32 C40 40 44 42 46 40 C42 30 44 18 50 8 Z" fill="{c}"/>'),
    "elevation": ('<path d="M6 82 L36 30 L52 56 L62 44 L92 82 Z" fill="{c}"/>'
                  ''),
}

def build():
    files = {}
    # Current mode
    files["current/background"] = write_png("current/background",
        svg_doc(ticks_svg() + numerals_svg(), bg=COLORS["bg"]))
    w,h = hand_canvas("hour"); files["current/hand_hour"] = write_png_wh("current/hand_hour", tight(hour_hand_svg(), w, h), w, h)
    w,h = hand_canvas("minute"); files["current/hand_minute"] = write_png_wh("current/hand_minute", tight(minute_hand_svg(), w, h), w, h)
    w,h = hand_canvas("second"); files["current/hand_second"] = write_png_wh("current/hand_second", tight(second_hand_svg(), w, h), w, h)
    w,h = hand_canvas("cap"); files["current/center_cap"] = write_png_wh("current/center_cap", tight(cap_svg(), w, h), w, h)
    # AOD mode
    files["aod/hour_ticks"] = write_png("aod/hour_ticks", svg_doc(ticks_svg(hour_only=True, aod=True)))
    # AOD dial: full tick ring + numerals on transparent, placed full-size via the arc_cut_icon overlay
    files["aod/dial_overlay"] = write_png("aod/dial_overlay", svg_doc(ticks_svg() + numerals_svg()))
    w,h = hand_canvas("hour"); files["aod/hand_hour"] = write_png_wh("aod/hand_hour", tight(hour_hand_svg(aod=True), w, h), w, h)
    w,h = hand_canvas("minute"); files["aod/hand_minute"] = write_png_wh("aod/hand_minute", tight(minute_hand_svg(aod=True), w, h), w, h)
    w,h = hand_canvas("cap"); files["aod/center_cap"] = write_png_wh("aod/center_cap", tight(cap_svg(aod=True), w, h), w, h)
    # AOD hub + cap in one image (no second hand in AOD, so the hub takes the minute hand's color)
    hub = HANDS["second"]["hub_r"]; r = HANDS["cap_r"]; sw = HANDS["cap_stroke"]; d = hub * 2 + 4
    files["aod/center_cap_hub"] = write_png_wh("aod/center_cap_hub", tight(
        f'<circle cx="{C}" cy="{C}" r="{hub}" fill="{COLORS["minute"]}"/>'
        f'<circle cx="{C}" cy="{C}" r="{r + sw}" fill="#000000"/>'
        f'<circle cx="{C}" cy="{C}" r="{r}" fill="{COLORS["cap"]}"/>', d, d), d, d)
    # Icons
    for name, body in ICONS.items():
        files[f"icons/{name}"] = write_png(f"icons/{name}", svg_doc(body.format(c=ICON_COLORS[name]), size=96), size=96)
    # battery state set in COROS order: 00 charging, 01 empty, 02..11 = 10%..100%  (120x68 source -> ~60x34 master)
    for i in range(12):
        files[f"battery/{i:02d}"] = write_png_wh(f"battery/{i:02d}", battery_frame_svg(i), 138, 108)
    # Preview composite (for a quick look)
    composite = (svg_doc(ticks_svg() + numerals_svg()
                 + f'<g transform="rotate(305 {C} {C})">{hour_hand_svg()}</g>'
                 + f'<g transform="rotate(60 {C} {C})">{minute_hand_svg()}</g>'
                 + f'<g transform="rotate(210 {C} {C})">{second_hand_svg()}</g>' + cap_svg(), bg=COLORS["bg"]))
    files["preview_composite"] = write_png("preview_composite", composite)
    with open(os.path.join(OUT, "spec.json"), "w") as f:
        json.dump({"master": MASTER, "colors": COLORS, "dial": DIAL, "hands": HANDS,
                   "widgets": WIDGETS, "selectable_order": SELECTABLE_ORDER}, f, indent=2)
    return files

if __name__ == "__main__":
    for k, v in build().items():
        print(k, "->", v)


# ---------- normalize icon mass: fit every icon's visible pixels into the same box on a 96x96 canvas ----------
# Per-icon fit boxes (w, h) inside the 96 px canvas, chosen for equal *visual mass*:
# compact shapes (heart) get a square box, narrow shapes (flame, footprints) more height,
# wide shapes (mountain, battery) more width.
ICON_BOXES = {
    "heart_rate": (78, 70),
    "steps": (64, 84),
    "calories": (60, 86),
    "elevation": (90, 62),
}
BATTERY_BOX = (94, 54)

def _fit(pth, box_w, box_h, canvas=96, anchor="center"):
    from PIL import Image
    im = Image.open(pth).convert("RGBA"); bbox = im.getbbox()
    if not bbox: return
    crop = im.crop(bbox); scale = min(box_w / crop.width, box_h / crop.height)
    new = crop.resize((max(1, round(crop.width * scale)), max(1, round(crop.height * scale))), Image.LANCZOS)
    out = Image.new("RGBA", (canvas, canvas), (0, 0, 0, 0))
    x = (canvas - new.width) // 2
    y = (canvas - new.height) // 2 if anchor == "center" else canvas - new.height
    out.alpha_composite(new, (x, y)); out.save(pth)

def normalize_icons():
    for name, (w, h) in ICON_BOXES.items():
        _fit(os.path.join(OUT, "icons", f"{name}.png"), w, h)
    # battery frames are drawn directly at the slot's aspect (see battery_frame_svg); no normalization

if __name__ == "__main__":
    normalize_icons()
