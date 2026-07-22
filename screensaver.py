#!/usr/bin/env python3
import sys
import os
import math
import gi

gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, Gdk, WebKit2, GLib

# Shared mouse position variables to handle multi-monitor coordinate tracking
initial_x = None
initial_y = None
threshold = 15 # pixels

class ScreensaverWindow(Gtk.Window):
    def __init__(self, html_path, monitor_idx):
        super().__init__(title=f"Screensaver Clock - Monitor {monitor_idx}")
        self.set_decorated(False)
        self.set_keep_above(True)
        
        # Position the window on the correct monitor geometry
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
        
        # Enable event masks
        self.add_events(Gdk.EventMask.POINTER_MOTION_MASK | 
                        Gdk.EventMask.BUTTON_PRESS_MASK | 
                        Gdk.EventMask.KEY_PRESS_MASK |
                        Gdk.EventMask.SCROLL_MASK)
        
        # WebKit WebView
        self.webview = WebKit2.WebView()
        self.webview.add_events(Gdk.EventMask.POINTER_MOTION_MASK | 
                                Gdk.EventMask.BUTTON_PRESS_MASK | 
                                Gdk.EventMask.KEY_PRESS_MASK |
                                Gdk.EventMask.SCROLL_MASK)
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
        query_string = f"?format={fmt}&size={size}&speed={speed}"
        self.webview.load_uri("file://" + os.path.abspath(html_path) + query_string)
        
        # Signals
        self.connect("destroy", Gtk.main_quit)
        self.connect("key-press-event", self.on_input_event)
        self.connect("button-press-event", self.on_input_event)
        self.connect("motion-notify-event", self.on_motion_event)
        self.connect("scroll-event", self.on_input_event)
        
        self.webview.connect("key-press-event", self.on_input_event)
        self.webview.connect("button-press-event", self.on_input_event)
        self.webview.connect("motion-notify-event", self.on_motion_event)
        self.webview.connect("scroll-event", self.on_input_event)
        
        self.show_all()
        if display and hasattr(display, 'get_n_monitors') and monitor_idx < display.get_n_monitors():
            self.fullscreen_on_monitor(self.get_screen(), monitor_idx)
        else:
            self.fullscreen()
        
    def on_input_event(self, widget, event):
        print(f"Input event detected: {event.type}. Exiting screensaver.")
        Gtk.main_quit()
        return True

    def on_motion_event(self, widget, event):
        global initial_x, initial_y
        
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
            
        if initial_x is None or initial_y is None:
            initial_x = x
            initial_y = y
            return True
            
        dist = math.sqrt((x - initial_x)**2 + (y - initial_y)**2)
        if dist > threshold:
            print(f"Mouse moved past threshold: {dist:.1f}px. Exiting.")
            Gtk.main_quit()
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: screensaver.py <html_file>")
        sys.exit(1)
    
    html_file = sys.argv[1]
    
    # Initialize GTK
    Gtk.init(None)
    
    # Spawn a window for each connected monitor
    display = Gdk.Display.get_default()
    n_monitors = display.get_n_monitors()
    print(f"Spawning screensaver clock windows on {n_monitors} monitors...")
    
    windows = []
    for i in range(n_monitors):
        win = ScreensaverWindow(html_file, monitor_idx=i)
        windows.append(win)
        
    Gtk.main()
