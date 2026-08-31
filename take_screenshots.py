#!/usr/bin/env python3
"""Take screenshots of all themes with premium card shapes for README."""
import subprocess
import os
import tempfile
import shutil

BASE_HTML = "/home/dev1035/dev-1035/smit.softvan.com/screensaver/clock.html"
SCREENSHOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "screenshots")
ASSETS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

with open(BASE_HTML, "r") as f:
    base_html = f.read()

THEMES = [
    "glass_clock", "luxury_black_gold", "obsidian_titanium", "dark_emerald", "forest_green",
    "racing_green", "ruby_executive", "burgundy_prestige", "crimson_royal",
    "royal_sapphire", "midnight_navy", "arctic_ice", "ocean_cyan",
    "royal_purple", "amethyst_elite", "platinum_silver", "graphite_gray",
    "copper_elite", "rose_gold", "champagne_gold", "matte_black_diamond",
    "classic_retro", "minimal_light", "liquid_glass"
]

SHAPES = [
    "rectangle", "rounded_rectangle", "squircle", "octagon", "hexagon",
    "pentagon", "diamond", "shield", "capsule", "pill",
    "circle", "oval", "trapezoid", "parallelogram", "rhombus",
    "chamfered", "beveled", "notched", "cut_corner", "chevron",
    "badge", "ticket", "arch", "stadium", "lozenge",
    "frame", "panel", "card", "tile"
]

def make_temp_html(theme, shape):
    config_script = f"""<script>window.screensaverConfig = {{ theme: '{theme}', card_shape: '{shape}', format: '12', show_seconds: 'true', show_date: 'true', show_greeting: 'true', user_name: 'User', digit_font: 'Cinzel', label_font: 'Cinzel' }};</script>"""
    html = base_html.replace("</head>", f"{config_script}</head>")
    tmp = tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", dir="/home/dev1035/dev-1035/smit.softvan.com/screensaver")
    tmp.write(html)
    tmp.close()
    return tmp.name

def screenshot(html_path, outfile):
    cmd = [
        "google-chrome", "--headless", "--disable-gpu", "--no-sandbox",
        f"--screenshot={outfile}", "--window-size=1920,1080",
        "--hide-scrollbars", f"file://{html_path}"
    ]
    res = subprocess.run(cmd, capture_output=True, timeout=20)
    if not os.path.exists(outfile):
        print(f"❌ Failed to create {outfile}!")
        print("Stdout:", res.stdout.decode())
        print("Stderr:", res.stderr.decode())

# Theme screenshots (with soft_squircle shape)
for theme in THEMES:
    outfile = os.path.join(SCREENSHOT_DIR, f"theme_{theme}.png")
    tmp = make_temp_html(theme, "squircle")
    print(f"📸 Theme: {theme}...")
    screenshot(tmp, outfile)
    os.unlink(tmp)

# Card shape screenshots (with luxury_black_gold theme)
for shape in SHAPES:
    outfile = os.path.join(SCREENSHOT_DIR, f"shape_{shape}.png")
    tmp = make_temp_html("luxury_black_gold", shape)
    print(f"📸 Shape: {shape}...")
    screenshot(tmp, outfile)
    os.unlink(tmp)

# Settings window screenshot
print("📸 Settings window...")
subprocess.run(["bash", "-c", """
flipclock --settings &
PID=$!
sleep 3
import -window root /home/dev1035/dev-1035/smit.softvan.com/screensaver/screenshots/settings_window.png 2>/dev/null || true
kill $PID 2>/dev/null
"""], capture_output=True, timeout=15)

print("✅ All screenshots captured!")
