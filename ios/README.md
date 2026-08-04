# Premium Flip Clock Screensaver - iOS Setup Guide

This directory contains the Swift/SwiftUI templates to compile the flip clock screensaver into a native iOS application for iPhone and iPad.

---

## 🛠️ Step-by-Step Xcode Setup

Follow these simple steps on your Mac to compile and install the application:

### 1. Create a New Xcode Project
1. Open **Xcode** on your Mac.
2. Select **Create a new Xcode project**.
3. Choose **iOS -> App** under the template selection, then click **Next**.
4. Set the project parameters:
   * **Product Name**: `FlipClock`
   * **Interface**: `SwiftUI`
   * **Language**: `Swift`
5. Click **Next** and save the project to a folder on your Mac.

### 2. Copy the Swift Templates
Replace the Xcode default code files with the provided templates from this directory:
1. Replace `FlipClockApp.swift` with [FlipClockApp.swift](FlipClock/FlipClockApp.swift).
2. Replace `ContentView.swift` with [ContentView.swift](FlipClock/ContentView.swift).
3. Add a new Swift file named `WebView.swift` and copy the contents of [WebView.swift](FlipClock/WebView.swift) into it.

### 3. Add the HTML Screensaver Asset
1. Locate the file `index.html` from `mobile/app/src/main/assets/index.html` (or copy it from the workspace).
2. Drag and drop `index.html` into your Xcode project navigator (usually under the `FlipClock` group folder).
3. In the dialog box that appears:
   * Check **Copy items if needed**.
   * Select **Create folder references** (or *Create groups*).
   * Ensure `FlipClock` is checked under **Add to targets**.
   * Click **Finish**.

### 4. Build and Install
1. Connect your iPhone via USB, or select an iOS Simulator (e.g. iPhone 15 Pro) from the target device dropdown at the top.
2. Click the **Play button (▶)** in the top-left corner (or press `Cmd + R`) to compile and run.
3. The screensaver app will launch on your device in full screen. Double-tap the background to change themes, shapes, formats, or toggle second cards!
