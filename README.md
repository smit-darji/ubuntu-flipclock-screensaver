# Premium Fliqlo-Style Flip Clock Screensaver for Ubuntu

[![Platform](https://img.shields.io/badge/platform-Ubuntu%2020.04%20%7C%2022.04%20%7C%2024.04-orange.svg)](https://ubuntu.com)
[![Download .deb Package](https://img.shields.io/badge/Download-flipclock--screensaver__1.0.0__all.deb-blue?style=for-the-badge&logo=debian)](https://raw.githubusercontent.com/smit-darji/ubuntu-flipclock-screensaver/Master/flipclock-screensaver_1.0.0_all.deb)
[![Language](https://img.shields.io/badge/language-Python%203%20%2B%20GTK3%20%2B%20HTML5-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

![Flip Clock Screensaver Preview](screenshot.png)

A native, high-fidelity, multi-monitor flip clock screensaver for Ubuntu Linux. It brings a vintage airport split-flap style retro clock to your desktop, rendering across all connected displays simultaneously with smooth 3D CSS animations and automatic screen scaling.

---

## 🚀 Quick Download & Installation

### Option 1: Direct `.deb` Package Download (Recommended)

Download the `.deb` file directly from GitHub and install with `apt`:

```bash
# 1. Download the latest .deb package from GitHub
wget https://raw.githubusercontent.com/smit-darji/ubuntu-flipclock-screensaver/Master/flipclock-screensaver_1.0.0_all.deb

# 2. Install the package (automatically handles dependencies)
sudo apt update
sudo apt install ./flipclock-screensaver_1.0.0_all.deb
```

---

### Option 2: Clone GitHub Repository & Install from Source

If you prefer to clone the repository and run the local installation script:

```bash
# 1. Clone the repository
git clone https://github.com/smit-darji/ubuntu-flipclock-screensaver.git
cd ubuntu-flipclock-screensaver

# 2. Install required system dependencies
sudo apt update
sudo apt install python3 python3-gi gir1.2-gtk-3.0 gir1.2-webkit2-4.0 libxss1

# 3. Run the installer
chmod +x install.sh
./install.sh
```

---

## ⚙️ Setup & Configuration

You can easily configure screensaver options (12H/24H format, idle timeout, clock scaling):

* **Open Graphical Settings**:
  Search for **"Flip Clock Settings"** in Ubuntu Applications menu or run in terminal:
  ```bash
  flipclock --settings
  ```
* **Test / Preview Immediately**:
  ```bash
  flipclock --run
  ```

---

## 💡 Usage & Commands

| Command | Action |
|---|---|
| `flipclock` or `flipclock --run` | Launches the screensaver preview immediately |
| `flipclock --settings` | Opens the GUI settings window |
| `flipclock --daemon` | Runs the background idle monitor daemon |
| `pkill -f "flipclock.*--daemon"` | Stops the background idle monitor daemon |

---

## 🗑️ Uninstallation

### Uninstall `.deb` Package (Option 1)
```bash
sudo apt remove flipclock-screensaver
```

### Uninstall Source Installation (Option 2)
```bash
cd ubuntu-flipclock-screensaver
chmod +x uninstall.sh
./uninstall.sh
```

---

## ✨ Key Features

* **Split-Flap Retro Clock UI**: Fliqlo-style charcoal cards with realistic flip animations.
* **Multi-Monitor Support**: Automatically detects all monitors and displays full-screen clock windows per display.
* **Auto Aspect-Ratio Scaling**: Adapts seamlessly to ultra-wide, standard, and vertical portrait screens.
* **Instant Exit on Input**: Exits immediately when keyboard keys or mouse movements/clicks are detected.
* **Zero CPU Overhead**: Idle monitoring daemon runs via native X11 Screen Saver extension with 0.0% CPU usage.
