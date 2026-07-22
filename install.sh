#!/bin/bash
set -e

echo "Installing Flip Clock Screensaver..."

# 1. Define paths
INSTALL_DIR="$HOME/.local/share/flipclock"
APP_LAUNCHER_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"
CONFIG_DIR="$HOME/.config/flipclock"

# 2. Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$APP_LAUNCHER_DIR"
mkdir -p "$AUTOSTART_DIR"
mkdir -p "$CONFIG_DIR"

# 3. Copy files to installation directory
cp flipclock.py "$INSTALL_DIR/flipclock.py"
cp clock.html "$INSTALL_DIR/clock.html"
chmod +x "$INSTALL_DIR/flipclock.py"

ICON_PATH="preferences-desktop-screensaver"
if [ -f "flipclock.png" ]; then
    mkdir -p "$HOME/.local/share/pixmaps"
    mkdir -p "$HOME/.local/share/icons/hicolor/512x512/apps"
    cp flipclock.png "$INSTALL_DIR/flipclock.png"
    cp flipclock.png "$HOME/.local/share/pixmaps/flipclock.png"
    cp flipclock.png "$HOME/.local/share/icons/hicolor/512x512/apps/flipclock.png"
    ICON_PATH="$HOME/.local/share/pixmaps/flipclock.png"
fi

# 4. Create default configuration if not present
if [ ! -f "$CONFIG_DIR/flipclock.conf" ]; then
    echo "Creating default configuration file..."
    cat <<EOF > "$CONFIG_DIR/flipclock.conf"
[Settings]
idle_timeout = 120
hour_format = 12
clock_size = 1.0
animation_speed = 500
monitors = all
EOF
fi

# 5. Create Desktop Application Launchers
echo "Creating application launchers..."
cat <<EOF > "$APP_LAUNCHER_DIR/flipclock.desktop"
[Desktop Entry]
Type=Application
Name=Flip Clock Screensaver
Comment=Start the Flip Clock screensaver immediately in fullscreen
Exec=python3 $INSTALL_DIR/flipclock.py --run
Icon=$ICON_PATH
Terminal=false
Categories=Utility;
EOF
chmod +x "$APP_LAUNCHER_DIR/flipclock.desktop"

cat <<EOF > "$APP_LAUNCHER_DIR/flipclock-settings.desktop"
[Desktop Entry]
Type=Application
Name=Flip Clock Settings
Comment=Configure Flip Clock screensaver settings
Exec=python3 $INSTALL_DIR/flipclock.py --settings
Icon=$ICON_PATH
Terminal=false
Categories=Settings;Utility;
EOF
chmod +x "$APP_LAUNCHER_DIR/flipclock-settings.desktop"

# 6. Create Autostart Entry for Daemon
echo "Creating autostart entry..."
cat <<EOF > "$AUTOSTART_DIR/flipclock-daemon.desktop"
[Desktop Entry]
Type=Application
Name=Flip Clock Screensaver Daemon
Comment=Monitors idle time and runs the Flip Clock screensaver
Exec=python3 $INSTALL_DIR/flipclock.py --daemon
Hidden=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
EOF
chmod +x "$AUTOSTART_DIR/flipclock-daemon.desktop"

# 7. Start the daemon process right now
echo "Stopping any existing screensaver processes..."
pkill -f "flipclock.py" || true
pkill -f "daemon.py" || true
pkill -f "screensaver.py" || true

echo "Starting Flip Clock screensaver daemon..."
DISPLAY=:1 nohup python3 -u "$INSTALL_DIR/flipclock.py" --daemon > "$INSTALL_DIR/daemon.log" 2>&1 &

echo "Installation complete! Flip Clock screensaver will start after 2 minutes of idle time."
echo "You can launch the screensaver immediately from your Applications menu or using command: ~/.local/share/flipclock/flipclock.py --run"
echo "Configuration is located at ~/.config/flipclock/flipclock.conf"
