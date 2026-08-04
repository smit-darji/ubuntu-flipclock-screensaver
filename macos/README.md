# Premium Flip Clock Screensaver - macOS Setup Guide

This directory contains the Swift templates to compile the flip clock screensaver into a native macOS Screensaver (`.saver` bundle) for Mac laptop and desktop systems.

---

## 🛠️ Step-by-Step Xcode Setup

Follow these steps on your Mac to compile and install the screensaver:

### 1. Create a New Xcode Project
1. Open **Xcode** on your Mac.
2. Select **Create a new Xcode project**.
3. Choose **macOS -> Screen Saver** under the template selection, then click **Next**.
4. Set the project parameters:
   * **Product Name**: `FlipClockScreensaver`
   * **Language**: `Swift`
5. Click **Next** and save the project to a folder on your Mac.

### 2. Add the Swift Templates
Replace the Xcode default code files with the provided templates from this directory:
1. Replace the generated principal view class (e.g. `FlipClockScreensaverView.swift`) with [FlipClockView.swift](FlipClockScreensaver/FlipClockView.swift).
2. Open your Xcode project settings, go to the project target **Info** tab, and verify that the `Principal class` key points to `FlipClockScreensaver.FlipClockView`. If not, update it or copy the [Info.plist](FlipClockScreensaver/Info.plist) keys.

### 3. Add the HTML Screensaver Asset
1. Locate the file `index.html` from `mobile/app/src/main/assets/index.html` (or copy it from this workspace).
2. Drag and drop `index.html` into your Xcode project navigator (under the `FlipClockScreensaver` group folder).
3. In the dialog box:
   * Check **Copy items if needed**.
   * Select **Create folder references**.
   * Ensure `FlipClockScreensaver` is checked under **Add to targets**.
   * Click **Finish**.

### 4. Build and Install
1. Build the project by selecting **Product -> Build** (or pressing `Cmd + B`).
2. In the Xcode project navigator, look for the **Products** folder. Under it, right-click on `FlipClockScreensaver.saver` and select **Show in Finder**.
3. In Finder, **double-click** on `FlipClockScreensaver.saver`.
4. macOS will ask: *"Do you want to install 'FlipClockScreensaver' for this user or all users?"* Click **Install**.
5. The screensaver is now active! Open macOS **System Settings -> Screen Saver** to preview or test. Double-click on the screensaver preview to open the settings menu and configure themes and shapes.
