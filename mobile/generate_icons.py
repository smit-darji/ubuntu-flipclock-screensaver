#!/usr/bin/env python3
import os
from PIL import Image

def generate_launcher_icons():
    source_icon = "../flipclock.png"
    if not os.path.exists(source_icon):
        source_icon = "../screenshot.png"
    
    if not os.path.exists(source_icon):
        print(f"Error: Source icon not found at {source_icon}")
        return

    sizes = {
        "app/src/main/res/mipmap-mdpi/ic_launcher.png": (48, 48),
        "app/src/main/res/mipmap-hdpi/ic_launcher.png": (72, 72),
        "app/src/main/res/mipmap-xhdpi/ic_launcher.png": (96, 96),
        "app/src/main/res/mipmap-xxhdpi/ic_launcher.png": (144, 144),
        "app/src/main/res/mipmap-xxxhdpi/ic_launcher.png": (192, 192)
    }

    try:
        img = Image.open(source_icon)
        for path, size in sizes.items():
            os.makedirs(os.path.dirname(path), exist_ok=True)
            resized_img = img.resize(size, Image.Resampling.LANCZOS)
            resized_img.save(path, "PNG")
            print(f"Generated launcher icon: {path} ({size[0]}x{size[1]})")
        print("Launcher icons generated successfully!")
    except Exception as e:
        print(f"Error generating launcher icons: {e}")

if __name__ == "__main__":
    generate_launcher_icons()
