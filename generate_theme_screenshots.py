#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

THEMES = {
    "glass_clock": {
        "title": "✨ Glass Clock (Frosted)",
        "bg_color": (10, 15, 25, 255),
        "card_top": (255, 255, 255, 25),
        "card_bot": (255, 255, 255, 15),
        "border_color": (255, 255, 255, 60),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (56, 189, 248, 255),
        "accent_color": (56, 189, 248, 255),
        "badge_bg": (15, 23, 42, 160),
        "badge_border": (255, 255, 255, 40),
        "greeting": "GOOD EVENING"
    },
    "glass_aurora": {
        "title": "🌌 Aurora Glass",
        "bg_color": (4, 13, 26, 255),
        "card_top": (255, 255, 255, 30),
        "card_bot": (255, 255, 255, 12),
        "border_color": (56, 189, 248, 180),
        "digit_color": (224, 242, 254, 255),
        "pin_color": (56, 189, 248, 255),
        "accent_color": (168, 85, 247, 255),
        "badge_bg": (15, 23, 42, 180),
        "badge_border": (56, 189, 248, 140),
        "greeting": "GOOD EVENING"
    },
    "glass_cyberpunk": {
        "title": "🌆 Cyberpunk Neon",
        "bg_color": (10, 5, 18, 255),
        "card_top": (236, 72, 153, 35),
        "card_bot": (139, 92, 246, 20),
        "border_color": (236, 72, 153, 180),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (236, 72, 153, 255),
        "accent_color": (236, 72, 153, 255),
        "badge_bg": (24, 12, 38, 200),
        "badge_border": (236, 72, 153, 140),
        "greeting": "GOOD EVENING"
    },
    "glass_emerald": {
        "title": "🌿 Emerald Gold",
        "bg_color": (5, 20, 13, 255),
        "card_top": (16, 185, 129, 30),
        "card_bot": (6, 78, 54, 20),
        "border_color": (212, 175, 55, 180),
        "digit_color": (245, 245, 247, 255),
        "pin_color": (212, 175, 55, 255),
        "accent_color": (212, 175, 55, 255),
        "badge_bg": (8, 32, 21, 200),
        "badge_border": (212, 175, 55, 140),
        "greeting": "GOOD EVENING"
    },
    "glass_sunset": {
        "title": "🌇 Sunset Champagne",
        "bg_color": (19, 9, 20, 255),
        "card_top": (251, 146, 60, 30),
        "card_bot": (236, 72, 153, 18),
        "border_color": (253, 230, 138, 180),
        "digit_color": (253, 230, 138, 255),
        "pin_color": (253, 230, 138, 255),
        "accent_color": (253, 230, 138, 255),
        "badge_bg": (30, 14, 32, 200),
        "badge_border": (253, 230, 138, 140),
        "greeting": "GOOD EVENING"
    },
    "glass_minimal_oled": {
        "title": "🧊 OLED Pure Frameless",
        "bg_color": (0, 0, 0, 255),
        "card_top": (0, 0, 0, 0),
        "card_bot": (0, 0, 0, 0),
        "border_color": (0, 0, 0, 0),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (255, 255, 255, 255),
        "accent_color": (255, 255, 255, 255),
        "badge_bg": (15, 15, 15, 200),
        "badge_border": (50, 50, 50, 140),
        "greeting": "GOOD EVENING"
    },
    "glass_spiderman": {
        "title": "🕷️ Spider-Man Web",
        "bg_color": (24, 3, 8, 255),
        "card_top": (220, 38, 38, 35),
        "card_bot": (37, 99, 235, 20),
        "border_color": (239, 68, 68, 180),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (239, 68, 68, 255),
        "accent_color": (239, 68, 68, 255),
        "badge_bg": (32, 6, 12, 200),
        "badge_border": (239, 68, 68, 140),
        "greeting": "GOOD EVENING"
    },
    "glass_ganesha": {
        "title": "🐘 Ganesha Divine Gold",
        "bg_color": (26, 12, 2, 255),
        "card_top": (245, 158, 11, 35),
        "card_bot": (234, 88, 12, 20),
        "border_color": (245, 158, 11, 180),
        "digit_color": (254, 243, 199, 255),
        "pin_color": (234, 88, 12, 255),
        "accent_color": (234, 88, 12, 255),
        "badge_bg": (40, 18, 4, 200),
        "badge_border": (245, 158, 11, 140),
        "greeting": "GOOD EVENING"
    },
    "glass_anime_hydrangea": {
        "title": "🌸 Anime Girl Hydrangea Garden",
        "bg_color": (13, 7, 20, 255),
        "card_top": (192, 132, 252, 0),
        "card_bot": (168, 85, 247, 0),
        "border_color": (192, 132, 252, 0),
        "digit_color": (248, 245, 255, 255),
        "pin_color": (192, 132, 252, 255),
        "accent_color": (192, 132, 252, 255),
        "badge_bg": (25, 12, 40, 200),
        "badge_border": (192, 132, 252, 140),
        "greeting": "GOOD EVENING"
    },
    "glass_misty_pavilion": {
        "title": "🏮 Misty Lakeside Pavilion",
        "bg_color": (6, 11, 18, 255),
        "card_top": (245, 158, 11, 0),
        "card_bot": (217, 119, 6, 0),
        "border_color": (245, 158, 11, 0),
        "digit_color": (254, 243, 199, 255),
        "pin_color": (245, 158, 11, 255),
        "accent_color": (245, 158, 11, 255),
        "badge_bg": (12, 22, 35, 200),
        "badge_border": (245, 158, 11, 140),
        "greeting": "GOOD EVENING"
    },
    "liquid_glass": {
        "title": "💧 Liquid Glass Dark",
        "bg_color": (6, 8, 16, 255),
        "card_top": (25, 40, 70, 255),
        "card_bot": (15, 23, 42, 255),
        "border_color": (56, 189, 248, 200),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (56, 189, 248, 255),
        "accent_color": (56, 189, 248, 255),
        "badge_bg": (15, 23, 42, 220),
        "badge_border": (56, 189, 248, 140),
        "greeting": "GOOD MORNING"
    },
    "luxury_black_gold": {
        "title": "🥇 Luxury Black Gold",
        "bg_color": (0, 0, 0, 255),
        "card_top": (28, 28, 30, 255),
        "card_bot": (14, 14, 16, 255),
        "border_color": (74, 74, 74, 180),
        "digit_color": (245, 245, 247, 255),
        "pin_color": (212, 175, 55, 255),
        "accent_color": (212, 175, 55, 255),
        "badge_bg": (28, 28, 30, 220),
        "badge_border": (212, 175, 55, 120),
        "greeting": "GOOD MORNING"
    },
    "obsidian_titanium": {
        "title": "🥈 Obsidian Titanium",
        "bg_color": (5, 5, 5, 255),
        "card_top": (31, 31, 31, 255),
        "card_bot": (18, 18, 18, 255),
        "border_color": (80, 84, 90, 180),
        "digit_color": (248, 248, 248, 255),
        "pin_color": (174, 181, 189, 255),
        "accent_color": (174, 181, 189, 255),
        "badge_bg": (31, 31, 31, 220),
        "badge_border": (174, 181, 189, 120),
        "greeting": "GOOD AFTERNOON"
    },
    "dark_emerald": {
        "title": "🥉 Dark Emerald",
        "bg_color": (7, 18, 12, 255),
        "card_top": (18, 33, 24, 255),
        "card_bot": (10, 20, 14, 255),
        "border_color": (54, 85, 65, 180),
        "digit_color": (247, 250, 247, 255),
        "pin_color": (0, 200, 83, 255),
        "accent_color": (0, 200, 83, 255),
        "badge_bg": (18, 33, 24, 220),
        "badge_border": (0, 200, 83, 120),
        "greeting": "GOOD EVENING"
    },
    "forest_green": {
        "title": "🌲 Forest Green",
        "bg_color": (8, 17, 10, 255),
        "card_top": (24, 38, 29, 255),
        "card_bot": (14, 22, 17, 255),
        "border_color": (72, 102, 81, 180),
        "digit_color": (244, 248, 244, 255),
        "pin_color": (76, 175, 80, 255),
        "accent_color": (76, 175, 80, 255),
        "badge_bg": (24, 38, 29, 220),
        "badge_border": (76, 175, 80, 120),
        "greeting": "GOOD NIGHT"
    },
    "racing_green": {
        "title": "🏎️ British Racing Green",
        "bg_color": (6, 17, 10, 255),
        "card_top": (14, 32, 23, 255),
        "card_bot": (8, 18, 13, 255),
        "border_color": (53, 86, 73, 180),
        "digit_color": (250, 250, 246, 255),
        "pin_color": (11, 143, 87, 255),
        "accent_color": (11, 143, 87, 255),
        "badge_bg": (14, 32, 23, 220),
        "badge_border": (11, 143, 87, 120),
        "greeting": "GOOD MORNING"
    },
    "ruby_executive": {
        "title": "💎 Ruby Executive",
        "bg_color": (9, 6, 6, 255),
        "card_top": (34, 21, 21, 255),
        "card_bot": (18, 11, 11, 255),
        "border_color": (91, 58, 58, 180),
        "digit_color": (250, 250, 250, 255),
        "pin_color": (211, 47, 47, 255),
        "accent_color": (211, 47, 47, 255),
        "badge_bg": (34, 21, 21, 220),
        "badge_border": (211, 47, 47, 120),
        "greeting": "GOOD AFTERNOON"
    },
    "burgundy_prestige": {
        "title": "🍷 Burgundy Prestige",
        "bg_color": (18, 8, 8, 255),
        "card_top": (42, 22, 22, 255),
        "card_bot": (22, 11, 11, 255),
        "border_color": (99, 69, 69, 180),
        "digit_color": (255, 249, 248, 255),
        "pin_color": (142, 36, 48, 255),
        "accent_color": (142, 36, 48, 255),
        "badge_bg": (42, 22, 22, 220),
        "badge_border": (142, 36, 48, 120),
        "greeting": "GOOD EVENING"
    },
    "crimson_royal": {
        "title": "🏎️ Crimson Royal",
        "bg_color": (10, 5, 5, 255),
        "card_top": (35, 19, 19, 255),
        "card_bot": (18, 9, 9, 255),
        "border_color": (96, 64, 64, 180),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (198, 40, 40, 255),
        "accent_color": (198, 40, 40, 255),
        "badge_bg": (35, 19, 19, 220),
        "badge_border": (198, 40, 40, 120),
        "greeting": "GOOD NIGHT"
    },
    "royal_sapphire": {
        "title": "🚙 Royal Sapphire",
        "bg_color": (3, 8, 22, 255),
        "card_top": (22, 32, 51, 255),
        "card_bot": (12, 18, 30, 255),
        "border_color": (54, 82, 122, 180),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (46, 125, 255, 255),
        "accent_color": (46, 125, 255, 255),
        "badge_bg": (22, 32, 51, 220),
        "badge_border": (46, 125, 255, 120),
        "greeting": "GOOD MORNING"
    },
    "midnight_navy": {
        "title": "⚓ Midnight Navy",
        "bg_color": (5, 11, 22, 255),
        "card_top": (24, 35, 54, 255),
        "card_bot": (14, 20, 32, 255),
        "border_color": (78, 101, 137, 180),
        "digit_color": (250, 250, 250, 255),
        "pin_color": (79, 139, 255, 255),
        "accent_color": (79, 139, 255, 255),
        "badge_bg": (24, 35, 54, 220),
        "badge_border": (79, 139, 255, 120),
        "greeting": "GOOD AFTERNOON"
    },
    "arctic_ice": {
        "title": "❄️ Arctic Ice",
        "bg_color": (5, 8, 10, 255),
        "card_top": (23, 33, 38, 255),
        "card_bot": (13, 19, 22, 255),
        "border_color": (75, 109, 119, 180),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (56, 217, 255, 255),
        "accent_color": (56, 217, 255, 255),
        "badge_bg": (23, 33, 38, 220),
        "badge_border": (56, 217, 255, 120),
        "greeting": "GOOD EVENING"
    },
    "ocean_cyan": {
        "title": "🌊 Ocean Cyan",
        "bg_color": (7, 17, 22, 255),
        "card_top": (23, 43, 51, 255),
        "card_bot": (13, 24, 29, 255),
        "border_color": (71, 99, 107, 180),
        "digit_color": (246, 255, 255, 255),
        "pin_color": (0, 188, 212, 255),
        "accent_color": (0, 188, 212, 255),
        "badge_bg": (23, 43, 51, 220),
        "badge_border": (0, 188, 212, 120),
        "greeting": "GOOD NIGHT"
    },
    "royal_purple": {
        "title": "👑 Royal Purple",
        "bg_color": (8, 4, 13, 255),
        "card_top": (31, 25, 48, 255),
        "card_bot": (16, 13, 25, 255),
        "border_color": (80, 65, 110, 180),
        "digit_color": (250, 250, 250, 255),
        "pin_color": (142, 68, 255, 255),
        "accent_color": (142, 68, 255, 255),
        "badge_bg": (31, 25, 48, 220),
        "badge_border": (142, 68, 255, 120),
        "greeting": "GOOD EVENING"
    },
    "amethyst_elite": {
        "title": "🔮 Amethyst Elite",
        "bg_color": (12, 7, 18, 255),
        "card_top": (36, 26, 46, 255),
        "card_bot": (20, 14, 26, 255),
        "border_color": (93, 81, 116, 180),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (162, 89, 255, 255),
        "accent_color": (162, 89, 255, 255),
        "badge_bg": (36, 26, 46, 220),
        "badge_border": (162, 89, 255, 120),
        "greeting": "GOOD NIGHT"
    },
    "platinum_silver": {
        "title": "🪙 Platinum Silver",
        "bg_color": (16, 16, 16, 255),
        "card_top": (38, 38, 38, 255),
        "card_bot": (22, 22, 22, 255),
        "border_color": (90, 90, 90, 180),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (199, 204, 212, 255),
        "accent_color": (199, 204, 212, 255),
        "badge_bg": (38, 38, 38, 220),
        "badge_border": (199, 204, 212, 120),
        "greeting": "GOOD MORNING"
    },
    "graphite_gray": {
        "title": "⚙️ Graphite Gray",
        "bg_color": (17, 17, 17, 255),
        "card_top": (42, 42, 42, 255),
        "card_bot": (24, 24, 24, 255),
        "border_color": (85, 85, 85, 180),
        "digit_color": (245, 245, 245, 255),
        "pin_color": (158, 158, 158, 255),
        "accent_color": (158, 158, 158, 255),
        "badge_bg": (42, 42, 42, 220),
        "badge_border": (158, 158, 158, 120),
        "greeting": "GOOD AFTERNOON"
    },
    "copper_elite": {
        "title": "🧱 Copper Elite",
        "bg_color": (9, 9, 9, 255),
        "card_top": (32, 26, 24, 255),
        "card_bot": (18, 14, 13, 255),
        "border_color": (92, 69, 55, 180),
        "digit_color": (255, 248, 242, 255),
        "pin_color": (184, 115, 51, 255),
        "accent_color": (184, 115, 51, 255),
        "badge_bg": (32, 26, 24, 220),
        "badge_border": (184, 115, 51, 120),
        "greeting": "GOOD EVENING"
    },
    "rose_gold": {
        "title": "🌹 Rose Gold",
        "bg_color": (10, 9, 9, 255),
        "card_top": (36, 28, 27, 255),
        "card_bot": (20, 15, 14, 255),
        "border_color": (106, 80, 74, 180),
        "digit_color": (255, 248, 246, 255),
        "pin_color": (232, 168, 124, 255),
        "accent_color": (232, 168, 124, 255),
        "badge_bg": (36, 28, 27, 220),
        "badge_border": (232, 168, 124, 120),
        "greeting": "GOOD NIGHT"
    },
    "champagne_gold": {
        "title": "🥂 Champagne Gold",
        "bg_color": (11, 10, 8, 255),
        "card_top": (36, 34, 29, 255),
        "card_bot": (20, 19, 16, 255),
        "border_color": (109, 102, 85, 180),
        "digit_color": (255, 253, 247, 255),
        "pin_color": (229, 192, 123, 255),
        "accent_color": (229, 192, 123, 255),
        "badge_bg": (36, 34, 29, 220),
        "badge_border": (229, 192, 123, 120),
        "greeting": "GOOD MORNING"
    },
    "matte_black_diamond": {
        "title": "✨ Matte Black Diamond",
        "bg_color": (1, 1, 1, 255),
        "card_top": (24, 24, 24, 255),
        "card_bot": (14, 14, 14, 255),
        "border_color": (58, 58, 58, 180),
        "digit_color": (252, 252, 252, 255),
        "pin_color": (240, 240, 240, 255),
        "accent_color": (240, 240, 240, 255),
        "badge_bg": (24, 24, 24, 220),
        "badge_border": (240, 240, 240, 120),
        "greeting": "GOOD NIGHT"
    },
    "classic_retro": {
        "title": "📜 Classic Retro",
        "bg_color": (10, 10, 12, 255),
        "card_top": (28, 28, 30, 255),
        "card_bot": (14, 14, 16, 255),
        "border_color": (74, 74, 74, 180),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (163, 163, 163, 255),
        "accent_color": (229, 229, 229, 255),
        "badge_bg": (26, 26, 26, 220),
        "badge_border": (255, 255, 255, 120),
        "greeting": "GOOD MORNING"
    },
    "minimal_light": {
        "title": "☀️ Minimalist Light",
        "bg_color": (241, 245, 249, 255),
        "card_top": (255, 255, 255, 255),
        "card_bot": (248, 250, 252, 255),
        "border_color": (148, 163, 184, 180),
        "digit_color": (15, 23, 42, 255),
        "pin_color": (71, 85, 105, 255),
        "accent_color": (30, 41, 59, 255),
        "badge_bg": (255, 255, 255, 230),
        "badge_border": (148, 163, 184, 120),
        "greeting": "GOOD MORNING"
    }
}

