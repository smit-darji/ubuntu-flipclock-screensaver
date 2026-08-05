# Changelog - Flip Clock Screensaver

All notable changes to the Flip Clock Screensaver project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.5.5] - 2026-08-05 - Minimalist Dark Theme, Shape Compatibility & Day Toggle

### Added
- **Minimalist Dark Theme**: A pure system dark mode aesthetic theme with #111111 background, #1C1C1E card backgrounds, and a subtle border for card lift.
- **Independent Day of Week Toggle**: Added settings UI options to show/hide the day name segment (e.g. TUESDAY) independently of the date segment.

### Fixed
- **Theme Shape Compatibility**: Corrected issue where the selected card shape was ignored by premium themes (`minimal_dark`, `swiss_minimalist`, `apple_liquid_glass`) due to hardcoded `!important` border-radius overrides.

## [2.5.4] - 2026-08-03 - Premium Apple Liquid Glass Theme & Gtk Font Wraps

### Added
- **Apple Liquid Glass Theme**: Integrated a premium, realistic Apple Liquid Glass theme with frosted sapphire glassmorphism (`blur(24px) saturate(180%)`), golden pivot pins, and elegant system serif typography (`New York` / `Cormorant Garamond`).
- **Gtk Font Dropdown Wrapping**: Configured font selection dropdown boxes in the GTK settings GUI window to show values in columns side-by-side (`set_wrap_width(2)`), improving options visibility and eliminating extremely long scrolling lists.

## [2.5.1] - 2026-07-31 - Patch Release: Shape-Wise AM/PM Visibility

### Fixed
- **Shape-Wise AM/PM Clipping Fix**: Solved the issue where the AM/PM badge was clipped or hidden entirely on custom card shapes due to CSS `clip-path` and `overflow: hidden` on the card elements.
- **Flip Card Wrapper**: Introduced a `.flip-card-wrapper` parent container around the hours flip-card to isolate the `#ampm-badge` element from the card's clipped boundary.
- **Shape-Specific Positioning Adjustments**: Added fine-tuned CSS absolute positioning offsets for all 29 shapes (including Diamond, Circle, Hexagon, Octagon, Pentagon, Shield, Capsule, Pill, Stadium, Lozenge, and Chevron) to ensure the AM/PM badge fits perfectly within the borders of each shape.

## [2.5.0] - 2026-07-30 - Major Release: 20 Executive Themes, Auto Color Palette & Custom Popups

### Added
- **20 Luxury Dark Themes**: Premium color themes including Luxury Black Gold, Obsidian Titanium, Dark Emerald, Forest Green, Racing Green, Ruby Executive, Burgundy Prestige, and more.
- **Auto Color & Typography Sync**: Theme selection automatically synchronizes background, card background, digit colors, border highlights, and 18 executive font combinations.
- **Custom Dark GTK Dialogs**: Native screensaver settings alerts replaced with custom dark GTK dialogs (`CustomDarkDialog`).

## [2.3.0] - 2026-07-30 - Minor Release: Executive Theme Collections, Category Filtering & Quick Visual Swatch Tiles

### Added
- **Executive Theme Collections Categorization**: Re-organized theme presets into 5 clean categories to eliminate long scrolling dropdown lists:
  1. 🏆 *Executive Dark & Gold*
  2. 🌿 *Executive Greens*
  3. 💎 *Ruby & Crimson Reds*
  4. 🚙 *Sapphire & Ocean Blues*
  5. 🔮 *Purple, Graphite & Custom*
- **Dynamic Category Theme Dropdown Filter**: Selecting a theme category filters the preset dropdown to show only the 3-5 themes in that category.
- **Quick Visual Theme Swatch Pill Buttons**: Added visual quick-select swatch buttons (`theme-tile-btn`) for 1-click theme selection.

---

## [2.2.0] - 2026-07-30 - Major Release: 20 Executive Dark Themes, Auto Palette Selection & Custom GTK Popups

### Added
- **20 Curated Executive Dark Themes**: Added 20 luxury dark color presets:
  1. *🥇 Luxury Black Gold (Executive Rolex / Bentley)*
  2. *🥈 Obsidian Titanium (Apple Pro / Tesla)*
  3. *🥉 Dark Emerald Premium (Luxury Finance)*
  4. *🌲 Forest Green Executive*
  5. *🏎️ British Racing Green (Aston Martin)*
  6. *💎 Ruby Executive (Premium Red)*
  7. *🍷 Burgundy Prestige (Wine & Leather)*
  8. *🏎️ Crimson Royal (Ferrari Cockpit)*
  9. *🚙 Royal Sapphire (BMW Digital Cockpit)*
  10. *⚓ Midnight Navy*
  11. *❄️ Arctic Ice*
  12. *🌊 Ocean Cyan*
  13. *👑 Royal Purple*
  14. *🔮 Amethyst Elite*
  15. *🪙 Platinum Silver*
  16. *⚙️ Graphite Gray*
  17. *🧱 Copper Elite*
  18. *🌹 Rose Gold*
  19. *🥂 Champagne Gold*
  20. *✨ Matte Black Diamond (Ultra Minimal)*
- **Automatic Color Palette & Font Sync**: Selecting any theme preset automatically populates background, card fill, text color, accent color, card border, and harmonized executive fonts (*Cinzel*, *Inter*, *Orbitron*, *Outfit*, *Roboto*, *Rajdhani*, *Exo 2*, *Oxanium*, *Bebas Neue*).
- **Sleek Minimal Color Pickers Layout**: Redesigned color swatch controls with compact right-aligned swatches instead of full-width bars.
- **Custom Dark GTK Dialog Popups**: Replaced default system dialog popups with custom dark GTK modal windows (`CustomDarkDialog`).
- **Clean Branding**: Removed all third-party watermark tags and replaced with clean "Flip Clock Screensaver" branding.

---

## [2.1.0] - 2026-07-29 - Feature Release: Custom Themes, Color Pickers & Font Styling

### Added
- **Custom Theme Engine & Color Pickers**: Full custom color picker support allowing users to pick custom hex/RGBA colors via `Gtk.ColorButton` for:
  - Scene Background Color
  - Card Background Color
  - Digit / Text Color
  - Accent & Pin Color
  - Card Border Color
- **Typography & Font Customization**: Dropdown selection for clock digit fonts and label/badge fonts supporting Google Fonts & system fonts:
  - *Digits Fonts*: Inter, Roboto, Orbitron, Cinzel, Outfit, Oswald, Courier Prime.
  - *Label Fonts*: Cinzel, Inter, Roboto, Orbitron, Outfit, Oswald, Courier Prime.
- **One-Click Reset to Defaults**: Prominent warning action button (`btn-reset`) in the GTK Settings Window to instantly restore all theme, color, font, and display options back to initial default values with dialog confirmation.
- **Enhanced Settings UI Layout & Visibility**: Re-architected GTK settings page with dedicated sections for *Custom Colors & Palette* and *Typography Customization*, real-time widget updates, and scrollable container optimization.

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
