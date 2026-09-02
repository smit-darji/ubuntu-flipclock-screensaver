#!/usr/bin/env python3
import sys
import os

# Disable WebKit hardware compositing mode to prevent GPU black screens on Linux
os.environ["WEBKIT_DISABLE_COMPOSITING_MODE"] = "1"

import math
import gi

gi.require_version('Gtk', '3.0')
try:
    gi.require_version('WebKit2', '4.0')
except ValueError:
    try:
        gi.require_version('WebKit2', '4.1')
    except ValueError:
        print("Error: WebKit2 namespace not found.")
        sys.exit(1)

from gi.repository import Gtk, Gdk, WebKit2, GLib

key_input_enabled = False
mouse_input_enabled = False
threshold = 30  # pixels to prevent micro-jitter exits

def enable_key_input():
    global key_input_enabled
    key_input_enabled = True
    return False

def enable_mouse_input():
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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Cinzel:wght@700;800;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; user-select:none; -webkit-user-select:none; }
        html, body { width:100vw; height:100vh; overflow:hidden; cursor:none; }

        /* ─── CSS Custom Property Theme Engine ─── */
        :root {
            --card-bg: linear-gradient(170deg,#1e1e22 0%,#141418 40%,#0c0c10 100%);
            --card-border: rgba(180,155,80,0.3);
            --card-top-bg: linear-gradient(180deg,rgba(255,255,255,0.06) 0%,rgba(255,255,255,0.015) 100%);
            --card-bot-bg: linear-gradient(180deg,rgba(0,0,0,0.2) 0%,rgba(0,0,0,0.08) 100%);
            --digit-color: #f0f0f0;
            --digit-shadow: 0 2px 10px rgba(0,0,0,0.5);
            --dot-bg: radial-gradient(circle at 30% 28%,#f0d860 0%,#c8a830 45%,#806818 100%);
            --dot-shadow: 0 0 12px rgba(200,168,48,0.4);
            --pin-bg: linear-gradient(180deg,#e8cc70 0%,#b09840 50%,#806820 100%);
            --accent-color: #d4af37;
            --badge-color: #c8a830;
            --badge-bg: rgba(20,20,24,0.7);
            --badge-border: rgba(180,155,80,0.22);
            --branding-color: rgba(212,175,55,0.4);
            --digit-font: 'Inter', system-ui, sans-serif;
            --label-font: 'Cinzel', serif;
        }

        /* ─── Luxury Themes ─── */
        .theme-luxury_black_gold {
            --card-bg: linear-gradient(170deg,#1C1C1E 0%,#141416 50%,#0c0c0e 100%);
            --card-border: #4A4A4A;
            --card-top-bg: linear-gradient(180deg,rgba(255,255,255,0.05) 0%,rgba(255,255,255,0.01) 100%);
            --card-bot-bg: linear-gradient(180deg,rgba(0,0,0,0.3) 0%,rgba(0,0,0,0.1) 100%);
            --digit-color: #F5F5F7;
            --digit-shadow: 0 2px 10px rgba(0,0,0,0.9);
            --pin-bg: linear-gradient(180deg,#fef08a 0%,#d4af37 50%,#854d0e 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#fef08a 0%,#d4af37 100%);
            --dot-shadow: 0 0 10px rgba(212,175,55,0.5);
            --accent-color: #D4AF37;
            --badge-color: #fef08a;
            --badge-bg: rgba(28,28,30,0.85);
            --badge-border: rgba(212,175,55,0.35);
        }
        .theme-obsidian_titanium {
            --card-bg: linear-gradient(170deg,#1F1F1F 0%,#161616 50%,#0d0d0d 100%);
            --card-border: #50545A;
            --digit-color: #F8F8F8;
            --digit-shadow: 0 2px 10px rgba(0,0,0,0.9);
            --pin-bg: linear-gradient(180deg,#e4e4e7 0%,#aeb5bd 50%,#50545a 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#ffffff 0%,#aeb5bd 100%);
            --dot-shadow: 0 0 10px rgba(174,181,189,0.4);
            --accent-color: #AEB5BD;
            --badge-color: #f8f8f8;
            --badge-bg: rgba(31,31,31,0.85);
            --badge-border: rgba(174,181,189,0.3);
        }
        .theme-dark_emerald {
            --card-bg: linear-gradient(170deg,#122118 0%,#0a1610 50%,#040d07 100%);
            --card-border: #365541;
            --card-top-bg: linear-gradient(180deg,rgba(0,200,83,0.08) 0%,rgba(0,200,83,0.02) 100%);
            --digit-color: #F7FAF7;
            --digit-shadow: 0 0 16px rgba(0,200,83,0.3);
            --pin-bg: linear-gradient(180deg,#a7f3d0 0%,#00c853 50%,#064e3b 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#a7f3d0 0%,#00c853 100%);
            --dot-shadow: 0 0 12px rgba(0,200,83,0.5);
            --accent-color: #00C853;
            --badge-color: #a7f3d0;
            --badge-bg: rgba(18,33,24,0.85);
            --badge-border: rgba(0,200,83,0.35);
        }
        .theme-forest_green {
            --card-bg: linear-gradient(170deg,#18261D 0%,#101c14 50%,#08110a 100%);
            --card-border: #486651;
            --digit-color: #F4F8F4;
            --pin-bg: linear-gradient(180deg,#81c784 0%,#4caf50 50%,#2e7d32 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#a5d6a7 0%,#4caf50 100%);
            --dot-shadow: 0 0 12px rgba(76,175,80,0.5);
            --accent-color: #4CAF50;
            --badge-color: #a5d6a7;
            --badge-bg: rgba(24,38,29,0.85);
            --badge-border: rgba(76,175,80,0.35);
        }
        .theme-racing_green {
            --card-bg: linear-gradient(170deg,#0E2017 0%,#091710 50%,#040c07 100%);
            --card-border: #355649;
            --digit-color: #FAFAF6;
            --pin-bg: linear-gradient(180deg,#6ecf9e 0%,#0b8f57 50%,#064d33 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#6ecf9e 0%,#0b8f57 100%);
            --dot-shadow: 0 0 12px rgba(11,143,87,0.5);
            --accent-color: #0B8F57;
            --badge-color: #6ecf9e;
            --badge-bg: rgba(14,32,23,0.85);
            --badge-border: rgba(11,143,87,0.35);
        }
        .theme-ruby_executive {
            --card-bg: linear-gradient(170deg,#221515 0%,#180d0d 50%,#0c0606 100%);
            --card-border: #5B3A3A;
            --digit-color: #FAFAFA;
            --pin-bg: linear-gradient(180deg,#f28b82 0%,#d32f2f 50%,#7f0000 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#f28b82 0%,#d32f2f 100%);
            --dot-shadow: 0 0 12px rgba(211,47,47,0.5);
            --accent-color: #D32F2F;
            --badge-color: #f28b82;
            --badge-bg: rgba(34,21,21,0.85);
            --badge-border: rgba(211,47,47,0.35);
        }
        .theme-burgundy_prestige {
            --card-bg: linear-gradient(170deg,#2A1616 0%,#1a0d0d 50%,#120808 100%);
            --card-border: #634545;
            --digit-color: #FFF9F8;
            --pin-bg: linear-gradient(180deg,#d4858f 0%,#8e2430 50%,#4a0e18 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#d4858f 0%,#8e2430 100%);
            --dot-shadow: 0 0 12px rgba(142,36,48,0.5);
            --accent-color: #8E2430;
            --badge-color: #d4858f;
            --badge-bg: rgba(42,22,22,0.85);
            --badge-border: rgba(142,36,48,0.35);
        }
        .theme-crimson_royal {
            --card-bg: linear-gradient(170deg,#231313 0%,#170b0b 50%,#0a0505 100%);
            --card-border: #604040;
            --digit-color: #FFFFFF;
            --pin-bg: linear-gradient(180deg,#ef9a9a 0%,#c62828 50%,#7f0000 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#ef9a9a 0%,#c62828 100%);
            --dot-shadow: 0 0 12px rgba(198,40,40,0.5);
            --accent-color: #C62828;
            --badge-color: #ef9a9a;
            --badge-bg: rgba(35,19,19,0.85);
            --badge-border: rgba(198,40,40,0.35);
        }
        .theme-royal_sapphire {
            --card-bg: linear-gradient(170deg,#162033 0%,#0d1622 50%,#030816 100%);
            --card-border: #36527A;
            --digit-color: #FFFFFF;
            --pin-bg: linear-gradient(180deg,#82b1ff 0%,#2e7dff 50%,#0d47a1 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#82b1ff 0%,#2e7dff 100%);
            --dot-shadow: 0 0 12px rgba(46,125,255,0.5);
            --accent-color: #2E7DFF;
            --badge-color: #82b1ff;
            --badge-bg: rgba(22,32,51,0.85);
            --badge-border: rgba(46,125,255,0.35);
        }
        .theme-midnight_navy {
            --card-bg: linear-gradient(170deg,#182336 0%,#0f1a28 50%,#050b16 100%);
            --card-border: #4E6589;
            --digit-color: #FAFAFA;
            --pin-bg: linear-gradient(180deg,#90caf9 0%,#4f8bff 50%,#1565c0 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#90caf9 0%,#4f8bff 100%);
            --dot-shadow: 0 0 12px rgba(79,139,255,0.5);
            --accent-color: #4F8BFF;
            --badge-color: #90caf9;
            --badge-bg: rgba(24,35,54,0.85);
            --badge-border: rgba(79,139,255,0.35);
        }
        .theme-arctic_ice {
            --card-bg: linear-gradient(170deg,#172126 0%,#0f181c 50%,#05080a 100%);
            --card-border: #4B6D77;
            --digit-color: #FFFFFF;
            --pin-bg: linear-gradient(180deg,#b2ebf2 0%,#38d9ff 50%,#006064 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#b2ebf2 0%,#38d9ff 100%);
            --dot-shadow: 0 0 12px rgba(56,217,255,0.5);
            --accent-color: #38D9FF;
            --badge-color: #b2ebf2;
            --badge-bg: rgba(23,33,38,0.85);
            --badge-border: rgba(56,217,255,0.35);
        }
        .theme-ocean_cyan {
            --card-bg: linear-gradient(170deg,#172b33 0%,#0f1e24 50%,#071116 100%);
            --card-border: #47636B;
            --digit-color: #F6FFFF;
            --pin-bg: linear-gradient(180deg,#80deea 0%,#00bcd4 50%,#006064 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#80deea 0%,#00bcd4 100%);
            --dot-shadow: 0 0 12px rgba(0,188,212,0.5);
            --accent-color: #00BCD4;
            --badge-color: #80deea;
            --badge-bg: rgba(23,43,51,0.85);
            --badge-border: rgba(0,188,212,0.35);
        }
        .theme-royal_purple {
            --card-bg: linear-gradient(170deg,#1F1930 0%,#150f21 50%,#08040d 100%);
            --card-border: #50416E;
            --digit-color: #FAFAFA;
            --pin-bg: linear-gradient(180deg,#ce93d8 0%,#8e44ff 50%,#4a148c 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#ce93d8 0%,#8e44ff 100%);
            --dot-shadow: 0 0 12px rgba(142,68,255,0.5);
            --accent-color: #8E44FF;
            --badge-color: #ce93d8;
            --badge-bg: rgba(31,25,48,0.85);
            --badge-border: rgba(142,68,255,0.35);
        }
        .theme-amethyst_elite {
            --card-bg: linear-gradient(170deg,#241A2E 0%,#190f22 50%,#0c0712 100%);
            --card-border: #5D5174;
            --digit-color: #FFFFFF;
            --pin-bg: linear-gradient(180deg,#e1bee7 0%,#a259ff 50%,#6a1b9a 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#e1bee7 0%,#a259ff 100%);
            --dot-shadow: 0 0 12px rgba(162,89,255,0.5);
            --accent-color: #A259FF;
            --badge-color: #e1bee7;
            --badge-bg: rgba(36,26,46,0.85);
            --badge-border: rgba(162,89,255,0.35);
        }
        .theme-platinum_silver {
            --card-bg: linear-gradient(170deg,#262626 0%,#1c1c1c 50%,#101010 100%);
            --card-border: #5A5A5A;
            --digit-color: #FFFFFF;
            --pin-bg: linear-gradient(180deg,#f5f5f5 0%,#c7ccd4 50%,#78909c 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#f5f5f5 0%,#c7ccd4 100%);
            --dot-shadow: 0 0 10px rgba(199,204,212,0.4);
            --accent-color: #C7CCD4;
            --badge-color: #f5f5f5;
            --badge-bg: rgba(38,38,38,0.85);
            --badge-border: rgba(199,204,212,0.3);
        }
        .theme-graphite_gray {
            --card-bg: linear-gradient(170deg,#2A2A2A 0%,#1e1e1e 50%,#111111 100%);
            --card-border: #555555;
            --digit-color: #F5F5F5;
            --pin-bg: linear-gradient(180deg,#bdbdbd 0%,#9e9e9e 50%,#616161 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#bdbdbd 0%,#9e9e9e 100%);
            --dot-shadow: 0 0 8px rgba(158,158,158,0.4);
            --accent-color: #9E9E9E;
            --badge-color: #bdbdbd;
            --badge-bg: rgba(42,42,42,0.85);
            --badge-border: rgba(158,158,158,0.3);
        }
        .theme-copper_elite {
            --card-bg: linear-gradient(170deg,#201A18 0%,#15100e 50%,#090909 100%);
            --card-border: #5C4537;
            --digit-color: #FFF8F2;
            --pin-bg: linear-gradient(180deg,#ffcc80 0%,#b87333 50%,#6d4c41 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#ffcc80 0%,#b87333 100%);
            --dot-shadow: 0 0 12px rgba(184,115,51,0.5);
            --accent-color: #B87333;
            --badge-color: #ffcc80;
            --badge-bg: rgba(32,26,24,0.85);
            --badge-border: rgba(184,115,51,0.35);
        }
        .theme-rose_gold {
            --card-bg: linear-gradient(170deg,#241C1B 0%,#18110f 50%,#0a0909 100%);
            --card-border: #6A504A;
            --digit-color: #FFF8F6;
            --pin-bg: linear-gradient(180deg,#ffccbc 0%,#e8a87c 50%,#bf360c 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#ffccbc 0%,#e8a87c 100%);
            --dot-shadow: 0 0 12px rgba(232,168,124,0.5);
            --accent-color: #E8A87C;
            --badge-color: #ffccbc;
            --badge-bg: rgba(36,28,27,0.85);
            --badge-border: rgba(232,168,124,0.35);
        }
        .theme-champagne_gold {
            --card-bg: linear-gradient(170deg,#24221D 0%,#18160f 50%,#0b0a08 100%);
            --card-border: #6D6655;
            --digit-color: #FFFDF7;
            --pin-bg: linear-gradient(180deg,#fff9c4 0%,#e5c07b 50%,#a07850 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#fff9c4 0%,#e5c07b 100%);
            --dot-shadow: 0 0 10px rgba(229,192,123,0.5);
            --accent-color: #E5C07B;
            --badge-color: #fff9c4;
            --badge-bg: rgba(36,34,29,0.85);
            --badge-border: rgba(229,192,123,0.35);
        }
        .theme-matte_black_diamond {
            --card-bg: linear-gradient(170deg,#181818 0%,#101010 50%,#010101 100%);
            --card-border: #3A3A3A;
            --digit-color: #FCFCFC;
            --digit-shadow: 0 2px 10px rgba(0,0,0,0.95);
            --pin-bg: linear-gradient(180deg,#ffffff 0%,#f0f0f0 50%,#a3a3a3 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#ffffff 0%,#f0f0f0 100%);
            --dot-shadow: 0 0 10px rgba(240,240,240,0.4);
            --accent-color: #F0F0F0;
            --badge-color: #fcfcfc;
            --badge-bg: rgba(24,24,24,0.85);
            --badge-border: rgba(240,240,240,0.3);
        }
        .theme-minimal_light {
            --card-bg: linear-gradient(170deg,#ffffff 0%,#f8fafc 50%,#f1f5f9 100%);
            --card-border: rgba(148,163,184,0.4);
            --card-top-bg: linear-gradient(180deg,rgba(255,255,255,0.9) 0%,rgba(241,245,249,0.5) 100%);
            --card-bot-bg: linear-gradient(180deg,rgba(226,232,240,0.6) 0%,rgba(203,213,225,0.3) 100%);
            --digit-color: #0f172a;
            --digit-shadow: 0 1px 3px rgba(0,0,0,0.15);
            --pin-bg: linear-gradient(180deg,#64748b 0%,#475569 50%,#1e293b 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#94a3b8 0%,#475569 100%);
            --dot-shadow: 0 0 8px rgba(71,85,105,0.3);
            --accent-color: #334155;
            --badge-color: #1e293b;
            --badge-bg: rgba(255,255,255,0.9);
            --badge-border: rgba(148,163,184,0.4);
        }
        .theme-classic_retro {
            --card-bg: linear-gradient(170deg,#1f1f1f 0%,#161616 50%,#0d0d0d 100%);
            --card-border: rgba(255,255,255,0.12);
            --digit-color: #ffffff;
            --digit-shadow: 0 2px 10px rgba(0,0,0,0.9);
            --pin-bg: linear-gradient(180deg,#a3a3a3 0%,#737373 50%,#404040 100%);
            --dot-bg: radial-gradient(circle at 30% 28%,#ffffff 0%,#d4d4d4 50%,#a3a3a3 100%);
            --dot-shadow: 0 0 10px rgba(255,255,255,0.4);
            --accent-color: #ffffff;
            --badge-color: #e5e5e5;
            --badge-bg: rgba(26,26,26,0.85);
            --badge-border: rgba(255,255,255,0.15);
        }
        .theme-liquid_glass {
            --card-bg: rgba(255,255,255,0.12);
            --card-border: rgba(255,255,255,0.18);
            --card-top-bg: linear-gradient(135deg,rgba(255,255,255,0.15) 0%,rgba(255,255,255,0) 50%);
            --card-bot-bg: linear-gradient(180deg,rgba(255,255,255,0.05) 0%,rgba(255,255,255,0.01) 100%);
            --digit-color: #FFFFFF;
            --digit-shadow: 0 4px 12px rgba(0,0,0,0.4);
            --pin-bg: #D4AF37;
            --dot-bg: radial-gradient(circle at 30% 28%,#FFFFFF 0%,#D8D8D8 100%);
            --dot-shadow: 0 0 10px rgba(255,255,255,0.2);
            --accent-color: #D4AF37;
            --badge-color: #D8D8D8;
            --badge-bg: rgba(255,255,255,0.12);
            --badge-border: rgba(255,255,255,0.15);
        }
        .theme-glass_clock {
            --card-bg: rgba(255,255,255,0.08);
            --card-border: rgba(255,255,255,0.18);
            --card-top-bg: linear-gradient(135deg,rgba(255,255,255,0.15) 0%,rgba(255,255,255,0.02) 100%);
            --card-bot-bg: linear-gradient(180deg,rgba(255,255,255,0.05) 0%,rgba(255,255,255,0.01) 100%);
            --digit-color: #FFFFFF;
            --digit-shadow: 0 4px 20px rgba(0,0,0,0.5);
            --pin-bg: #38BDF8;
            --dot-bg: #38BDF8;
            --dot-shadow: 0 0 12px rgba(56,189,248,0.6);
            --accent-color: #38BDF8;
            --badge-color: #38BDF8;
            --badge-bg: rgba(15,23,42,0.85);
            --badge-border: rgba(56,189,248,0.3);
        }
        .theme-glass_aurora {
            --card-bg: rgba(20,184,166,0.08);
            --card-border: rgba(56,189,248,0.25);
            --digit-color: #E0F2FE;
            --accent-color: #38BDF8;
            --badge-color: #E0F2FE;
            --badge-bg: rgba(4,19,38,0.85);
            --badge-border: rgba(56,189,248,0.3);
        }
        .theme-glass_cyberpunk {
            --card-bg: rgba(236,72,153,0.08);
            --card-border: rgba(236,72,153,0.35);
            --digit-color: #FFFFFF;
            --accent-color: #EC4899;
            --badge-color: #EC4899;
            --badge-bg: rgba(20,7,34,0.85);
            --badge-border: rgba(236,72,153,0.4);
        }
        .theme-glass_emerald {
            --card-bg: rgba(16,185,129,0.08);
            --card-border: rgba(212,175,55,0.35);
            --digit-color: #F5F5F7;
            --accent-color: #D4AF37;
            --badge-color: #D4AF37;
            --badge-bg: rgba(5,32,20,0.85);
            --badge-border: rgba(212,175,55,0.4);
        }
        .theme-glass_sunset {
            --card-bg: rgba(251,146,60,0.08);
            --card-border: rgba(253,230,138,0.3);
            --digit-color: #FDE68A;
            --accent-color: #FDE68A;
            --badge-color: #FDE68A;
            --badge-bg: rgba(31,11,30,0.85);
            --badge-border: rgba(253,230,138,0.35);
        }
        .theme-glass_spiderman {
            --card-bg: rgba(220,38,38,0.08);
            --card-border: rgba(239,68,68,0.35);
            --digit-color: #FFFFFF;
            --accent-color: #EF4444;
            --badge-color: #EF4444;
            --badge-bg: rgba(24,3,8,0.85);
            --badge-border: rgba(239,68,68,0.4);
        }
        .theme-glass_ganesha {
            --card-bg: rgba(245,158,11,0.08);
            --card-border: rgba(245,158,11,0.35);
            --digit-color: #FEF3C7;
            --accent-color: #EA580C;
            --badge-color: #FEF3C7;
            --badge-bg: rgba(26,12,2,0.85);
            --badge-border: rgba(245,158,11,0.4);
        }
        .theme-glass_minimal_oled {
            --card-bg: transparent;
            --card-border: transparent;
            --digit-color: #FFFFFF;
            --accent-color: #FFFFFF;
            --badge-color: #FFFFFF;
            --badge-bg: rgba(0,0,0,0.9);
            --badge-border: rgba(255,255,255,0.2);
        }
        .theme-glass_anime_hydrangea {
            --card-bg: transparent;
            --card-border: transparent;
            --digit-color: #F8F5FF;
            --accent-color: #C084FC;
            --badge-color: #F8F5FF;
            --badge-bg: rgba(13,7,20,0.85);
            --badge-border: rgba(192,132,252,0.4);
        }
        .theme-glass_misty_pavilion {
            --card-bg: transparent;
            --card-border: transparent;
            --digit-color: #FEF3C7;
            --accent-color: #F59E0B;
            --badge-color: #FEF3C7;
            --badge-bg: rgba(6,11,18,0.85);
            --badge-border: rgba(245,158,11,0.4);
        }
        .theme-apple_liquid_glass {
            --card-bg: rgba(255,255,255,0.12);
            --card-border: rgba(255,255,255,0.18);
            --card-top-bg: linear-gradient(135deg,rgba(255,255,255,0.15) 0%,rgba(255,255,255,0) 50%);
            --card-bot-bg: linear-gradient(180deg,rgba(255,255,255,0.05) 0%,rgba(255,255,255,0.01) 100%);
            --digit-color: #FFFFFF;
            --digit-shadow: 0 4px 12px rgba(0,0,0,0.4);
            --pin-bg: #D4AF37;
            --dot-bg: radial-gradient(circle at 30% 28%,#FFFFFF 0%,#D8D8D8 100%);
            --dot-shadow: 0 0 10px rgba(255,255,255,0.2);
            --accent-color: #D4AF37;
            --badge-color: #D8D8D8;
            --badge-bg: rgba(255,255,255,0.12);
            --badge-border: rgba(255,255,255,0.18);
        }
        .theme-swiss_minimalist {
            --card-bg: #181818;
            --card-border: transparent;
            --card-top-bg: #181818;
            --card-bot-bg: #181818;
            --digit-color: #FFFFFF;
            --digit-shadow: none;
            --pin-bg: #000000;
            --dot-bg: #FFFFFF;
            --dot-shadow: 0 0 10px rgba(255,255,255,0.4);
            --accent-color: #FFFFFF;
            --badge-color: #F2F2F2;
            --badge-bg: transparent;
            --badge-border: transparent;
        }
        /* Swiss Minimalist structural overrides */
        .theme-swiss_minimalist #scene::before { display:none; }
        .theme-swiss_minimalist #date-badge { display:none; }
        .theme-swiss_minimalist .flip-card {
            background: #181818 !important;
            border: none !important;
            border-radius: 28px;
            box-shadow: 0 18px 40px rgba(0,0,0,0.45), inset 0 0 15px rgba(0,0,0,0.4) !important;
        }
        .theme-swiss_minimalist .card-top, .theme-swiss_minimalist .flipper-top {
            background: #181818 !important;
            border-bottom: none !important;
            border-radius: 28px 28px 0 0;
        }
        .theme-swiss_minimalist .card-bottom, .theme-swiss_minimalist .flipper-bottom {
            background: #181818 !important;
            border-radius: 0 0 28px 28px;
        }
        .theme-swiss_minimalist .card-divider {
            height: 2px !important; background: #000 !important;
            border: none !important; box-shadow: none !important;
        }
        .theme-swiss_minimalist .card-divider::before,
        .theme-swiss_minimalist .card-divider::after { display:none !important; }
        .theme-swiss_minimalist .digit-text {
            font-weight: 900 !important;
            font-size: clamp(90px,22vh,310px) !important;
            letter-spacing: -0.04em !important;
            text-shadow: none !important;
        }
        .theme-swiss_minimalist .sep-dot { background: #FFF !important; box-shadow: 0 0 8px rgba(255,255,255,0.4) !important; }

        /* 23. Minimalist Dark */
        .theme-minimal_dark {
            --card-bg: #1C1C1E;
            --card-border: rgba(255,255,255,0.06);
            --card-top-bg: linear-gradient(180deg,rgba(255,255,255,0.04) 0%,rgba(255,255,255,0.01) 100%);
            --card-bot-bg: linear-gradient(180deg,rgba(0,0,0,0.15) 0%,rgba(0,0,0,0.04) 100%);
            --digit-color: #FFFFFF;
            --digit-shadow: none;
            --pin-bg: rgba(255,255,255,0.15);
            --dot-bg: rgba(235,235,245,0.6);
            --dot-shadow: none;
            --accent-color: rgba(235,235,245,0.6);
            --badge-color: rgba(235,235,245,0.85);
            --badge-bg: rgba(44,44,46,0.9);
            --badge-border: rgba(255,255,255,0.1);
        }
        /* Minimalist Dark structural overrides */
        .theme-minimal_dark #scene { background: #111111 !important; }
        .theme-minimal_dark #scene::before { display:none !important; }
        .theme-minimal_dark #branding-tag { display:none !important; }
        .theme-minimal_dark .flip-card {
            background: #1C1C1E !important;
            border: 1px solid rgba(255,255,255,0.06) !important;
            border-radius: 20px;
            box-shadow: 0 12px 32px rgba(0,0,0,0.55), inset 0 1px 0 rgba(255,255,255,0.05) !important;
        }
        .theme-minimal_dark .card-top, .theme-minimal_dark .flipper-top {
            background: rgba(255,255,255,0.03) !important;
            border-radius: 20px 20px 0 0;
            border-bottom: 1px solid rgba(0,0,0,0.4) !important;
        }
        .theme-minimal_dark .card-bottom, .theme-minimal_dark .flipper-bottom {
            background: rgba(0,0,0,0.1) !important;
            border-radius: 0 0 20px 20px;
        }
        .theme-minimal_dark .card-divider {
            height: 1px !important; background: rgba(0,0,0,0.6) !important;
            border: none !important; box-shadow: none !important;
        }
        .theme-minimal_dark .card-divider::before,
        .theme-minimal_dark .card-divider::after { display:none !important; }
        .theme-minimal_dark .digit-text {
            font-weight: 700 !important;
            font-size: clamp(90px,22vh,310px) !important;
            letter-spacing: -0.03em !important;
            text-shadow: none !important;
        }
        .theme-minimal_dark .sep-dot { background: rgba(235,235,245,0.6) !important; box-shadow: none !important; }

        /* ─── Scene ─── */
        #scene {
            position:relative;
            width:100vw; height:100vh;
            display:flex; flex-direction:column;
            align-items:center; justify-content:center;
            gap:5vh; overflow:hidden;
            background: #000000;
        }
        #scene::before {
            content:''; position:absolute; inset:0;
            background: radial-gradient(ellipse 70% 55% at 50% 48%,rgba(255,255,255,0.015) 0%,transparent 70%);
            pointer-events:none; z-index:0;
        }

        .clock-row {
            display:flex; align-items:center; justify-content:center;
            gap:clamp(14px,3vw,48px); z-index:10; width:100%; max-width:94vw;
        }

        .flip-card {
            position:relative;
            width: clamp(160px,36vh,440px);
            height: clamp(220px,52vh,620px);
            border-radius: clamp(10px,1.8vh,24px);
            overflow:hidden; perspective:1400px; flex-shrink:0;
            background: var(--card-bg);
            border: 1.5px solid var(--card-border);
            box-shadow: 0 18px 70px rgba(0,0,0,0.95), 0 0 0 1px rgba(255,255,255,0.04),
                inset 0 1px 0 rgba(255,255,255,0.08), inset 0 -1px 0 rgba(0,0,0,0.8);
        }

        .card-half { position:absolute; left:0; width:100%; height:50%; overflow:hidden; }
        .card-top {
            top:0; border-radius: clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px) 0 0;
            background: var(--card-top-bg);
            border-bottom: 1px solid rgba(0,0,0,0.85);
        }
        .card-bottom {
            bottom:0; border-radius: 0 0 clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px);
            background: var(--card-bot-bg);
        }

        .card-divider {
            position:absolute; top:50%; left:0;
            width:100%; height:3px;
            transform:translateY(-50%); z-index:12;
            background: #000000;
            box-shadow: 0 1px 4px rgba(0,0,0,0.95);
        }
        .card-divider::before, .card-divider::after {
            content:''; position:absolute; top:50%; transform:translateY(-50%);
            width: clamp(5px,0.7vh,10px); height: clamp(10px,1.5vh,18px);
            border-radius: clamp(2px,0.4vh,5px);
            background: var(--pin-bg);
            box-shadow: 0 1px 3px rgba(0,0,0,0.8), inset 0 1px 0 rgba(255,255,255,0.2);
        }
        .card-divider::before { left: clamp(8px,1.2vh,16px); }
        .card-divider::after  { right: clamp(8px,1.2vh,16px); }

        .digit-wrapper {
            position:absolute; left:0; width:100%; height:200%;
            display:flex; align-items:center; justify-content:center;
        }
        .card-top .digit-wrapper, .flipper-top .digit-wrapper { top:0; }
        .card-bottom .digit-wrapper, .flipper-bottom .digit-wrapper { bottom:0; }

        .digit-text {
            font-family: var(--digit-font);
            font-size: clamp(90px,22vh,310px);
            font-weight:800;
            color: var(--digit-color);
            letter-spacing:-0.02em;
            line-height:1; text-align:center;
            text-shadow: var(--digit-shadow);
        }

        .flipper { position:absolute; left:0; width:100%; overflow:hidden; backface-visibility:hidden; }
        .flipper-top {
            top:0; height:50%; transform-origin:bottom center;
            border-radius: clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px) 0 0;
            background: var(--card-top-bg);
        }
        .flipper-bottom {
            bottom:0; height:50%; transform-origin:top center;
            border-radius: 0 0 clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px);
            background: var(--card-bot-bg);
        }
        @keyframes flipTopOut   { 0%{transform:rotateX(0deg)}   100%{transform:rotateX(-90deg)} }
        @keyframes flipBottomIn { 0%{transform:rotateX(90deg)}  100%{transform:rotateX(0deg)}   }
        .flip-top-out   { animation: flipTopOut   0.3s cubic-bezier(0.45,0,0.55,1) forwards; }
        .flip-bottom-in { animation: flipBottomIn 0.3s cubic-bezier(0.45,0,0.55,1) 0.3s forwards; transform:rotateX(90deg); }

        .sep { display:flex; flex-direction:column; align-items:center; gap:clamp(14px,2.8vh,32px); }
        .sep-dot {
            width: clamp(7px,1vh,14px); height: clamp(7px,1vh,14px);
            border-radius:50%;
            background: var(--dot-bg);
            box-shadow: var(--dot-shadow);
        }

        #date-badge {
            z-index:10;
            padding: clamp(7px,1vh,14px) clamp(22px,3.2vw,52px);
            border-radius:50px;
            font-family: var(--label-font);
            font-size:clamp(10px,1.3vw,18px);
            font-weight:700; letter-spacing:0.2em; text-transform:uppercase;
            color: var(--badge-color);
            background: var(--badge-bg);
            border: 1px solid var(--badge-border);
            box-shadow: 0 6px 30px rgba(0,0,0,0.7);
            backdrop-filter: blur(10px); -webkit-backdrop-filter: blur(10px);
        }
        .hide-date-badge #date-badge { display:none !important; }

        #close-btn {
            position:fixed; top:18px; right:18px; z-index:9999;
            width:44px; height:44px; border-radius:50%;
            border:1.5px solid var(--badge-border, rgba(180,155,80,0.3));
            background: var(--badge-bg, rgba(20,20,24,0.85));
            backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
            color: var(--accent-color, #c8a830);
            font-size:20px; font-weight:300;
            font-family: var(--digit-font, 'Inter',sans-serif);
            cursor:pointer; display:flex; align-items:center; justify-content:center;
            opacity:0;
            transition: opacity 0.4s ease, background 0.3s ease, transform 0.3s ease;
            box-shadow: 0 4px 20px rgba(0,0,0,0.6);
        }
        #close-btn:hover { background:rgba(200,168,48,0.2); border-color:rgba(200,168,48,0.5); transform:scale(1.1); }
        #scene.show-close #close-btn { opacity:1; }
    </style>
</head>
<body>

<div id="scene">
    <button id="close-btn" onclick="forceClose()" title="Close Screensaver">✕</button>

    <div class="clock-row">
        <div class="flip-card" id="fc-h">
            <div class="card-half card-top"><div class="digit-wrapper"><span class="digit-text" id="fc-h-top">00</span></div></div>
            <div class="card-half card-bottom"><div class="digit-wrapper"><span class="digit-text" id="fc-h-bot">00</span></div></div>
            <div class="card-divider"></div>
        </div>

        <div class="sep"><div class="sep-dot"></div><div class="sep-dot"></div></div>

        <div class="flip-card" id="fc-m">
            <div class="card-half card-top"><div class="digit-wrapper"><span class="digit-text" id="fc-m-top">00</span></div></div>
            <div class="card-half card-bottom"><div class="digit-wrapper"><span class="digit-text" id="fc-m-bot">00</span></div></div>
            <div class="card-divider"></div>
        </div>

        <div class="sep"><div class="sep-dot"></div><div class="sep-dot"></div></div>

        <div class="flip-card" id="fc-s">
            <div class="card-half card-top"><div class="digit-wrapper"><span class="digit-text" id="fc-s-top">00</span></div></div>
            <div class="card-half card-bottom"><div class="digit-wrapper"><span class="digit-text" id="fc-s-bot">00</span></div></div>
            <div class="card-divider"></div>
        </div>
    </div>

    <div id="date-badge"></div>
</div>

<script>
function updateDate() {
    const cfg = window.screensaverConfig || {};
    const showDate = cfg.show_date !== 'false';
    const showDay = cfg.show_day !== 'false';
    const b = document.getElementById('date-badge');
    if (!b) return;

    const scene = document.getElementById('scene');
    if (scene) {
        if (!showDate && !showDay) scene.classList.add('hide-date-badge');
        else scene.classList.remove('hide-date-badge');
    }

    const now = new Date();
    const days   = ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY'];
    const months = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'];

    const dayName = days[now.getDay()];
    const dateNum = now.getDate();
    const monthName = months[now.getMonth()];
    const yearNum = now.getFullYear();

    let content = '';
    if (showDay) {
        content += dayName;
    }
    if (showDay && showDate) {
        content += ' \u25C6 ';
    }
    if (showDate) {
        content += `${dateNum} ${monthName} ${yearNum}`;
    }
    b.textContent = content;
}

let pH = -1, pM = -1, pS = -1;
function updateFlip() {
    const now = new Date();
    const h = now.getHours(), m = now.getMinutes(), s = now.getSeconds();
    const p = n => String(n).padStart(2,'0');
    if (h !== pH) { doFlip('fc-h', p(h)); pH = h; }
    if (m !== pM) { doFlip('fc-m', p(m)); pM = m; }
    if (s !== pS) { doFlip('fc-s', p(s)); pS = s; }
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
    setTimeout(function() { ft.remove(); fb.remove(); }, 700);
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

let hideTimer = null;
document.addEventListener('mousemove', function() {
    document.getElementById('scene').classList.add('show-close');
    clearTimeout(hideTimer);
    hideTimer = setTimeout(function() {
        document.getElementById('scene').classList.remove('show-close');
    }, 3000);
});

document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') forceClose();
});

window.addEventListener('load', function() {
    applyTheme();
    updateDate(); updateFlip();
    setInterval(updateFlip, 1000);
    setInterval(updateDate, 30000);
});

function applyTheme() {
    const cfg = window.screensaverConfig || {};
    const theme = cfg.theme || 'luxury_black_gold';
    const scene = document.getElementById('scene');
    if (!scene) return;

    // Remove any existing theme classes
    scene.className = scene.className.replace(/\\btheme-\\S+/g, '').trim();
    scene.classList.add('theme-' + theme);

    // Apply background
    const lightBg = { minimal_light: '#f1f5f9' };
    if (theme === 'custom') {
        scene.style.background = cfg.custom_bg_color || '#000000';
    } else if (lightBg[theme]) {
        scene.style.background = lightBg[theme];
    } else if (theme === 'minimal_dark') {
        scene.style.background = '#111111';
    } else {
        scene.style.background = '#000000';
    }

    // Apply fonts if specified
    if (cfg.digit_font) {
        document.documentElement.style.setProperty('--digit-font', "'" + cfg.digit_font + "', system-ui, sans-serif");
    }
    if (cfg.label_font) {
        document.documentElement.style.setProperty('--label-font', "'" + cfg.label_font + "', serif");
    }
}
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

class ScreensaverWindow(Gtk.Window):
    def __init__(self, html_path, monitor_idx):
        super().__init__(title=f"Screensaver Clock - Monitor {monitor_idx}")
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
        if hasattr(settings, 'set_media_playback_requires_user_gesture'):
            settings.set_media_playback_requires_user_gesture(False)
            
        self.webview.add_events(Gdk.EventMask.POINTER_MOTION_MASK | 
                                Gdk.EventMask.BUTTON_PRESS_MASK | 
                                Gdk.EventMask.KEY_PRESS_MASK |
                                Gdk.EventMask.SCROLL_MASK |
                                Gdk.EventMask.TOUCH_MASK)
        
        # Guard against WebKit load failures
        self.webview.connect("load-failed", self.on_load_failed)
        
        # Script Message Handler for DOM exit events
        ucm = self.webview.get_user_content_manager()
        ucm.register_script_message_handler("screensaverExit")
        ucm.connect("script-message-received::screensaverExit", self.on_script_message)
        
        self.add(self.webview)
        
        # Load config if present
        config_path = os.path.expanduser("~/.config/flipclock/flipclock.conf")
        fmt, size, speed = "12", "1.0", "500"
        theme = "luxury_black_gold"
        show_seconds = "true"
        show_date = "true"
        show_day = "true"
        show_greeting = "true"
        user_name = ""
        custom_credit = "FLIP CLOCK SCREENSAVER"
        digit_font = "Cinzel"
        label_font = "Cinzel"
        custom_bg_color = "#000000"
        custom_card_color = "#1C1C1E"
        custom_digit_color = "#F5F5F7"
        custom_accent_color = "#D4AF37"
        custom_border_color = "#4A4A4A"
        card_shape = "soft_squircle"
        
        if os.path.exists(config_path):
            try:
                import configparser
                cp = configparser.ConfigParser()
                cp.read(config_path)
                if 'Settings' in cp:
                    fmt = cp['Settings'].get('hour_format', '12')
                    size = cp['Settings'].get('clock_size', '1.0')
                    speed = cp['Settings'].get('animation_speed', '500')
                    theme = cp['Settings'].get('theme', 'luxury_black_gold')
                    show_seconds = cp['Settings'].get('show_seconds', 'true')
                    show_date = cp['Settings'].get('show_date', 'true')
                    show_day = cp['Settings'].get('show_day', 'true')
                    show_greeting = cp['Settings'].get('show_greeting', 'true')
                    user_name = cp['Settings'].get('user_name', '').replace("'", "\\'")
                    custom_credit = cp['Settings'].get('custom_credit', 'FLIP CLOCK SCREENSAVER')
                    digit_font = cp['Settings'].get('digit_font', 'Cinzel').replace("'", "\\'")
                    label_font = cp['Settings'].get('label_font', 'Cinzel').replace("'", "\\'")
                    custom_bg_color = cp['Settings'].get('custom_bg_color', '#000000').replace("'", "\\'")
                    custom_card_color = cp['Settings'].get('custom_card_color', '#1C1C1E').replace("'", "\\'")
                    custom_digit_color = cp['Settings'].get('custom_digit_color', '#F5F5F7').replace("'", "\\'")
                    custom_accent_color = cp['Settings'].get('custom_accent_color', '#D4AF37').replace("'", "\\'")
                    custom_border_color = cp['Settings'].get('custom_border_color', '#4A4A4A').replace("'", "\\'")
                    card_shape = cp['Settings'].get('card_shape', 'soft_squircle').replace("'", "\\'")
            except Exception:
                pass
                
        html_content, base_dir = get_html_content(html_path)
        if not html_content:
            print("Error: Could not locate clock.html or index.html")
            sys.exit(1)
            
        config_script = f"<script>window.screensaverConfig = {{ monitor: '{monitor_idx}', format: '{fmt}', size: '{size}', speed: '{speed}', theme: '{theme}', card_shape: '{card_shape}', show_seconds: '{show_seconds}', show_date: '{show_date}', show_day: '{show_day}', show_greeting: '{show_greeting}', user_name: '{user_name}', custom_credit: '{custom_credit}', digit_font: '{digit_font}', label_font: '{label_font}', custom_bg_color: '{custom_bg_color}', custom_card_color: '{custom_card_color}', custom_digit_color: '{custom_digit_color}', custom_accent_color: '{custom_accent_color}', custom_border_color: '{custom_border_color}' }};</script>"
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", f"{config_script}</head>")
        else:
            html_content = config_script + html_content
            
        base_uri = "file://" + base_dir + "/"
        self.webview.load_html(html_content, base_uri)
        
        # GTK signals
        self.connect("destroy", Gtk.main_quit)
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
            print(f"GTK key press event: {event.keyval}. Exiting screensaver.")
            Gtk.main_quit()
        return True

    def on_input_event(self, widget, event):
        global mouse_input_enabled
        if mouse_input_enabled:
            print(f"GTK input event: {event.type}. Exiting screensaver.")
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
        if dist > threshold:
            print(f"Mouse moved {dist:.1f}px. Exiting.")
            Gtk.main_quit()
        return True

if __name__ == "__main__":
    html_file = sys.argv[1] if len(sys.argv) > 1 else None
    
    Gtk.init(None)
    
    display = Gdk.Display.get_default()
    n_monitors = display.get_n_monitors() if (display and hasattr(display, 'get_n_monitors')) else 1
    print(f"Spawning screensaver clock windows on {n_monitors} monitors...")
    
    windows = []
    for i in range(n_monitors):
        win = ScreensaverWindow(html_file, monitor_idx=i)
        windows.append(win)
        
    GLib.timeout_add(400, enable_key_input)
    GLib.timeout_add(800, enable_mouse_input)
    Gtk.main()
