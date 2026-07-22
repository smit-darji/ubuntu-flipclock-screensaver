#!/bin/bash
# Script to build a portable Debian package (.deb) of the Flip Clock Screensaver

set -e

# Package name and version
PKG_NAME="flipclock-screensaver"
PKG_VER="1.0.0"
PKG_DIR="flipclock-build"

echo "Creating Debian package structure..."
rm -rf "$PKG_DIR"
mkdir -p "$PKG_DIR/DEBIAN"
mkdir -p "$PKG_DIR/usr/share/flipclock"
mkdir -p "$PKG_DIR/usr/share/applications"
mkdir -p "$PKG_DIR/etc/xdg/autostart"

mkdir -p "$PKG_DIR/usr/share/pixmaps"
mkdir -p "$PKG_DIR/usr/share/icons/hicolor/512x512/apps"

# Copy application files
cp clock.html "$PKG_DIR/usr/share/flipclock/"
cp flipclock.py "$PKG_DIR/usr/share/flipclock/"
if [ -f "flipclock.png" ]; then
    cp flipclock.png "$PKG_DIR/usr/share/pixmaps/flipclock.png"
    cp flipclock.png "$PKG_DIR/usr/share/icons/hicolor/512x512/apps/flipclock.png"
fi

# Create DEBIAN/control file
cat << 'EOF' > "$PKG_DIR/DEBIAN/control"
Package: flipclock-screensaver
Version: 1.0.0
Section: utils
Priority: optional
Architecture: all
Maintainer: Antigravity <antigravity@google.com>
Depends: python3, python3-gi, gir1.2-gtk-3.0, gir1.2-webkit2-4.0 | gir1.2-webkit2-4.1, libxss1
Description: Premium Fliqlo-style flip clock screensaver for Ubuntu
 A high-aesthetic, multi-monitor flip clock screensaver designed for Ubuntu Linux.
 Runs as a background daemon, auto-detects idle time, and exits instantly on input.
EOF

# Create DEBIAN/postinst (post-installation script)
cat << 'EOF' > "$PKG_DIR/DEBIAN/postinst"
#!/bin/bash
set -e

# Ensure executable permissions
chmod +x /usr/share/flipclock/flipclock.py

# Create system bin symlinks
ln -sf /usr/share/flipclock/flipclock.py /usr/bin/flipclock
ln -sf /usr/share/flipclock/flipclock.py /usr/local/bin/flipclock

# Refresh icon cache if command exists
if command -v gtk-update-icon-cache >/dev/null 2>&1; then
    gtk-update-icon-cache -f /usr/share/icons/hicolor || true
fi

echo "=========================================================="
echo " Flip Clock Screensaver successfully installed!"
echo " The daemon will start automatically on next login."
echo " To start it manually for the current session, run:"
echo "   flipclock --daemon"
echo " To preview screensaver immediately, run:"
echo "   flipclock --run"
echo "=========================================================="
EOF
chmod 755 "$PKG_DIR/DEBIAN/postinst"

# Create DEBIAN/postrm (post-removal script)
cat << 'EOF' > "$PKG_DIR/DEBIAN/postrm"
#!/bin/bash
set -e

if [ "$1" = "remove" ] || [ "$1" = "purge" ]; then
    # Remove system bin symlinks
    rm -f /usr/bin/flipclock
    rm -f /usr/local/bin/flipclock
    echo "Flip Clock Screensaver successfully removed."
fi
EOF
chmod 755 "$PKG_DIR/DEBIAN/postrm"

# Create desktop launcher file
cat << 'EOF' > "$PKG_DIR/usr/share/applications/flipclock.desktop"
[Desktop Entry]
Type=Application
Name=Flip Clock Screensaver
Comment=Launch Flip Clock Screensaver immediately
Exec=flipclock --run
Icon=flipclock
Terminal=false
Categories=Utility;
EOF

# Create settings launcher file
cat << 'EOF' > "$PKG_DIR/usr/share/applications/flipclock-settings.desktop"
[Desktop Entry]
Type=Application
Name=Flip Clock Settings
Comment=Configure Flip Clock screensaver settings
Exec=flipclock --settings
Icon=flipclock
Terminal=false
Categories=Settings;Utility;
EOF

# Create system-wide desktop autostart entry
cat << 'EOF' > "$PKG_DIR/etc/xdg/autostart/flipclock-daemon.desktop"
[Desktop Entry]
Type=Application
Name=Flip Clock Screensaver Daemon
Comment=Autostart Flip Clock Screensaver Daemon
Exec=flipclock --daemon
Icon=flipclock
Terminal=false
NoDisplay=true
X-GNOME-Autostart-enabled=true
EOF

# Correct directories/files permissions for Debian packaging
find "$PKG_DIR" -type d -exec chmod 755 {} \;
find "$PKG_DIR" -type f -not -path "$PKG_DIR/DEBIAN/*" -exec chmod 644 {} \;
chmod 755 "$PKG_DIR/usr/share/flipclock/flipclock.py"

echo "Building Debian package using dpkg-deb..."
dpkg-deb --build "$PKG_DIR" "${PKG_NAME}_${PKG_VER}_all.deb"

echo "Cleaning up temporary files..."
rm -rf "$PKG_DIR"

echo "Debian package created: ${PKG_NAME}_${PKG_VER}_all.deb"
