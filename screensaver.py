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
        if os.path.exists(config_path):
            try:
                import configparser
                cp = configparser.ConfigParser()
                cp.read(config_path)
                if 'Settings' in cp:
                    fmt = cp['Settings'].get('hour_format', '12')
                    size = cp['Settings'].get('clock_size', '1.0')
                    speed = cp['Settings'].get('animation_speed', '500')
            except Exception:
                pass
                
        html_content, base_dir = get_html_content(html_path)
        if not html_content:
            print("Error: Could not locate clock.html or index.html")
            sys.exit(1)
            
        config_script = f"<script>window.screensaverConfig = {{ monitor: '{monitor_idx}', format: '{fmt}', size: '{size}', speed: '{speed}' }};</script>"
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
