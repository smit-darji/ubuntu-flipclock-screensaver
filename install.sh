#!/bin/bash
set -e

echo "Installing Flip Clock Screensaver..."

# 1. Define paths
INSTALL_DIR="$HOME/.local/share/flipclock"
APP_LAUNCHER_DIR="$HOME/.local/share/applications"
AUTOSTART_DIR="$HOME/.config/autostart"
CONFIG_DIR="$HOME/.config/flipclock"
SYSTEMD_USER_DIR="$HOME/.config/systemd/user"

# 2. Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$APP_LAUNCHER_DIR"
mkdir -p "$AUTOSTART_DIR"
mkdir -p "$CONFIG_DIR"
mkdir -p "$SYSTEMD_USER_DIR"

# 3. Copy files to installation directory
cp flipclock.py "$INSTALL_DIR/flipclock.py"
cp clock.html "$INSTALL_DIR/clock.html"
if [ -f "index.html" ]; then cp index.html "$INSTALL_DIR/index.html"; fi
if [ -f "daemon.py" ]; then cp daemon.py "$INSTALL_DIR/daemon.py"; fi
if [ -f "screensaver.py" ]; then cp screensaver.py "$INSTALL_DIR/screensaver.py"; fi
if [ -d "assets" ]; then cp -r assets "$INSTALL_DIR/"; fi
if [ -d "live-wallpaper" ]; then cp -r live-wallpaper "$INSTALL_DIR/"; fi
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
idle_timeout = 60
hour_format = 12
clock_size = 1.0
animation_speed = 500
monitors = all
theme = luxury_black_gold
show_seconds = true
show_date = true
show_greeting = true
user_name = 
bg_style = vignette
custom_credit = FLIP CLOCK SCREENSAVER
digit_font = Cinzel
label_font = Cinzel
custom_bg_color = #000000
custom_card_color = #1C1C1E
custom_digit_color = #F5F5F7
custom_accent_color = #D4AF37
custom_border_color = #4A4A4A
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

# 6. Create Autostart Desktop Entry for Daemon
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

# 7. Create Systemd User Service for automatic restart on reboot
echo "Creating systemd user service..."
cat <<EOF > "$SYSTEMD_USER_DIR/flipclock-daemon.service"
[Unit]
Description=Flip Clock Screensaver Daemon
After=graphical-session.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $INSTALL_DIR/flipclock.py --daemon
Restart=always
RestartSec=3
Environment=DISPLAY=${DISPLAY:-:1}
Environment=XAUTHORITY=${XAUTHORITY:-/run/user/1000/gdm/Xauthority}

[Install]
WantedBy=default.target
EOF

# Enable & start systemd service if systemctl is available
if command -v systemctl &> /dev/null; then
    echo "Enabling systemd user service..."
    systemctl --user daemon-reload || true
    systemctl --user enable flipclock-daemon.service || true
    systemctl --user restart flipclock-daemon.service || true
fi

# 8. Ensure background daemon process is running right now
echo "Stopping any existing screensaver processes..."
pkill -f "flipclock.py" || true
pkill -f "daemon.py" || true
pkill -f "screensaver.py" || true

echo "Starting Flip Clock screensaver daemon..."
DISPLAY="${DISPLAY:-:0}" nohup python3 -u "$INSTALL_DIR/flipclock.py" --daemon > "$INSTALL_DIR/daemon.log" 2>&1 &

echo "Installation complete!"
echo "The screensaver daemon is enabled via Systemd & Autostart to automatically start after 2 minutes of idle time on every restart."
