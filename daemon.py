#!/usr/bin/env python3
import os
import sys

# Disable WebKit hardware compositing mode to prevent GPU black screens on Linux
os.environ["WEBKIT_DISABLE_COMPOSITING_MODE"] = "1"

import time
import subprocess
import ctypes
import argparse

# Load X11 and Xss
try:
    x11 = ctypes.cdll.LoadLibrary('libX11.so.6')
    xss = ctypes.cdll.LoadLibrary('libXss.so.1')
except Exception as e:
    print(f"Error loading X11/Xss libraries: {e}")
    sys.exit(1)

class XScreenSaverInfo(ctypes.Structure):
    _fields_ = [
        ('window', ctypes.c_ulong),
        ('state', ctypes.c_int),
        ('kind', ctypes.c_int),
        ('til_or_since', ctypes.c_ulong),
        ('idle', ctypes.c_ulong),
        ('event_mask', ctypes.c_ulong)
    ]

# Setup ctypes signatures
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

def get_idle_time(display, root, info_ptr):
    if xss.XScreenSaverQueryInfo(display, root, info_ptr) != 0:
        return info_ptr.contents.idle
    return 0

def main():
    parser = argparse.ArgumentParser(description="Screensaver Clock Daemon")
    parser.add_argument("--timeout", type=int, default=60, help="Idle timeout in seconds (default: 60)")
    args = parser.parse_args()

    display = x11.XOpenDisplay(None)
    if not display:
        print("Cannot open X11 Display. Is DISPLAY environment variable set?")
        sys.exit(1)
        
    root = x11.XDefaultRootWindow(display)
    info_ptr = xss.XScreenSaverAllocInfo()
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    screensaver_path = os.path.join(script_dir, "screensaver.py")
    html_path = os.path.join(script_dir, "clock.html")
    
    proc = None
    idle_limit = args.timeout * 1000  # convert to milliseconds
    state = "IDLE"  # IDLE, RUNNING, WAIT_USER_ACTIVE
    
    print(f"Screensaver clock daemon started. Timeout set to {args.timeout}s.")
    print("Monitoring idle time...")
    
    try:
        while True:
            idle = get_idle_time(display, root, info_ptr)
            
            if state == "IDLE":
                if idle >= idle_limit:
                    print(f"System idle for {idle/1000:.1f}s. Launching screensaver clock...")
                    try:
                        subprocess.run(["xscreensaver-command", "-exit"], capture_output=True)
                    except FileNotFoundError:
                        pass
                    proc = subprocess.Popen([sys.executable, screensaver_path, html_path])
                    state = "RUNNING"
            
            elif state == "RUNNING":
                if proc is None or proc.poll() is not None:
                    print("Screensaver closed by user input.")
                    proc = None
                    state = "WAIT_USER_ACTIVE"
                elif idle < idle_limit:
                    print("Activity detected. Stopping screensaver.")
                    proc.terminate()
                    try:
                        proc.wait(timeout=1)
                    except subprocess.TimeoutExpired:
                        proc.kill()
                    proc = None
                    state = "IDLE"
                    
            elif state == "WAIT_USER_ACTIVE":
                if idle < idle_limit:
                    state = "IDLE"
                    
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("\nExiting daemon.")
    finally:
        if proc and proc.poll() is None:
            proc.terminate()
        x11.XFree(info_ptr)
        x11.XCloseDisplay(display)

if __name__ == "__main__":
    main()
