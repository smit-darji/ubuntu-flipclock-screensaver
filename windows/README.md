# Premium Flip Clock Screensaver - Windows Setup Guide

This directory explains how to deploy and run the responsive flip clock as a native screensaver on Windows systems (Windows 10 and 11) using a lightweight webpage screensaver wrapper.

---

## 🛠️ Step-by-Step Windows Installation

To run the clock on Windows, you can wrap the offline `index.html` asset using a standard Webpage Screensaver wrapper (which runs locally on top of Microsoft Edge WebView2 / Chromium with zero CPU overhead).

### 1. Download the Webpage Screensaver Wrapper
1. Download the lightweight utility **Webpage Screensaver** (created by *cwebster*):
   * [Download ZIP (GitHub Releases)](https://github.com/cwebster/webpage-screensaver/releases)
2. Extract the ZIP file to find the screensaver file: `WebpageScreensaver.scr`.

### 2. Install the Screensaver
1. Right-click on `WebpageScreensaver.scr` and select **Install** from the context menu (or copy it directly into `C:\Windows\System32`).
2. The Windows **Screen Saver Settings** control panel window will open automatically with **WebpageScreensaver** selected.

### 3. Link the HTML Clock File
1. Locate the responsive clock file `index.html` in this workspace under `mobile/app/src/main/assets/index.html` (or copy it to a secure local folder on your Windows PC, e.g. `C:\FlipClock\index.html`).
2. In the Windows Screen Saver Settings window, click **Settings...** next to WebpageScreensaver.
3. In the Configuration dialog:
   * **URL / Path**: Enter the absolute local path to your HTML file, prefixed with `file:///` (for example: `file:///C:/FlipClock/index.html`).
   * Check **Allow interactive actions** (to enable double-tap/double-click settings drawer).
4. Click **OK** to save the configuration.

### 4. Preview and Run
1. Click **Preview** in the Screen Saver Settings window to see the clock run in full-screen.
2. Double-click anywhere on the screen background to slide open the custom settings overlay panel, allowing you to change themes, shapes, formats, and toggle seconds cards.
3. Move the mouse to exit screensaver mode.
