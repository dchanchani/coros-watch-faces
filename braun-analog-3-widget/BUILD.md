# Building Braun Analog 3-widget

How to rebuild the face in CorosLink Watch Face Studio. The values here come from the working PACE 4 Pro project (Studio revision 62). All positions are in the 800 x 800 master frame unless marked 466.

## Before you start

1. **Install the fonts:** install both files in `font/`, then restart CorosLink.
2. **Start from Analog 4-widget:** this face was made by duplicating [Analog 4-widget](../analog-4-widget/BUILD.md), which supplies the template, the working always-on setup and the manual config edits. Build that face first (or open your copy), then duplicate it in Studio and apply the changes below.

## Current display

**Background:** `dial/dial_current.png` as the artwork at 800 x 800, on #000000.

**Hands:** native size, no tint.

| Slot | File | Size |
|---|---|---|
| `time_hour_icon` | `hands/hour_hand.png` | 20 x 484 |
| `time_minute_icon` | `hands/minute_hand.png` | 16 x 614 |
| `time_second_icon` | `hands/second_hand.png` | 38 x 776 |
| `time_center_polygon_icon2` | `hands/center_cap.png` | 26 x 26 |

**Remove the sunrise/sunset field** from Analog 4-widget, and keep sunrise and sunset off in the 6 o'clock metric.

**Date styles:**

| Element | Style | Box |
|---|---|---|
| Weekday | Barlow 600, size 49, #8C8C8C, uppercase | 112 x 42 |
| Day of the month | Raster font from `digits/`: glyphs `0123456789`, tint on, size 64, #F2F2F2 | 33 x 48 |

**Layout offsets:** weekday `dy -520`; day `dx -49, dy -402`; metric slot `dx -27, dy 487`.

**Native fields:**

| Field | x, y | Style | Parts |
|---|---|---|---|
| `weather_temp` | 496, 386 | Barlow 400, #F2F2F2 | value 148 x 81, digit width 35, centered; unit and symbols 25 x 81; unit text `°` |
| `weather_temp_min` | 508, 338 | Barlow 600, #8C8C8C | value 54 x 58, digit width 27, left; unit 20; symbols 19; separator 19, text `/` |
| `weather_temp_max` | 580, 352 | Barlow 600, #8C8C8C | value 54 x 58, digit width 27, left; unit 20; symbols 19 |

The current temperature is set to weight 400 on purpose. On the Mac this was built on, Studio drew its native text about one weight heavier than asked, and 400 gave the Medium look the design calls for. If your temperature looks lighter than the day digits, set it to 500.

**6 o'clock metric:** enable heart rate, battery, steps, calories and elevation only, with heart rate as the preview default. Value style: raster font from `digits/` (tint on), #F2F2F2, scale 0.94, letter spacing −4. The digit images avoid the same heavy-weight problem, and −4 is the tightest spacing that still leaves a gap between two 4s.

| Metric | Icon | Size | Icon offset |
|---|---|---|---|
| Heart rate | `icons/heart.png` | 64 x 64 | 86, -62 |
| Steps | `icons/steps.png` | 64 x 64 | 127, -66 |
| Calories | `icons/calories.png` | 64 x 64 | 127, -66 |
| Elevation | `icons/elevation.png` | 64 x 64 | 147, -56 |
| Battery | `icons/battery/00.png` to `11.png`, one per state | 69 x 54 | 43, -50 |

The icons are drawn so their bottoms sit on one line, 7 px (466) above the digits. The battery states follow COROS's order: `00` charging, `01` empty, `02`–`11` = 10–100%. The watch stretches battery images into the 69 x 54 slot, which is why they're drawn at that shape.

**Hide:** month, arc cut, weather icon, and the Bluetooth and Do Not Disturb indicators.

## Always-on display

**Background:** #000000 with the artwork hidden.

**Dial:** put `dial/dial_aod.png` in the `arc_cut_icon` slot at native size (800 x 800), and make `arcCut` visible in always-on.

**Hands:** native size, no second hand.

| Slot | File | Size |
|---|---|---|
| `time_hour_icon` | `hands/hour_hand.png` | 20 x 484 |
| `time_minute_icon` | `hands/minute_hand.png` | 16 x 614 |
| `time_center_polygon_icon2` | `hands/aod_center_cap.png` | 38 x 38 |

**Date:** the same styles as Current. Use weekday `dy -518` (2 px below Current's: the always-on build otherwise lands 1 px higher) and day `dx -49, dy -402`.

## Check the compiled build

After compiling, these lines in `watchface_466x466/config.txt` should match:

```
[english_date_week_rect]={201,95,266,119,hcenter|vcenter}
[english_date_day_rect]={214,129,252,157,hcenter|vcenter}
[weather_temp_rect]={289,225,375,272,hcenter|vcenter}
[weather_temp_min_rect]={296,197,327,231,left|vcenter}
[rect_control1_pos]={129,296}
[control_hr_icon_pos]={86,2}
[control_hr_rect]={75,40,132,68,hcenter|vcenter}
```

And in `watchface_466x466/AODconfig.txt`:

```
[arc_cut_icon_pos]={0,0}
[arc_cut_icon]=studio\...\00.png
[english_date_week_rect]={201,95,266,119,hcenter|vcenter}
[english_date_day_rect]={214,129,252,157,hcenter|vcenter}
```

The `studio\` folder name changes between builds. Then render both displays at 466 x 466 and run validation. Studio's preview doesn't prove what the watch will draw, so check both displays on a real watch.

## Rebuilding the art

Everything except the digits is generated from `tools/spec.py`. You need Python 3 with Pillow, `rsvg-convert` (librsvg), and Barlow installed for fontconfig. Without Barlow, rsvg quietly substitutes another font, so the script refuses to run.

```
cd tools
python3 gen_assets.py
```

It writes to `tools/out/`:

| Output | Repo file |
|---|---|
| `current/background.png` | `dial/dial_current.png` |
| `aod/dial_overlay.png` | `dial/dial_aod.png` |
| `current/hand_hour.png`, `hand_minute.png`, `hand_second.png`, `center_cap.png` | `hands/hour_hand.png`, `minute_hand.png`, `second_hand.png`, `center_cap.png` |
| `aod/center_cap_hub.png` | `hands/aod_center_cap.png` |
| `icons/heart_rate.png`, `steps.png`, `calories.png`, `elevation.png` | `icons/heart.png`, `steps.png`, `calories.png`, `elevation.png` |
| `battery/00.png` to `11.png` | `icons/battery/00.png` to `11.png` |

The script also writes a few files this face doesn't use: always-on copies of the hands and cap, an hour-ticks-only dial, a static battery icon, a preview composite and `spec.json`.

## Install

1. Open the **Send to COROS** window in Studio.
2. Set the watch face name to `Braun Analog 3-widget`.
3. Choose your watch languages. This build uses English.
4. Check Current and Always-on at 466 x 466.
5. Send it with **Install on watch** over Bluetooth, or the iPhone option. The QR share link signs your phone out of the COROS app, because COROS allows one mobile session per account.