def render_theme_screenshot(theme_key, theme_info, output_dir="assets"):
    os.makedirs(output_dir, exist_ok=True)
    scale = 2
    w, h = 640 * scale, 380 * scale
    img = Image.new("RGBA", (w, h), theme_info["bg_color"])
    bg_img_map = {
        "glass_spiderman": "assets/spiderman_bg.png",
        "glass_ganesha": "assets/ganesha_murti_bg.png",
        "glass_anime_hydrangea": "assets/anime_hydrangea_bg.png",
        "glass_misty_pavilion": "assets/misty_pavilion_bg.png"
    }
    if theme_key in bg_img_map and os.path.exists(bg_img_map[theme_key]):
        try:
            bg_art = Image.open(bg_img_map[theme_key]).convert("RGBA")
            bg_art = bg_art.resize((w, h), Image.Resampling.LANCZOS)
            darkener = Image.new("RGBA", (w, h), (0, 0, 0, 90))
            bg_art = Image.alpha_composite(bg_art, darkener)
            img.paste(bg_art, (0, 0))
        except Exception:
            pass
    draw = ImageDraw.Draw(img)

    # 1. Fonts
    font_bold = None
    font_cinzel = None
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
    ]
    for fp in font_paths:
        try:
            font_bold = ImageFont.truetype(fp, int(82 * scale))
            font_cinzel = ImageFont.truetype(fp, int(18 * scale))
            break
        except Exception:
            pass

    if font_bold is None:
        font_bold = ImageFont.load_default()
        font_cinzel = ImageFont.load_default()

    # 2. Greeting Badge Text
    greeting_text = theme_info["greeting"]
    gb = draw.textbbox((0, 0), greeting_text, font=font_cinzel)
    gw = gb[2] - gb[0]
    draw.text(((w - gw) // 2, int(22 * scale)), greeting_text, font=font_cinzel, fill=theme_info["accent_color"])

    if theme_key in ["glass_misty_pavilion", "glass_anime_hydrangea"]:
        # Draw aesthetic glass clock layout matching user's reference images
        font_large = None
        font_sub = None
        font_paths = [
            "/usr/share/fonts/truetype/ubuntu/Ubuntu-Light.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans-ExtraLight.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        ]
        for fp in font_paths:
            try:
                font_large = ImageFont.truetype(fp, int(85 * scale))
                font_sub = ImageFont.truetype(fp, int(14 * scale))
                break
            except Exception:
                pass
        if font_large is None:
            font_large = font_bold
            font_sub = font_cinzel

        time_str = "11:47"
        sec_str = ":36"
        ampm_str = "AM"
        day_str = "T U E S D A Y"
        date_str = "02  SEPTEMBER  2026"
        week_str = "📅 ── WEEK 36 ──"

        tb = draw.textbbox((0, 0), time_str, font=font_large)
        tw = tb[2] - tb[0]
        th = tb[3] - tb[1]



        if theme_key == "glass_anime_hydrangea":
            # Left-aligned frameless 3D glass clock
            clock_x = int(50 * scale)
            clock_y = int(85 * scale)

            draw.text((clock_x, clock_y), time_str, font=font_large, fill=(255, 255, 255, 255))
            draw.text((clock_x + tw + int(8 * scale), clock_y + int(28 * scale)), sec_str, font=font_sub, fill=(186, 230, 253, 230))
            draw.text((clock_x + tw + int(50 * scale), clock_y + int(45 * scale)), ampm_str, font=font_sub, fill=(186, 230, 253, 230))

            # Day divider line
            line_y = clock_y + th + int(30 * scale)
            db = draw.textbbox((0, 0), day_str, font=font_sub)
            dw = db[2] - db[0]
            day_x = clock_x + (tw - dw) // 2

            line_len = int(80 * scale)
            draw.line([(day_x - line_len - int(12 * scale), line_y), (day_x - int(12 * scale), line_y)], fill=(224, 242, 254, 150), width=int(1.2 * scale))
            draw.text((day_x, line_y - int(8 * scale)), day_str, font=font_sub, fill=(224, 242, 254, 240))
            draw.line([(day_x + dw + int(12 * scale), line_y), (day_x + dw + line_len + int(12 * scale), line_y)], fill=(224, 242, 254, 150), width=int(1.2 * scale))

            # Date text
            dtb = draw.textbbox((0, 0), date_str, font=font_sub)
            dtw = dtb[2] - dtb[0]
            date_x = clock_x + (tw - dtw) // 2
            date_y = line_y + int(22 * scale)
            draw.text((date_x, date_y), date_str, font=font_sub, fill=(224, 242, 254, 200))

        else:
            # Frameless right-aligned for Misty Pavilion matching Image 2
            right_margin = int(48 * scale)
            clock_x = w - right_margin - tw - int(50 * scale)
            clock_y = int(85 * scale)

            draw.text((clock_x, clock_y), time_str, font=font_large, fill=(224, 242, 254, 255))
            draw.text((clock_x + tw + int(10 * scale), clock_y + int(45 * scale)), ampm_str, font=font_sub, fill=(186, 230, 253, 230))

            # Day divider line
            line_y = clock_y + th + int(35 * scale)
            db = draw.textbbox((0, 0), day_str, font=font_sub)
            dw = db[2] - db[0]
            day_x = clock_x + (tw - dw) // 2

            line_len = int(120 * scale)
            draw.line([(day_x - line_len - int(15 * scale), line_y), (day_x - int(15 * scale), line_y)], fill=(224, 242, 254, 160), width=int(1.5 * scale))
            draw.text((day_x, line_y - int(8 * scale)), day_str, font=font_sub, fill=(224, 242, 254, 240))
            draw.line([(day_x + dw + int(15 * scale), line_y), (day_x + dw + line_len + int(15 * scale), line_y)], fill=(224, 242, 254, 160), width=int(1.5 * scale))

            # Date text line
            dtb = draw.textbbox((0, 0), date_str, font=font_sub)
            dtw = dtb[2] - dtb[0]
            date_x = clock_x + (tw - dtw) // 2
            date_y = line_y + int(24 * scale)
            draw.text((date_x, date_y), date_str, font=font_sub, fill=(224, 242, 254, 200))

    else:
        # 3. Flip Cards ("10" : "45")
        card_w = int(170 * scale)
        card_h = int(220 * scale)
        card_y = int(60 * scale)
        gap = int(24 * scale)
        card_r = int(14 * scale)

        cards_total_w = card_w * 2 + gap + int(30 * scale)
        start_x = (w - cards_total_w) // 2

        # Helper function to draw card
        def draw_card(cx, text_val):
            c_box = [cx, card_y, cx + card_w, card_y + card_h]
            half_y = (c_box[1] + c_box[3]) // 2

            # Card image mask
            c_img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
            c_draw = ImageDraw.Draw(c_img)

            # Top half
            c_draw.rectangle([c_box[0], c_box[1], c_box[2], half_y], fill=theme_info["card_top"])
            # Bottom half
            c_draw.rectangle([c_box[0], half_y, c_box[2], c_box[3]], fill=theme_info["card_bot"])

            mask = Image.new("L", (w, h), 0)
            m_draw = ImageDraw.Draw(mask)
            m_draw.rounded_rectangle(c_box, radius=card_r, fill=255)

            img.paste(c_img, (0, 0), mask)

            # Card outline
            draw.rounded_rectangle(c_box, radius=card_r, outline=theme_info["border_color"], width=int(2 * scale))

            # Split divider line
            div_h = int(3 * scale)
            draw.rectangle([c_box[0], half_y - div_h // 2, c_box[2], half_y + div_h // 2], fill=(0, 0, 0, 240))

            # Side pins
            pin_w = int(6 * scale)
            pin_h = int(12 * scale)
            pin_r = int(2 * scale)
            draw.rounded_rectangle([c_box[0] + int(6 * scale), half_y - pin_h // 2, c_box[0] + int(6 * scale) + pin_w, half_y + pin_h // 2], radius=pin_r, fill=theme_info["pin_color"])
            draw.rounded_rectangle([c_box[2] - int(6 * scale) - pin_w, half_y - pin_h // 2, c_box[2] - int(6 * scale), half_y + pin_h // 2], radius=pin_r, fill=theme_info["pin_color"])

            # Digit text
            tb = draw.textbbox((0, 0), text_val, font=font_bold)
            tw = tb[2] - tb[0]
            th = tb[3] - tb[1]
            tx = cx + (card_w - tw) // 2 - tb[0]
            ty = card_y + (card_h - th) // 2 - tb[1]
            draw.text((tx, ty), text_val, font=font_bold, fill=theme_info["digit_color"])

        # Draw Hours ("10") & Minutes ("45")
        draw_card(start_x, "10")

        # Separator Dots
        sep_x = start_x + card_w + int(15 * scale)
        dot_r = int(5 * scale)
        dot_y1 = card_y + card_h // 3
        dot_y2 = card_y + (card_h * 2) // 3
        draw.ellipse([sep_x - dot_r, dot_y1 - dot_r, sep_x + dot_r, dot_y1 + dot_r], fill=theme_info["accent_color"])
        draw.ellipse([sep_x - dot_r, dot_y2 - dot_r, sep_x + dot_r, dot_y2 + dot_r], fill=theme_info["accent_color"])

        draw_card(sep_x + int(15 * scale), "45")

        # 4. Date Badge at Bottom
        date_text = "THURSDAY ◆ 30 JULY 2026"
        db = draw.textbbox((0, 0), date_text, font=font_cinzel)
        dw = db[2] - db[0]
        dh = db[3] - db[1]
        badge_y = card_y + card_h + int(20 * scale)
        badge_pad_x = int(20 * scale)
        badge_pad_y = int(6 * scale)
        b_box = [(w - dw) // 2 - badge_pad_x, badge_y - badge_pad_y, (w + dw) // 2 + badge_pad_x, badge_y + dh + badge_pad_y]

        draw.rounded_rectangle(b_box, radius=int(20 * scale), fill=theme_info["badge_bg"], outline=theme_info["badge_border"], width=int(1.5 * scale))
        draw.text(((w - dw) // 2, badge_y), date_text, font=font_cinzel, fill=theme_info["accent_color"])

    # Scale down for smooth anti-aliased output (640x380)
    out_img = img.resize((640, 380), Image.Resampling.LANCZOS)
    filename = f"theme_{theme_key}.png"
    filepath = os.path.join(output_dir, filename)
    out_img.save(filepath, "PNG")
    print(f"Generated theme screenshot: {filepath}")
    return filepath

if __name__ == "__main__":
    for key, info in THEMES.items():
        render_theme_screenshot(key, info, "assets")
