#!/bin/bash
set -e

echo "Uninstalling Flip Clock Screensaver..."

# 1. Stop any running screensaver/daemon instances
echo "Stopping running instances..."
pkill -f "flipclock.py" || true

# 2. Define paths
INSTALL_DIR="$HOME/.local/share/flipclock"
APP_LAUNCHER="$HOME/.local/share/applications/flipclock.desktop"
AUTOSTART_ENTRY="$HOME/.config/autostart/flipclock-daemon.desktop"
CONFIG_DIR="$HOME/.config/flipclock"

# 3. Remove files
echo "Removing installed files..."
rm -rf "$INSTALL_DIR"
rm -f "$APP_LAUNCHER"
rm -f "$AUTOSTART_ENTRY"

# Optional: Remove config
read -p "Do you want to delete your configuration file at $CONFIG_DIR? (y/N) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Removing configuration..."
    rm -rf "$CONFIG_DIR"
fi

echo "Uninstallation complete!"
