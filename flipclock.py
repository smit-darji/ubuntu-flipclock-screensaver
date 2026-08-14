#!/usr/bin/env python3
import os
import sys

# Disable WebKit hardware compositing mode to prevent GPU black screens on Linux
os.environ["WEBKIT_DISABLE_COMPOSITING_MODE"] = "1"

import time
import subprocess
import ctypes
import math
import argparse
import configparser
import re
import gi

# Initialize GI namespaces
gi.require_version('Gtk', '3.0')
try:
    gi.require_version('WebKit2', '4.0')
except ValueError:
    try:
        gi.require_version('WebKit2', '4.1')
    except ValueError:
        print("Error: WebKit2 namespace not found. Please install gir1.2-webkit2-4.0 or gir1.2-webkit2-4.1.")
        sys.exit(1)
from gi.repository import Gtk, Gdk, WebKit2, GLib, GdkPixbuf

APP_VERSION = "2.5.7"

THEME_CATEGORIES = {
    "liquid_glass": {
        "label": "💧 Liquid Glass & Crystal Dark",
        "themes": ["apple_liquid_glass", "liquid_glass", "luxury_black_gold", "obsidian_titanium", "arctic_ice", "ocean_cyan"]
    },
    "executive": {
        "label": "🏆 Executive Dark & Gold",
        "themes": ["luxury_black_gold", "obsidian_titanium", "platinum_silver", "champagne_gold", "matte_black_diamond", "swiss_minimalist", "minimal_dark", "dark_black"]
    },
    "greens": {
        "label": "🌿 Executive Greens",
        "themes": ["dark_emerald", "forest_green", "racing_green"]
    },
    "reds": {
        "label": "💎 Ruby & Crimson Reds",
        "themes": ["ruby_executive", "burgundy_prestige", "crimson_royal", "rose_gold", "copper_elite"]
    },
    "blues": {
        "label": "🚙 Sapphire & Ocean Blues",
        "themes": ["royal_sapphire", "midnight_navy", "arctic_ice", "ocean_cyan"]
    },
    "purple_custom": {
        "label": "🔮 Purple, Graphite & Custom",
        "themes": ["royal_purple", "amethyst_elite", "graphite_gray", "custom"]
    }
}

PRESET_THEMES = {
    "liquid_glass": {
        "name": "💧 Translucent Liquid Cyan",
        "bg_color": "#060810",
        "card_color": "#0F172A",
        "digit_color": "#FFFFFF",
        "accent_color": "#38BDF8",
        "border_color": "#1E293B",
        "digit_font": "Audiowide",
        "label_font": "Outfit"
    },
    "apple_liquid_glass": {
        "name": "💧 Apple Liquid Glass",
        "bg_color": "#000000",
        "card_color": "rgba(255, 255, 255, 0.12)",
        "digit_color": "#FFFFFF",
        "accent_color": "#D4AF37",
        "border_color": "rgba(255, 255, 255, 0.18)",
        "digit_font": "New York",
        "label_font": "New York"
    },
    "luxury_black_gold": {
        "name": "🥇 Luxury Black Gold",
        "bg_color": "#000000",
        "card_color": "#1C1C1E",
        "digit_color": "#F5F5F7",
        "accent_color": "#D4AF37",
        "border_color": "#4A4A4A",
        "digit_font": "Cinzel",
        "label_font": "Cinzel"
    },
    "obsidian_titanium": {
        "name": "🥈 Obsidian Titanium",
        "bg_color": "#050505",
        "card_color": "#1F1F1F",
        "digit_color": "#F8F8F8",
        "accent_color": "#AEB5BD",
        "border_color": "#50545A",
        "digit_font": "Inter",
        "label_font": "Inter"
    },
    "dark_emerald": {
        "name": "🥉 Dark Emerald",
        "bg_color": "#07120C",
        "card_color": "#122118",
        "digit_color": "#F7FAF7",
        "accent_color": "#00C853",
        "border_color": "#365541",
        "digit_font": "Cinzel",
        "label_font": "Cinzel"
    },
    "forest_green": {
        "name": "🌲 Forest Green",
        "bg_color": "#08110A",
        "card_color": "#18261D",
        "digit_color": "#F4F8F4",
        "accent_color": "#4CAF50",
        "border_color": "#486651",
        "digit_font": "Inter",
        "label_font": "Inter"
    },
    "racing_green": {
        "name": "🏎️ British Racing Green",
        "bg_color": "#06110A",
        "card_color": "#0E2017",
        "digit_color": "#FAFAF6",
        "accent_color": "#0B8F57",
        "border_color": "#355649",
        "digit_font": "Cinzel",
        "label_font": "Cinzel"
    },
    "ruby_executive": {
        "name": "💎 Ruby Executive",
        "bg_color": "#090606",
        "card_color": "#221515",
        "digit_color": "#FAFAFA",
        "accent_color": "#D32F2F",
        "border_color": "#5B3A3A",
        "digit_font": "Outfit",
        "label_font": "Outfit"
    },
    "burgundy_prestige": {
        "name": "🍷 Burgundy Prestige",
        "bg_color": "#120808",
        "card_color": "#2A1616",
        "digit_color": "#FFF9F8",
        "accent_color": "#8E2430",
        "border_color": "#634545",
        "digit_font": "Cinzel",
        "label_font": "Cinzel"
    },
    "crimson_royal": {
        "name": "🏎️ Crimson Royal",
        "bg_color": "#0A0505",
        "card_color": "#231313",
        "digit_color": "#FFFFFF",
        "accent_color": "#C62828",
        "border_color": "#604040",
        "digit_font": "Outfit",
        "label_font": "Outfit"
    },
    "royal_sapphire": {
        "name": "🚙 Royal Sapphire",
        "bg_color": "#030816",
        "card_color": "#162033",
        "digit_color": "#FFFFFF",
        "accent_color": "#2E7DFF",
        "border_color": "#36527A",
        "digit_font": "Orbitron",
        "label_font": "Orbitron"
    },
    "midnight_navy": {
        "name": "⚓ Midnight Navy",
        "bg_color": "#050B16",
        "card_color": "#182336",
        "digit_color": "#FAFAFA",
        "accent_color": "#4F8BFF",
        "border_color": "#4E6589",
        "digit_font": "Inter",
        "label_font": "Inter"
    },
    "arctic_ice": {
        "name": "❄️ Arctic Ice",
        "bg_color": "#05080A",
        "card_color": "#172126",
        "digit_color": "#FFFFFF",
        "accent_color": "#38D9FF",
        "border_color": "#4B6D77",
        "digit_font": "Roboto",
        "label_font": "Roboto"
    },
    "ocean_cyan": {
        "name": "🌊 Ocean Cyan",
        "bg_color": "#071116",
        "card_color": "#172B33",
        "digit_color": "#F6FFFF",
        "accent_color": "#00BCD4",
        "border_color": "#47636B",
        "digit_font": "Orbitron",
        "label_font": "Orbitron"
    },
    "royal_purple": {
        "name": "👑 Royal Purple",
        "bg_color": "#08040D",
        "card_color": "#1F1930",
        "digit_color": "#FAFAFA",
        "accent_color": "#8E44FF",
        "border_color": "#50416E",
        "digit_font": "Outfit",
        "label_font": "Outfit"
    },
    "amethyst_elite": {
        "name": "🔮 Amethyst Elite",
        "bg_color": "#0C0712",
        "card_color": "#241A2E",
        "digit_color": "#FFFFFF",
        "accent_color": "#A259FF",
        "border_color": "#5D5174",
        "digit_font": "Cinzel",
        "label_font": "Cinzel"
    },
    "platinum_silver": {
        "name": "🪙 Platinum Silver",
        "bg_color": "#101010",
        "card_color": "#262626",
        "digit_color": "#FFFFFF",
        "accent_color": "#C7CCD4",
        "border_color": "#5A5A5A",
        "digit_font": "Inter",
        "label_font": "Inter"
    },
    "graphite_gray": {
        "name": "⚙️ Graphite Gray",
        "bg_color": "#111111",
        "card_color": "#2A2A2A",
        "digit_color": "#F5F5F5",
        "accent_color": "#9E9E9E",
        "border_color": "#555555",
        "digit_font": "Roboto",
        "label_font": "Roboto"
    },
    "copper_elite": {
        "name": "🧱 Copper Elite",
        "bg_color": "#090909",
        "card_color": "#201A18",
        "digit_color": "#FFF8F2",
        "accent_color": "#B87333",
        "border_color": "#5C4537",
        "digit_font": "Cinzel",
        "label_font": "Cinzel"
    },
    "rose_gold": {
        "name": "🌹 Rose Gold",
        "bg_color": "#0A0909",
        "card_color": "#241C1B",
        "digit_color": "#FFF8F6",
        "accent_color": "#E8A87C",
        "border_color": "#6A504A",
        "digit_font": "Outfit",
        "label_font": "Outfit"
    },
    "champagne_gold": {
        "name": "🥂 Champagne Gold",
        "bg_color": "#0B0A08",
        "card_color": "#24221D",
        "digit_color": "#FFFDF7",
        "accent_color": "#E5C07B",
        "border_color": "#6D6655",
        "digit_font": "Cinzel",
        "label_font": "Cinzel"
    },
    "matte_black_diamond": {
        "name": "✨ Matte Black Diamond",
        "bg_color": "#010101",
        "card_color": "#181818",
        "digit_color": "#FCFCFC",
        "accent_color": "#F0F0F0",
        "border_color": "#3A3A3A",
        "digit_font": "Inter",
        "label_font": "Inter"
    },
    "swiss_minimalist": {
        "name": "⬜ Swiss Minimalist",
        "bg_color": "#000000",
        "card_color": "#181818",
        "digit_color": "#FFFFFF",
        "accent_color": "#FFFFFF",
        "border_color": "#000000",
        "digit_font": "Inter",
        "label_font": "Inter"
    },
    "minimal_dark": {
        "name": "🌑 Minimalist Dark",
        "bg_color": "#111111",
        "card_color": "#1C1C1E",
        "digit_color": "#FFFFFF",
        "accent_color": "rgba(235,235,245,0.6)",
        "border_color": "rgba(255,255,255,0.06)",
        "digit_font": "Inter",
        "label_font": "Inter"
    },
    "dark_black": {
        "name": "🌑 Dark Black",
        "bg_color": "#000000",
        "card_color": "#0C0C0F",
        "digit_color": "#FFFFFF",
        "accent_color": "#E5E5E7",
        "border_color": "rgba(255,255,255,0.08)",
        "digit_font": "Inter",
        "label_font": "Inter"
    },
    "classic_retro": {
        "name": "📜 Classic Retro",
        "bg_color": "#0A0A0C",
        "card_color": "#1C1C1E",
        "digit_color": "#FFFFFF",
        "accent_color": "#E5E5E5",
        "border_color": "#4A4A4A",
        "digit_font": "Inter",
        "label_font": "Cinzel"
    },
    "minimal_light": {
        "name": "☀️ Minimalist Light",
        "bg_color": "#F1F5F9",
        "card_color": "#FFFFFF",
        "digit_color": "#0F172A",
        "accent_color": "#1E293B",
        "border_color": "#94A3B8",
        "digit_font": "Roboto",
        "label_font": "Roboto"
    },
    "custom": {
        "name": "🎨 Custom Theme",
        "bg_color": "#000000",
        "card_color": "#1C1C1E",
        "digit_color": "#FFFFFF",
        "accent_color": "#D4AF37",
        "border_color": "#4A4A4A",
        "digit_font": "Inter",
        "label_font": "Cinzel"
    }
}

class CustomDarkDialog(Gtk.Dialog):
    """Custom dark GTK modal dialog matching app dark theme layout."""
    def __init__(self, parent, title, primary_msg, secondary_msg="", is_confirm=False):
        super().__init__(title=title, transient_for=parent, modal=True, destroy_with_parent=True)
        self.set_default_size(440, 190)
        self.set_position(Gtk.WindowPosition.CENTER_ON_PARENT)
        self.set_resizable(False)
        self.get_style_context().add_class("custom-dark-dialog")

        box = self.get_content_area()
        box.set_spacing(12)
        box.set_margin_top(20)
        box.set_margin_bottom(20)
        box.set_margin_start(24)
        box.set_margin_end(24)

        lbl_title = Gtk.Label(label=primary_msg)
        lbl_title.get_style_context().add_class("dialog-title")
        lbl_title.set_xalign(0)
        lbl_title.set_line_wrap(True)
        box.pack_start(lbl_title, False, False, 0)

        if secondary_msg:
            lbl_sec = Gtk.Label(label=secondary_msg)
            lbl_sec.get_style_context().add_class("dialog-secondary")
            lbl_sec.set_xalign(0)
            lbl_sec.set_line_wrap(True)
            box.pack_start(lbl_sec, False, False, 0)

        action_area = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        action_area.set_halign(Gtk.Align.END)
        action_area.set_margin_top(16)

        if is_confirm:
            btn_no = Gtk.Button(label="Cancel")
            btn_no.get_style_context().add_class("btn-secondary")
            btn_no.connect("clicked", lambda w: self.response(Gtk.ResponseType.NO))
            action_area.pack_start(btn_no, False, False, 0)

            btn_yes = Gtk.Button(label="Confirm")
            btn_yes.get_style_context().add_class("btn-reset" if "Reset" in title else "btn-primary")
            btn_yes.connect("clicked", lambda w: self.response(Gtk.ResponseType.YES))
            action_area.pack_start(btn_yes, False, False, 0)
        else:
            btn_ok = Gtk.Button(label="OK")
            btn_ok.get_style_context().add_class("btn-primary")
            btn_ok.connect("clicked", lambda w: self.response(Gtk.ResponseType.OK))
            action_area.pack_start(btn_ok, False, False, 0)

        box.pack_start(action_area, False, False, 0)
        self.show_all()

def hex_to_rgba(hex_str, default_hex="#000000"):
    try:
        hex_str = str(hex_str).strip().lstrip('#')
        if len(hex_str) == 6:
            r = int(hex_str[0:2], 16) / 255.0
            g = int(hex_str[2:4], 16) / 255.0
            b = int(hex_str[4:6], 16) / 255.0
            return Gdk.RGBA(r, g, b, 1.0)
    except Exception:
        pass
    rgba = Gdk.RGBA()
    rgba.parse(default_hex)
    return rgba

def rgba_to_hex(rgba):
    r = int(round(max(0, min(1, rgba.red)) * 255))
    g = int(round(max(0, min(1, rgba.green)) * 255))
    b = int(round(max(0, min(1, rgba.blue)) * 255))
    return f"#{r:02x}{g:02x}{b:02x}"

# X11 Idle time struct and ctypes declarations
class XScreenSaverInfo(ctypes.Structure):
    _fields_ = [
        ('window', ctypes.c_ulong),
        ('state', ctypes.c_int),
        ('kind', ctypes.c_int),
        ('til_or_since', ctypes.c_ulong),
        ('idle', ctypes.c_ulong),
        ('event_mask', ctypes.c_ulong)
    ]

try:
    x11 = ctypes.cdll.LoadLibrary('libX11.so.6')
    xss = ctypes.cdll.LoadLibrary('libXss.so.1')
    
    x11.XOpenDisplay.argtypes = [ctypes.c_char_p]
    x11.XOpenDisplay.restype = ctypes.c_void_p
    
    x11.XDefaultRootWindow.argtypes = [ctypes.c_void_p]
    x11.XDefaultRootWindow.restype = ctypes.c_ulong
    
    xss.XScreenSaverAllocInfo.argtypes = []
    xss.XScreenSaverAllocInfo.restype = ctypes.POINTER(XScreenSaverInfo)
    
    xss.XScreenSaverQueryInfo.argtypes = [ctypes.c_void_p, ctypes.c_ulong, ctypes.POINTER(XScreenSaverInfo)]
    xss.XScreenSaverQueryInfo.restype = ctypes.c_int
    
    x11.XFree.argtypes = [ctypes.c_void_p]
    x11.XFree.restype = ctypes.c_int
    
    x11.XCloseDisplay.argtypes = [ctypes.c_void_p]
    x11.XCloseDisplay.restype = ctypes.c_int
    X11_AVAILABLE = True
except Exception as e:
    X11_AVAILABLE = False

# Input tracking flags
key_input_enabled = False
mouse_input_enabled = False
exit_threshold = 30  # pixels

def enable_key_tracking():
    global key_input_enabled
    key_input_enabled = True
    return False

def enable_mouse_tracking():
    global mouse_input_enabled
    mouse_input_enabled = True
    return False

