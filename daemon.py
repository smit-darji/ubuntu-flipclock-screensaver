#!/usr/bin/env python3
import time
import subprocess
import ctypes
import os
import sys
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
    parser.add_argument("--timeout", type=int, default=120, help="Idle timeout in seconds (default: 120)")
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
    idle_limit = args.timeout * 1000 # convert to milliseconds
    
    print(f"Screensaver clock daemon started. Timeout set to {args.timeout}s.")
    print("Monitoring idle time...")
    
    try:
        while True:
            idle = get_idle_time(display, root, info_ptr)
            
            if idle >= idle_limit:
                # If screensaver is not already running, start it
                if proc is None:
                    print(f"System idle for {idle/1000:.1f}s. Launching screensaver clock...")
                    
                    # Stop system xscreensaver if running to avoid overlap conflicts
                    subprocess.run(["xscreensaver-command", "-exit"], capture_output=True)
                    
                    # Start our fullscreen clock
                    proc = subprocess.Popen([sys.executable, screensaver_path, html_path])
                else:
                    # If screensaver was launched but closed by itself (e.g. via its internal input listener),
                    # we should wait until the idle time resets (user activity) before launching it again.
                    if proc.poll() is not None:
                        # The screensaver closed itself (which means activity occurred, but x11 idle hasn't reset yet,
                        # or it closed due to some signal). We clean up and wait.
                        proc = None
            else:
                # If system is active and screensaver process is active, stop it
                if proc is not None:
                    if proc.poll() is None:
                        print("Activity detected. Stopping screensaver.")
                        proc.terminate()
                        try:
                            proc.wait(timeout=1)
                        except subprocess.TimeoutExpired:
                            proc.kill()
                    proc = None
                    
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
