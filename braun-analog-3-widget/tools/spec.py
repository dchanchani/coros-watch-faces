"""Single source of truth for the Braun Analog 3-widget geometry.

All values are in CorosLink's master frame: 800 x 800 px, center (400, 400).
PACE 4 Pro renders at 466 x 466 (scale 0.5825).
"""

MASTER = 800
C = MASTER / 2
R = MASTER / 2

COLORS = {
    "bg": "#000000",
    "inner_ring": "#1c1c1c",  # unused (no inner ring on this face)
    "tick_minute": "#686e72",
    "tick_hour": "#f2f2f2",
    "numeral": "#686e72",
    "label": "#8c8c8c",
    "value": "#f2f2f2",
    "hour": "#d9341c",
    "hour_tip": "#8fd1d2",
    "minute": "#9c911c",   # olive-yellow, sampled from the reference (second hand is the bright one)
    "second": "#d2d156",
    "cap": "#9c911c",
    "cap_rim": "#8f6f2a",
    "cap_hilite": "#e6c879",
    # AOD: same colors as Current (the watch dims the panel itself)
    "aod_tick": "#f2f2f2",
    "aod_hour": "#d9341c",
    "aod_hour_tip": "#8fd1d2",
    "aod_minute": "#9c911c",
    "aod_cap": "#9c911c",
    "aod_cap_rim": "#3d3118",
    "aod_text": "#6a6f74",
}

DIAL = {
    "inner_ring_r": 290,
    "inner_ring_w": 2,
    "tick_outer_r": 392,
    "tick_minute_len": 24,
    "tick_minute_w": 3,
    "tick_hour_len": 32,
    "tick_hour_w": 5,
    "numeral_r": 318,
    "numeral_size": 54,
    "numeral_font": "Barlow",
    "numeral_weight": 500,
}

HANDS = {
    # Measured from the reference (R = dial radius): hour 0.59R long / 0.036R wide with a 0.10R tip,
    # minute 0.76R / 0.022R, second 0.96R / 0.013R with a 0.26R counterweight, hub 0.04R, cap 0.023R.
    "hour": {"len": 238, "w_base": 15, "w_tip": 14, "tip_len": 40, "corner": 3},
    "minute": {"len": 303, "w_base": 12, "w_tip": 10, "corner": 3},
    "second": {"len": 384, "w": 5, "tail_len": 100, "tail_w": 16, "hub_r": 17},
    "cap_r": 9,
    "cap_stroke": 2,  # black ring between cap and the second-hand hub (~1 px on the 466 display)
}

# Widget placement (centers) in master px
WIDGETS = {
    "font": "Barlow",
    "label": {"weight": 600, "size": 47, "color": "#8c8c8c"},
    "value": {"weight": 500, "size": 64, "color": "#f2f2f2"},
    # 12 o'clock: weekday (label) stacked over day (value), centered
    "date": {"x": 400, "y_weekday": 180, "y_day": 242},
    # 3 o'clock: min/max (label) stacked over current weather temp (value)
    "temp": {"x": 582, "y_minmax": 362, "y_cur": 422},
    # 6 o'clock: selectable metric icon (64 px) stacked over value
    "metric": {"x": 400, "y_icon": 534, "icon": 64, "y_value": 598},
}

SELECTABLE_ORDER = ["heart_rate", "battery", "steps", "calories", "elevation"]
ICON_COLORS = {
    "heart_rate": "#d9341c",   # red (hour-hand red)
    "battery": "#4ccf6a",      # green
    "steps": "#8c8c8c",        # grey
    "calories": "#f28c28",     # orange
    "elevation": "#4a9eff",    # blue
}

# 6 o'clock icon boxes (x, y, w, h) in master px, as exported by CorosLink (Studio build r62:
# rect_control1_pos + control_*_icon_pos, sprite size / 0.5825). Icons are bottom-aligned on one
# baseline above the value; the battery frame is stretched by the firmware into its 69x54 slot.
METRIC_ICON_BOXES = {
    "heart_rate": (369.1, 511.6, 63.5, 63.5),
    "battery": (365.7, 523.6, 68.7, 53.2),
    "steps": (367.4, 508.2, 63.5, 63.5),
    "calories": (367.4, 508.2, 63.5, 63.5),
    "elevation": (369.1, 516.7, 63.5, 63.5),
}
