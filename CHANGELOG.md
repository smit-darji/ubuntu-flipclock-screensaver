# Changelog - Flip Clock Screensaver

All notable changes to the Flip Clock Screensaver project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [5.0.4] - 2026-09-02 - Collapsed Tile Width & Option B Auto-Update Release

### Added
- **⏱️ Collapsed Tile Width & Snug HH:MM:SS**: Overrode default `width` and `height` clamp rules on `.glass-digit-tile` (`width: auto !important`, `height: auto !important`, `min-width: 0 !important`) to eliminate giant empty 400px gaps between digits and colons.
- **📄 Option B Header Auto-Update**: Added regex pattern to `build_deb.sh` to automatically sync `Option B: Install Versioned Release Archive (v5.0.4)` in `README.md`.

## [5.0.3] - 2026-09-02 - Mandatory 3D Glass Seconds & Ultra-Smooth WebP Live Background Sync

### Added
- **⏱️ Mandatory Ticking Seconds (`: SS`)**: Enforced real-time seconds ticking (`HH : MM : SS AM/PM`) for live wallpaper themes (`glass_misty_pavilion` & `glass_anime_hydrangea`).
- **🌸 60FPS Smooth WebP Live Background**: Prioritized Z-index layering (`z-index: 5`) for `misty_pavilion.webp` and `anime_hydrangea.webp` ensuring ultra-smooth 60fps native animated video backgrounds.

## [5.0.2] - 2026-09-02 - Compact HH:MM:SS Glass Clock Spacing Release

### Added
- **⏱️ Tighter & Compact HH:MM:SS Digit Spacing**: Reduced colon margins (`margin: 0 -10px`) and letter-spacing (`-0.03em`) to eliminate wide empty gaps between hours, minutes, seconds, and colons.
- **💎 Uniform 3D Glass Seconds Display**: Seconds (`SS`) rendered in the exact same 3D rounded liquid glass font (`Comfortaa`/`Outfit`) alongside hours and minutes.

## [5.0.1] - 2026-09-02 - WebP Live Animated Wallpaper & 3D Glass Seconds Sync

### Added
- **🌸 Real-Time Animated WebP Live Backdrop**: Explicit Z-index layering for `misty_pavilion.webp` and `anime_hydrangea.webp` ensuring ultra-smooth 60fps native animated video backgrounds.
- **⏱️ Ticking 3D Glass Seconds & Matching AM/PM Typography**: `HH:MM:SS AM/PM` with matching translucent liquid glass 3D stroke reflections and glowing drop shadows.
- **✨ Dual Live Wallpaper Theme Support**: Seamless support for both `glass_misty_pavilion` and `glass_anime_hydrangea` themes.

## [5.0.0] - 2026-09-02 - Master 3D Glass Live Clock Release

### Added
- **🏮 Frameless 3D Glass Live Clock Overlay**: Ultra-sleek 100% cardless 3D glass clock overlay (`11:47:36 AM`) positioned in the right-center area over live WebM/WebP video backgrounds (`misty_pavilion.webp` & `misty_pavilion.webm`).
- **── T U E S D A Y ── Day Line Divider**: Centered weekday text flanked by left and right horizontal silver lines.
- **📅 Real-Time HH:MM:SS Ticking & Uppercase Date**: Real-time ticking seconds and uppercase date (`02 SEPTEMBER 2026`).
- **🚀 Single Instance & Process Cleanup**: Added singleton guards to prevent multiple overlapping screensaver instances.

## [4.0.4] - 2026-09-02 - Frameless 3D Glass Live Clock & WebP Wallpaper Release

### Added
- **🏮 Frameless 3D Glass Live Clock Overlay**: 100% cardless floating 3D glass clock overlay (`11:47:36 AM`) positioned in the right-center area over the lake background (`misty_pavilion.webp` & `misty_pavilion.webm`).
- **── T U E S D A Y ── Day Line Divider**: Left and right horizontal divider lines flanking the uppercase weekday text.
- **📅 Real-Time HH:MM:SS Ticking & Uppercase Date**: Real-time ticking seconds and uppercase date (`02 SEPTEMBER 2026`).
- **📦 Latest Debian Package Build**: Built `releases/flipclock-screensaver_4.0.4.deb` and updated installation scripts.

## [4.0.0] - 2026-09-02 - Aesthetic Frameless Glass Clock & Day Line Divider Release

