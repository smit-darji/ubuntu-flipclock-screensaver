# Premium Fliqlo-Style Flip Clock Screensaver for Ubuntu

[![Platform](https://img.shields.io/badge/platform-Ubuntu%2020.04%20%7C%2022.04%20%7C%2024.04-orange.svg)](https://ubuntu.com)
[![Download .deb Package](https://img.shields.io/badge/Download-flipclock--screensaver__1.0.0__all.deb-blue?style=for-the-badge&logo=debian)](https://github.com/smit-darji/ubuntu-flipclock-screensaver/releases/download/v1.0.0/flipclock-screensaver_1.0.0_all.deb)
[![Language](https://img.shields.io/badge/language-Python%203%20%2B%20GTK3%20%2B%20HTML5-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![Flip Clock Screensaver Preview](screenshot.png)

A native, high-fidelity, dual-monitor flip clock screensaver for Ubuntu Linux. It brings a stunning, vintage airport split-flap style retro clock to your workstation, rendering across all connected displays simultaneously with smooth 3D CSS animations and automatic screen size scaling.

---

## Key Features

* **Vintage split-flap clock UI** — Beautiful Fliqlo-style charcoal cards, subtle border highlights, rounded corners, and realistic card flip shadows.
* **Dual-monitor & multi-monitor support** — Automatically detects monitor count, geometry, and placement. Spawns independent fullscreen screensaver windows per display.
* **Aspect ratio auto-scaling** — Dynamically adjusts visual scale using CSS transforms. Adapts to ultra-wide, standard, and portrait (vertical) monitors without any cut-offs or side cropping.
* **Graphical settings application** — Simple desktop GUI to adjust:
  * **Time format** (12-Hour AM/PM vs 24-Hour).
  * **Idle timeout** (2, 3, 4, 5, 10, 15, 30 minutes, or 1 hour).
  * **Clock size** (slider from `0.5x` to `2.0x` scale).
* **Safe input listener** — Instantly shuts down the screensaver when keyboard activity, mouse clicks, mouse scrolls, or mouse movements (exceeding a small threshold to avoid accidental bumps) are registered.
* **Visible cursor** — Keeps the default mouse pointer visible on start for easy navigation and interactive control.
* **Ultra-lightweight** — Uses a native background daemon querying the low-level X11 Screen Saver extension (`libXss` via `ctypes`), resulting in **0.0% idle CPU utilization** and near-zero power consumption.

---

## Installation Methods

### Method 1: Download & Install Debian Package (`flipclock-screensaver_1.0.0_all.deb`) — *Recommended*

Click the button below to download the official `.deb` package file:

[<img src="https://img.shields.io/badge/Download-flipclock--screensaver__1.0.0__all.deb-2088FF?style=for-the-badge&logo=debian&logoColor=white" height="42">](https://github.com/smit-darji/ubuntu-flipclock-screensaver/releases/download/v1.0.0/flipclock-screensaver_1.0.0_all.deb)

#### 1. Download & Install via Terminal or GUI
Download `flipclock-screensaver_1.0.0_all.deb` and install it using `apt` (which automatically fetches required dependencies):

```bash
# Download package file via terminal (or click the Download button above)
wget https://github.com/smit-darji/ubuntu-flipclock-screensaver/releases/download/v1.0.0/flipclock-screensaver_1.0.0_all.deb

# Install package
sudo apt update
sudo apt install ./flipclock-screensaver_1.0.0_all.deb
```
*(Alternatively, double-click the downloaded `flipclock-screensaver_1.0.0_all.deb` file to install via Ubuntu Software Center / GDebi).*

#### 2. Configure & Save Settings (Per User)
Any logged-in user on the system can configure and save their personalized screensaver settings:
* Open **"Flip Clock Settings"** from the Ubuntu Applications menu, or run in terminal:
  ```bash
  flipclock --settings
  ```
* Custom options include **Time Format** (12-Hour AM/PM vs 24-Hour), **Idle Timeout** (2, 3, 5, 10, 15, 30 min, 1 hour), and **Clock Scaling**.
* Click **"Save & Apply"** to write settings to `~/.config/flipclock/flipclock.conf` and restart the idle daemon for your account.

#### 3. Perform / Run Screensaver
* **Automatic Idle Screen**: The background daemon starts automatically at login and triggers the flip clock screensaver after your configured idle duration.
* **Manual Trigger**: Launch **"Flip Clock Screensaver"** from the Applications menu or run:
  ```bash
  flipclock --run
  ```

---

### Method 2: Installing from Source (Local Script)

If you prefer to install it locally inside your user profile directory without using `apt`:

#### 1. Install System Dependencies
Make sure you have the required Python GI binding and WebKit library:
```bash
sudo apt update
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.0 libxss1
```
*(Note: Newer systems like Ubuntu 24.04 use `gir1.2-webkit2-4.1` which is automatically supported by our dynamic loader).*

#### 2. Run the Local Installer
Run the local `install.sh` script:
```bash
chmod +x install.sh
./install.sh
```

---

## Usage & Commands

Once installed via the Debian package, the commands are added to your global user path:

| Command | Action |
|---|---|
| `flipclock` or `flipclock --run` | Previews/starts the screensaver windows immediately. |
| `flipclock --settings` | Opens the graphical settings panel (also searchable as **"Flip Clock Settings"** in the Applications menu). |
| `flipclock --daemon` | Starts the background idle monitor daemon. |
| `pkill -f "flipclock.*--daemon"` | Stops the background idle monitor daemon. |

---

## Package Security & Verification

We value system security. The `.deb` package compiles standard sandboxed dependencies and operates with the following security guidelines:
* **Fully offline operation** — The screensaver tracks time locally and does not establish network connections.
* **No sudo needed at runtime** — The background daemon and configuration editor run entirely in user-space under the active user's permissions.
* **System packages only** — Relies exclusively on official, security-maintained Ubuntu repository libraries (`libX11`, `libXss`, `WebKitGTK`).
* **Source inspection** — Inspect the packaging script anytime:
  ```bash
  cat build_deb.sh
  ```

---

## Configuration

Settings are saved in the standard user config path at `~/.config/flipclock/flipclock.conf`. You can edit this file manually or use the Settings GUI application:

```ini
[Settings]
idle_timeout = 180        # Idle duration in seconds before screensaver starts (e.g., 180 = 3 minutes)
hour_format = 24          # Time format: 12 (AM/PM style) or 24 (24-hour style)
clock_size = 1.0          # Scaling factor (0.5 to 2.0)
animation_speed = 500     # Flipping transition duration in milliseconds
monitors = all            # Spawning targets: "all" or specific monitor indices (e.g., "0,1")
```

---

## Uninstallation

### Package Uninstall (Method 1)
To completely remove the package, launcher entries, and clean up system symlinks:
```bash
sudo apt remove flipclock-screensaver
```

### Local Script Uninstall (Method 2)
If you installed using the local source script:
```bash
chmod +x uninstall.sh
./uninstall.sh
```
