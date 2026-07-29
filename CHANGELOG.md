# Changelog - Flip Clock Screensaver

All notable changes to the Flip Clock Screensaver project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.0] - 2026-07-29 - Major Release

### Added
- **Personalized Time-Based Greetings**: Dynamic greetings based on time of day (`GOOD MORNING`, `GOOD AFTERNOON`, `GOOD EVENING`, `GOOD NIGHT`).
- **User Name Personalization**: Custom name support in Settings GUI (e.g. `GOOD MORNING, SMIT`).
- **Multi-Theme Engine**: 6 curated CSS variable theme layouts:
  1. **Classic Retro (Fliqlo Style)** (*Default*)
  2. **Dark Luxury (Gold Accent)**
  3. **Midnight Cyber (Neon Blue)**
  4. **Emerald OLED (Matrix Green)**
  5. **Sunset Glow (Amber / Crimson)**
  6. **Minimalist Light (Clean Silver)**
- **Modern Dark GTK Settings Application**: Complete GUI redesign using GTK CSS provider styling, dark cards, section headers, switches, scale sliders, and generous button spacing.
- **Ultra-High Resolution Application Assets**: 512x512 transparent PNG logo icon (`flipclock.png`) and screenshot assets generated using PIL with anti-aliased squircle borders and gold pins.
- **CLI Options**:
  - `--theme <theme_id>`: Instant theme testing via terminal.
  - `--version`: Displays software version info.
  - `--settings`: Opens GTK configuration window.
  - `--run`: Launches full-screen screensaver preview.

### Changed
- Default theme restored to **Classic Retro (Fliqlo Style)**.
- Adjusted GTK HeaderBar contrast, ComboBox dropdown visibility, and action button top margin (`22px`).
- Updated system autostart and Systemd service integration.

---

## [1.2.0] - 2026-07-29

### Added
- Dropdown contrast and hover state styling for GTK ComboBox popup menus.
- Action button spacing and window size adjustment (`540x680`).

---

## [1.1.0] - 2026-07-29

### Added
- Theme engine infrastructure and GTK Settings window prototype.
- CLI `--version` and `--theme` flags.

---

## [1.0.0] - Initial Release

### Added
- Core Fliqlo-style 3D split-flap flip clock implementation in WebKit2/HTML5.
- Native X11 Screen Saver idle monitoring daemon (`libXss` ctypes binding) with 0.0% CPU overhead.
- Multi-monitor geometry detection and full-screen window spawning.
- Debian package installer script (`build_deb.sh`, `install.sh`, `uninstall.sh`).
