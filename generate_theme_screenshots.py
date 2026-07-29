#!/usr/bin/env python3
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

THEMES = {
    "classic_retro": {
        "title": "Classic Retro (Fliqlo Style)",
        "bg_color": (10, 10, 12, 255),
        "card_top": (28, 28, 30, 255),
        "card_bot": (14, 14, 16, 255),
        "border_color": (255, 255, 255, 30),
        "digit_color": (255, 255, 255, 255),
        "pin_color": (163, 163, 163, 255),
        "accent_color": (229, 229, 229, 255),
        "badge_bg": (26, 26, 26, 220),
        "badge_border": (255, 255, 255, 40),
        "greeting": "GOOD MORNING, SMIT"
    },
    "dark_gold": {
        "title": "Dark Luxury (Gold Accent)",
        "bg_color": (12, 12, 16, 255),
        "card_top": (30, 30, 34, 255),
        "card_bot": (18, 18, 22, 255),
        "border_color": (212, 175, 55, 100),
        "digit_color": (245, 245, 245, 255),
        "pin_color": (232, 204, 112, 255),
        "accent_color": (212, 175, 55, 255),
        "badge_bg": (20, 20, 24, 220),
        "badge_border": (212, 175, 55, 80),
        "greeting": "GOOD AFTERNOON, SMIT"
    },
    "midnight_cyber": {
        "title": "Midnight Cyber (Neon Blue)",
        "bg_color": (2, 6, 23, 255),
        "card_top": (15, 23, 42, 255),
        "card_bot": (9, 13, 22, 255),
        "border_color": (56, 189, 248, 110),
        "digit_color": (224, 242, 254, 255),
        "pin_color": (125, 211, 252, 255),
        "accent_color": (56, 189, 248, 255),
        "badge_bg": (15, 23, 42, 220),
        "badge_border": (56, 189, 248, 90),
        "greeting": "GOOD EVENING, SMIT"
    },
    "emerald_oled": {
        "title": "Emerald OLED (Matrix Green)",
        "bg_color": (1, 4, 9, 255),
        "card_top": (13, 17, 23, 255),
        "card_bot": (4, 13, 8, 255),
        "border_color": (52, 211, 153, 110),
        "digit_color": (167, 243, 208, 255),
        "pin_color": (110, 231, 183, 255),
        "accent_color": (52, 211, 153, 255),
        "badge_bg": (13, 17, 23, 220),
        "badge_border": (52, 211, 153, 90),
        "greeting": "GOOD NIGHT, SMIT"
    },
    "sunset_glow": {
        "title": "Sunset Glow (Amber / Crimson)",
        "bg_color": (13, 5, 8, 255),
        "card_top": (36, 20, 25, 255),
        "card_bot": (23, 11, 16, 255),
        "border_color": (251, 146, 60, 110),
        "digit_color": (255, 247, 237, 255),
        "pin_color": (253, 186, 116, 255),
        "accent_color": (251, 146, 60, 255),
        "badge_bg": (36, 20, 25, 220),
        "badge_border": (251, 146, 60, 90),
        "greeting": "GOOD EVENING, SMIT"
    },
    "minimal_light": {
        "title": "Minimalist Light (Clean Silver)",
        "bg_color": (241, 245, 249, 255),
        "card_top": (255, 255, 255, 255),
        "card_bot": (248, 250, 252, 255),
        "border_color": (148, 163, 184, 120),
        "digit_color": (15, 23, 42, 255),
        "pin_color": (71, 85, 105, 255),
        "accent_color": (30, 41, 59, 255),
        "badge_bg": (255, 255, 255, 230),
        "badge_border": (148, 163, 184, 100),
        "greeting": "GOOD MORNING, SMIT"
    }
}

def render_theme_screenshot(theme_key, theme_info, output_dir="assets"):
    os.makedirs(output_dir, exist_ok=True)
    scale = 2
    w, h = 640 * scale, 380 * scale
    img = Image.new("RGBA", (w, h), theme_info["bg_color"])
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
    date_text = "WEDNESDAY ◆ 29 JULY 2026"
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
