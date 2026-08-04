# Premium Flip Clock Screensaver - Android Mobile App

This directory contains the native Android WebView implementation of the Fliqlo-style flip clock screensaver.

## 📥 Direct APK Download

Click the button below to download the compiled mobile application directly:

<p align="center">
  <a href="../releases/flipclock-screensaver.apk" target="_blank">
    <img src="https://img.shields.io/badge/DOWNLOAD-Android%20Mobile%20APK-FFB000?style=for-the-badge&logo=android&logoColor=white" height="54" alt="Download Android Mobile APK">
  </a>
</p>

---

## 📱 Mobile-Specific Features

1. **Responsive Vertical Stack (Portrait)**:
   Hours (HH), Minutes (MM), and Seconds (SS) cards automatically stack top-to-bottom on vertical portrait mobile viewports to maximize text size and legibility.
2. **Horizontal Layout (Landscape)**:
   Cards rotate side-by-side automatically when rotating the mobile screen.
3. **Double-Tap Settings Drawer**:
   Double-tap anywhere on the screen background to slide open the options panel to customize themes, shapes, username, and formats.
4. **Local Storage Persistence**:
   User settings automatically persist across app launches.
5. **Always-On Screen (Wake Lock)**:
   Configures system window flags to keep the screen active indefinitely while displaying the screensaver.

---

## 🛠️ How to Compile / Rebuild

To rebuild the APK from scratch:
1. Ensure the setup script has run:
   ```bash
   ./setup_sdk.sh
   ```
2. Execute the compile script:
   ```bash
   ./compile_apk.sh
   ```
3. Find your built APK at `app/build/outputs/apk/debug/app-debug.apk`.
