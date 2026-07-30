# Premium Fliqlo-Style Flip Clock Screensaver for Ubuntu

[![Platform](https://img.shields.io/badge/Platform-Ubuntu%2020.04%20%7C%2022.04%20%7C%2024.04-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)](https://ubuntu.com)
[![Download .deb Package](https://img.shields.io/badge/Download-flipclock--screensaver.deb-10B981?style=for-the-badge&logo=debian&logoColor=white)](https://raw.githubusercontent.com/smit-darji/ubuntu-flipclock-screensaver/Master/flipclock-screensaver.deb)
[![Language](https://img.shields.io/badge/Language-Python%203%20%2B%20GTK3-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-6D28D9?style=for-the-badge)](LICENSE)

---

## 📷 Themes & Visual Previews

A native, high-fidelity, multi-monitor flip clock screensaver for Ubuntu Linux. It brings a vintage airport split-flap style retro clock to your workstation, rendering across all connected displays simultaneously with smooth 3D CSS animations, dynamic time-based greetings, and 21 executive color theme collections.

| Theme Name | Visual Style |
|---|---|
| **1. 🥇 Luxury Black Gold** *(Executive Rolex / Bentley)* | Pitch black background, gold accent highlights, Cinzel typography |
| **2. 🥈 Obsidian Titanium** *(Apple Pro / Tesla)* | Obsidian dark plates, titanium gray border highlights |
| **3. 🥉 Dark Emerald** *(Luxury Finance)* | Rich deep emerald cards, gold digits & pins |
| **4. 🌲 Forest Green Executive** | Deep forest green background & card accents |
| **5. 🏎️ British Racing Green** *(Aston Martin)* | Dark racing green cards with metallic yellow accents |
| **6. 💎 Ruby Executive** *(Royal Red)* | Crimson ruby dark plates, vivid red highlights |
| **7. 🍷 Burgundy Prestige** *(Wine & Leather)* | Rich deep burgundy background & cards |
| **8. 🏎️ Crimson Royal** *(Scuderia Ferrari)* | Matte crimson red cards with gold trim |
| **9. 🚙 Royal Sapphire** *(Executive Blue)* | Deep navy blue cards with vibrant sapphire accents |
| **10. ⚓ Midnight Navy** | Pitch dark navy cards with soft ice blue digits |
| **11. 🔮 Amethyst Elite** *(Royal Purple)* | Deep amethyst violet background & gold digits |
| **12. 🪙 Platinum Silver** | Ultra-clean platinum silver cards & dark slate digits |
| **13. 🎨 Custom Theme** | Full custom theme builder with live color pickers & font selection |

---

## ✨ Key Features

* **Vintage Split-Flap Clock UI**: Fliqlo-style charcoal cards, subtle border highlights, rounded corners, and realistic 3D card flip shadows.
* **21 Executive Luxury Dark Themes**: Rolex Black Gold, Obsidian Titanium, Dark Emerald, Racing Green, Ruby Executive, Royal Sapphire, Amethyst Elite, and custom palette fine-tuning.
* **Live Color Palette Preview**: Displays live color swatches (`Bg`, `Card`, `Digit`, `Accent`, `Border`) inside settings.
* **Time-based Personalized Greetings**:
  - Automatically displays greetings based on time of day: `GOOD MORNING`, `GOOD AFTERNOON`, `GOOD EVENING`, `GOOD NIGHT`.
  - Personalize with your custom name (e.g. `GOOD MORNING, SMIT`).
  - Toggle greeting visibility on or off via checkbox/switch in settings.
* **Multi-Monitor Support**: Automatically detects monitor count, geometry, and placement to spawn independent full-screen screensaver windows per display.
* **Aspect-Ratio Scaling**: Dynamically adjusts visual scale using CSS transforms. Adapts seamlessly to ultra-wide, standard, and portrait (vertical) monitors without cut-offs.
* **Modern Executive GTK Settings Application**:
  - **Direct Active Theme Selector** with 2-column compact grid
  - **Live Palette Color Swatches Preview**
  - **Display Time Greeting** toggle & **Custom User Name** input
  - **Time Format** (12-Hour AM/PM vs 24-Hour)
  - **Seconds Display** toggle & **Date Badge** toggle
  - **Clock Scale Slider** (`0.5x` to `2.0x`)
  - **Idle Timeout Selector** (1, 2, 3, 5, 10, 15, 30 min, 1 hr)
  - High-contrast **Test Preview**, **Reset Defaults** & **Save & Apply** buttons
* **Zero CPU Overhead**: Background idle monitoring daemon queries native X11 Screen Saver extension (`libXss` via `ctypes`) resulting in **0.0% idle CPU utilization**.

---

## 🚀 Installation Methods

### Method 1: Download & Install Debian Package (`.deb`) — *Recommended*

Download `flipclock-screensaver.deb` directly using `wget` and install via `apt`:

```bash
# 1. Download the standard .deb package via wget
wget https://raw.githubusercontent.com/smit-darji/ubuntu-flipclock-screensaver/Master/flipclock-screensaver.deb

# 2. Install package using apt (automatically resolves system dependencies)
sudo apt update
sudo apt install ./flipclock-screensaver.deb
```

---

### Method 2: Install from Source

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

## ⚙️ Configuration & GUI Settings

Open **"Flip Clock Settings"** from Ubuntu Applications menu, or run in terminal:
```bash
flipclock --settings
```

### Configuration File (`~/.config/flipclock/flipclock.conf`)
```ini
[Settings]
idle_timeout = 60         # Idle time in seconds before screensaver starts (e.g., 60 = 1 minute)
hour_format = 12           # Time format: 12 (AM/PM) or 24 (24-Hour)
clock_size = 1.0           # Scaling factor (0.5 to 2.0)
animation_speed = 500      # Flip transition duration in ms
monitors = all             # Targets: "all" or specific monitor indices (e.g. "0,1")
theme = luxury_black_gold  # Active theme preset ID
show_seconds = true        # Toggle seconds flip card visibility
show_date = true           # Toggle date badge visibility
show_greeting = true       # Toggle time-based greeting visibility
user_name = Smit           # Custom name for greeting (e.g. GOOD MORNING, SMIT)
custom_credit = Customized by Antigravity AI
```

---

## 💡 Usage & CLI Commands

Once installed, the following commands are available globally in your terminal:

| Command | Action |
|---|---|
| `flipclock` or `flipclock --run` | Previews/launches screensaver full-screen windows immediately |
| `flipclock --settings` | Opens the graphical settings configuration window |
| `flipclock --version` | Outputs current software version (`v2.3.0`) |
| `flipclock --daemon` | Starts the background idle monitor daemon |
| `pkill -f "flipclock.*--daemon"` | Stops the background idle monitor daemon |

---

## 🛠️ Building `.deb` Package from Source

To build a fresh `.deb` package file locally:

```bash
chmod +x build_deb.sh
./build_deb.sh
```
This generates `flipclock-screensaver.deb` (and `flipclock-screensaver_2.3.0_all.deb`) in the project root directory.

---

## 🗑️ Uninstallation Guide

To completely remove the application package, system symlinks, launchers, and autostart entries:

```bash
sudo apt remove flipclock-screensaver
sudo apt purge flipclock-screensaver
```