### Added
- **✨ Frameless Cardless Glass Clock Layout**: Designed 100% frameless aesthetic rounded glass digits floating over live video scenes with zero cards or container boxes.
- **── T U E S D A Y ── Day Line Divider**: Integrated horizontal line divider with uppercase day-of-week typography.
- **📅 Tracked Uppercase Date Display**: Added clean date formatting below day divider line (`02 SEPTEMBER 2026`).
- **⚡ Live Ticking HH:MM:SS Updates**: Real-time live second ticking (`HH:MM:SS AM/PM`) smoothly updating on screen.

## [3.9.0] - 2026-09-02 - Animated WebP Live Wallpaper & Codec-Free Support

### Added
- **🎆 Ultra-Lightweight Animated WebP Live Wallpapers**: Created high-definition 24-bit 60fps WebP animated files (`anime_hydrangea.webp` & `misty_pavilion.webp`) providing 100% instant native animation with zero GStreamer codec dependencies.
- **🖼️ Codec-Free Image + Video Layering**: Combined WebP animated image layers with WebM and MP4 video fallbacks for flawless background rendering across all Linux systems and GTK WebKit versions.

## [3.8.0] - 2026-09-02 - Live Video Wallpaper Autoplay & Path Resolution Release

### Added
- **🎥 Dynamic Live Video Path Fallbacks**: Multi-source resolution handling in HTML (`<source src="live-wallpaper/..." type="video/mp4">` and absolute workspace paths) for 100% reliable background rendering.
- **⚡ GTK WebKit Autoplay Configuration**: Enabled `set_media_playback_requires_user_gesture(False)` in `flipclock.py` and `screensaver.py` for seamless headless screensaver video playback.
- **🌸 Optimized 4K Video Assets**: High-efficiency MP4 compression preserving 4K video fidelity while keeping the Debian package lightweight.

## [3.7.0] - 2026-09-02 - Misty Lakeside Pavilion Live Wallpaper Theme & Frameless Lantern Glow Clock

### Added
- **🏮 Misty Lakeside Pavilion Theme (`glass_misty_pavilion`)**: Integrated 4K live video wallpaper backdrop (`live-wallpaper/6964bab862_misty-lakeside-pavilion-live-wallpaper-wallsflow-com.mp4`) capturing misty lake fog, ancient forest shadows, and amber lantern reflections.
- **✨ Frameless Floating Amber Lantern Clock Display**: Designed frameless transparent typography overlay (`background: transparent; border: none; box-shadow: none`) featuring warm glowing lantern amber-gold digits (`#FEF3C7` with `#F59E0B` / `#D97706` text shadow) floating above the lake mist.

## [3.6.0] - 2026-09-02 - Anime Girl Hydrangea Garden Live Wallpaper Theme & Frameless Aesthetic Clock

### Added
- **🌸 Anime Girl Hydrangea Garden Theme (`glass_anime_hydrangea`)**: Integrated seamless live video wallpaper backdrop (`live-wallpaper/ba98956200_anime-girl-hydrangea-garden-live-wallpaper-wallsflow-com.mp4`) with smooth autoplay and dark vignette overlay.
- **✨ Frameless Floating Aesthetic Clock Display**: Designed frameless transparent typography overlay (`background: transparent; border: none; box-shadow: none`) featuring glowing soft hydrangea lavender digits (`#F8F5FF` with `#C084FC` / `#A855F7` text shadow) floating seamlessly on top of the live video background.

## [3.5.0] - 2026-08-31 - Frosted Dark Ruby Spider-Man Glass Cards & Deep High-Contrast Ganesha Theme

### Added
- **🕷️ Frosted Dark Ruby Glass Cards (`glass_spiderman`)**: Added translucent frosted dark ruby glass tiles (`background: rgba(14, 4, 9, 0.76); border: 1px solid rgba(239, 68, 68, 0.5); backdrop-filter: blur(22px);`) to blur out busy background window lights and guarantee 100% crystal-clear digit visibility (`07:47:17`).
- **🐘 Deep High-Contrast Ganesha Theme (`glass_ganesha`)**: Enhanced background artwork filter (`brightness(0.55) contrast(1.22)`), dark teak glass tiles (`rgba(12, 5, 2, 0.78)`), and pure white digits (`#FFFFFF`) with glowing saffron text shadow.

## [3.4.0] - 2026-08-31 - High-Contrast Ganesha Theme & Frameless Spider-Man Theme

### Added
- **🐘 High-Contrast Ganesha Theme Visibility (`glass_ganesha`)**: Darkened background artwork filter (`brightness(0.70) contrast(1.18)`), dark teak glass tiles (`rgba(14, 6, 2, 0.72)`), and pure white digits (`#FFFFFF`) with glowing golden amber text shadow for 100% crystal-clear readability.
- **🕷️ 100% Invisible Frameless Spider-Man Theme (`glass_spiderman`)**: Completely removed card boxes, borders, and shadows (`background: transparent; border: none; box-shadow: none`), allowing digits to float cleanly in full-screen space with web lighting.

