# Premium Fliqlo-Style Flip Clock Screensaver for Ubuntu

[![Platform](https://img.shields.io/badge/platform-Ubuntu%2020.04%20%7C%2022.04%20%7C%2024.04-orange.svg)](https://ubuntu.com)
[![Download .deb Package](https://img.shields.io/badge/Download-flipclock--screensaver__1.0.0__all.deb-blue?style=for-the-badge&logo=debian)](https://raw.githubusercontent.com/smit-darji/ubuntu-flipclock-screensaver/Master/flipclock-screensaver_1.0.0_all.deb)
[![Language](https://img.shields.io/badge/language-Python%203%20%2B%20GTK3%20%2B%20HTML5-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 📷 Preview & Screenshots

![Flip Clock Screensaver Fullscreen Preview](screenshot.png)

A native, high-fidelity, multi-monitor flip clock screensaver for Ubuntu Linux. It brings a vintage airport split-flap style retro clock to your workstation, rendering across all connected displays simultaneously with smooth 3D CSS animations and automatic screen size scaling.

---

## ✨ Key Features

* **Vintage Split-Flap Clock UI**: Fliqlo-style charcoal cards, subtle border highlights, rounded corners, and realistic card flip shadows.
* **Multi-Monitor Support**: Automatically detects monitor count, geometry, and placement to spawn independent full-screen screensaver windows per display.
* **Auto Aspect-Ratio Scaling**: Dynamically adjusts visual scale using CSS transforms. Adapts seamlessly to ultra-wide, standard, and portrait (vertical) monitors without cut-offs.
* **Graphical Settings Application**: Simple desktop GUI to adjust:
  * **Time Format** (12-Hour AM/PM vs 24-Hour).
  * **Idle Timeout** (1, 2, 3, 4, 5, 10, 15, 30 minutes, or 1 hour).
  * **Clock Scale** (slider from `0.5x` to `2.0x` zoom).
* **Safe Input Listener**: Instantly exits the screensaver upon keyboard activity, mouse clicks, scrolls, or deliberate mouse movements.
* **Zero CPU Overhead**: Idle monitoring daemon queries native X11 Screen Saver extension (`libXss` via `ctypes`) resulting in **0.0% idle CPU utilization**.

---

## 🚀 Installation Methods

### Method 1: Download & Install Debian Package (`.deb`) — *Recommended*

Download `flipclock-screensaver_1.0.0_all.deb` directly from GitHub and install via `apt` (which automatically resolves required system dependencies):

```bash
# 1. Download the latest .deb package from GitHub
wget https://raw.githubusercontent.com/smit-darji/ubuntu-flipclock-screensaver/Master/flipclock-screensaver_1.0.0_all.deb

# 2. Install package using apt
sudo apt update
sudo apt install ./flipclock-screensaver_1.0.0_all.deb
```

---

### Method 2: Clone GitHub Repository & Install from Source

If you prefer to clone the repository and run the local installation script:

```bash
# 1. Clone the repository
git clone https://github.com/smit-darji/ubuntu-flipclock-screensaver.git
cd ubuntu-flipclock-screensaver

# 2. Install required system dependencies
sudo apt update
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.0 libxss1

# 3. Run the installer script
chmod +x install.sh
./install.sh
```

---

## 🔄 Updating / Upgrading

To update to the latest version of Flip Clock Screensaver:

```bash
# 1. Download the updated .deb package
wget https://raw.githubusercontent.com/smit-darji/ubuntu-flipclock-screensaver/Master/flipclock-screensaver_1.0.0_all.deb

# 2. Install/Upgrade package
sudo apt update
sudo apt install --only-upgrade ./flipclock-screensaver_1.0.0_all.deb
```
*(Or simply re-run `sudo apt install ./flipclock-screensaver_1.0.0_all.deb`)*

---

## 🔁 Reinstalling

If you need to repair or reinstall the package files:

```bash
# Reinstall the package completely
sudo apt install --reinstall ./flipclock-screensaver_1.0.0_all.deb
```

---

## ⚙️ Configuration & GUI Settings

Settings can be customized per logged-in user via the Graphical Settings application or by editing the config file directly:

* **Graphical Settings GUI**:
  Open **"Flip Clock Settings"** from Ubuntu Applications menu, or run in terminal:
  ```bash
  flipclock --settings
  ```
* **Configuration File Path**:
  Saved at `~/.config/flipclock/flipclock.conf`:
  ```ini
  [Settings]
  idle_timeout = 120        # Idle time in seconds before screensaver starts (e.g., 120 = 2 minutes)
  hour_format = 12          # Time format: 12 (AM/PM) or 24 (24-Hour)
  clock_size = 1.0          # Scaling factor (0.5 to 2.0)
  animation_speed = 500     # Flip transition duration in ms
  monitors = all            # Targets: "all" or specific monitor indices (e.g. "0,1")
  ```

---

## 💡 Usage & CLI Commands

Once installed, the following commands are available globally in your terminal:

| Command | Action |
|---|---|
| `flipclock` or `flipclock --run` | Previews/launches screensaver full-screen windows immediately |
| `flipclock --settings` | Opens the graphical settings configuration window |
| `flipclock --daemon` | Starts the background idle monitor daemon |
| `pkill -f "flipclock.*--daemon"` | Stops the background idle monitor daemon |

---

## 🗑️ Uninstallation Guide

### Option A: Remove Debian (`.deb`) Package

To completely remove the application package, system symlinks, launchers, and autostart entries:

```bash
# Remove application package
sudo apt remove flipclock-screensaver

# Optional: Purge remaining package configurations
sudo apt purge flipclock-screensaver
```

---

### Option B: Remove Source Installation

If you installed using the local `install.sh` source script:

```bash
cd ubuntu-flipclock-screensaver
chmod +x uninstall.sh
./uninstall.sh
```

---

## 🛠️ Building `.deb` Package from Source

To build a fresh `.deb` package file locally:

```bash
chmod +x build_deb.sh
./build_deb.sh
```
This generates `flipclock-screensaver_1.0.0_all.deb` in the project root directory.