DEFAULT_HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Premium Flip Clock Screensaver</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Audiowide&family=Bebas+Neue&family=Chakra+Petch:wght@600;700&family=Cinzel:wght@700;800;900&family=Courier+Prime:wght@400;700&family=Exo+2:wght@600;800&family=IBM+Plex+Sans:wght@500;700&family=Inter:wght@300;400;500;600;700;800;900&family=Michroma&family=Orbitron:wght@700;800;900&family=Oswald:wght@500;700&family=Outfit:wght@600;800&family=Oxanium:wght@600;800&family=Rajdhani:wght@600;700&family=Roboto:wght@500;700;900&family=Share+Tech+Mono&family=Teko:wght@600;700&family=VT323&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; user-select:none; -webkit-user-select:none; }
        html, body { width:100vw; height:100vh; overflow:hidden; cursor:none; font-family:var(--digit-font, 'Inter',system-ui,sans-serif); }

        /* ═══ BASE SCENE ═══════════════════════════════════ */
        #scene {
            position:relative;
            width:100vw; height:100vh;
            display:flex; flex-direction:column;
            align-items:center; justify-content:center;
            gap:3.5vh;
            overflow:hidden;
            background: #000000;
            transition: background 0.5s ease;
        }

        #scene::before {
            content:'';
            position:absolute; inset:0;
            background: radial-gradient(ellipse 70% 55% at 50% 48%, var(--vignette-color, rgba(255,255,255,0.02)) 0%, transparent 75%);
            pointer-events:none; z-index:0;
        }

        /* ═══ UNIFIED RESPONSIVE CLOCK CONTAINER ═══ */
        #clock-container {
            display:flex; flex-direction:column;
            align-items:center; justify-content:center;
            gap: clamp(14px, 3vh, 36px);
            z-index:10;
            width:100%;
            max-width:96vw;
            transform-origin: center center;
            transition: transform 0.4s ease;
        }

        /* ═══ GREETING BADGE ═══════════════════════════════ */
        #greeting-badge {
            z-index:10;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 12px;
            padding: clamp(6px, 1vh, 12px) clamp(22px, 2.8vw, 44px);
            border-radius: 40px;
            font-family: var(--label-font, 'Cinzel', serif);
            font-size: clamp(11px, 1.4vw, 22px);
            font-weight: 800;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            color: var(--accent-color, #ffffff);
            background: var(--badge-bg, rgba(20,20,24,0.75));
            border: 1px solid var(--badge-border, rgba(255,255,255,0.18));
            box-shadow: 0 8px 32px rgba(0,0,0,0.75), inset 0 1px 0 rgba(255,255,255,0.12);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            text-shadow: 0 2px 12px rgba(0,0,0,0.9);
            text-align: center;
            max-width: 92vw;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            transition: all 0.4s ease;
        }

        .badge-ornament {
            color: var(--accent-color, #d4af37);
            font-size: 0.85em;
            opacity: 0.85;
        }

        /* ═══ CLOCK ROW ═══════════════════════════════════ */
        .clock-row {
            display:flex;
            align-items:center;
            justify-content:center;
            gap:clamp(12px, 2.5vw, 44px);
            z-index:10;
            width:100%;
            max-width:96vw;
            transition: transform 0.3s ease;
        }

        /* ═══ FLIP CARD ═══════════════════════════════════ */
        .flip-card {
            position:relative;
            width:  clamp(150px, 34vh, 420px);
            height: clamp(210px, 50vh, 600px);
            border-radius: clamp(10px, 1.8vh, 24px);
            overflow:hidden;
            perspective:1400px;
            flex-shrink:0;
            background: var(--card-bg, linear-gradient(170deg, #1f1f1f 0%, #161616 50%, #0d0d0d 100%));
            border: 1.5px solid var(--card-border, rgba(255,255,255,0.12));
            box-shadow:
                0 18px 70px rgba(0,0,0,0.95),
                0 0 0 1px rgba(255,255,255,0.04),
                inset 0 1px 0 rgba(255,255,255,0.08),
                inset 0 -1px 0 rgba(0,0,0,0.8);
            transition: background 0.4s ease, border-color 0.4s ease, box-shadow 0.4s ease;
        }

        .card-half { position:absolute; left:0; width:100%; height:50%; overflow:hidden; }
        .card-top {
            top:0;
            border-radius: clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px) 0 0;
            background: var(--card-top-bg, linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%));
            border-bottom: 1px solid var(--divider-border, rgba(0,0,0,0.85));
        }
        .card-bottom {
            bottom:0;
            border-radius: 0 0 clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px);
            background: var(--card-bot-bg, linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.1) 100%));
        }

        /* Divider line */
        .card-divider {
            position:absolute; top:50%; left:0;
            width:100%; height:3px;
            transform:translateY(-50%);
            z-index:12;
            background: var(--divider-line, #000000);
            box-shadow: 0 1px 4px rgba(0,0,0,0.95);
        }
        /* Side hinges/pins */
        .card-divider::before, .card-divider::after {
            content:'';
            position:absolute; top:50%; transform:translateY(-50%);
            width:  clamp(5px, 0.7vh, 10px);
            height: clamp(10px, 1.5vh, 18px);
            border-radius: clamp(2px, 0.4vh, 5px);
            background: var(--pin-bg, linear-gradient(180deg, #a3a3a3 0%, #737373 50%, #404040 100%));
            box-shadow: 0 1px 3px rgba(0,0,0,0.8), inset 0 1px 0 rgba(255,255,255,0.2);
        }
        .card-divider::before { left:  clamp(8px, 1.2vh, 16px); }
        .card-divider::after  { right: clamp(8px, 1.2vh, 16px); }

        /* Digit text */
        .digit-wrapper {
            position:absolute; left:0; width:100%; height:200%;
            display:flex; align-items:center; justify-content:center;
        }
        .card-top    .digit-wrapper, .flipper-top    .digit-wrapper { top:0; }
        .card-bottom .digit-wrapper, .flipper-bottom .digit-wrapper { bottom:0; }

        .digit-text {
            font-family:'Inter',system-ui,sans-serif;
            font-size: clamp(85px, 21vh, 300px);
            font-weight:800;
            color: var(--digit-color, #ffffff);
            letter-spacing:-0.02em;
            line-height:1;
            text-align:center;
            text-shadow: var(--digit-shadow, 0 2px 10px rgba(0,0,0,0.9));
        }

        /* AM/PM Badge inside hours/seconds card */
        .ampm-badge {
            position:absolute;
            bottom:clamp(12px, 2.5vh, 32px);
            left:clamp(12px, 2vh, 24px);
            z-index:15;
            font-size:clamp(10px, 1.4vh, 18px);
            font-weight:700;
            letter-spacing:0.1em;
            color: var(--accent-color, #ffffff);
            text-transform:uppercase;
            opacity:0.9;
        }

        /* Flip animations */
        .flipper { position:absolute; left:0; width:100%; overflow:hidden; backface-visibility:hidden; }
        .flipper-top {
            top:0; height:50%;
            transform-origin:bottom center;
            border-radius: clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px) 0 0;
            background: var(--card-top-bg, linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%));
        }
        .flipper-bottom {
            bottom:0; height:50%;
            transform-origin:top center;
            border-radius: 0 0 clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px);
            background: var(--card-bot-bg, linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.1) 100%));
        }
        @keyframes flipTopOut    { 0%{transform:rotateX(0deg)}  100%{transform:rotateX(-90deg)} }
        @keyframes flipBottomIn  { 0%{transform:rotateX(90deg)} 100%{transform:rotateX(0deg)}   }
        .flip-top-out   { animation: flipTopOut   0.3s cubic-bezier(0.45,0,0.55,1) forwards; }
        .flip-bottom-in { animation: flipBottomIn 0.3s cubic-bezier(0.45,0,0.55,1) 0.3s forwards; transform:rotateX(90deg); }

        /* ═══ SEPARATOR ═══════════════════════════════════ */
        .sep {
            display:flex; flex-direction:column;
            align-items:center;
            gap:clamp(12px, 2.6vh, 30px);
        }
        .sep-dot {
            width:  clamp(7px, 1vh, 14px);
            height: clamp(7px, 1vh, 14px);
            border-radius:50%;
            background: var(--dot-bg, radial-gradient(circle at 30% 28%, #ffffff 0%, #d4d4d4 50%, #a3a3a3 100%));
            box-shadow: var(--dot-shadow, 0 0 10px rgba(255,255,255,0.4));
        }

        /* ═══ DATE BADGE ══════════════════════════════════ */
        #date-badge {
            z-index:10;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: clamp(8px, 1.2vw, 18px);
            padding: clamp(8px, 1.2vh, 14px) clamp(22px, 3vw, 48px);
            border-radius: 50px;
            font-family: var(--label-font, 'Cinzel', serif);
            font-size: clamp(10px, 1.3vw, 19px);
            font-weight: 700;
            letter-spacing: 0.2em;
            text-transform: uppercase;
            color: var(--badge-color, #e5e5e5);
            background: var(--badge-bg, rgba(18,18,22,0.85));
            border: 1px solid var(--badge-border, rgba(255,255,255,0.18));
            box-shadow: 0 8px 35px rgba(0,0,0,0.8), inset 0 1px 0 rgba(255,255,255,0.12);
            backdrop-filter: blur(14px);
            -webkit-backdrop-filter: blur(14px);
            text-align: center;
            max-width: 92vw;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
            transition: all 0.4s ease;
        }

        .date-segment { display: inline-block; }
        .date-dayname { color: var(--accent-color, #ffffff); font-weight: 800; }
        .date-sep { color: var(--accent-color, #ffffff); opacity: 0.65; font-size: 0.8em; }
        .date-num {
            background: rgba(255, 255, 255, 0.08);
            border: 1px solid rgba(255, 255, 255, 0.15);
            border-radius: 6px;
            padding: 2px 10px;
            font-weight: 800;
            color: var(--digit-color, #ffffff);
            box-shadow: inset 0 1px 0 rgba(255,255,255,0.1);
        }
        .date-month, .date-year { color: var(--badge-color, #e5e5e5); }

        /* ═══ BRANDING WATERMARK FOOTER ════════════════════ */
        #branding-tag {
            position:fixed;
            bottom:14px;
            z-index:10;
            font-size:11px;
            letter-spacing:0.12em;
            text-transform:uppercase;
            font-weight:600;
            color: var(--branding-color, rgba(255,255,255,0.35));
            opacity:0.6;
            transition: opacity 0.3s ease;
        }

        /* ═══ CLOSE BUTTON ════════════════════════════════ */
        #close-btn {
            position:fixed;
            top:18px; right:18px;
            z-index:9999;
            width:44px; height:44px;
            border-radius:50%;
            border:1.5px solid var(--card-border, rgba(255,255,255,0.2));
            background:var(--badge-bg, rgba(20,20,24,0.85));
            backdrop-filter:blur(12px);
            -webkit-backdrop-filter:blur(12px);
            color:var(--accent-color, #ffffff);
            font-size:20px;
            font-weight:300;
            font-family:'Inter',sans-serif;
            cursor:pointer;
            display:flex;
            align-items:center;
            justify-content:center;
            opacity:0;
            transition: opacity 0.4s ease, background 0.3s ease, transform 0.3s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        }
        #close-btn:hover {
            background:rgba(255,255,255,0.2);
            transform:scale(1.1);
        }
        #scene.show-close #close-btn {
            opacity:1;
        }

        /* ═══ THEME PRESETS ═══════════════════════════════ */
        .theme-classic_retro {
            --vignette-color: rgba(255, 255, 255, 0.01);
            --card-bg: linear-gradient(170deg, #1f1f1f 0%, #161616 50%, #0d0d0d 100%);
            --card-border: rgba(255, 255, 255, 0.12);
            --card-top-bg: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
            --card-bot-bg: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.1) 100%);
            --divider-line: #000000;
            --pin-bg: linear-gradient(180deg, #a3a3a3 0%, #737373 50%, #404040 100%);
            --digit-color: #ffffff;
            --digit-shadow: 0 2px 10px rgba(0,0,0,0.9);
            --dot-bg: radial-gradient(circle at 30% 28%, #ffffff 0%, #d4d4d4 50%, #a3a3a3 100%);
            --dot-shadow: 0 0 10px rgba(255,255,255,0.4);
            --accent-color: #ffffff;
            --badge-color: #e5e5e5;
            --badge-bg: rgba(26,26,26,0.85);
            --badge-border: rgba(255,255,255,0.15);
            --branding-color: rgba(255, 255, 255, 0.4);
        }

        .theme-dark_gold {
            --vignette-color: rgba(255, 215, 0, 0.025);
            --card-bg: linear-gradient(170deg, #1e1e22 0%, #141418 40%, #0c0c10 100%);
            --card-border: rgba(212, 175, 55, 0.4);
            --card-top-bg: linear-gradient(180deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.015) 100%);
            --card-bot-bg: linear-gradient(180deg, rgba(0,0,0,0.25) 0%, rgba(0,0,0,0.1) 100%);
            --divider-line: #000000;
            --pin-bg: linear-gradient(180deg, #e8cc70 0%, #b09840 50%, #806820 100%);
            --digit-color: #f5f5f5;
            --digit-shadow: 0 2px 12px rgba(0,0,0,0.8);
            --dot-bg: radial-gradient(circle at 30% 28%, #f0d860 0%, #c8a830 45%, #806818 100%);
            --dot-shadow: 0 0 12px rgba(200,168,48,0.5);
            --accent-color: #d4af37;
            --badge-color: #e5c158;
            --badge-bg: rgba(20,20,24,0.8);
            --badge-border: rgba(212,175,55,0.3);
            --branding-color: rgba(212, 175, 55, 0.45);
        }

        .theme-midnight_cyber {
            --vignette-color: rgba(56, 189, 248, 0.04);
            --card-bg: linear-gradient(170deg, #0f172a 0%, #090d16 50%, #020617 100%);
            --card-border: rgba(56, 189, 248, 0.45);
            --card-top-bg: linear-gradient(180deg, rgba(56,189,248,0.08) 0%, rgba(56,189,248,0.02) 100%);
            --card-bot-bg: linear-gradient(180deg, rgba(2,6,23,0.4) 0%, rgba(2,6,23,0.1) 100%);
            --divider-line: #020617;
            --pin-bg: linear-gradient(180deg, #7dd3fc 0%, #38bdf8 50%, #0284c7 100%);
            --digit-color: #e0f2fe;
            --digit-shadow: 0 0 20px rgba(56,189,248,0.35);
            --dot-bg: radial-gradient(circle at 30% 28%, #7dd3fc 0%, #38bdf8 50%, #0284c7 100%);
            --dot-shadow: 0 0 14px rgba(56,189,248,0.6);
            --accent-color: #38bdf8;
            --badge-color: #38bdf8;
            --badge-bg: rgba(15,23,42,0.85);
            --badge-border: rgba(56,189,248,0.35);
            --branding-color: rgba(56, 189, 248, 0.5);
        }

        .theme-emerald_oled {
            --vignette-color: rgba(52, 211, 153, 0.03);
            --card-bg: linear-gradient(170deg, #0d1117 0%, #040d08 50%, #010409 100%);
            --card-border: rgba(52, 211, 153, 0.45);
            --card-top-bg: linear-gradient(180deg, rgba(52,211,153,0.08) 0%, rgba(52,211,153,0.02) 100%);
            --card-bot-bg: linear-gradient(180deg, rgba(0,0,0,0.5) 0%, rgba(0,0,0,0.2) 100%);
            --divider-line: #000000;
            --pin-bg: linear-gradient(180deg, #6ee7b7 0%, #34d399 50%, #059669 100%);
            --digit-color: #a7f3d0;
            --digit-shadow: 0 0 20px rgba(52,211,153,0.4);
            --dot-bg: radial-gradient(circle at 30% 28%, #6ee7b7 0%, #34d399 50%, #059669 100%);
            --dot-shadow: 0 0 14px rgba(52,211,153,0.6);
            --accent-color: #34d399;
            --badge-color: #34d399;
            --badge-bg: rgba(13,17,23,0.85);
            --badge-border: rgba(52,211,153,0.35);
            --branding-color: rgba(52, 211, 153, 0.5);
        }

        .theme-sunset_glow {
            --vignette-color: rgba(251, 146, 60, 0.04);
            --card-bg: linear-gradient(170deg, #241419 0%, #170b10 50%, #0d0508 100%);
            --card-border: rgba(251, 146, 60, 0.45);
            --card-top-bg: linear-gradient(180deg, rgba(251,146,60,0.08) 0%, rgba(251,146,60,0.02) 100%);
            --card-bot-bg: linear-gradient(180deg, rgba(13,5,8,0.5) 0%, rgba(13,5,8,0.2) 100%);
            --divider-line: #0d0508;
            --pin-bg: linear-gradient(180deg, #ffedd5 0%, #fb923c 50%, #ea580c 100%);
            --digit-color: #fff7ed;
            --digit-shadow: 0 0 20px rgba(251,146,60,0.35);
            --dot-bg: radial-gradient(circle at 30% 28%, #fdba74 0%, #fb923c 50%, #ea580c 100%);
            --dot-shadow: 0 0 14px rgba(251,146,60,0.6);
            --accent-color: #fb923c;
            --badge-color: #fb923c;
            --badge-bg: rgba(36,20,25,0.85);
            --badge-border: rgba(251,146,60,0.35);
            --branding-color: rgba(251, 146, 60, 0.5);
        }

        .theme-minimal_light {
            --vignette-color: rgba(0, 0, 0, 0.02);
            --card-bg: linear-gradient(170deg, #ffffff 0%, #f8fafc 50%, #f1f5f9 100%);
            --card-border: rgba(148, 163, 184, 0.4);
            --card-top-bg: linear-gradient(180deg, rgba(255,255,255,0.9) 0%, rgba(241,245,249,0.5) 100%);
            --card-bot-bg: linear-gradient(180deg, rgba(226,232,240,0.6) 0%, rgba(203,213,225,0.3) 100%);
            --divider-line: #cbd5e1;
            --pin-bg: linear-gradient(180deg, #64748b 0%, #475569 50%, #1e293b 100%);
            --digit-color: #0f172a;
            --digit-shadow: 0 1px 3px rgba(0,0,0,0.15);
            --dot-bg: radial-gradient(circle at 30% 28%, #94a3b8 0%, #475569 100%);
            --dot-shadow: 0 0 8px rgba(71,85,105,0.3);
            --accent-color: #334155;
            --badge-color: #1e293b;
            --badge-bg: rgba(255,255,255,0.9);
            --badge-border: rgba(148,163,184,0.4);
            --branding-color: rgba(30, 41, 59, 0.5);
        }

        /* 22. Swiss Minimalist */
        .theme-swiss_minimalist {
            --vignette-color: transparent;
            --card-bg: #181818;
            --card-border: transparent;
            --card-top-bg: #181818;
            --card-bot-bg: #181818;
            --divider-line: #000000;
            --pin-bg: #000000;
            --digit-color: #FFFFFF;
            --digit-shadow: none;
            --dot-bg: #FFFFFF;
            --dot-shadow: 0 0 10px rgba(255,255,255,0.4);
            --accent-color: #FFFFFF;
            --badge-color: #F2F2F2;
            --badge-bg: transparent;
            --badge-border: transparent;
            --branding-color: rgba(255, 255, 255, 0.2);
        }

        /* 23. Minimalist Dark */
        .theme-minimal_dark {
            --vignette-color: transparent;
            --card-bg: #1C1C1E;
            --card-border: rgba(255,255,255,0.06);
            --card-top-bg: linear-gradient(180deg,rgba(255,255,255,0.04) 0%,rgba(255,255,255,0.01) 100%);
            --card-bot-bg: linear-gradient(180deg,rgba(0,0,0,0.15) 0%,rgba(0,0,0,0.04) 100%);
            --divider-line: #111111;
            --pin-bg: rgba(255,255,255,0.15);
            --digit-color: #FFFFFF;
            --digit-shadow: none;
            --dot-bg: rgba(235,235,245,0.6);
            --dot-shadow: none;
            --accent-color: rgba(235,235,245,0.6);
            --badge-color: rgba(235,235,245,0.85);
            --badge-bg: rgba(44,44,46,0.9);
            --badge-border: rgba(255,255,255,0.1);
            --branding-color: rgba(235,235,245,0.3);
        }

        /* 24. Dark Black Theme */
        .theme-dark_black {
            --vignette-color: transparent;
            --card-bg: #0C0C0F;
            --card-border: rgba(255,255,255,0.08);
            --card-top-bg: linear-gradient(180deg,rgba(255,255,255,0.03) 0%,rgba(255,255,255,0.01) 100%);
            --card-bot-bg: linear-gradient(180deg,rgba(0,0,0,0.2) 0%,rgba(0,0,0,0.05) 100%);
            --divider-line: #000000;
            --pin-bg: rgba(255,255,255,0.18);
            --digit-color: #FFFFFF;
            --digit-shadow: 0 4px 20px rgba(0,0,0,0.5);
            --dot-bg: #FFFFFF;
            --dot-shadow: 0 0 8px rgba(255,255,255,0.3);
            --accent-color: #E5E5E7;
            --badge-color: #FFFFFF;
            --badge-bg: rgba(28,28,30,0.9);
            --badge-border: rgba(255,255,255,0.12);
            --branding-color: rgba(255,255,255,0.3);
        }

        /* 21. Liquid Glass Dark (Translucent Liquid Cyan) */
        .theme-liquid_glass {
            --vignette-color: rgba(255, 255, 255, 0.02);
            --card-bg: rgba(255, 255, 255, 0.12);
            --card-border: rgba(255, 255, 255, 0.18);
            --card-top-bg: linear-gradient(135deg, rgba(255, 255, 255, 0.15) 0%, rgba(255, 255, 255, 0) 50%);
            --card-bot-bg: linear-gradient(180deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.01) 100%);
            --divider-line: rgba(255, 255, 255, 0.08);
            --pin-bg: #D4AF37;
            --digit-color: #FFFFFF;
            --digit-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
            --dot-bg: radial-gradient(circle at 30% 28%, #FFFFFF 0%, #D8D8D8 100%);
            --dot-shadow: 0 0 10px rgba(255, 255, 255, 0.2);
            --accent-color: #D4AF37;
            --badge-color: #D8D8D8;
            --badge-bg: rgba(255, 255, 255, 0.12);
            --badge-border: rgba(255, 255, 255, 0.18);
            --branding-color: rgba(255, 255, 255, 0.35);
        }

        /* Apple Liquid Glass Overrides */
        .theme-liquid_glass #scene {
            background: #000000 !important;
        }
        .theme-liquid_glass #scene::before {
            content: '' !important;
            position: absolute !important;
            inset: 0 !important;
            background: 
                radial-gradient(circle at 20% 20%, rgba(255, 255, 255, 0.05) 0%, transparent 45%),
                radial-gradient(circle at 50% 50%, rgba(255, 255, 255, 0.03) 0%, transparent 70%) !important;
            pointer-events: none !important;
            z-index: 0 !important;
        }
        .theme-liquid_glass .flip-card {
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 48px !important;
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.45),
                inset 0 1px rgba(255, 255, 255, 0.35),
                inset 0 -1px rgba(255, 255, 255, 0.05) !important;
            animation: liquidGlassFloat 8s ease-in-out infinite alternate;
            overflow: visible !important;
        }
        .theme-liquid_glass .flip-card::before {
            content: '';
            position: absolute;
            inset: 0;
            background: linear-gradient(135deg, rgba(255,255,255,0) 30%, rgba(255,255,255,0.04) 50%, rgba(255,255,255,0) 70%);
            background-size: 200% 200%;
            background-position: -200% 0;
            pointer-events: none;
            z-index: 13;
            border-radius: 48px;
            animation: glassShimmerSweep 12s cubic-bezier(0.25, 1, 0.5, 1) infinite;
        }
        .theme-liquid_glass .flip-card::after {
            content: '';
            position: absolute;
            top: 1px;
            left: 16px;
            right: 16px;
            height: 1.5px;
            background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.55) 50%, rgba(255,255,255,0) 100%);
            pointer-events: none;
            z-index: 14;
        }
        .theme-liquid_glass .card-top,
        .theme-liquid_glass .flipper-top {
            border-radius: 48px 48px 0 0 !important;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.16) 0%, rgba(255, 255, 255, 0.02) 100%) !important;
            border-bottom: 1px solid rgba(0, 0, 0, 0.25) !important;
        }
        .theme-liquid_glass .card-bottom,
        .theme-liquid_glass .flipper-bottom {
            border-radius: 0 0 48px 48px !important;
            background: linear-gradient(180deg, rgba(255, 255, 255, 0.04) 0%, rgba(0, 0, 0, 0.12) 100%) !important;
        }
        .theme-liquid_glass .card-divider {
            height: 1px !important;
            background: rgba(255, 255, 255, 0.08) !important;
            border: none !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.5) !important;
        }
        .theme-liquid_glass .card-divider::before,
        .theme-liquid_glass .card-divider::after {
            content: '' !important;
            width: 6px !important;
            height: 10px !important;
            border-radius: 3px !important;
            background: radial-gradient(circle at 35% 35%, #fff6d1 0%, #D4AF37 60%, #876211 100%) !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.4) !important;
        }
        .theme-liquid_glass .card-divider::before {
            left: 8px !important;
        }
        .theme-liquid_glass .card-divider::after {
            right: 8px !important;
        }
        .theme-liquid_glass .divider-dot {
            width: 10px !important;
            height: 10px !important;
            border-radius: 50% !important;
            background: radial-gradient(circle at 35% 35%, #fff6d1 0%, #D4AF37 60%, #876211 100%) !important;
            box-shadow: 0 1px 3px rgba(0,0,0,0.5), inset 0 1px 1px rgba(255,255,255,0.4) !important;
            border: 1px solid rgba(0, 0, 0, 0.4) !important;
        }
        .theme-liquid_glass .digit-text {
            font-family: -apple-system-ny, "New York", "Cormorant Garamond", "Georgia", serif !important;
            font-weight: 500 !important;
            color: #FFFFFF !important;
            text-shadow: 
                -1px -1px 0px rgba(255, 255, 255, 0.25), 
                1px 1px 0px rgba(0, 0, 0, 0.55), 
                0 6px 12px rgba(0, 0, 0, 0.35) !important;
            letter-spacing: -0.02em !important;
        }
        .theme-liquid_glass #greeting-badge {
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
            border: 1px solid rgba(212, 175, 55, 0.45) !important;
            border-radius: 40px !important;
            box-shadow: 
                0 10px 30px rgba(0,0,0,0.35),
                inset 0 1px rgba(255, 255, 255, 0.25),
                inset 0 -1px rgba(255, 255, 255, 0.05) !important;
            color: #D8D8D8 !important;
            font-family: -apple-system-ny, "New York", "Cormorant Garamond", "Georgia", serif !important;
            font-weight: 500 !important;
            letter-spacing: 0.3em !important;
            padding: clamp(8px, 1.2vh, 14px) clamp(26px, 3.2vw, 50px) !important;
            text-shadow: 0 2px 4px rgba(0,0,0,0.5) !important;
            animation: liquidGlassFloat 8s ease-in-out infinite alternate;
        }
        .theme-liquid_glass #greeting-badge .badge-ornament {
            color: #D4AF37 !important;
            text-shadow: 0 0 6px rgba(212, 175, 55, 0.6) !important;
        }
        .theme-liquid_glass #date-badge {
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 50px !important;
            box-shadow: 
                0 10px 30px rgba(0,0,0,0.35),
                inset 0 1px rgba(255, 255, 255, 0.25),
                inset 0 -1px rgba(255, 255, 255, 0.05) !important;
            color: #D8D8D8 !important;
            font-family: -apple-system-ny, "New York", "Cormorant Garamond", "Georgia", serif !important;
            font-weight: 500 !important;
            letter-spacing: 0.25em !important;
            padding: clamp(8px, 1.2vh, 14px) clamp(26px, 3.2vw, 50px) !important;
            animation: liquidGlassFloat 8s ease-in-out infinite alternate 1.5s;
        }
        .theme-liquid_glass #date-badge .date-dayname {
            color: #FFFFFF !important;
            font-weight: 600 !important;
        }
        .theme-liquid_glass #date-badge .date-sep {
            color: #D4AF37 !important;
            opacity: 0.9 !important;
        }
        .theme-liquid_glass #date-badge .date-num {
            background: rgba(255, 255, 255, 0.10) !important;
            border: 1px solid rgba(255, 255, 255, 0.20) !important;
            box-shadow: inset 0 1px rgba(255, 255, 255, 0.2) !important;
            color: #FFFFFF !important;
            border-radius: 8px !important;
            padding: 2px 10px !important;
        }
        .theme-liquid_glass #ampm-badge {
            background: rgba(255, 255, 255, 0.12) !important;
            backdrop-filter: blur(24px) saturate(180%) !important;
            -webkit-backdrop-filter: blur(24px) saturate(180%) !important;
            border: 1px solid rgba(255, 255, 255, 0.18) !important;
            border-radius: 10px !important;
            box-shadow: 
                0 4px 12px rgba(0,0,0,0.35),
                inset 0 1px rgba(255, 255, 255, 0.25),
                inset 0 -1px rgba(255, 255, 255, 0.05) !important;
            color: #D4AF37 !important;
            font-family: -apple-system-ny, "New York", "Cormorant Garamond", "Georgia", serif !important;
            font-weight: 600 !important;
            letter-spacing: 0.1em !important;
            padding: clamp(3px, 0.5vh, 6px) clamp(8px, 1.2vh, 14px) !important;
            text-shadow: 0 0 4px rgba(212, 175, 55, 0.3) !important;
        }
        .theme-liquid_glass .sep-dot,
        .theme-liquid_glass .colon-dot {
            background: radial-gradient(circle at 35% 35%, #FFFFFF 0%, #D8D8D8 100%) !important;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.3), 0 2px 4px rgba(0,0,0,0.5) !important;
        }
        .theme-liquid_glass .flip-top-out {
            animation: flipTopOut 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards !important;
        }
        .theme-liquid_glass .flip-bottom-in {
            animation: flipBottomIn 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.1) 0.35s forwards !important;
            transform: rotateX(90deg);
        }

        @keyframes liquidGlassFloat {
            0% { transform: translateY(0px); }
            100% { transform: translateY(-6px); }
        }
        @keyframes glassShimmerSweep {
            0% { background-position: -200% 0; }
            20% { background-position: 200% 200%; }
            100% { background-position: 200% 200%; }
        }

        /* Swiss Minimalist Theme Overrides */
        .theme-swiss_minimalist #scene {
            background: #000000 !important;
        }
        .theme-swiss_minimalist #scene::before {
            display: none !important;
        }
        .theme-swiss_minimalist #branding-tag,
        .theme-swiss_minimalist #date-badge,
        .theme-swiss_minimalist #greeting-badge {
            display: none !important;
        }
        .theme-swiss_minimalist .flip-card {
            background: #181818 !important;
            border: none !important;
            border-radius: 28px;
            box-shadow:
                0 18px 40px rgba(0,0,0,0.45),
                inset 0 0 15px rgba(0, 0, 0, 0.4) !important;
            width: clamp(200px, 45vh, 480px) !important;
            height: clamp(240px, 54vh, 576px) !important;
        }
        .theme-swiss_minimalist .card-top,
        .theme-swiss_minimalist .flipper-top {
            border-radius: 28px 28px 0 0;
            background: #181818 !important;
            border-bottom: none !important;
        }
        .theme-swiss_minimalist .card-bottom,
        .theme-swiss_minimalist .flipper-bottom {
            border-radius: 0 0 28px 28px;
            background: #181818 !important;
        }
        .theme-swiss_minimalist .card-divider {
            height: 2px !important;
            background: #000000 !important;
            border: none !important;
            box-shadow: none !important;
        }
        .theme-swiss_minimalist .divider-dot,
        .theme-swiss_minimalist .card-divider::before,
        .theme-swiss_minimalist .card-divider::after {
            display: none !important;
        }
        .theme-swiss_minimalist .digit-text {
            font-family: "SF Pro Display", "Helvetica Neue", "Inter", sans-serif !important;
            font-weight: 900 !important;
            color: #FFFFFF !important;
            font-size: clamp(140px, 33vh, 440px) !important;
            text-shadow: none !important;
            letter-spacing: -0.04em !important;
        }
        .theme-swiss_minimalist #ampm-badge {
            position: absolute !important;
            top: 24px !important;
            left: 24px !important;
            bottom: auto !important;
            right: auto !important;
            font-family: "Inter", sans-serif !important;
            font-weight: 600 !important;
            font-size: 24px !important;
            color: #F2F2F2 !important;
            background: transparent !important;
            border: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            box-shadow: none !important;
            letter-spacing: normal !important;
            z-index: 20 !important;
        }
        .theme-swiss_minimalist .clock-row {
            gap: 18px !important;
        }
        .theme-swiss_minimalist .sep {
            gap: 28px !important;
            margin: 0 40px !important;
        }
        .theme-swiss_minimalist .sep-dot {
            width: 14px !important;
            height: 14px !important;
            border-radius: 50% !important;
            background: #FFFFFF !important;
            box-shadow: 0 0 8px rgba(255, 255, 255, 0.4) !important;
        }
        .theme-swiss_minimalist .flip-top-out {
            animation: flipTopOut 0.35s cubic-bezier(0.4, 0, 0.2, 1) forwards !important;
        }
        .theme-swiss_minimalist .flip-bottom-in {
            animation: flipBottomIn 0.35s cubic-bezier(0.4, 0, 0.2, 1) 0s forwards !important;
            transform: rotateX(90deg);
        }

        /* Minimalist Dark Theme Overrides */
        .theme-minimal_dark #scene {
            background: #111111 !important;
        }
        .theme-minimal_dark #scene::before { display:none !important; }
        .theme-minimal_dark #branding-tag { display:none !important; }
        .theme-minimal_dark .flip-card {
            background: #1C1C1E !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 20px;
            box-shadow: 0 12px 32px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        }
        .theme-minimal_dark .card-top,
        .theme-minimal_dark .flipper-top {
            background: rgba(255,255,255,0.03) !important;
            border-radius: 20px 20px 0 0;
            border-bottom: 1px solid rgba(0,0,0,0.4) !important;
        }
        .theme-minimal_dark .card-bottom,
        .theme-minimal_dark .flipper-bottom {
            background: rgba(0,0,0,0.1) !important;
            border-radius: 0 0 20px 20px;
        }
        .theme-minimal_dark .card-divider {
            height: 1px !important;
            background: rgba(0,0,0,0.6) !important;
            border: none !important; box-shadow: none !important;
        }
        .theme-minimal_dark .divider-dot,
        .theme-minimal_dark .card-divider::before,
        .theme-minimal_dark .card-divider::after { display:none !important; }
        .theme-minimal_dark .digit-text {
            font-weight: 700 !important;
            color: #FFFFFF !important;
            font-size: clamp(110px,28vh,380px) !important;
            text-shadow: none !important;
            letter-spacing: -0.03em !important;
        }
        .theme-minimal_dark #date-badge {
            font-weight: 500 !important;
            font-size: clamp(10px,1.1vw,15px) !important;
            letter-spacing: 0.05em !important;
            color: rgba(235,235,245,0.85) !important;
            background: rgba(44,44,46,0.9) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            backdrop-filter: blur(20px) !important;
        }
        .theme-minimal_dark #greeting-badge {
            color: rgba(235,235,245,0.5) !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        .theme-minimal_dark #ampm-badge {
            font-weight: 500 !important;
            font-size: 18px !important;
            color: rgba(235,235,245,0.6) !important;
            background: rgba(44,44,46,0.8) !important;
            border: 1px solid rgba(255,255,255,0.08) !important;
            border-radius: 8px !important;
            padding: 4px 10px !important;
            box-shadow: none !important;
        }
        .theme-minimal_dark .sep-dot {
            background: rgba(235,235,245,0.6) !important;
            box-shadow: none !important;
        }

        /* Dark Black Theme Overrides */
        .theme-dark_black #scene {
            background: #000000 !important;
        }
        .theme-dark_black #scene::before {
            display: none !important;
        }
        .theme-dark_black #branding-tag {
            display: none !important;
        }
        .theme-dark_black .flip-card {
            background: #0A0A0C !important;
            border: 1px solid rgba(255, 255, 255, 0.08) !important;
            border-radius: 20px;
            box-shadow:
                0 16px 40px rgba(0, 0, 0, 0.8),
                inset 0 1px 0 rgba(255, 255, 255, 0.06) !important;
        }
        .theme-dark_black .card-top,
        .theme-dark_black .flipper-top {
            background: rgba(255, 255, 255, 0.02) !important;
            border-radius: 20px 20px 0 0;
            border-bottom: 1px solid rgba(0, 0, 0, 0.5) !important;
        }
        .theme-dark_black .card-bottom,
        .theme-dark_black .flipper-bottom {
            background: rgba(0, 0, 0, 0.2) !important;
            border-radius: 0 0 20px 20px;
        }
        .theme-dark_black .card-divider {
            height: 1px !important;
            background: rgba(0, 0, 0, 0.7) !important;
            border: none !important;
            box-shadow: none !important;
        }
        .theme-dark_black .divider-dot,
        .theme-dark_black .card-divider::before,
        .theme-dark_black .card-divider::after {
            display: none !important;
        }
        .theme-dark_black .digit-text {
            font-family: "SF Pro Display", "Inter", sans-serif !important;
            font-weight: 800 !important;
            color: #FFFFFF !important;
            font-size: clamp(110px, 28vh, 380px) !important;
            text-shadow: 0 4px 15px rgba(0, 0, 0, 0.6) !important;
            letter-spacing: -0.03em !important;
        }
        .theme-dark_black #date-badge {
            font-family: "Inter", sans-serif !important;
            font-weight: 500 !important;
            font-size: clamp(10px, 1.1vw, 15px) !important;
            letter-spacing: 0.05em !important;
            color: #FFFFFF !important;
            background: rgba(28, 28, 30, 0.9) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 10px !important;
            box-shadow: none !important;
            backdrop-filter: blur(20px) !important;
        }
        .theme-dark_black #greeting-badge {
            font-family: "Inter", sans-serif !important;
            font-weight: 400 !important;
            color: rgba(255, 255, 255, 0.5) !important;
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
        }
        .theme-dark_black #ampm-badge {
            font-family: "Inter", sans-serif !important;
            font-weight: 500 !important;
            font-size: 18px !important;
            color: #FFFFFF !important;
            background: rgba(28, 28, 30, 0.8) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 8px !important;
            padding: 4px 10px !important;
            box-shadow: none !important;
        }
        .theme-dark_black .sep-dot {
            background: #FFFFFF !important;
            box-shadow: 0 0 8px rgba(255, 255, 255, 0.4) !important;
        }

        /* ═══ 10 PREMIUM CARD SHAPE STYLES ═══ */

        /* 1. Soft Squircle ⭐ (Apple Vision Pro — 28px ultra-smooth) */
        .shape-soft_squircle .flip-card { border-radius: clamp(24px, 3.5vh, 42px); }
        .shape-soft_squircle .card-top, .shape-soft_squircle .flipper-top { border-radius: clamp(24px,3.5vh,42px) clamp(24px,3.5vh,42px) 0 0; }
        .shape-soft_squircle .card-bottom, .shape-soft_squircle .flipper-bottom { border-radius: 0 0 clamp(24px,3.5vh,42px) clamp(24px,3.5vh,42px); }

        /* 2. Split Flip Card ⭐ (Classic retro airport flip) */
        .shape-split_flip .flip-card { border-radius: clamp(10px,1.6vh,20px); }
        .shape-split_flip .card-top, .shape-split_flip .flipper-top { border-radius: clamp(10px,1.6vh,20px) clamp(10px,1.6vh,20px) 0 0; }
        .shape-split_flip .card-bottom, .shape-split_flip .flipper-bottom { border-radius: 0 0 clamp(10px,1.6vh,20px) clamp(10px,1.6vh,20px); }
        .shape-split_flip .card-divider { height: 5px; box-shadow: 0 2px 8px rgba(0,0,0,1); }

        /* 3. Glass Floating Card ⭐ (Hexagonal angled sides) */
        .shape-glass_floating .flip-card {
            clip-path: polygon(12% 0, 88% 0, 100% 15%, 100% 85%, 88% 100%, 12% 100%, 0 85%, 0 15%);
            border-radius: 0;
        }
        .shape-glass_floating .card-top, .shape-glass_floating .flipper-top {
            clip-path: polygon(12% 0, 88% 0, 100% 30%, 100% 100%, 0 100%, 0 30%);
            border-radius: 0;
        }
        .shape-glass_floating .card-bottom, .shape-glass_floating .flipper-bottom {
            clip-path: polygon(0 0, 100% 0, 100% 70%, 88% 100%, 12% 100%, 0 70%);
            border-radius: 0;
        }

        /* 4. Capsule Card (Wide pill / stadium horizontal) */
        .shape-capsule .flip-card { border-radius: clamp(40px,8vh,90px); }
        .shape-capsule .card-top, .shape-capsule .flipper-top { border-radius: clamp(40px,8vh,90px) clamp(40px,8vh,90px) 0 0; }
        .shape-capsule .card-bottom, .shape-capsule .flipper-bottom { border-radius: 0 0 clamp(40px,8vh,90px) clamp(40px,8vh,90px); }

        /* 5. Ticket Card (Side notch cutouts) */
        .shape-ticket .flip-card {
            clip-path: polygon(
                0 8%, 4% 0, 96% 0, 100% 8%,
                100% 42%, 96% 50%, 100% 58%,
                100% 92%, 96% 100%, 4% 100%, 0 92%,
                0 58%, 4% 50%, 0 42%
            );
            border-radius: 0;
        }
        .shape-ticket .card-top, .shape-ticket .flipper-top {
            clip-path: polygon(0 16%, 4% 0, 96% 0, 100% 16%, 100% 84%, 96% 100%, 4% 100%, 0 84%);
            border-radius: 0;
        }
        .shape-ticket .card-bottom, .shape-ticket .flipper-bottom {
            clip-path: polygon(0 0, 4% 0, 96% 0, 100% 0, 100% 84%, 96% 100%, 4% 100%, 0 84%);
            border-radius: 0;
        }

        /* 6. Octagon Card ⭐ (Classic 8-corner chamfer) */
        .shape-octagon .flip-card {
            clip-path: polygon(18px 0, calc(100% - 18px) 0, 100% 18px, 100% calc(100% - 18px), calc(100% - 18px) 100%, 18px 100%, 0 calc(100% - 18px), 0 18px);
            border-radius: 0;
        }
        .shape-octagon .card-top, .shape-octagon .flipper-top {
            clip-path: polygon(18px 0, calc(100% - 18px) 0, 100% 18px, 100% 100%, 0 100%, 0 18px);
            border-radius: 0;
        }
        .shape-octagon .card-bottom, .shape-octagon .flipper-bottom {
            clip-path: polygon(0 0, 100% 0, 100% calc(100% - 18px), calc(100% - 18px) 100%, 18px 100%, 0 calc(100% - 18px));
            border-radius: 0;
        }

        /* 7. Fold Corner Card (Top-right folded page corner) */
        .shape-fold_corner .flip-card {
            clip-path: polygon(0 0, calc(100% - 28px) 0, 100% 28px, 100% 100%, 0 100%);
            border-radius: 0;
        }
        .shape-fold_corner .card-top, .shape-fold_corner .flipper-top {
            clip-path: polygon(0 0, calc(100% - 28px) 0, 100% 28px, 100% 100%, 0 100%);
            border-radius: 0;
        }
        .shape-fold_corner .card-bottom, .shape-fold_corner .flipper-bottom {
            border-radius: 0;
        }

        /* 8. Neo Rounded Rectangle ⭐ (Modern 16px clean) */
        .shape-neo_rounded .flip-card { border-radius: clamp(14px, 2vh, 24px); }
        .shape-neo_rounded .card-top, .shape-neo_rounded .flipper-top { border-radius: clamp(14px,2vh,24px) clamp(14px,2vh,24px) 0 0; }
        .shape-neo_rounded .card-bottom, .shape-neo_rounded .flipper-bottom { border-radius: 0 0 clamp(14px,2vh,24px) clamp(14px,2vh,24px); }

        /* 9. Stadium Vertical (Extreme top/bottom pill rounding) */
        .shape-stadium .flip-card { border-radius: clamp(60px,14vh,140px) / clamp(40px,6vh,80px); }
        .shape-stadium .card-top, .shape-stadium .flipper-top { border-radius: clamp(60px,14vh,140px) clamp(60px,14vh,140px) 0 0 / clamp(40px,6vh,80px) clamp(40px,6vh,80px) 0 0; }
        .shape-stadium .card-bottom, .shape-stadium .flipper-bottom { border-radius: 0 0 clamp(60px,14vh,140px) clamp(60px,14vh,140px) / 0 0 clamp(40px,6vh,80px) clamp(40px,6vh,80px); }

        /* 10. Premium Bevel Card ⭐ (Asymmetric diagonal TL + BR) */
        .shape-premium_bevel .flip-card {
            clip-path: polygon(24px 0, 100% 0, 100% calc(100% - 24px), calc(100% - 24px) 100%, 0 100%, 0 24px);
            border-radius: 0;
        }
        .shape-premium_bevel .card-top, .shape-premium_bevel .flipper-top {
            clip-path: polygon(24px 0, 100% 0, 100% 100%, 0 100%, 0 24px);
            border-radius: 0;
        }
        .shape-premium_bevel .card-bottom, .shape-premium_bevel .flipper-bottom {
            clip-path: polygon(0 0, 100% 0, 100% calc(100% - 24px), calc(100% - 24px) 100%, 0 100%);
            border-radius: 0;
        }

        .theme-custom {
            --vignette-color: rgba(255, 255, 255, 0.02);
            --card-bg: var(--custom-card-color, #1e1e22);
            --card-border: var(--custom-border-color, rgba(255,255,255,0.2));
            --card-top-bg: linear-gradient(180deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.015) 100%);
            --card-bot-bg: linear-gradient(180deg, rgba(0,0,0,0.3) 0%, rgba(0,0,0,0.1) 100%);
            --divider-line: #000000;
            --pin-bg: var(--custom-accent-color, #d4af37);
            --digit-color: var(--custom-digit-color, #ffffff);
            --digit-shadow: 0 2px 10px rgba(0,0,0,0.9);
            --dot-bg: var(--custom-accent-color, #d4af37);
            --dot-shadow: 0 0 10px var(--custom-accent-color, rgba(255,255,255,0.4));
            --accent-color: var(--custom-accent-color, #d4af37);
            --badge-color: var(--custom-digit-color, #ffffff);
            --badge-bg: rgba(20,20,24,0.85);
            --badge-border: var(--custom-border-color, rgba(255,255,255,0.2));
            --branding-color: var(--custom-accent-color, rgba(255,255,255,0.4));
        }

        .hide-seconds #fc-s, .hide-seconds #sep-s { display:none !important; }
        .hide-date #date-badge { display:none !important; }
        .hide-greeting #greeting-badge { display:none !important; }
    </style>
</head>
<body class="theme-classic_retro">

<div id="scene">
    <button id="close-btn" onclick="forceClose()" title="Close Screensaver">✕</button>

    <div id="clock-container">
        <div id="greeting-badge">GOOD MORNING</div>

        <div class="clock-row" id="clock-row">
            <!-- Hours Card -->
            <div class="flip-card" id="fc-h">
                <div class="card-half card-top"><div class="digit-wrapper"><span class="digit-text" id="fc-h-top">00</span></div></div>
                <div class="card-half card-bottom"><div class="digit-wrapper"><span class="digit-text" id="fc-h-bot">00</span></div></div>
                <div class="card-divider"></div>
            </div>

            <div class="sep" id="sep-m"><div class="sep-dot"></div><div class="sep-dot"></div></div>

            <!-- Minutes Card -->
            <div class="flip-card" id="fc-m">
                <div class="card-half card-top"><div class="digit-wrapper"><span class="digit-text" id="fc-m-top">00</span></div></div>
                <div class="card-half card-bottom"><div class="digit-wrapper"><span class="digit-text" id="fc-m-bot">00</span></div></div>
                <div class="card-divider"></div>
            </div>

            <div class="sep" id="sep-s"><div class="sep-dot"></div><div class="sep-dot"></div></div>

            <!-- Seconds Card -->
            <div class="flip-card" id="fc-s">
                <span class="ampm-badge" id="ampm-badge"></span>
                <div class="card-half card-top"><div class="digit-wrapper"><span class="digit-text" id="fc-s-top">00</span></div></div>
                <div class="card-half card-bottom"><div class="digit-wrapper"><span class="digit-text" id="fc-s-bot">00</span></div></div>
                <div class="card-divider"></div>
            </div>
        </div>

        <div id="date-badge"></div>
    </div>

    <div id="branding-tag">FLIP CLOCK SCREENSAVER</div>
</div>

<script>
let config = window.screensaverConfig || {};
let themeName = config.theme || 'classic_retro';
let rawShape = config.card_shape || 'squircle';
let legacyMap = { 'soft_squircle': 'squircle', 'neo_rounded': 'rounded_rectangle', 'glass_floating': 'card', 'fold_corner': 'notched', 'split_flip': 'rectangle', 'premium_bevel': 'beveled' };
let cardShape = legacyMap[rawShape] || rawShape;
let hourFormat = config.format || '12';
let showSeconds = config.show_seconds !== 'false';
let showDate = config.show_date !== 'false';
let showDay = config.show_day !== 'false';
let showGreeting = config.show_greeting !== 'false';
let userName = config.user_name || '';
let clockScale = parseFloat(config.size || '1.0');
let customCredit = config.custom_credit || 'FLIP CLOCK SCREENSAVER';
let digitFont = config.digit_font || 'Inter';
let labelFont = config.label_font || 'Cinzel';
let customBgColor = config.custom_bg_color || '#000000';
let customCardColor = config.custom_card_color || '#1e1e22';
let customDigitColor = config.custom_digit_color || '#ffffff';
let customAccentColor = config.custom_accent_color || '#d4af37';
let customBorderColor = config.custom_border_color || '#333333';

function applyConfiguration() {
    document.documentElement.style.setProperty('--digit-font', `'${digitFont}', system-ui, sans-serif`);
    document.documentElement.style.setProperty('--label-font', `'${labelFont}', serif`);

    document.documentElement.style.setProperty('--custom-bg-color', customBgColor);
    document.documentElement.style.setProperty('--custom-card-color', customCardColor);
    document.documentElement.style.setProperty('--custom-digit-color', customDigitColor);
    document.documentElement.style.setProperty('--custom-accent-color', customAccentColor);
    document.documentElement.style.setProperty('--custom-border-color', customBorderColor);

    document.body.className = `theme-${themeName}`;

    const scene = document.getElementById('scene');
    if (scene) {
        scene.className = `shape-${cardShape}`;
        if (!showSeconds) scene.classList.add('hide-seconds');
        else scene.classList.remove('hide-seconds');

        if (!showDate && !showDay) scene.classList.add('hide-date-badge');
        else scene.classList.remove('hide-date-badge');

        if (!showGreeting) scene.classList.add('hide-greeting');
        else scene.classList.remove('hide-greeting');
    }

    const container = document.getElementById('clock-container');
    if (container && clockScale !== 1.0) {
        container.style.transform = `scale(${clockScale})`;
    }

    const brandEl = document.getElementById('branding-tag');
    if (brandEl) brandEl.textContent = customCredit;

    if (themeName === 'custom') {
        scene.style.background = customBgColor;
    } else if (themeName === 'minimal_light') {
        scene.style.background = '#f1f5f9';
    } else if (themeName === 'swiss_minimalist') {
        scene.style.background = '#000000';
    } else if (themeName === 'dark_black') {
        scene.style.background = '#000000';
    } else if (themeName === 'minimal_dark') {
        scene.style.background = '#111111';
    } else {
        scene.style.background = '#000000';
    }
}

function updateGreeting() {
    const h = new Date().getHours();
    let period = 'MORNING';
    if (h >= 12 && h < 17) period = 'AFTERNOON';
    else if (h >= 17 && h < 22) period = 'EVENING';
    else if (h >= 22 || h < 5) period = 'NIGHT';

    const gEl = document.getElementById('greeting-badge');
    if (!gEl) return;

    const nameStr = userName ? userName.trim().toUpperCase() : '';
    const text = nameStr ? `GOOD ${period}, ${nameStr}` : `GOOD ${period}`;
    gEl.innerHTML = `<span class="badge-ornament">✦</span><span class="greeting-text">${text}</span><span class="badge-ornament">✦</span>`;
}

function updateDate() {
    const now = new Date();
    const days   = ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY'];
    const months = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'];
    const b = document.getElementById('date-badge');
    if (!b) return;

    const dayName = days[now.getDay()];
    const dateNum = String(now.getDate()).padStart(2, '0');
    const monthName = months[now.getMonth()];
    const yearNum = now.getFullYear();

    let content = '';
    if (showDay) {
        content += `<span class="date-segment date-dayname">${dayName}</span>`;
    }
    if (showDay && showDate) {
        content += `<span class="date-sep">◆</span>`;
    }
    if (showDate) {
        content += `<span class="date-segment date-num">${dateNum}</span>` +
                   `<span class="date-segment date-month">${monthName}</span>` +
                   `<span class="date-segment date-year">${yearNum}</span>`;
    }
    b.innerHTML = content;
}

let pH = -1, pM = -1, pS = -1;
function updateFlip() {
    const now = new Date();
    let h = now.getHours();
    const m = now.getMinutes();
    const s = now.getSeconds();

    let ampmText = '';
    if (hourFormat === '12') {
        ampmText = h >= 12 ? 'PM' : 'AM';
        h = h % 12;
        if (h === 0) h = 12;
    }

    const ampmEl = document.getElementById('ampm-badge');
    if (ampmEl) ampmEl.textContent = ampmText;

    const p = n => String(n).padStart(2,'0');
    if (h !== pH) { doFlip('fc-h', p(h)); pH = h; }
    if (m !== pM) { doFlip('fc-m', p(m)); pM = m; }
    if (showSeconds && s !== pS) { doFlip('fc-s', p(s)); pS = s; }
}

function doFlip(id, val) {
    const t = document.getElementById(id+'-top');
    const b = document.getElementById(id+'-bot');
    const c = document.getElementById(id);
    if (!t||!b||!c) return;
    const prev = t.textContent;
    if (prev === val) return;

    const ft = document.createElement('div');
    ft.className = 'flipper flipper-top';
    ft.innerHTML = '<div class="digit-wrapper"><span class="digit-text">'+prev+'</span></div>';
    const fb = document.createElement('div');
    fb.className = 'flipper flipper-bottom';
    fb.innerHTML = '<div class="digit-wrapper"><span class="digit-text">'+val+'</span></div>';

    c.appendChild(ft); c.appendChild(fb);
    requestAnimationFrame(function() { ft.classList.add('flip-top-out'); fb.classList.add('flip-bottom-in'); });
    t.textContent = val; b.textContent = val;
    setTimeout(function() { ft.remove(); fb.remove(); }, 650);
}

function forceClose() {
    try {
        if (window.webkit && window.webkit.messageHandlers && window.webkit.messageHandlers.screensaverExit) {
            window.webkit.messageHandlers.screensaverExit.postMessage("forceClose");
        }
    } catch(e) {}
    window.close();
    try { document.title = 'EXIT_SCREENSAVER'; } catch(e) {}
}

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') forceClose();
});

window.addEventListener('load', function() {
    applyConfiguration();
    updateGreeting();
    updateDate(); updateFlip();
    setInterval(updateFlip, 1000);
    setInterval(updateGreeting, 10000);
    setInterval(updateDate, 30000);
});
</script>
</body>
</html>"""

def get_html_content(html_path_arg=None):
    candidates = []
    if html_path_arg and os.path.exists(html_path_arg):
        candidates.append(html_path_arg)
        
    script_dir = os.path.dirname(os.path.realpath(__file__))
    candidates.extend([
        os.path.join(script_dir, "clock.html"),
        os.path.join(script_dir, "index.html"),
        "/usr/share/flipclock/clock.html",
        "/usr/share/flipclock/index.html",
        "/usr/local/share/flipclock/clock.html",
        "/usr/local/share/flipclock/index.html",
        os.path.expanduser("~/.local/share/flipclock/clock.html"),
        os.path.expanduser("~/.local/share/flipclock/index.html"),
        os.path.join(os.getcwd(), "clock.html"),
        os.path.join(os.getcwd(), "index.html")
    ])
    
    for candidate in candidates:
        if candidate and os.path.exists(candidate):
            try:
                with open(candidate, 'r', encoding='utf-8') as f:
                    return f.read(), os.path.abspath(os.path.dirname(candidate))
            except Exception:
                pass
                
    fallback_dir = "/usr/share/flipclock" if os.path.exists("/usr/share/flipclock") else os.getcwd()
    return DEFAULT_HTML_CONTENT, fallback_dir


def get_asset_image_path(filename):
    script_dir = os.path.dirname(os.path.realpath(__file__))
    candidates = [
        os.path.join(script_dir, "screenshots", filename),
        os.path.join(script_dir, "assets", filename),
        os.path.join(script_dir, filename),
        os.path.join("/usr/share/flipclock/screenshots", filename),
        os.path.join("/usr/share/flipclock/assets", filename),
        os.path.join("/usr/share/flipclock", filename),
        os.path.join("/usr/local/share/flipclock/screenshots", filename),
        os.path.join("/usr/local/share/flipclock/assets", filename),
        os.path.join("/usr/local/share/flipclock", filename),
        os.path.join(os.getcwd(), "screenshots", filename),
        os.path.join(os.getcwd(), "assets", filename),
    ]
    for c in candidates:
        if c and os.path.exists(c):
            return c
    return None


class FlipClockWindow(Gtk.Window):
    """Fullscreen GTK window hosting the WebKit flip clock."""
    def __init__(self, html_path, monitor_idx, config_params):
        super().__init__(title=f"Flip Clock - Screen {monitor_idx}")
        self.set_decorated(False)
        self.set_keep_above(True)
        self.set_can_focus(True)
        
        self.initial_x = None
        self.initial_y = None
        
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(b"window { background-color: black; }")
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )
        
        display = Gdk.Display.get_default()
        monitor = None
        if display and hasattr(display, 'get_n_monitors') and monitor_idx < display.get_n_monitors():
            monitor = display.get_monitor(monitor_idx)
            
        if monitor:
            geom = monitor.get_geometry()
            self.move(geom.x, geom.y)
            self.resize(geom.width, geom.height)
        else:
            self.maximize()
        
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK | 
                        Gdk.EventMask.BUTTON_PRESS_MASK | 
                        Gdk.EventMask.KEY_PRESS_MASK |
                        Gdk.EventMask.SCROLL_MASK |
                        Gdk.EventMask.TOUCH_MASK)
        
        # WebKit WebView
        self.webview = WebKit2.WebView()
        if hasattr(self.webview, 'set_background_color'):
            self.webview.set_background_color(Gdk.RGBA(0, 0, 0, 1.0))
            
        settings = self.webview.get_settings()
        settings.set_enable_javascript(True)
        if hasattr(settings, 'set_allow_file_access_from_file_urls'):
            settings.set_allow_file_access_from_file_urls(True)
        if hasattr(settings, 'set_allow_universal_access_from_file_urls'):
            settings.set_allow_universal_access_from_file_urls(True)
            
        self.webview.add_events(Gdk.EventMask.POINTER_MOTION_MASK | 
                                Gdk.EventMask.BUTTON_PRESS_MASK | 
                                Gdk.EventMask.KEY_PRESS_MASK |
                                Gdk.EventMask.SCROLL_MASK |
                                Gdk.EventMask.TOUCH_MASK)
        
        # Guard against WebKit load failures
        self.webview.connect("load-failed", self.on_load_failed)
        
        # DOM script exit trigger listener
        ucm = self.webview.get_user_content_manager()
        ucm.register_script_message_handler("screensaverExit")
        ucm.connect("script-message-received::screensaverExit", self.on_script_message)
        
        self.add(self.webview)
        
        html_content, base_dir = get_html_content(html_path)
        if not html_content:
            print("Error: Could not locate clock.html or index.html")
            sys.exit(1)
            
        fmt = config_params.get('hour_format', '12')
        size = config_params.get('clock_size', '1.0')
        speed = config_params.get('animation_speed', 500)
        theme = config_params.get('theme', 'classic_retro')
        show_seconds = str(config_params.get('show_seconds', 'true')).lower()
        show_date = str(config_params.get('show_date', 'true')).lower()
        show_day = str(config_params.get('show_day', 'true')).lower()
        show_greeting = str(config_params.get('show_greeting', 'true')).lower()
        user_name = config_params.get('user_name', '').replace("'", "\\'")
        custom_credit = config_params.get('custom_credit', 'FLIP CLOCK SCREENSAVER')
        digit_font = config_params.get('digit_font', 'Inter').replace("'", "\\'")
        label_font = config_params.get('label_font', 'Cinzel').replace("'", "\\'")
        custom_bg_color = config_params.get('custom_bg_color', '#000000').replace("'", "\\'")
        custom_card_color = config_params.get('custom_card_color', '#1f1f1f').replace("'", "\\'")
        custom_digit_color = config_params.get('custom_digit_color', '#ffffff').replace("'", "\\'")
        custom_accent_color = config_params.get('custom_accent_color', '#d4af37').replace("'", "\\'")
        custom_border_color = config_params.get('custom_border_color', '#333333').replace("'", "\\'")
        raw_shape = config_params.get('card_shape', 'squircle')
        legacy_shape_map = {'soft_squircle': 'squircle', 'neo_rounded': 'rounded_rectangle', 'glass_floating': 'card', 'fold_corner': 'notched', 'split_flip': 'rectangle', 'premium_bevel': 'beveled'}
        card_shape = legacy_shape_map.get(raw_shape, raw_shape)
        
        config_script = f"<script>window.screensaverConfig = {{ monitor: '{monitor_idx}', format: '{fmt}', size: '{size}', speed: '{speed}', theme: '{theme}', card_shape: '{card_shape}', show_seconds: '{show_seconds}', show_date: '{show_date}', show_day: '{show_day}', show_greeting: '{show_greeting}', user_name: '{user_name}', custom_credit: '{custom_credit}', digit_font: '{digit_font}', label_font: '{label_font}', custom_bg_color: '{custom_bg_color}', custom_card_color: '{custom_card_color}', custom_digit_color: '{custom_digit_color}', custom_accent_color: '{custom_accent_color}', custom_border_color: '{custom_border_color}' }};</script>"
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", f"{config_script}</head>")
        else:
            html_content = config_script + html_content
            
        base_uri = "file://" + base_dir + "/"
        self.webview.load_html(html_content, base_uri)
        
        self.connect("destroy", lambda w: Gtk.main_quit() if Gtk.main_level() > 0 else None)
        self.connect("key-press-event", self.on_key_event)
        self.connect("button-press-event", self.on_input_event)
        self.connect("motion-notify-event", self.on_motion_event)
        self.connect("scroll-event", self.on_input_event)
        
        self.webview.connect("key-press-event", self.on_key_event)
        self.webview.connect("button-press-event", self.on_input_event)
        self.webview.connect("motion-notify-event", self.on_motion_event)
        self.webview.connect("scroll-event", self.on_input_event)
        
        self.show_all()
        self.present_with_time(Gdk.CURRENT_TIME)
        self.present()
        self.webview.grab_focus()

        if display and hasattr(display, 'get_n_monitors') and monitor_idx < display.get_n_monitors():
            self.fullscreen_on_monitor(self.get_screen(), monitor_idx)
        else:
            self.fullscreen()

    def on_load_failed(self, webview, load_event, failing_uri, error):
        print(f"WebView load failed ({failing_uri}): {error}")
        Gtk.main_quit()
        return True

    def on_script_message(self, ucm, result):
        reason = "DOM trigger"
        try:
            js_val = result.get_js_value()
            if js_val:
                reason = js_val.to_string()
        except Exception:
            pass
            
        print(f"Script message exit trigger ({reason}). Exiting.")
        Gtk.main_quit()

    def on_key_event(self, widget, event):
        global key_input_enabled
        if key_input_enabled:
            print(f"Key press event: {event.keyval}. Exiting.")
            Gtk.main_quit()
        return True

    def on_input_event(self, widget, event):
        global mouse_input_enabled
        if mouse_input_enabled:
            print(f"Input event: {event.type}. Exiting.")
            Gtk.main_quit()
        return True

    def on_motion_event(self, widget, event):
        global mouse_input_enabled
        
        x = getattr(event, 'x_root', None)
        y = getattr(event, 'y_root', None)
        
        if x is None or y is None:
            display = Gdk.Display.get_default()
            if display:
                seat = display.get_default_seat()
                if seat:
                    pointer = seat.get_pointer()
                    if pointer:
                        _, x, y = pointer.get_position()
                        
        if x is None or y is None:
            return True
        
        if self.initial_x is None or self.initial_y is None or not mouse_input_enabled:
            self.initial_x = x
            self.initial_y = y
            return True
            
        dist = math.sqrt((x - self.initial_x)**2 + (y - self.initial_y)**2)
        if dist > exit_threshold:
            print(f"Mouse moved {dist:.1f}px. Exiting.")
            Gtk.main_quit()
        return True
class FlipClockSettingsWindow(Gtk.Window):
    """Modern configuration GUI window for Flip Clock Screensaver."""
    def __init__(self, manager):
        super().__init__(title="Flip Clock Settings")
        self.manager = manager
        self.set_default_size(680, 720)
        self.set_default_size(680, 720)
        self.set_border_width(0)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        # Apply custom GTK3 CSS for professional modern dark theme layout
        css_provider = Gtk.CssProvider()
        css_data = b"""
        window {
            background-color: #121215;
            color: #e4e4e7;
            font-family: 'Inter', system-ui, sans-serif;
        }
        headerbar {
            background-color: #18181c;
            background-image: linear-gradient(180deg, #222226 0%, #18181c 100%);
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
            color: #ffffff;
            box-shadow: none;
        }
        headerbar .title {
            color: #ffffff;
            font-weight: bold;
        }
        headerbar .subtitle {
            color: #d4af37;
            font-size: 11px;
        }
        headerbar button {
            background: rgba(255, 255, 255, 0.08);
            color: #ffffff;
            border: 1px solid rgba(255, 255, 255, 0.12);
            border-radius: 6px;
        }
        headerbar button:hover {
            background: rgba(255, 255, 255, 0.16);
            color: #ffffff;
        }
        .header-box {
            background-color: #1e1e24;
            background-image: linear-gradient(to bottom, #1e1e24, #141418);
            padding: 14px 20px;
            border-bottom: 1px solid rgba(255,255,255,0.08);
        }
        .app-title {
            font-size: 20px;
            font-weight: 800;
            color: #ffffff;
        }
        .app-subtitle {
            font-size: 12px;
            font-weight: 700;
            color: #d4af37;
            letter-spacing: 0.05em;
        }
        .section-box {
            background-color: #18181c;
            border: 1px solid rgba(255,255,255,0.07);
            border-radius: 12px;
            padding: 12px 18px;
            margin: 4px 14px;
        }
        .section-header {
            font-size: 12px;
            font-weight: 800;
            color: #d4af37;
            letter-spacing: 0.1em;
            margin-bottom: 12px;
        }
        .field-label {
            font-size: 15px;
            font-weight: 600;
            color: #e4e4e7;
            font-size: 15px;
            font-weight: 600;
            color: #e4e4e7;
        }
        combobox {
            background-color: #22222a;
            background-image: none;
            border: 1px solid rgba(212, 175, 55, 0.7);
            border-radius: 10px;
            box-shadow: none;
            min-height: 46px;
            min-width: 260px;
        }
        combobox button {
            background-color: transparent;
            background-image: none;
            color: #ffffff;
            border: none;
            padding: 0 16px;
            font-size: 15px;
            font-weight: 600;
            box-shadow: none;
            min-height: 44px;
        }
        combobox button:hover {
            background-color: #2e2e38;
        }
        combobox cellview {
            color: #ffffff;
            background-color: transparent;
            font-weight: 600;
            font-size: 15px;
        }
        combobox arrow {
            color: #d4af37;
            min-width: 16px;
            min-height: 16px;
        }
        menu {
            background-color: #16161b;
            border: 1px solid #d4af37;
            border-radius: 10px;
            padding: 6px 0px;
            color: #ffffff;
        }
        menuitem {
            color: #f4f4f5;
            background-color: #16161b;
            padding: 10px 18px;
            font-weight: 600;
            font-size: 15px;
        }
        menuitem:hover, menuitem:selected {
            background-color: #d4af37;
            color: #000000;
            font-weight: 800;
        }
        .custom-dark-dialog {
            background-color: #141419;
            border: 1px solid rgba(212, 175, 55, 0.45);
            border-radius: 12px;
        }
        .dialog-title {
            font-size: 16px;
            font-weight: 800;
            color: #fef08a;
            letter-spacing: 0.02em;
        }
        .dialog-secondary {
            font-size: 13px;
            font-weight: 500;
            color: #d4d4d8;
        }
        .btn-primary {
            background-color: #e5c158;
            background-image: linear-gradient(to bottom, #e5c158, #c8a830);
            color: #000000;
            font-weight: 800;
            font-size: 14px;
            border-radius: 8px;
            padding: 10px 24px;
            border: none;
        }
        .btn-primary:hover {
            background-color: #f0d860;
            background-image: linear-gradient(to bottom, #f0d860, #d4af37);
        }
        .btn-secondary {
            background-color: #2563eb;
            background-image: linear-gradient(to bottom, #3b82f6, #1d4ed8);
            color: #ffffff;
            font-weight: 800;
            font-size: 14px;
            border-radius: 8px;
            padding: 10px 20px;
            border: none;
        }
        .btn-secondary:hover {
            background-color: #60a5fa;
            background-image: linear-gradient(to bottom, #60a5fa, #2563eb);
            color: #ffffff;
        }
        .btn-reset {
            background-color: #ef4444;
            background-image: linear-gradient(to bottom, #ef4444, #dc2626);
            color: #ffffff;
            font-weight: 700;
            font-size: 14px;
            border-radius: 8px;
            padding: 10px 18px;
            border: none;
        }
        .btn-reset:hover {
            background-color: #f87171;
            background-image: linear-gradient(to bottom, #f87171, #ef4444);
        }
        .theme-tile-btn {
            background-color: #22222a;
            border: 1px solid rgba(255, 255, 255, 0.18);
            border-radius: 8px;
            padding: 7px 12px;
            color: #ffffff;
            font-size: 13px;
            font-weight: 600;
        }
        .theme-tile-btn:hover {
            background-color: #2e2e3a;
            border-color: #d4af37;
        }
        .theme-tile-btn.active {
            background-color: #e5c158;
            background-image: linear-gradient(to bottom, #e5c158, #c8a830);
            color: #000000;
            border-color: #ffffff;
            font-weight: 800;
        }
        .branding-footer {
            font-size: 11px;
            font-weight: 600;
            color: #a1a1aa;
            letter-spacing: 0.08em;
        }
        """
        css_provider.load_from_data(css_data)
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_USER
        )

        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title("Flip Clock Settings")
        hb.set_subtitle(f"Executive Edition v{APP_VERSION}")
        self.set_titlebar(hb)

        main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.add(main_box)

        # Header Banner
        header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=4)
        header_box.get_style_context().add_class("header-box")
        
        lbl_title = Gtk.Label(label="Flip Clock Screensaver")
        lbl_title.get_style_context().add_class("app-title")
        lbl_title.set_xalign(0)
        header_box.pack_start(lbl_title, False, False, 0)
        
        lbl_sub = Gtk.Label(label="✦ Executive Color Collections • High Aesthetic Desktop Clock")
        lbl_sub.get_style_context().add_class("app-subtitle")
        lbl_sub.set_xalign(0)
        header_box.pack_start(lbl_sub, False, False, 0)
        
        main_box.pack_start(header_box, False, False, 0)

        # Scrollable container for settings sections
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        main_box.pack_start(scrolled, True, True, 0)

        content_vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        content_vbox.set_margin_top(4)
        content_vbox.set_margin_bottom(8)
        content_vbox.set_valign(Gtk.Align.START)
        scrolled.add(content_vbox)

        # SECTION 1: THEMES & VISUAL PRESETS
        sec_theme = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        sec_theme.get_style_context().add_class("section-box")
        
        lbl_sec1 = Gtk.Label(label="Executive Theme & Preset Collection")
        lbl_sec1.get_style_context().add_class("section-header")
        lbl_sec1.set_xalign(0)
        sec_theme.pack_start(lbl_sec1, False, False, 0)

        grid_t = Gtk.Grid()
        grid_t.set_column_spacing(16)
        grid_t.set_row_spacing(10)
        sec_theme.pack_start(grid_t, False, False, 0)

        lbl_t_choice = Gtk.Label(label="Active Theme Preset:")
        lbl_t_choice.get_style_context().add_class("field-label")
        lbl_t_choice.set_xalign(0)
        grid_t.attach(lbl_t_choice, 0, 0, 1, 1)

        self.combo_theme = Gtk.ComboBoxText()
        self.combo_theme.set_wrap_width(2)
        for t_key, t_info in PRESET_THEMES.items():
            self.combo_theme.append(t_key, t_info["name"])

        cur_theme = self.manager.config.get('theme', 'luxury_black_gold')
        self.combo_theme.set_active_id(cur_theme if cur_theme in PRESET_THEMES else 'luxury_black_gold')
        self.combo_theme.set_hexpand(True)
        self.combo_theme.connect("changed", self.on_theme_combo_changed)
        grid_t.attach(self.combo_theme, 1, 0, 1, 1)

        self.img_theme_preview = Gtk.Image()
        self.img_theme_preview.set_margin_top(8)
        self.img_theme_preview.set_margin_bottom(8)
        self.img_theme_preview.set_halign(Gtk.Align.CENTER)
        sec_theme.pack_start(self.img_theme_preview, False, False, 0)

        content_vbox.pack_start(sec_theme, False, False, 0)

        # SECTION 1.5: CUSTOM COLORS & PALETTE (Compact & Minimal Swatches)
        sec_colors = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sec_colors.get_style_context().add_class("section-box")
        
        lbl_sec_c = Gtk.Label(label="Color Palette & Fine-Tuning")
        lbl_sec_c.get_style_context().add_class("section-header")
        lbl_sec_c.set_xalign(0)
        sec_colors.pack_start(lbl_sec_c, False, False, 0)

        grid_c = Gtk.Grid()
        grid_c.set_column_spacing(24)
        grid_c.set_row_spacing(12)
        sec_colors.pack_start(grid_c, False, False, 0)

        # Helper function for compact color swatch button
        def create_color_row(label_text, config_key, default_hex, grid_obj, left_col, top_row):
            lbl = Gtk.Label(label=label_text)
            lbl.get_style_context().add_class("field-label")
            lbl.set_xalign(0)
            grid_obj.attach(lbl, left_col, top_row, 1, 1)

            btn = Gtk.ColorButton()
            btn.set_rgba(hex_to_rgba(self.manager.config.get(config_key, default_hex)))
            btn.set_size_request(80, 32)
            btn.set_halign(Gtk.Align.END)
            btn.connect("color-set", self.on_color_button_changed)
            grid_obj.attach(btn, left_col + 1, top_row, 1, 1)
            return btn

        self.btn_bg_color = create_color_row("Background:", 'custom_bg_color', '#000000', grid_c, 0, 0)
        self.btn_card_color = create_color_row("Card Fill:", 'custom_card_color', '#1C1C1E', grid_c, 0, 1)
        self.btn_digit_color = create_color_row("Digit Text:", 'custom_digit_color', '#F5F5F7', grid_c, 0, 2)
        self.btn_accent_color = create_color_row("Accent & Pin:", 'custom_accent_color', '#D4AF37', grid_c, 0, 3)
        self.btn_border_color = create_color_row("Card Border:", 'custom_border_color', '#4A4A4A', grid_c, 0, 4)

        # Render initial live swatches and theme screenshot preview
        self.on_theme_combo_changed(self.combo_theme)

        content_vbox.pack_start(sec_colors, False, False, 0)

        # SECTION 1.6: TYPOGRAPHY & FONT STYLING
        sec_fonts = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sec_fonts.get_style_context().add_class("section-box")
        
        lbl_sec_f = Gtk.Label(label="Typography & Font Customization")
        lbl_sec_f.get_style_context().add_class("section-header")
        lbl_sec_f.set_xalign(0)
        sec_fonts.pack_start(lbl_sec_f, False, False, 0)

        grid_f = Gtk.Grid()
        grid_f.set_column_spacing(24)
        grid_f.set_row_spacing(6)
        sec_fonts.pack_start(grid_f, False, False, 0)

        lbl_dfont = Gtk.Label(label="Clock Digits Font:")
        lbl_dfont.get_style_context().add_class("field-label")
        lbl_dfont.set_xalign(0)
        lbl_dfont.set_valign(Gtk.Align.CENTER)
        grid_f.attach(lbl_dfont, 0, 0, 1, 1)

        font_options = [
            ("Cinzel", "Cinzel (Serif)"),
            ("Inter", "Inter (Sans)"),
            ("Roboto", "Roboto (Clean)"),
            ("Orbitron", "Orbitron (Digital LED)"),
            ("Outfit", "Outfit (Bold Sans)"),
            ("Oswald", "Oswald (Condensed)"),
            ("Courier Prime", "Courier (Vintage Mono)"),
            ("Rajdhani", "Rajdhani (Tech Digits)"),
            ("Exo 2", "Exo 2 (Geometric Tech)"),
            ("Oxanium", "Oxanium (Modern Display)"),
            ("Bebas Neue", "Bebas Neue (Tall Headline)"),
            ("IBM Plex Sans", "IBM Plex Sans (Pro Dashboard)"),
            ("Audiowide", "Audiowide (Futuristic LCD Clock)"),
            ("Teko", "Teko (Ultra-Tall Flip Digits)"),
            ("Share Tech Mono", "Share Tech Mono (Tech Clock)"),
            ("VT323", "VT323 (Retro Digital LED Clock)"),
            ("Chakra Petch", "Chakra Petch (Cyber Clock)"),
            ("Michroma", "Michroma (Cockpit Clock)")
        ]

        self.combo_digit_font = Gtk.ComboBoxText()
        self.combo_digit_font.set_wrap_width(2)
        for f_id, f_label in font_options:
            self.combo_digit_font.append(f_id, f_label)

        cur_dfont = self.manager.config.get('digit_font', 'Cinzel')
        self.combo_digit_font.set_active_id(cur_dfont if any(cur_dfont == f[0] for f in font_options) else "Cinzel")
        self.combo_digit_font.set_hexpand(True)
        self.combo_digit_font.set_valign(Gtk.Align.CENTER)
        grid_f.attach(self.combo_digit_font, 0, 1, 1, 1)

        lbl_lfont = Gtk.Label(label="Badges & Greetings Font:")
        lbl_lfont.get_style_context().add_class("field-label")
        lbl_lfont.set_xalign(0)
        lbl_lfont.set_valign(Gtk.Align.CENTER)
        grid_f.attach(lbl_lfont, 1, 0, 1, 1)

        self.combo_label_font = Gtk.ComboBoxText()
        self.combo_label_font.set_wrap_width(2)
        for f_id, f_label in font_options:
            self.combo_label_font.append(f_id, f_label)

        cur_lfont = self.manager.config.get('label_font', 'Cinzel')
        self.combo_label_font.set_active_id(cur_lfont if any(cur_lfont == f[0] for f in font_options) else "Cinzel")
        self.combo_label_font.set_hexpand(True)
        self.combo_label_font.set_valign(Gtk.Align.CENTER)
        grid_f.attach(self.combo_label_font, 1, 1, 1, 1)

        content_vbox.pack_start(sec_fonts, False, False, 0)

        # SECTION 2: PERSONALIZATION & GREETINGS
        sec_greet = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sec_greet.get_style_context().add_class("section-box")
        
        lbl_sec_g = Gtk.Label(label="Personalization & Greetings")
        lbl_sec_g.get_style_context().add_class("section-header")
        lbl_sec_g.set_xalign(0)
        sec_greet.pack_start(lbl_sec_g, False, False, 0)

        grid_g = Gtk.Grid()
        grid_g.set_column_spacing(16)
        grid_g.set_row_spacing(12)
        sec_greet.pack_start(grid_g, False, False, 0)

        # Show Greeting Toggle
        lbl_g_toggle = Gtk.Label(label="Display Time Greeting:")
        lbl_g_toggle.get_style_context().add_class("field-label")
        lbl_g_toggle.set_xalign(0)
        grid_g.attach(lbl_g_toggle, 0, 0, 1, 1)

        self.switch_greeting = Gtk.Switch()
        self.switch_greeting.set_active(str(self.manager.config.get('show_greeting', 'true')).lower() == 'true')
        self.switch_greeting.set_halign(Gtk.Align.END)
        grid_g.attach(self.switch_greeting, 1, 0, 1, 1)

        # Custom User Name Input
        lbl_name = Gtk.Label(label="Your Custom Name:")
        lbl_name.get_style_context().add_class("field-label")
        lbl_name.set_xalign(0)
        grid_g.attach(lbl_name, 0, 1, 1, 1)

        self.entry_name = Gtk.Entry()
        self.entry_name.set_placeholder_text("e.g. Executive (Leave empty for generic greeting)")
        self.entry_name.set_text(self.manager.config.get('user_name', ''))
        self.entry_name.set_hexpand(True)
        grid_g.attach(self.entry_name, 1, 1, 1, 1)

        content_vbox.pack_start(sec_greet, False, False, 0)

        # SECTION 3: DISPLAY OPTIONS
        sec_disp = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sec_disp.get_style_context().add_class("section-box")
        
        lbl_sec2 = Gtk.Label(label="Display & Clock Customization")
        lbl_sec2.get_style_context().add_class("section-header")
        lbl_sec2.set_xalign(0)
        sec_disp.pack_start(lbl_sec2, False, False, 0)

        grid_d = Gtk.Grid()
        grid_d.set_column_spacing(16)
        grid_d.set_row_spacing(12)
        sec_disp.pack_start(grid_d, False, False, 0)

        # Time Format
        lbl_fmt = Gtk.Label(label="Time Format:")
        lbl_fmt.get_style_context().add_class("field-label")
        lbl_fmt.set_xalign(0)
        lbl_fmt.set_valign(Gtk.Align.CENTER)
        grid_d.attach(lbl_fmt, 0, 0, 1, 1)

        self.combo_format = Gtk.ComboBoxText()
        self.combo_format.append("12", "12-Hour (AM/PM)")
        self.combo_format.append("24", "24-Hour (24:00)")
        self.combo_format.set_active_id(self.manager.config.get('hour_format', '12'))
        self.combo_format.set_hexpand(True)
        self.combo_format.set_valign(Gtk.Align.CENTER)
        grid_d.attach(self.combo_format, 1, 0, 1, 1)

        # Show Seconds Toggle
        lbl_sec_toggle = Gtk.Label(label="Display Seconds Card:")
        lbl_sec_toggle.get_style_context().add_class("field-label")
        lbl_sec_toggle.set_xalign(0)
        lbl_sec_toggle.set_valign(Gtk.Align.CENTER)
        grid_d.attach(lbl_sec_toggle, 0, 1, 1, 1)

        self.switch_seconds = Gtk.Switch()
        self.switch_seconds.set_active(str(self.manager.config.get('show_seconds', 'true')).lower() == 'true')
        self.switch_seconds.set_halign(Gtk.Align.END)
        self.switch_seconds.set_valign(Gtk.Align.CENTER)
        grid_d.attach(self.switch_seconds, 1, 1, 1, 1)

        # Show Date Badge Toggle
        lbl_date_toggle = Gtk.Label(label="Display Date Badge:")
        lbl_date_toggle.get_style_context().add_class("field-label")
        lbl_date_toggle.set_xalign(0)
        lbl_date_toggle.set_valign(Gtk.Align.CENTER)
        grid_d.attach(lbl_date_toggle, 0, 2, 1, 1)

        self.switch_date = Gtk.Switch()
        self.switch_date.set_active(str(self.manager.config.get('show_date', 'true')).lower() == 'true')
        self.switch_date.set_halign(Gtk.Align.END)
        self.switch_date.set_valign(Gtk.Align.CENTER)
        grid_d.attach(self.switch_date, 1, 2, 1, 1)

        # Show Day of Week Toggle
        lbl_day_toggle = Gtk.Label(label="Display Day of Week:")
        lbl_day_toggle.get_style_context().add_class("field-label")
        lbl_day_toggle.set_xalign(0)
        lbl_day_toggle.set_valign(Gtk.Align.CENTER)
        grid_d.attach(lbl_day_toggle, 0, 3, 1, 1)

        self.switch_day = Gtk.Switch()
        self.switch_day.set_active(str(self.manager.config.get('show_day', 'true')).lower() == 'true')
        self.switch_day.set_halign(Gtk.Align.END)
        self.switch_day.set_valign(Gtk.Align.CENTER)
        grid_d.attach(self.switch_day, 1, 3, 1, 1)

        # Clock Scale Slider
        lbl_scale = Gtk.Label(label="Clock Scale / Size:")
        lbl_scale.get_style_context().add_class("field-label")
        lbl_scale.set_xalign(0)
        lbl_scale.set_valign(Gtk.Align.CENTER)
        grid_d.attach(lbl_scale, 0, 4, 1, 1)

        cur_scale = float(self.manager.config.get('clock_size', '1.0'))
        self.adj_size = Gtk.Adjustment(value=cur_scale, lower=0.5, upper=2.0, step_increment=0.1, page_increment=0.5, page_size=0)
        self.scale_size = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.adj_size)
        self.scale_size.set_digits(1)
        self.scale_size.set_hexpand(True)
        self.scale_size.set_valign(Gtk.Align.CENTER)
        grid_d.attach(self.scale_size, 1, 4, 1, 1)

        # Flip Card Corner Shape Selection
        lbl_shape = Gtk.Label(label="Flip Card Design / Shape:")
        lbl_shape.get_style_context().add_class("field-label")
        lbl_shape.set_xalign(0)
        lbl_shape.set_valign(Gtk.Align.CENTER)
        grid_d.attach(lbl_shape, 0, 5, 1, 1)

        self.combo_card_shape = Gtk.ComboBoxText()
        shapes_list = [
            ("rectangle", "Rectangle"),
            ("rounded_rectangle", "Rounded Rectangle"),
            ("squircle", "Squircle"),
            ("octagon", "Octagon"),
            ("hexagon", "Hexagon"),
            ("pentagon", "Pentagon"),
            ("diamond", "Diamond"),
            ("shield", "Shield"),
            ("capsule", "Capsule"),
            ("pill", "Pill"),
            ("circle", "Circle"),
            ("oval", "Oval"),
            ("trapezoid", "Trapezoid"),
            ("parallelogram", "Parallelogram"),
            ("rhombus", "Rhombus"),
            ("chamfered", "Chamfered"),
            ("beveled", "Beveled"),
            ("notched", "Notched"),
            ("cut_corner", "Cut Corner"),
            ("chevron", "Chevron"),
            ("badge", "Badge"),
            ("ticket", "Ticket"),
            ("arch", "Arch"),
            ("stadium", "Stadium"),
            ("lozenge", "Lozenge"),
            ("frame", "Frame"),
            ("panel", "Panel"),
            ("card", "Card"),
            ("tile", "Tile")
        ]
        for s_id, s_name in shapes_list:
            self.combo_card_shape.append(s_id, s_name)

        cur_shape = self.manager.config.get('card_shape', 'squircle')
        legacy_map = {
            'soft_squircle': 'squircle',
            'neo_rounded': 'rounded_rectangle',
            'glass_floating': 'hexagon',
            'premium_bevel': 'beveled',
            'fold_corner': 'cut_corner',
            'split_flip': 'rectangle'
        }
        if cur_shape in legacy_map:
            cur_shape = legacy_map[cur_shape]

        self.combo_card_shape.set_wrap_width(2)
        self.combo_card_shape.set_active_id(cur_shape)
        self.combo_card_shape.set_hexpand(True)
        self.combo_card_shape.set_valign(Gtk.Align.CENTER)
        self.combo_card_shape.connect("changed", self.on_shape_combo_changed)
        grid_d.attach(self.combo_card_shape, 1, 5, 1, 1)

        self.img_shape_preview = Gtk.Image()
        self.img_shape_preview.set_margin_top(8)
        self.img_shape_preview.set_margin_bottom(8)
        self.img_shape_preview.set_halign(Gtk.Align.CENTER)
        sec_disp.pack_start(self.img_shape_preview, False, False, 0)
        self.on_shape_combo_changed(self.combo_card_shape)

        content_vbox.pack_start(sec_disp, False, False, 0)

        # SECTION 3: IDLE TIMEOUT & BEHAVIOR
        sec_idle = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        sec_idle.get_style_context().add_class("section-box")
        
        lbl_sec3 = Gtk.Label(label="Idle Timeout & Behavior")
        lbl_sec3.get_style_context().add_class("section-header")
        lbl_sec3.set_xalign(0)
        sec_idle.pack_start(lbl_sec3, False, False, 0)

        grid_i = Gtk.Grid()
        grid_i.set_column_spacing(16)
        grid_i.set_row_spacing(10)
        sec_idle.pack_start(grid_i, False, False, 0)

        lbl_to = Gtk.Label(label="Idle Timeout:")
        lbl_to.get_style_context().add_class("field-label")
        lbl_to.set_xalign(0)
        grid_i.attach(lbl_to, 0, 0, 1, 1)

        self.combo_timeout = Gtk.ComboBoxText()
        self.combo_timeout.append("60", "1 Minute")
        self.combo_timeout.append("120", "2 Minutes")
        self.combo_timeout.append("180", "3 Minutes")
        self.combo_timeout.append("300", "5 Minutes")
        self.combo_timeout.append("600", "10 Minutes")
        self.combo_timeout.append("900", "15 Minutes")
        self.combo_timeout.append("1800", "30 Minutes")
        self.combo_timeout.append("3600", "1 Hour")

        cur_to = str(self.manager.config.get('idle_timeout', 60))
        if cur_to not in ["60", "120", "180", "300", "600", "900", "1800", "3600"]:
            self.combo_timeout.append(cur_to, f"{int(cur_to)//60} Minutes")
        self.combo_timeout.set_active_id(cur_to)
        self.combo_timeout.set_hexpand(True)
        grid_i.attach(self.combo_timeout, 1, 0, 1, 1)

        content_vbox.pack_start(sec_idle, False, False, 0)

        # ACTION BUTTONS & FOOTER
        action_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=14)
        action_box.set_margin_top(22)
        action_box.set_margin_bottom(20)
        action_box.set_margin_start(16)
        action_box.set_margin_end(16)

        btn_row = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        btn_row.set_halign(Gtk.Align.END)

        self.btn_reset = Gtk.Button(label="Reset Defaults")
        self.btn_reset.get_style_context().add_class("btn-reset")
        self.btn_reset.connect("clicked", self.on_reset_clicked)
        btn_row.pack_start(self.btn_reset, False, False, 0)

        self.btn_preview = Gtk.Button(label="Test Preview")
        self.btn_preview.get_style_context().add_class("btn-secondary")
        self.btn_preview.connect("clicked", self.on_preview_clicked)
        btn_row.pack_start(self.btn_preview, False, False, 0)

        self.btn_save = Gtk.Button(label="Save & Apply")
        self.btn_save.get_style_context().add_class("btn-primary")
        self.btn_save.connect("clicked", self.on_save_clicked)
        btn_row.pack_start(self.btn_save, False, False, 0)

        action_box.pack_start(btn_row, False, False, 0)

        lbl_footer = Gtk.Label(label=f"Executive Desktop Flip Clock • v{APP_VERSION}")
        lbl_footer.get_style_context().add_class("branding-footer")
        lbl_footer.set_xalign(0.5)
        action_box.pack_start(lbl_footer, False, False, 0)

        main_box.pack_start(action_box, False, False, 0)

        self.connect("destroy", lambda w: Gtk.main_quit() if Gtk.main_level() > 0 else None)
        self.show_all()

    def on_theme_combo_changed(self, widget):
        t_id = widget.get_active_id()
        if not t_id or t_id not in PRESET_THEMES:
            return
        preset = PRESET_THEMES[t_id]
        if t_id != 'custom':
            if hasattr(self, 'btn_bg_color'):
                self.btn_bg_color.set_rgba(hex_to_rgba(preset['bg_color']))
                self.btn_card_color.set_rgba(hex_to_rgba(preset['card_color']))
                self.btn_digit_color.set_rgba(hex_to_rgba(preset['digit_color']))
                self.btn_accent_color.set_rgba(hex_to_rgba(preset['accent_color']))
                self.btn_border_color.set_rgba(hex_to_rgba(preset['border_color']))
            
            if hasattr(self, 'combo_digit_font'):
                self.combo_digit_font.set_active_id(preset['digit_font'])
            if hasattr(self, 'combo_label_font'):
                self.combo_label_font.set_active_id(preset['label_font'])

        if t_id and hasattr(self, 'img_theme_preview'):
            img_path = get_asset_image_path(f"theme_{t_id}.png")
            if img_path:
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 360, 200, True)
                    self.img_theme_preview.set_from_pixbuf(pixbuf)
                    self.img_theme_preview.show()
                except Exception:
                    pass

    def on_shape_combo_changed(self, widget):
        s_id = widget.get_active_id()
        if s_id and hasattr(self, 'img_shape_preview'):
            img_path = get_asset_image_path(f"shape_{s_id}.png")
            if img_path:
                try:
                    pixbuf = GdkPixbuf.Pixbuf.new_from_file_at_scale(img_path, 360, 200, True)
                    self.img_shape_preview.set_from_pixbuf(pixbuf)
                    self.img_shape_preview.show()
                except Exception:
                    pass
        if hasattr(self, 'combo_timeout'):
            self.update_config_from_ui()
            self.manager.save_config()

    def get_coordinating_palette(self, bg_hex):
        best_match = None
        min_dist = 999999.0
        try:
            hex_clean = bg_hex.lstrip('#')
            r1, g1, b1 = int(hex_clean[0:2], 16), int(hex_clean[2:4], 16), int(hex_clean[4:6], 16)
        except Exception:
            return None
            
        for t_key, t_info in PRESET_THEMES.items():
            if t_key == 'custom':
                continue
            try:
                th_clean = t_info['bg_color'].lstrip('#')
                r2, g2, b2 = int(th_clean[0:2], 16), int(th_clean[2:4], 16), int(th_clean[4:6], 16)
                dist = ((r1 - r2) ** 2 + (g1 - g2) ** 2 + (b1 - b2) ** 2) ** 0.5
                if dist < min_dist:
                    min_dist = dist
                    best_match = t_key
            except Exception:
                continue
                
        if best_match and min_dist < 15:
            return PRESET_THEMES[best_match]
            
        brightness = (0.299 * r1 + 0.587 * g1 + 0.114 * b1)
        is_dark = brightness < 128
        
        if is_dark:
            card_r = min(255, r1 + 25)
            card_g = min(255, g1 + 25)
            card_b = min(255, b1 + 25)
            card_hex = f"#{card_r:02X}{card_g:02X}{card_b:02X}"
            
            border_r = min(255, card_r + 20)
            border_g = min(255, card_g + 20)
            border_b = min(255, card_b + 20)
            border_hex = f"#{border_r:02X}{border_g:02X}{border_b:02X}"
            
            digit_hex = "#F5F5F7"
            
            max_val = max(r1, g1, b1)
            if max_val < 30:
                accent_hex = "#D4AF37"
            elif r1 == max_val:
                accent_hex = "#D32F2F"
            elif g1 == max_val:
                accent_hex = "#00C853"
            elif b1 == max_val:
                accent_hex = "#2E7DFF"
            else:
                accent_hex = "#D4AF37"
        else:
            card_r = max(0, r1 - 25)
            card_g = max(0, g1 - 25)
            card_b = max(0, b1 - 25)
            card_hex = f"#{card_r:02X}{card_g:02X}{card_b:02X}"
            
            border_r = max(0, card_r - 20)
            border_g = max(0, card_g - 20)
            border_b = max(0, card_b - 20)
            border_hex = f"#{border_r:02X}{border_g:02X}{border_b:02X}"
            
            digit_hex = "#0F172A"
            accent_hex = "#1E293B"
            
        return {
            "bg_color": bg_hex,
            "card_color": card_hex,
            "digit_color": digit_hex,
            "accent_color": accent_hex,
            "border_color": border_hex,
            "digit_font": "Inter",
            "label_font": "Inter"
        }

    def on_color_button_changed(self, button):
        if button == self.btn_bg_color:
            bg_hex = rgba_to_hex(self.btn_bg_color.get_rgba()).upper()
            palette = self.get_coordinating_palette(bg_hex)
            if palette:
                self.btn_card_color.set_rgba(hex_to_rgba(palette['card_color']))
                self.btn_digit_color.set_rgba(hex_to_rgba(palette['digit_color']))
                self.btn_accent_color.set_rgba(hex_to_rgba(palette['accent_color']))
                self.btn_border_color.set_rgba(hex_to_rgba(palette['border_color']))
                if 'digit_font' in palette and hasattr(self, 'combo_digit_font'):
                    self.combo_digit_font.set_active_id(palette['digit_font'])
                if 'label_font' in palette and hasattr(self, 'combo_label_font'):
                    self.combo_label_font.set_active_id(palette['label_font'])
            
            matched_theme = None
            for t_key, t_info in PRESET_THEMES.items():
                if t_key == 'custom':
                    continue
                if t_info['bg_color'].upper() == bg_hex:
                    matched_theme = t_key
                    break
            
            if matched_theme:
                if self.combo_theme.get_active_id() != matched_theme:
                    self.combo_theme.set_active_id(matched_theme)
            else:
                if self.combo_theme.get_active_id() != 'custom':
                    self.combo_theme.set_active_id('custom')
        else:
            if self.combo_theme.get_active_id() != 'custom':
                self.combo_theme.set_active_id('custom')

    def update_config_from_ui(self):
        theme = self.combo_theme.get_active_id() or "luxury_black_gold"
        fmt = self.combo_format.get_active_id() or "12"
        timeout_str = self.combo_timeout.get_active_id() or "60"
        try:
            timeout = int(timeout_str)
        except ValueError:
            timeout = 60
        size = f"{self.scale_size.get_value():.1f}"
        show_sec = 'true' if self.switch_seconds.get_active() else 'false'
        show_dt = 'true' if self.switch_date.get_active() else 'false'
        show_day = 'true' if self.switch_day.get_active() else 'false'
        show_greet = 'true' if self.switch_greeting.get_active() else 'false'
        uname = self.entry_name.get_text().strip()
        card_shape = self.combo_card_shape.get_active_id() or "squircle"

        dfont = self.combo_digit_font.get_active_id() or "Cinzel"
        lfont = self.combo_label_font.get_active_id() or "Cinzel"
        bg_col = rgba_to_hex(self.btn_bg_color.get_rgba())
        card_col = rgba_to_hex(self.btn_card_color.get_rgba())
        digit_col = rgba_to_hex(self.btn_digit_color.get_rgba())
        accent_col = rgba_to_hex(self.btn_accent_color.get_rgba())
        border_col = rgba_to_hex(self.btn_border_color.get_rgba())

        self.manager.config['theme'] = theme
        self.manager.config['hour_format'] = fmt
        self.manager.config['idle_timeout'] = timeout
        self.manager.config['clock_size'] = size
        self.manager.config['show_seconds'] = show_sec
        self.manager.config['show_date'] = show_dt
        self.manager.config['show_day'] = show_day
        self.manager.config['show_greeting'] = show_greet
        self.manager.config['user_name'] = uname
        self.manager.config['card_shape'] = card_shape
        self.manager.config['custom_credit'] = 'FLIP CLOCK SCREENSAVER'
        self.manager.config['digit_font'] = dfont
        self.manager.config['label_font'] = lfont
        self.manager.config['custom_bg_color'] = bg_col
        self.manager.config['custom_card_color'] = card_col
        self.manager.config['custom_digit_color'] = digit_col
        self.manager.config['custom_accent_color'] = accent_col
        self.manager.config['custom_border_color'] = border_col

    def update_ui_from_config(self):
        cur_theme = self.manager.config.get('theme', 'luxury_black_gold')
        self.combo_theme.set_active_id(cur_theme if cur_theme in PRESET_THEMES else 'luxury_black_gold')
        self.on_theme_combo_changed(self.combo_theme)

        self.combo_format.set_active_id(str(self.manager.config.get('hour_format', '12')))
        self.switch_seconds.set_active(str(self.manager.config.get('show_seconds', 'true')).lower() == 'true')
        self.switch_date.set_active(str(self.manager.config.get('show_date', 'true')).lower() == 'true')
        self.switch_day.set_active(str(self.manager.config.get('show_day', 'true')).lower() == 'true')
        self.switch_greeting.set_active(str(self.manager.config.get('show_greeting', 'true')).lower() == 'true')
        self.entry_name.set_text(self.manager.config.get('user_name', ''))
        cur_shape = self.manager.config.get('card_shape', 'squircle')
        legacy_map = {
            'soft_squircle': 'squircle',
            'neo_rounded': 'rounded_rectangle',
            'glass_floating': 'hexagon',
            'premium_bevel': 'beveled',
            'fold_corner': 'cut_corner',
            'split_flip': 'rectangle'
        }
        if cur_shape in legacy_map:
            cur_shape = legacy_map[cur_shape]
        self.combo_card_shape.set_active_id(cur_shape)
        
        try:
            sz = float(self.manager.config.get('clock_size', '1.0'))
            self.scale_size.set_value(sz)
        except ValueError:
            self.scale_size.set_value(1.0)
            
        cur_to = str(self.manager.config.get('idle_timeout', 60))
        self.combo_timeout.set_active_id(cur_to)
        
        self.combo_digit_font.set_active_id(self.manager.config.get('digit_font', 'Cinzel'))
        self.combo_label_font.set_active_id(self.manager.config.get('label_font', 'Cinzel'))
        
        self.btn_bg_color.set_rgba(hex_to_rgba(self.manager.config.get('custom_bg_color', '#000000')))
        self.btn_card_color.set_rgba(hex_to_rgba(self.manager.config.get('custom_card_color', '#1C1C1E')))
        self.btn_digit_color.set_rgba(hex_to_rgba(self.manager.config.get('custom_digit_color', '#F5F5F7')))
        self.btn_accent_color.set_rgba(hex_to_rgba(self.manager.config.get('custom_accent_color', '#D4AF37')))
        self.btn_border_color.set_rgba(hex_to_rgba(self.manager.config.get('custom_border_color', '#4A4A4A')))

    def on_reset_clicked(self, button):
        dialog = CustomDarkDialog(
            parent=self,
            title="Reset Settings",
            primary_msg="Reset Settings to Executive Defaults?",
            secondary_msg="This will restore the default Luxury Black Gold theme, default executive fonts, and standard clock options.",
            is_confirm=True
        )
        resp = dialog.run()
        dialog.destroy()
        
        if resp == Gtk.ResponseType.YES:
            self.manager.reset_to_defaults()
            self.update_ui_from_config()
            self.manager.restart_daemon()
            
            toast = CustomDarkDialog(
                parent=self,
                title="Reset Complete",
                primary_msg="Settings Reset Successful!",
                secondary_msg="All settings have been restored to executive defaults."
            )
            toast.run()
            toast.destroy()

    def on_preview_clicked(self, button):
        self.update_config_from_ui()
        self.manager.save_config()
        try:
            script_path = os.path.realpath(__file__)
            subprocess.Popen([sys.executable, script_path, "--run"])
        except Exception as e:
            print(f"Error starting preview: {e}")

    def on_save_clicked(self, button):
        self.update_config_from_ui()
        self.manager.save_config()
        self.manager.restart_daemon()
        
        dialog = CustomDarkDialog(
            parent=self,
            title="Settings Saved",
            primary_msg="Settings Saved Successfully!",
            secondary_msg="Your executive theme & layout settings have been applied cleanly."
        )
        dialog.run()
        dialog.destroy()
        
        try:
            script_path = os.path.realpath(__file__)
            subprocess.Popen([sys.executable, script_path, "--run"])
        except Exception as e:
            print(f"Error starting preview: {e}")
            
        self.close()


class FlipClockManager:
    """Manages configuration, daemon monitoring, and window spawning."""
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/flipclock")
        self.config_path = os.path.join(self.config_dir, "flipclock.conf")
        self.script_dir = os.path.dirname(os.path.realpath(__file__))
        if not os.path.exists(os.path.join(self.script_dir, "clock.html")):
            for candidate_dir in ["/usr/share/flipclock", "/usr/local/share/flipclock", os.path.expanduser("~/.local/share/flipclock"), os.getcwd()]:
                if os.path.exists(os.path.join(candidate_dir, "clock.html")):
                    self.script_dir = candidate_dir
                    break
        self.html_path = os.path.join(self.script_dir, "clock.html")
        
        self.config = {
            'idle_timeout': 60,
            'hour_format': '12',
            'clock_size': '1.0',
            'animation_speed': 500,
            'monitors': 'all',
            'theme': 'luxury_black_gold',
            'card_shape': 'squircle',
            'show_seconds': 'true',
            'show_date': 'true',
            'show_day': 'true',
            'show_greeting': 'true',
            'user_name': '',
            'bg_style': 'vignette',
            'custom_credit': 'FLIP CLOCK SCREENSAVER',
            'digit_font': 'Cinzel',
            'label_font': 'Cinzel',
            'custom_bg_color': '#000000',
            'custom_card_color': '#1C1C1E',
            'custom_digit_color': '#F5F5F7',
            'custom_accent_color': '#D4AF37',
            'custom_border_color': '#4A4A4A'
        }
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
            
        parser = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            try:
                parser.read(self.config_path)
                if 'Settings' in parser:
                    settings = parser['Settings']
                    self.config['idle_timeout'] = settings.getint('idle_timeout', 60)
                    self.config['hour_format'] = settings.get('hour_format', '12')
                    self.config['clock_size'] = settings.get('clock_size', '1.0')
                    self.config['animation_speed'] = settings.getint('animation_speed', 500)
                    self.config['monitors'] = settings.get('monitors', 'all')
                    self.config['theme'] = settings.get('theme', 'luxury_black_gold')
                    self.config['card_shape'] = settings.get('card_shape', 'squircle')
                    self.config['show_seconds'] = settings.get('show_seconds', 'true')
                    self.config['show_date'] = settings.get('show_date', 'true')
                    self.config['show_day'] = settings.get('show_day', 'true')
                    self.config['show_greeting'] = settings.get('show_greeting', 'true')
                    self.config['user_name'] = settings.get('user_name', '')
                    self.config['bg_style'] = settings.get('bg_style', 'vignette')
                    self.config['custom_credit'] = settings.get('custom_credit', 'FLIP CLOCK SCREENSAVER')
                    self.config['digit_font'] = settings.get('digit_font', 'Cinzel')
                    self.config['label_font'] = settings.get('label_font', 'Cinzel')
                    self.config['custom_bg_color'] = settings.get('custom_bg_color', '#000000')
                    self.config['custom_card_color'] = settings.get('custom_card_color', '#1C1C1E')
                    self.config['custom_digit_color'] = settings.get('custom_digit_color', '#F5F5F7')
                    self.config['custom_accent_color'] = settings.get('custom_accent_color', '#D4AF37')
                    self.config['custom_border_color'] = settings.get('custom_border_color', '#4A4A4A')
            except Exception as e:
                print(f"Error reading config, using defaults: {e}")
        else:
            self.save_config()

    def save_config(self):
        parser = configparser.ConfigParser()
        parser['Settings'] = {
            'idle_timeout': str(self.config.get('idle_timeout', 60)),
            'hour_format': str(self.config.get('hour_format', '12')),
            'clock_size': str(self.config.get('clock_size', '1.0')),
            'animation_speed': str(self.config.get('animation_speed', 500)),
            'monitors': str(self.config.get('monitors', 'all')),
            'theme': str(self.config.get('theme', 'luxury_black_gold')),
            'card_shape': str(self.config.get('card_shape', 'squircle')),
            'show_seconds': str(self.config.get('show_seconds', 'true')),
            'show_date': str(self.config.get('show_date', 'true')),
            'show_day': str(self.config.get('show_day', 'true')),
            'show_greeting': str(self.config.get('show_greeting', 'true')),
            'user_name': str(self.config.get('user_name', '')),
            'bg_style': str(self.config.get('bg_style', 'vignette')),
            'custom_credit': str(self.config.get('custom_credit', 'FLIP CLOCK SCREENSAVER')),
            'digit_font': str(self.config.get('digit_font', 'Cinzel')),
            'label_font': str(self.config.get('label_font', 'Cinzel')),
            'custom_bg_color': str(self.config.get('custom_bg_color', '#000000')),
            'custom_card_color': str(self.config.get('custom_card_color', '#1C1C1E')),
            'custom_digit_color': str(self.config.get('custom_digit_color', '#F5F5F7')),
            'custom_accent_color': str(self.config.get('custom_accent_color', '#D4AF37')),
            'custom_border_color': str(self.config.get('custom_border_color', '#4A4A4A'))
        }
        try:
            with open(self.config_path, 'w') as f:
                parser.write(f)
        except Exception as e:
            print(f"Error saving config file: {e}")

    def reset_to_defaults(self):
        self.config = {
            'idle_timeout': 60,
            'hour_format': '12',
            'clock_size': '1.0',
            'animation_speed': 500,
            'monitors': 'all',
            'theme': 'luxury_black_gold',
            'card_shape': 'squircle',
            'show_seconds': 'true',
            'show_date': 'true',
            'show_day': 'true',
            'show_greeting': 'true',
            'user_name': '',
            'bg_style': 'vignette',
            'custom_credit': 'FLIP CLOCK SCREENSAVER',
            'digit_font': 'Cinzel',
            'label_font': 'Cinzel',
            'custom_bg_color': '#000000',
            'custom_card_color': '#1C1C1E',
            'custom_digit_color': '#F5F5F7',
            'custom_accent_color': '#D4AF37',
            'custom_border_color': '#4A4A4A'
        }
        self.save_config()

    def restart_daemon(self):
        try:
            uid = os.getuid()
            subprocess.run(["pkill", "-u", str(uid), "-f", "flipclock.*--daemon"], capture_output=True)
        except Exception as e:
            print(f"Error stopping daemon: {e}")
            
        try:
            if os.path.exists("/usr/bin/flipclock"):
                subprocess.Popen(["/usr/bin/flipclock", "--daemon"])
            elif os.path.exists("/usr/share/flipclock/flipclock.py"):
                subprocess.Popen([sys.executable, "/usr/share/flipclock/flipclock.py", "--daemon"])
            else:
                script_path = os.path.realpath(__file__)
                subprocess.Popen([sys.executable, script_path, "--daemon"])
            print("Daemon restarted successfully.")
        except Exception as e:
            print(f"Error starting daemon: {e}")

    def run_screensaver(self):
        Gtk.init(None)
        
        display = Gdk.Display.get_default()
        if not display:
            print("Error: Gdk display not available.")
            sys.exit(1)
            
        n_monitors = display.get_n_monitors() if hasattr(display, 'get_n_monitors') else 1
        if n_monitors < 1:
            n_monitors = 1
            
        target_monitors = []
        mon_setting = str(self.config.get('monitors', 'all')).lower()
        if mon_setting == 'all':
            target_monitors = list(range(n_monitors))
        else:
            try:
                target_monitors = [int(i.strip()) for i in mon_setting.split(',') if i.strip().isdigit() and int(i.strip()) < n_monitors]
            except Exception:
                target_monitors = list(range(n_monitors))
                
        if not target_monitors:
            target_monitors = [0]
            
        print(f"Spawning screensaver clock windows on monitors: {target_monitors}")
        
        windows = []
        for monitor_idx in target_monitors:
            win = FlipClockWindow(self.html_path, monitor_idx, self.config)
            windows.append(win)
            
        GLib.timeout_add(400, enable_key_tracking)
        GLib.timeout_add(800, enable_mouse_tracking)
            
        Gtk.main()

    def get_system_idle_time_ms(self):
        try:
            res = subprocess.run(
                ["gdbus", "call", "--session", "--dest", "org.gnome.Mutter.IdleMonitor",
                 "--object-path", "/org/gnome/Mutter/IdleMonitor/Core",
                 "--method", "org.gnome.Mutter.IdleMonitor.GetIdletime"],
                capture_output=True, text=True, timeout=1
            )
            if res.returncode == 0 and res.stdout:
                match = re.search(r'\b(\d+)\b', res.stdout)
                if match:
                    return int(match.group(1))
        except Exception:
            pass

        try:
            res = subprocess.run(["xprintidle"], capture_output=True, text=True, timeout=1)
            if res.returncode == 0 and res.stdout.strip().isdigit():
                return int(res.stdout.strip())
        except Exception:
            pass

        if X11_AVAILABLE:
            try:
                display = x11.XOpenDisplay(None)
                if display:
                    root = x11.XDefaultRootWindow(display)
                    info_ptr = xss.XScreenSaverAllocInfo()
                    if xss.XScreenSaverQueryInfo(display, root, info_ptr) != 0:
                        idle_ms = info_ptr.contents.idle
                        x11.XFree(info_ptr)
                        x11.XCloseDisplay(display)
                        return idle_ms
                    x11.XFree(info_ptr)
                    x11.XCloseDisplay(display)
            except Exception:
                pass

        return 0

    def run_daemon(self):
        proc = None
        state = "IDLE"  # IDLE, RUNNING, WAIT_USER_ACTIVE
        
        print(f"Flip Clock screensaver daemon started. Default timeout: {self.config.get('idle_timeout', 60)}s.")
        
        try:
            while True:
                self.load_config()
                
                idle_ms = self.get_system_idle_time_ms()
                try:
                    idle_limit_ms = int(self.config.get('idle_timeout', 60)) * 1000
                except (ValueError, TypeError):
                    idle_limit_ms = 60000
                    
                if state == "IDLE":
                    if idle_ms >= idle_limit_ms:
                        print(f"System idle for {idle_ms/1000:.1f}s. Spawning screensaver windows...")
                        try:
                            subprocess.run(["xscreensaver-command", "-exit"], capture_output=True)
                        except FileNotFoundError:
                            pass
                        
                        script_path = os.path.realpath(__file__)
                        proc = subprocess.Popen([sys.executable, script_path, "--run"])
                        state = "RUNNING"

                elif state == "RUNNING":
                    if proc is None or proc.poll() is not None:
                        print("Screensaver closed by user input.")
                        proc = None
                        state = "WAIT_USER_ACTIVE"
                    elif idle_ms < idle_limit_ms:
                        print("User activity detected. Closing screensaver.")
                        proc.terminate()
                        try:
                            proc.wait(timeout=1)
                        except subprocess.TimeoutExpired:
                            proc.kill()
                        proc = None
                        state = "IDLE"

                elif state == "WAIT_USER_ACTIVE":
                    if idle_ms < idle_limit_ms:
                        # User activity confirmed by system idle reset
                        state = "IDLE"

                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nStopping daemon.")
        finally:
            if proc and proc.poll() is None:
                proc.terminate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ubuntu Dual-Monitor Flip Clock Screensaver")
    parser.add_argument("--run", action="store_true", help="Launch fullscreen flip clock windows directly")
    parser.add_argument("--daemon", action="store_true", help="Start background idle monitor daemon")
    parser.add_argument("--settings", action="store_true", help="Configure Flip Clock settings")
    parser.add_argument("--theme", choices=["dark_gold", "midnight_cyber", "emerald_oled", "sunset_glow", "minimal_light", "classic_retro"], help="Test theme directly")
    parser.add_argument("--version", action="version", version=f"Flip Clock Screensaver v{APP_VERSION}")
    args = parser.parse_args()
    
    manager = FlipClockManager()
    if args.theme:
        manager.config['theme'] = args.theme
    
    if args.daemon:
        manager.run_daemon()
    elif args.run:
        manager.run_screensaver()
    elif args.settings:
        Gtk.init(None)
        FlipClockSettingsWindow(manager)
        Gtk.main()
    else:
        manager.run_screensaver()