## [3.3.0] - 2026-08-31 - User Lord Ganesha Temple Mandap Artwork & Auto-Approve Uninstall Guide

### Added
- **🐘 User Uploaded Lord Ganesha Temple Mandap Artwork (`glass_ganesha`)**: Integrated native 16:9 widescreen temple mandap artwork (`assets/ganesha_murti_bg.png`) with teakwood & warm amber color harmonization.
- **🕷️ Ultra-Premium Realistic Spider-Man Theme Redesign (`glass_spiderman`)**: Upgraded 3D suit graphics, metallic white eye lenses (`.eye-lens`), dark ruby glass cards, and high-res NYC skyline backdrop.
- **🗑️ Auto-Approve Uninstallation Guide**: Updated `README.md` to document `-y` auto-approval commands (`sudo apt remove -y flipclock-screensaver` & `sudo apt purge -y flipclock-screensaver`).

## [3.2.0] - 2026-08-31 - Widescreen Panoramic Lalbaugcha Raja Artwork & Extended Font Calibration

### Added
- **🐘 1920x1080 Widescreen Panoramic Lalbaugcha Raja Artwork (`glass_ganesha`)**: Full-screen edge-to-edge depiction with blended bokeh ambient side wings, zero black side bars, and glowing saffron halo lighting across all widescreen & ultrawide monitor resolutions.
- **🔤 Universal Font Scaling & Proportional Margins**: Calibrated digit font size (`clamp(3.8rem, 11vw, 15rem)`) and extended font overrides for Orbitron (`clamp(3.1rem, 9vw, 12.5rem) !important; letter-spacing: -0.04em !important`) to guarantee ~15% side margins with zero card edge spillover across all 31 themes.
- **🕷️ Animated Real Spider-Man Web-Slinger Hero Sprite (`glass_spiderman`)**: High-detail suit figure with glowing eye lenses (`.eye-lens`), chest spider emblem, and animated web shooter lines.

## [3.1.0] - 2026-08-31 - Unified Card Dimensions & Full-Screen Spider-Man NYC Theme

### Added
- **🕷️ Full-Screen Cinematic Spider-Man NYC Theme (`glass_spiderman`)**: Dedicated NYC night atmosphere with radial web overlay grids, vignette edge textures, floating particles, dark skyline, and glowing red/blue digits.
- **Unified Universal Card Dimensions**: Standardized card dimensions (`width: clamp(170px, 25vw, 400px); height: clamp(210px, 29vw, 470px)`) across all 31 themes (retro flip cards & glass tiles).
- **Anti-Clipping Digit Typography**: Calibrated digit sizing (`clamp(4.5rem, 13.5vw, 18rem)`), line height (`1.1`), and overflow handling to completely eliminate digit font clipping.

## [3.0.0] - 2026-08-31 - Tall Flip-Card Proportions, Animated Spider-Man & Lord Ganesha Divine Murti

### Added
- **🕷️ Animated Spider-Man NYC Web-Slinger**: Added animated NYC building skyline background with Spider-Man swinging dynamically between skyscrapers in a continuous pendulum arc with web shooting lines.
- **🐘 Lord Ganesha Divine Murti Background (`glass_ganesha`)**: Integrated high-resolution golden Lord Ganesha Murti artwork with pulsating saffron halo aura (`ganeshaPulseAura`) and marigold lighting.
- **Tall Vertical Flip-Card Proportions for Glass Themes**: Standardized all Glass themes to feature exact tall vertical flip card dimensions (`1 : 1.35` aspect ratio) with authentic middle split-flap divider lines (`.glass-digit-tile::after`) and hinge dots.
- **Internal AM/PM Pill Badge**: Moved the AM/PM badge inside the bottom right corner of the last card (`#gc-s` / `#gc-m`), matching retro split-flap clock layouts.

## [2.9.0] - 2026-08-31 - Ganesha Festival Divine Gold Theme & Fluid Sizing

### Added
- **🐘 Ganesha Festival Divine Gold Theme (`glass_ganesha`)**: Royal saffron & temple gold ambient backdrop (`#1a0c02`) with animated glowing marigold orange and sacred saffron light orbs.
- **Fluid Code-Based Responsive Layout System**: Standardized all Glass theme layout dimensions with fluid CSS variables and responsive calc logic for seamless scaling across all display aspect ratios.

