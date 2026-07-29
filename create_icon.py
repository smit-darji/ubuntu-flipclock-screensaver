#!/usr/bin/env python3
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_premium_icon(output_path="flipclock.png", size=512):
    # 4x higher resolution canvas for ultra anti-aliased rendering (2048x2048)
    scale = 4
    canvas_size = size * scale
    img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))

    margin = int(canvas_size * 0.05)
    rect_box = [margin, margin, canvas_size - margin, canvas_size - margin]
    radius = int(canvas_size * 0.22)

    # 1. Soft Ambient Outer Drop Shadow
    shadow_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    shadow_draw = ImageDraw.Draw(shadow_img)
    shadow_offset = int(canvas_size * 0.025)
    shadow_box = [rect_box[0], rect_box[1] + shadow_offset, rect_box[2], rect_box[3] + shadow_offset]
    shadow_draw.rounded_rectangle(shadow_box, radius=radius, fill=(0, 0, 0, 180))
    shadow_img = shadow_img.filter(ImageFilter.GaussianBlur(radius=int(canvas_size * 0.04)))
    img.paste(shadow_img, (0, 0), shadow_img)

    # 2. Main Squircle Body (Obsidian Dark Glass Gradient)
    body_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    body_draw = ImageDraw.Draw(body_img)

    for y in range(rect_box[1], rect_box[3]):
        factor = (y - rect_box[1]) / (rect_box[3] - rect_box[1])
        r = int(28 - factor * 18)
        g = int(28 - factor * 18)
        b = int(34 - factor * 20)
        body_draw.line([(rect_box[0], y), (rect_box[2], y)], fill=(r, g, b, 255))

    # Mask to rounded rect
    mask = Image.new("L", (canvas_size, canvas_size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.rounded_rectangle(rect_box, radius=radius, fill=255)

    img.paste(body_img, (0, 0), mask)

    # 3. Glossy Glass Sheen Diagonal Overlay
    sheen_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    sheen_draw = ImageDraw.Draw(sheen_img)
    points = [
        (rect_box[0], rect_box[1]),
        (rect_box[2], rect_box[1]),
        (rect_box[0], rect_box[1] + int((rect_box[3] - rect_box[1]) * 0.6))
    ]
    sheen_draw.polygon(points, fill=(255, 255, 255, 12))
    img.paste(sheen_img, (0, 0), mask)

    # 4. Premium Gold Metallic Border
    border_draw = ImageDraw.Draw(img)
    border_width = int(canvas_size * 0.016)
    border_draw.rounded_rectangle(rect_box, radius=radius, outline=(229, 193, 88, 200), width=border_width)

    # 5. Flip Card Container Inside
    card_margin_x = int(canvas_size * 0.13)
    card_margin_y = int(canvas_size * 0.17)
    card_box = [card_margin_x, card_margin_y, canvas_size - card_margin_x, canvas_size - card_margin_y]
    card_radius = int(canvas_size * 0.08)

    card_img = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    card_draw = ImageDraw.Draw(card_img)

    half_y = (card_box[1] + card_box[3]) // 2

    # Top Half (Matte Dark Charcoal)
    top_box = [card_box[0], card_box[1], card_box[2], half_y]
    card_draw.rectangle(top_box, fill=(24, 24, 28, 255))

    # Bottom Half (Deep Obsidian Black)
    bot_box = [card_box[0], half_y, card_box[2], card_box[3]]
    card_draw.rectangle(bot_box, fill=(12, 12, 16, 255))

    # Card Mask
    card_mask = Image.new("L", (canvas_size, canvas_size), 0)
    card_mask_draw = ImageDraw.Draw(card_mask)
    card_mask_draw.rounded_rectangle(card_box, radius=card_radius, fill=255)

    img.paste(card_img, (0, 0), card_mask)

    # Card Border
    border_draw.rounded_rectangle(card_box, radius=card_radius, outline=(180, 150, 60, 140), width=int(canvas_size * 0.009))

    # Center Split-Flap Divider Line
    line_y = half_y
    divider_height = int(canvas_size * 0.012)
    divider_box = [card_box[0] - 2, line_y - divider_height // 2, card_box[2] + 2, line_y + divider_height // 2]
    border_draw.rectangle(divider_box, fill=(0, 0, 0, 255))

    # Gold Metallic Hinge Pins (Left & Right)
    pin_w = int(canvas_size * 0.026)
    pin_h = int(canvas_size * 0.046)
    pin_r = int(canvas_size * 0.01)

    pin_left = [card_box[0] + int(canvas_size * 0.02), line_y - pin_h // 2, card_box[0] + int(canvas_size * 0.02) + pin_w, line_y + pin_h // 2]
    pin_right = [card_box[2] - int(canvas_size * 0.02) - pin_w, line_y - pin_h // 2, card_box[2] - int(canvas_size * 0.02), line_y + pin_h // 2]

    border_draw.rounded_rectangle(pin_left, radius=pin_r, fill=(232, 204, 112, 255))
    border_draw.rounded_rectangle(pin_right, radius=pin_r, fill=(232, 204, 112, 255))

    # 6. Render Crisp Bold Digits ("10:45")
    font = None
    font_size = int(canvas_size * 0.28)
    font_paths = [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/ubuntu/Ubuntu-Bold.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
        "/usr/share/fonts/truetype/freefont/FreeSansBold.ttf"
    ]
    for fp in font_paths:
        try:
            font = ImageFont.truetype(fp, font_size)
            break
        except Exception:
            pass

    if font is None:
        font = ImageFont.load_default()

    text = "10:45"
    text_draw = ImageDraw.Draw(img)

    bbox = text_draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]

    tx = (canvas_size - tw) // 2 - bbox[0]
    ty = (canvas_size - th) // 2 - bbox[1] - int(canvas_size * 0.01)

    # Text Drop Shadow
    text_draw.text((tx, ty + int(canvas_size * 0.015)), text, font=font, fill=(0, 0, 0, 200))
    # Bright Crisp Text
    text_draw.text((tx, ty), text, font=font, fill=(248, 248, 250, 255))

    # High quality LANCZOS anti-aliased scale down
    final_img = img.resize((size, size), Image.Resampling.LANCZOS)
    final_img.save(output_path, "PNG")
    print(f"Generated premium icon: {output_path}")

if __name__ == "__main__":
    create_premium_icon("flipclock.png", 512)
    create_premium_icon("screenshot.png", 512)
