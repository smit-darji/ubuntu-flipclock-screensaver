#!/bin/bash
set -e

echo "Uninstalling Flip Clock Screensaver..."

# 1. Stop any running screensaver/daemon instances
echo "Stopping running instances..."
pkill -f "flipclock.py" || true
pkill -f "daemon.py" || true
pkill -f "screensaver.py" || true

# 2. Define paths
INSTALL_DIR="$HOME/.local/share/flipclock"
APP_LAUNCHER="$HOME/.local/share/applications/flipclock.desktop"
SETTINGS_LAUNCHER="$HOME/.local/share/applications/flipclock-settings.desktop"
AUTOSTART_ENTRY="$HOME/.config/autostart/flipclock-daemon.desktop"
SYSTEMD_SERVICE="$HOME/.config/systemd/user/flipclock-daemon.service"
CONFIG_DIR="$HOME/.config/flipclock"

# 3. Disable systemd service if available
if command -v systemctl &> /dev/null; then
    systemctl --user stop flipclock-daemon.service || true
    systemctl --user disable flipclock-daemon.service || true
fi

# 4. Remove files
echo "Removing installed files..."
rm -rf "$INSTALL_DIR"
rm -f "$APP_LAUNCHER"
rm -f "$SETTINGS_LAUNCHER"
rm -f "$AUTOSTART_ENTRY"
rm -f "$SYSTEMD_SERVICE"
rm -f "$HOME/.local/share/pixmaps/flipclock.png"
rm -f "$HOME/.local/share/icons/hicolor/512x512/apps/flipclock.png"

# Optional: Remove config
read -p "Do you want to delete your configuration file at $CONFIG_DIR? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing configuration..."
    rm -rf "$CONFIG_DIR"
fi

echo "Uninstallation complete!"
