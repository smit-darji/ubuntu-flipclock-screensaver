#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import ctypes
import math
import argparse
import configparser
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
    print(f"X11 screensaver library not available: {e}")

# Global mouse tracking variables
initial_x = None
initial_y = None
exit_threshold = 15 # pixels
tracking_enabled = False

def enable_mouse_tracking():
    global tracking_enabled, initial_x, initial_y
    display = Gdk.Display.get_default()
    if display:
        seat = display.get_default_seat()
        if seat:
            pointer = seat.get_pointer()
            if pointer:
                _, x, y = pointer.get_position()
                initial_x = x
                initial_y = y
    tracking_enabled = True
    print(f"Mouse motion tracking activated at base: ({initial_x}, {initial_y})")
    return False # Run once

class FlipClockWindow(Gtk.Window):
    """Fullscreen GTK window hosting the WebKit flip clock."""
    def __init__(self, html_path, monitor_idx, config_params):
        super().__init__(title=f"Flip Clock - Screen {monitor_idx}")
        self.set_decorated(False)
        self.set_keep_above(True)
        
        # Position window on correct monitor geometry
        display = Gdk.Display.get_default()
        monitor = display.get_monitor(monitor_idx)
        geom = monitor.get_geometry()
        self.move(geom.x, geom.y)
        self.resize(geom.width, geom.height)
        
        # Add event listeners for interaction
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
        
        # Formulate query string based on configuration
        query_string = f"?format={config_params['hour_format']}&size={config_params['clock_size']}&speed={config_params['animation_speed']}"
        full_uri = "file://" + os.path.abspath(html_path) + query_string
        self.webview.load_uri(full_uri)
        
        # Connect exit triggers
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
        self.fullscreen_on_monitor(self.get_screen(), monitor_idx)

    def on_input_event(self, widget, event):
        print(f"Input event: {event.type}. Exiting.")
        Gtk.main_quit()
        return True

    def on_motion_event(self, widget, event):
        global tracking_enabled, initial_x, initial_y
        
        if not tracking_enabled:
            return True
            
        display = Gdk.Display.get_default()
        seat = display.get_default_seat()
        pointer = seat.get_pointer()
        _, x, y = pointer.get_position()
        
        if initial_x is None or initial_y is None:
            initial_x = x
            initial_y = y
            return True
            
        dist = math.sqrt((x - initial_x)**2 + (y - initial_y)**2)
        if dist > exit_threshold:
            print(f"Mouse moved past threshold: {dist:.1f}px. Exiting.")
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
        
        # Header bar
        hb = Gtk.HeaderBar()
        hb.set_show_close_button(True)
        hb.set_title("Flip Clock Settings")
        self.set_titlebar(hb)
        
        # Grid layout
        grid = Gtk.Grid()
        grid.set_column_spacing(15)
        grid.set_row_spacing(15)
        grid.set_halign(Gtk.Align.CENTER)
        grid.set_valign(Gtk.Align.CENTER)
        self.add(grid)
        
        # Row 0: Time Format
        lbl_format = Gtk.Label(label="Time Format:")
        lbl_format.set_xalign(0)
        grid.attach(lbl_format, 0, 0, 1, 1)
        
        self.combo_format = Gtk.ComboBoxText()
        self.combo_format.append("12", "12-Hour (AM/PM)")
        self.combo_format.append("24", "24-Hour")
        current_fmt = self.manager.config.get('hour_format', '12')
        self.combo_format.set_active_id(current_fmt)
        grid.attach(self.combo_format, 1, 0, 1, 1)
        
        # Row 1: Idle Timeout
        lbl_timeout = Gtk.Label(label="Idle Timeout:")
        lbl_timeout.set_xalign(0)
        grid.attach(lbl_timeout, 0, 1, 1, 1)
        
        self.combo_timeout = Gtk.ComboBoxText()
        self.combo_timeout.append("120", "2 Minutes")
        self.combo_timeout.append("180", "3 Minutes")
        self.combo_timeout.append("240", "4 Minutes")
        self.combo_timeout.append("300", "5 Minutes")
        self.combo_timeout.append("600", "10 Minutes")
        self.combo_timeout.append("900", "15 Minutes")
        self.combo_timeout.append("1800", "30 Minutes")
        self.combo_timeout.append("3600", "1 Hour")
        
        current_to = str(self.manager.config.get('idle_timeout', 120))
        if current_to not in ["120", "180", "240", "300", "600", "900", "1800", "3600"]:
            self.combo_timeout.append(current_to, f"{int(current_to)//60} Minutes")
        self.combo_timeout.set_active_id(current_to)
        grid.attach(self.combo_timeout, 1, 1, 1, 1)
        
        # Row 2: Clock Size
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
        
        # Row 3: Save Button
        self.btn_save = Gtk.Button(label="Save & Apply")
        self.btn_save.connect("clicked", self.on_save_clicked)
        grid.attach(self.btn_save, 0, 3, 2, 1)
        
        self.connect("destroy", Gtk.main_quit)
        self.show_all()
        
    def on_save_clicked(self, button):
        fmt = self.combo_format.get_active_id()
        timeout = int(self.combo_timeout.get_active_id())
        size = f"{self.scale_size.get_value():.1f}"
        
        self.manager.config['hour_format'] = fmt
        self.manager.config['idle_timeout'] = timeout
        self.manager.config['clock_size'] = size
        
        self.manager.save_config()
        self.manager.restart_daemon()
        
        # Success dialog
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
        
        # Launch screensaver preview
        try:
            if os.path.exists("/usr/share/flipclock/flipclock.py"):
                subprocess.Popen(["/usr/local/bin/flipclock", "--run"])
            else:
                script_path = os.path.abspath(__file__)
                subprocess.Popen([sys.executable, script_path, "--run"])
        except Exception as e:
            print(f"Error starting preview: {e}")
            
        self.close()