## [2.8.0] - 2026-08-31 - Larger Responsive Sizing, Spider-Man Theme & Star Badges

### Added
- **🕷️ Spider-Man Web Theme (`glass_spiderman`)**: Dark crimson red & midnight blue ambient backdrop (`#180308`) with spider-red neon glowing colons and web highlights.
- **Larger Hero Responsive Sizing**: Scaled up digit font size (`clamp(5.5rem, 17vw, 22rem)`), card dimensions (`min-width: clamp(120px, 25vw, 400px)`), and colon spacing for a grand full-screen screensaver presentation across 1080p, 2K, 4K, and ultra-wide displays.
- **Vertically Centered AM/PM Pill Badge**: Centered `.gc-ampm-pill` vertically (`align-self: center`) alongside the time row for balanced, pixel-perfect alignment.
- **`✦` Star Badge Indicator**: Replaced literal "NEW" text labels with sleek gold star badge icons (`✦`) in quick menus and GTK settings.

## [2.7.0] - 2026-08-31 - Frameless Glass Clock & 5 New Aesthetic Themes

### Added
- **Frameless Glass Clock Layout**: Completely removed the heavy outer container box (`#glass-clock-display`), allowing sleek frosted glass digit tiles to float directly on the screen against rich aesthetic backgrounds.
- **5 Brand-New Aesthetic Glass Themes**:
  - 🌌 **Aurora Glass (`glass_aurora`)**: Deep cosmic navy backdrop with flowing cyan/violet/teal aurora light waves.
  - 🌆 **Cyberpunk Neon (`glass_cyberpunk`)**: Synthwave dark backdrop with electric magenta/cyan plasma glow.
  - 🌿 **Emerald Gold (`glass_emerald`)**: Midnight emerald green backdrop with warm gold ambient illumination.
  - 🌇 **Sunset Champagne (`glass_sunset`)**: Twilight dusk backdrop with warm rose gold & peach sunset lights.
  - 🧊 **OLED Pure Frameless (`glass_minimal_oled`)**: Pitch black backdrop (`#000000`) with pure floating white digits and zero card borders.
- **Clean AM/PM Frosted Pill Badge**: Re-architected the AM/PM badge into an elegant, non-overlapping frosted capsule badge (`.gc-ampm-pill`) positioned cleanly beside the seconds tile.
- **`✦ NEW` Badging**: Added clear visual indicators for all new Glass Clock themes across the floating quick menu overlay and GTK settings GUI (`flipclock --settings`).

## [2.6.0] - 2026-08-31 - Premium Glass Clock Face & Quick Menu Integration

### Added
- **✨ Glass Clock Face**: A completely new premium full-screen clock face design featuring a modern transparent frosted glass container (`backdrop-filter: blur(24px)`), semi-transparent dark background (`rgba(10, 15, 25, 0.35)`), light glass borders, and soft glowing depth effects.
- **Ambient Lighting Background**: Added subtle hardware-accelerated animated floating light circles/orbs in the background for ambient depth.
- **Responsive Typography & Date**: Large high-readability digit display (`clamp(4rem, 14vw, 16rem)` font sizing) with thin/medium font weight and an elegant date badge (`Sunday, August 31, 2026`).
- **Interactive Quick Menu**: Added a floating top-right **🪟 Clock Faces** overlay menu button in `clock.html` / `index.html` for switching between Flip Clock mode, theme presets, and the new Glass Clock face.
- **OLED Burn-In Protection**: Automatic subtle position shifting (±8px X/Y) every 2 minutes with smooth CSS transitions to prevent static monitor burn-in.

### Changed
- **GTK Settings GUI Integration**: Registered `glass_clock` in `THEME_CATEGORIES` and `PRESET_THEMES` inside `flipclock.py` for selection in `flipclock --settings`.

## [2.5.7] - 2026-08-14 - Dark Black Theme & Seconds Card AM/PM Badge

### Added
- **Dark Black Theme**: A premium, ultra-clean theme with a deep black background (`#000000`), subtle dark slate card backgrounds (`#0A0A0C`), and high-visibility white digits with soft drop shadows.

### Changed
- **AM/PM Badge Relocation**: Relocated the AM/PM badge from the Minutes card to the Seconds card (`#fc-s`), positioned slightly higher to sit cleanly underneath the digits.

## [2.5.6] - 2026-08-14 - AM/PM Badge Position Update

### Changed
- **AM/PM Badge Position**: Relocated the AM/PM badge from the Hours (first) card to the Minutes (second) card to improve layout balance.

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
