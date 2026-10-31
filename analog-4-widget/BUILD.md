# Building Analog 4-widget

How to rebuild the face in CorosLink Watch Face Studio. The values here come from the working PACE 4 Pro project. All positions are in the 800 x 800 master frame unless marked 466.

## Before you start

1. **Install the fonts:** install both files in `font/`, then restart CorosLink.
2. **Get the template:** start from POINTER (template ID 2609197). You need a copy that includes `AODconfig.txt`. As of October 2026, the package Studio downloads for this template had no working always-on setup, so this face was built from an earlier download of it. COROS's template files aren't in this repo.

## Current display

**Background:** `dial/dial_current.png` at 800 x 800, on #000000.

**Hands:** use native size and no tint.

| Slot | File |
|---|---|
| `time_hour_icon` | `hands/hour_hand.png` |
| `time_minute_icon` | `hands/minute_hand.png` |
| `time_second_icon` | `hands/second_hand.png` |
| `time_center_polygon_icon2` | `hands/center_cap.png` |

**Widgets:**

| Element | Center | Style |
|---|---|---|
| Weekday | 400, 188 | Barlow 600, size 30, #8C8C8C |
| Day of the month | 400, 236 | Barlow 500, size 56, #F2F2F2 |
| Low/high temperature | 580, 368 | Barlow 600, size 30, #8C8C8C |
| Current temperature | 580, 416 | Barlow 500, size 56, #F2F2F2 |
| Metric icon | 400, 548 | 34 x 34 PNG |
| Metric value | 400, 596 | Barlow 500, size 56, #F2F2F2 |
| Sunrise/sunset icon | 220, 368 | 34 x 34 PNG |
| Sunrise/sunset time | 220, 416 | Barlow 500, size 56, #F2F2F2 |

**Date styles:** weekday box 65 x 25, day box 31 x 46.

**Layout offsets:** weekday `dy -514`; day `dx -48, dy -411`; metric slot `dx -27, dy 483`.

**Native fields:**

| Field | x, y | Parts |
|---|---|---|
| `weather_temp` | 503, 381 | value 130 x 71, digit width 31, centered; unit and symbols width 22; unit text `°` |
| `weather_temp_min` | 534, 352 | value 34 x 37, digit width 17, left; unit 13; symbols 12; separator 12; separator text `/` |
| `weather_temp_max` | 580, 352 | value 34 x 37, digit width 17, left; unit 13; symbols 12 |
| `sunriseset` | 148, 381 | icon at 55, -30, 34 x 34; value 150 x 71, digit width 31, centered; symbols width 14; progress off |

**6 o'clock metric:** enable heart rate, steps, calories, battery and elevation only. Style: scale 1.09, Barlow 500, #F2F2F2.

| Metric | Icon | Icon offset |
|---|---|---|
| Heart rate | `icons/heart.png` | 100, -38 |
| Steps | `icons/steps.png` | 141, -38 |
| Calories | `icons/calories.png` | 141, -38 |
| Elevation | `icons/elevation.png` | 161, -38 |
| Battery | `icons/battery_69x54.png`, in all 12 states | 43, -48 |

**Hide:** month, arc cut, fixed metrics, weather icon, battery icons, and Bluetooth and Do Not Disturb indicators.

## Always-on display

**Background:** #000000 with the artwork hidden.

**Ticks:** put `dial/aod_ticks.png` in the `arc_cut_icon` slot at native size, and make `arcCut` visible in always-on. Don't use the background or a sprite: those show in Studio's preview, but a build with the ticks there didn't show them on the watch.

**Hands:** native size, with no second hand.

| Slot | File |
|---|---|
| `time_hour_icon` | `hands/hour_hand.png` |
| `time_minute_icon` | `hands/minute_hand.png` |
| `time_center_polygon_icon2` | `hands/aod_center_cap.png` |

**Date:** use the same layout offsets as Current, with raster fonts instead of live text. Live text rendered badly in always-on at 466 (TUE looked like `IUI`). The color is baked into the images, so turn tint off.

| Element | Images | Style box |
|---|---|---|
| Weekday | `aod_date/weekday/MON.png` to `SUN.png` | 72 x 21 |
| Day of the month | `aod_date/digits.png`, glyphs `0123456789` in 10 columns | 31 x 46 |

## Manual config edits

Studio can't set these, so edit the raw config files. These edits replaced the whole file text and removed its comment lines.

| File | Key | Value |
|---|---|---|
| 466 `config.txt` | `control_battery_level_rect` | `{67,0,140,32,hcenter\|vcenter}` |
| 800 `config.txt` | `control_battery_level_rect` | `{116,0,241,55,hcenter\|vcenter}` |
| 466 `config.txt`, `AODconfig.txt` | `english_date_day_rect` | `{238,361,285,392,hcenter\|vcenter}` |
| 466 `AODconfig.txt` | `arc_cut_icon_pos` | `{0,0}` |
| 466 `AODconfig.txt` | `arc_cut_icon` | `icon\aod_cut.png` |

Two more edits are needed in both `AODconfig.txt` files:

- **Date fields:** this template's always-on config has no date, and Studio's add-date settings only change `config.txt`. Fill in `*_date_day_rect`, `*_date_day_font`, `*_date_week_rect` and `*_date_week_font` for each language.
- **Tick slot at 466:** POINTER fills `arc_cut_icon` in its 800 config but leaves it blank at 466, which is the size the watch uses. Without the edit above, the ticks are missing at 466.

## Check the compiled build

After compiling, check these lines in `watchface_466x466/AODconfig.txt`:

```
[arc_cut_icon_pos]={0,0}
[arc_cut_icon]=studio\...\00.png
[english_date_day_rect]={216,124,252,151,hcenter|vcenter}
[english_date_week_rect]={212,104,254,116,hcenter|vcenter}
```

The `studio\` folder name changes between builds. Then render both displays at 466 x 466 and run validation.

Studio's preview doesn't prove what the watch will draw, so always check the always-on display on a real watch.

## Install

1. Open the **Send to COROS** window in Studio.
2. Set the watch face name to `Analog 4-widget`.
3. Choose your watch languages. This build uses English.
4. Check Current and Always-on at 466 x 466.
5. Send it using **Send to COROS** or the iPhone option, or **Send to watch** over Bluetooth, which the app marks as experimental.
