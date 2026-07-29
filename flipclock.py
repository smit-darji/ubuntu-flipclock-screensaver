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
from gi.repository import Gtk, Gdk, WebKit2, GLib

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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Cinzel:wght@700;800;900&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin:0; padding:0; box-sizing:border-box; user-select:none; -webkit-user-select:none; }
        html, body { width:100vw; height:100vh; overflow:hidden; cursor:none; }

        #scene {
            position:relative;
            width:100vw; height:100vh;
            display:flex; flex-direction:column;
            align-items:center; justify-content:center;
            gap:5vh;
            overflow:hidden;
            background: #000000;
        }

        #scene::before {
            content:'';
            position:absolute; inset:0;
            background: radial-gradient(ellipse 70% 55% at 50% 48%, rgba(255,255,255,0.015) 0%, transparent 70%);
            pointer-events:none; z-index:0;
        }

        .clock-row {
            display:flex;
            align-items:center;
            justify-content:center;
            gap:clamp(14px, 3vw, 48px);
            z-index:10;
            width:100%;
            max-width:94vw;
        }

        .flip-card {
            position:relative;
            width:  clamp(160px, 36vh, 440px);
            height: clamp(220px, 52vh, 620px);
            border-radius: clamp(10px, 1.8vh, 24px);
            overflow:hidden;
            perspective:1400px;
            flex-shrink:0;
            background: linear-gradient(170deg, #1e1e22 0%, #141418 40%, #0c0c10 100%);
            border: 1.5px solid rgba(180,155,80,0.3);
            box-shadow:
                0 18px 70px rgba(0,0,0,0.95),
                0 0 0 1px rgba(255,255,255,0.04),
                inset 0 1px 0 rgba(255,255,255,0.08),
                inset 0 -1px 0 rgba(0,0,0,0.8);
        }

        .card-half { position:absolute; left:0; width:100%; height:50%; overflow:hidden; }
        .card-top {
            top:0;
            border-radius: clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px) 0 0;
            background: linear-gradient(180deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.015) 100%);
            border-bottom: 1px solid rgba(0,0,0,0.85);
        }
        .card-bottom {
            bottom:0;
            border-radius: 0 0 clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px);
            background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.08) 100%);
        }

        .card-divider {
            position:absolute; top:50%; left:0;
            width:100%; height:3px;
            transform:translateY(-50%);
            z-index:12;
            background: #000000;
            box-shadow: 0 1px 4px rgba(0,0,0,0.95);
        }
        .card-divider::before, .card-divider::after {
            content:'';
            position:absolute; top:50%; transform:translateY(-50%);
            width:  clamp(5px, 0.7vh, 10px);
            height: clamp(10px, 1.5vh, 18px);
            border-radius: clamp(2px, 0.4vh, 5px);
            background: linear-gradient(180deg, #e8cc70 0%, #b09840 50%, #806820 100%);
            box-shadow: 0 1px 3px rgba(0,0,0,0.8), inset 0 1px 0 rgba(255,255,255,0.2);
        }
        .card-divider::before { left:  clamp(8px, 1.2vh, 16px); }
        .card-divider::after  { right: clamp(8px, 1.2vh, 16px); }

        .digit-wrapper {
            position:absolute; left:0; width:100%; height:200%;
            display:flex; align-items:center; justify-content:center;
        }
        .card-top    .digit-wrapper, .flipper-top    .digit-wrapper { top:0; }
        .card-bottom .digit-wrapper, .flipper-bottom .digit-wrapper { bottom:0; }

        .digit-text {
            font-family:'Inter',system-ui,sans-serif;
            font-size: clamp(90px, 22vh, 310px);
            font-weight:800;
            color: #f0f0f0;
            letter-spacing:-0.02em;
            line-height:1;
            text-align:center;
            text-shadow: 0 2px 10px rgba(0,0,0,0.5);
        }

        .flipper { position:absolute; left:0; width:100%; overflow:hidden; backface-visibility:hidden; }
        .flipper-top {
            top:0; height:50%;
            transform-origin:bottom center;
            border-radius: clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px) 0 0;
            background: linear-gradient(180deg, rgba(255,255,255,0.06) 0%, rgba(255,255,255,0.015) 100%);
        }
        .flipper-bottom {
            bottom:0; height:50%;
            transform-origin:top center;
            border-radius: 0 0 clamp(10px,1.8vh,24px) clamp(10px,1.8vh,24px);
            background: linear-gradient(180deg, rgba(0,0,0,0.2) 0%, rgba(0,0,0,0.08) 100%);
        }
        @keyframes flipTopOut    { 0%{transform:rotateX(0deg)}  100%{transform:rotateX(-90deg)} }
        @keyframes flipBottomIn  { 0%{transform:rotateX(90deg)} 100%{transform:rotateX(0deg)}   }
        .flip-top-out   { animation: flipTopOut   0.3s cubic-bezier(0.45,0,0.55,1) forwards; }
        .flip-bottom-in { animation: flipBottomIn 0.3s cubic-bezier(0.45,0,0.55,1) 0.3s forwards; transform:rotateX(90deg); }

        .sep {
            display:flex; flex-direction:column;
            align-items:center;
            gap:clamp(14px, 2.8vh, 32px);
        }
        .sep-dot {
            width:  clamp(7px, 1vh, 14px);
            height: clamp(7px, 1vh, 14px);
            border-radius:50%;
            background: radial-gradient(circle at 30% 28%, #f0d860 0%, #c8a830 45%, #806818 100%);
            box-shadow: 0 0 12px rgba(200,168,48,0.4), 0 0 4px rgba(200,168,48,0.6);
        }

        #date-badge {
            z-index:10;
            padding: clamp(7px,1vh,14px) clamp(22px,3.2vw,52px);
            border-radius:50px;
            font-family:'Cinzel',serif;
            font-size:clamp(10px, 1.3vw, 18px);
            font-weight:700;
            letter-spacing:0.2em;
            text-transform:uppercase;
            color: #c8a830;
            background: rgba(20,20,24,0.7);
            border: 1px solid rgba(180,155,80,0.22);
            box-shadow: 0 6px 30px rgba(0,0,0,0.7);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
        }

        #close-btn {
            position:fixed;
            top:18px; right:18px;
            z-index:9999;
            width:44px; height:44px;
            border-radius:50%;
            border:1.5px solid rgba(180,155,80,0.3);
            background:rgba(20,20,24,0.85);
            backdrop-filter:blur(12px);
            -webkit-backdrop-filter:blur(12px);
            color:#c8a830;
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
            background:rgba(200,168,48,0.2);
            border-color:rgba(200,168,48,0.5);
            transform:scale(1.1);
        }
        #scene.show-close #close-btn {
            opacity:1;
        }
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
    const now = new Date();
    const days   = ['SUNDAY','MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY'];
    const months = ['JANUARY','FEBRUARY','MARCH','APRIL','MAY','JUNE','JULY','AUGUST','SEPTEMBER','OCTOBER','NOVEMBER','DECEMBER'];
    const b = document.getElementById('date-badge');
    if (b) b.textContent = `${days[now.getDay()]} \u25C6 ${now.getDate()} ${months[now.getMonth()]} ${now.getFullYear()}`;
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
    updateDate(); updateFlip();
    setInterval(updateFlip, 1000);
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
        
        config_script = f"<script>window.screensaverConfig = {{ monitor: '{monitor_idx}', format: '{fmt}', size: '{size}', speed: '{speed}' }};</script>"
        if "</head>" in html_content:
            html_content = html_content.replace("</head>", f"{config_script}</head>")
        else:
            html_content = config_script + html_content
            
        base_uri = "file://" + base_dir + "/"
        self.webview.load_html(html_content, base_uri)
        
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
    """Configuration GUI window for Flip Clock Screensaver."""
    def __init__(self, manager):
        super().__init__(title="Flip Clock Settings")
        self.manager = manager
        self.set_default_size(350, 250)
        self.set_border_width(15)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title("Flip Clock Settings")
        self.set_titlebar(hb)
        
        grid = Gtk.Grid()
        grid.set_column_spacing(15)
        grid.set_row_spacing(15)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.add(grid)
        
        lbl_format = Gtk.Label(label="Time Format:")
        lbl_format.set_xalign(0)
        grid.attach(lbl_format, 0, 0, 1, 1)
        
        self.combo_format = Gtk.ComboBoxText()
        self.combo_format.append("12", "12-Hour (AM/PM)")
        self.combo_format.append("24", "24-Hour")
        current_fmt = self.manager.config.get('hour_format', '12')
        self.combo_format.set_active_id(current_fmt)
        grid.attach(self.combo_format, 1, 0, 1, 1)
        
        lbl_timeout = Gtk.Label(label="Idle Timeout:")
        lbl_timeout.set_xalign(0)
        grid.attach(lbl_timeout, 0, 1, 1, 1)
        
        self.combo_timeout = Gtk.ComboBoxText()
        self.combo_timeout.append("60", "1 Minute")
        self.combo_timeout.append("120", "2 Minutes")
        self.combo_timeout.append("180", "3 Minutes")
        self.combo_timeout.append("240", "4 Minutes")
        self.combo_timeout.append("300", "5 Minutes")
        self.combo_timeout.append("600", "10 Minutes")
        self.combo_timeout.append("900", "15 Minutes")
        self.combo_timeout.append("1800", "30 Minutes")
        self.combo_timeout.append("3600", "1 Hour")
        
        current_to = str(self.manager.config.get('idle_timeout', 60))
        if current_to not in ["60", "120", "180", "240", "300", "600", "900", "1800", "3600"]:
            self.combo_timeout.append(current_to, f"{int(current_to)//60} Minutes")
        self.combo_timeout.set_active_id(current_to)
        grid.attach(self.combo_timeout, 1, 1, 1, 1)
        
        lbl_size = Gtk.Label(label="Clock Size:")
        lbl_size.set_xalign(0)
        grid.attach(lbl_size, 0, 2, 1, 1)
        
        current_size = float(self.manager.config.get('clock_size', '1.0'))
        self.adj_size = Gtk.Adjustment(value=current_size, lower=0.5, upper=2.0, step_increment=0.1, page_increment=0.5, page_size=0)
        self.scale_size = Gtk.Scale(orientation=Gtk.Orientation.HORIZONTAL, adjustment=self.adj_size)
        self.scale_size.set_digits(1)
        self.scale_size.set_hexpand(True)
        self.scale_size.set_size_request(150, -1)
        grid.attach(self.scale_size, 1, 2, 1, 1)
        
        self.btn_save = Gtk.Button(label="Save & Apply")
        self.btn_save.connect("clicked", self.on_save_clicked)
        grid.attach(self.btn_save, 0, 3, 2, 1)
        
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        
    def on_save_clicked(self, button):
        fmt = self.combo_format.get_active_id() or "12"
        timeout_str = self.combo_timeout.get_active_id() or "60"
        try:
            timeout = int(timeout_str)
        except ValueError:
            timeout = 60
        size = f"{self.scale_size.get_value():.1f}"
        
        self.manager.config['hour_format'] = fmt
        self.manager.config['idle_timeout'] = timeout
        self.manager.config['clock_size'] = size
        
        self.manager.save_config()
        self.manager.restart_daemon()
        
        dialog = Gtk.MessageDialog(
            transient_for=self,
            flags=0,
            message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK,
            text="Settings Saved!",
        )
        dialog.format_secondary_text("Configuration applied and screensaver daemon restarted.\n\nThe screensaver preview will start now.")
        dialog.run()
        dialog.destroy()
        
        try:
            if os.path.exists("/usr/bin/flipclock"):
                subprocess.Popen(["/usr/bin/flipclock", "--run"])
            elif os.path.exists("/usr/share/flipclock/flipclock.py"):
                subprocess.Popen([sys.executable, "/usr/share/flipclock/flipclock.py", "--run"])
            else:
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
            'monitors': 'all'
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
            except Exception as e:
                print(f"Error reading config, using defaults: {e}")
        else:
            parser['Settings'] = {
                'idle_timeout': str(self.config['idle_timeout']),
                'hour_format': self.config['hour_format'],
                'clock_size': self.config['clock_size'],
                'animation_speed': str(self.config['animation_speed']),
                'monitors': self.config['monitors']
            }
            try:
                with open(self.config_path, 'w') as f:
                    parser.write(f)
            except Exception as e:
                print(f"Could not write default configuration: {e}")

    def save_config(self):
        parser = configparser.ConfigParser()
        parser['Settings'] = {
            'idle_timeout': str(self.config['idle_timeout']),
            'hour_format': self.config['hour_format'],
            'clock_size': self.config['clock_size'],
            'animation_speed': str(self.config['animation_speed']),
            'monitors': self.config['monitors']
        }
        try:
            with open(self.config_path, 'w') as f:
                parser.write(f)
        except Exception as e:
            print(f"Error saving config file: {e}")

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
    args = parser.parse_args()
    
    manager = FlipClockManager()
    
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