class FlipClockManager:
    """Manages configuration, daemon monitoring, and window spawning."""
    def __init__(self):
        self.config_dir = os.path.expanduser("~/.config/flipclock")
        self.config_path = os.path.join(self.config_dir, "flipclock.conf")
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        self.html_path = os.path.join(self.script_dir, "clock.html")
        
        # Default configuration
        self.config = {
            'idle_timeout': 120,       # 2 minutes
            'hour_format': '12',       # 12 or 24
            'clock_size': '1.0',       # Scale factor
            'animation_speed': 500,    # milliseconds
            'monitors': 'all'          # all or comma separated indices (e.g. 0,1)
        }
        self.load_config()

    def load_config(self):
        """Loads or creates the ini style configuration file."""
        if not os.path.exists(self.config_dir):
            os.makedirs(self.config_dir, exist_ok=True)
            
        parser = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            try:
                parser.read(self.config_path)
                if 'Settings' in parser:
                    settings = parser['Settings']
                    self.config['idle_timeout'] = settings.getint('idle_timeout', 120)
                    self.config['hour_format'] = settings.get('hour_format', '12')
                    self.config['clock_size'] = settings.get('clock_size', '1.0')
                    self.config['animation_speed'] = settings.getint('animation_speed', 500)
                    self.config['monitors'] = settings.get('monitors', 'all')
            except Exception as e:
                print(f"Error reading config, using defaults: {e}")
        else:
            # Create default config file
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
        """Saves current config back to config file."""
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
        """Restarts the screensaver daemon process to apply new settings."""
        try:
            subprocess.run(["pkill", "-f", "flipclock.*--daemon"], capture_output=True)
        except Exception as e:
            print(f"Error stopping daemon: {e}")
            
        try:
            # Re-spawn daemon in background
            if os.path.exists("/usr/share/flipclock/flipclock.py"):
                subprocess.Popen(["/usr/local/bin/flipclock", "--daemon"])
            else:
                script_path = os.path.abspath(__file__)
                subprocess.Popen([sys.executable, script_path, "--daemon"])
            print("Daemon restarted successfully.")
        except Exception as e:
            print(f"Error starting daemon: {e}")

    def run_screensaver(self):
        """Spawns the screensaver window on each configured monitor."""
        Gtk.init(None)
        
        display = Gdk.Display.get_default()
        n_monitors = display.get_n_monitors()
        
        # Determine target monitors
        target_monitors = []
        if self.config['monitors'].lower() == 'all':
            target_monitors = list(range(n_monitors))
        else:
            try:
                target_monitors = [int(i.strip()) for i in self.config['monitors'].split(',') if int(i.strip()) < n_monitors]
            except ValueError:
                target_monitors = list(range(n_monitors))
                
        if not target_monitors:
            target_monitors = [0]
            
        print(f"Spawning screensaver clock windows on monitors: {target_monitors}")
        
        windows = []
        for monitor_idx in target_monitors:
            win = FlipClockWindow(self.html_path, monitor_idx, self.config)
            windows.append(win)
            
        # Register mouse tracking timeout (1.5 seconds)
        GLib.timeout_add(1500, enable_mouse_tracking)
            
        Gtk.main()

    def run_daemon(self):
        """Monitors idle time and launches/kills screensaver window dynamically."""
        if not X11_AVAILABLE:
            print("X11 is required for daemon idle detection. Exiting.")
            sys.exit(1)
            
        display = x11.XOpenDisplay(None)
        if not display:
            print("Cannot open X11 Display. Is DISPLAY environment variable set?")
            sys.exit(1)
            
        root = x11.XDefaultRootWindow(display)
        info_ptr = xss.XScreenSaverAllocInfo()
        
        proc = None
        idle_limit_ms = self.config['idle_timeout'] * 1000
        
        print(f"Flip Clock screensaver daemon started. Timeout: {self.config['idle_timeout']}s.")
        
        try:
            while True:
                if xss.XScreenSaverQueryInfo(display, root, info_ptr) != 0:
                    idle_ms = info_ptr.contents.idle
                else:
                    idle_ms = 0
                    
                if idle_ms >= idle_limit_ms:
                    if proc is None:
                        print(f"System idle for {idle_ms/1000:.1f}s. Spawning screensaver windows...")
                        
                        # Stop xscreensaver to avoid overlapping conflicts
                        subprocess.run(["xscreensaver-command", "-exit"], capture_output=True)
                        
                        # Launch screensaver wrapper
                        proc = subprocess.Popen([sys.executable, __file__, "--run"])
                    else:
                        if proc.poll() is not None:
                            proc = None # Screensaver exited internally
                else:
                    if proc is not None:
                        if proc.poll() is None:
                            print("User activity detected. Closing screensaver.")
                            proc.terminate()
                            try:
                                proc.wait(timeout=1)
                            except subprocess.TimeoutExpired:
                                proc.kill()
                        proc = None
                        
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\nStopping daemon.")
        finally:
            if proc and proc.poll() is None:
                proc.terminate()
            x11.XFree(info_ptr)
            x11.XCloseDisplay(display)


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
        # Default behavior: run the screensaver
        manager.run_screensaver()
