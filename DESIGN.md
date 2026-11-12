---
name: Networking Pedagogical Workspace
colors:
  surface: '#f7f9ff'
  surface-dim: '#d7dae0'
  surface-bright: '#f7f9ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f1f4fa'
  surface-container: '#ebeef4'
  surface-container-high: '#e5e8ee'
  surface-container-highest: '#dfe3e8'
  on-surface: '#181c20'
  on-surface-variant: '#424654'
  inverse-surface: '#2d3135'
  inverse-on-surface: '#eef1f7'
  outline: '#737785'
  outline-variant: '#c3c6d6'
  surface-tint: '#0856cf'
  primary: '#0041a2'
  on-primary: '#ffffff'
  primary-container: '#0b57d0'
  on-primary-container: '#ced9ff'
  inverse-primary: '#b2c5ff'
  secondary: '#006e2a'
  on-secondary: '#ffffff'
  secondary-container: '#8ffa9b'
  on-secondary-container: '#00752d'
  tertiary: '#940004'
  on-tertiary: '#ffffff'
  tertiary-container: '#bc1813'
  on-tertiary-container: '#ffcec7'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#dae2ff'
  primary-fixed-dim: '#b2c5ff'
  on-primary-fixed: '#001847'
  on-primary-fixed-variant: '#0040a1'
  secondary-fixed: '#8ffa9b'
  secondary-fixed-dim: '#73dc82'
  on-secondary-fixed: '#002108'
  on-secondary-fixed-variant: '#00531e'
  tertiary-fixed: '#ffdad5'
  tertiary-fixed-dim: '#ffb4a9'
  on-tertiary-fixed: '#410001'
  on-tertiary-fixed-variant: '#930004'
  background: '#f7f9ff'
  on-background: '#181c20'
  surface-variant: '#dfe3e8'
typography:
  headline-xl:
    fontFamily: Plus Jakarta Sans
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Plus Jakarta Sans
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Plus Jakarta Sans
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Plus Jakarta Sans
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Plus Jakarta Sans
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-lg:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style
The design system establishes a high-clarity, institutional yet approachable workspace tailored for networking instructors and vocational students. It blends the functional minimalism of modern productivity suites with specialized diagrammatic density. 

The emotional tone is reliable, analytical, and uncluttered. Visual hierarchy prioritizes dense data sets, packet flows, and hardware schematics without inducing cognitive fatigue. Clean white canvas zones, precise structural lines, and authoritative blue highlights cultivate an environment of technical rigor and effortless navigation.

## Colors
The palette is rooted in an ultra-crisp, educational-grade spectrum engineered for legibility across structural topologies and administrative dashboards.

- **Primary (`#0B57D0`):** Acts as the foundational anchor for active network states, primary calls-to-action, navigation selection, and interactive topology nodes.
- **Secondary (`#1E8E3E`):** Represents verified states, successful handshakes, active interfaces, and completion signals.
- **Tertiary (`#D93025`):** Reserved for dropped packets, collision alerts, misconfigurations, and critical diagnostic stops.
- **Neutral (`#5F6368`):** Dictates secondary annotations, interface labels, structural grid borders, and non-active tooltips.

### Surface Architecture
- **Surface Canvas:** `#FFFFFF`
- **Surface Subdued / Workspace Well:** `#F8F9FA`
- **Surface Container / Inset Groups:** `#F1F3F4`
- **Text Primary:** `#202124`
- **Text Secondary:** `#3C4043`
- **Text Muted:** `#5F6368`
- **Border Subtle:** `#DADCE0`

## Typography
The system employs `Plus Jakarta Sans` for display and heading hierarchies, delivering a polished, modern, geometric clarity. For high-density utility views—including IP tables, routing prefixes, subnet calculations, and console panels—`Inter` delivers maximum character differentiation and legibility at small sizes.

Maintain strict adherence to tracking values: headings use slight negative letter spacing to preserve compactness, while utility labels under 12px utilize slight positive letter spacing for rapid scanning under classroom conditions.

## Layout & Spacing
The layout follows a fluid 12-column grid system built on an 8px base rhythm, contracting to 4 columns on mobile viewports (<600px) and 8 columns on tablet devices (600px - 1024px).

Panels and technical canvas regions utilize fixed sidebars (280px standard) paired with fluid workspace wells. Vertical rhythm must prioritize scannable blocks: interactive node settings use `space-md` gaps, while metadata arrays collapse to `space-xs` and `space-sm` for high-efficiency instruction.

## Elevation & Depth
Elevation mirrors modern suite layered surfaces, relying on ambient diffusion and tonal differentiation rather than prominent drop shadows.

- **Level 0 (Flat):** Surface `#FFFFFF` bordered with `#DADCE0` (1px solid). Used for default canvas nodes, inspection panels, and data tables.
- **Level 1 (Subtle Stack):** `0px 1px 2px rgba(60, 64, 67, 0.12), 0px 1px 3px 1px rgba(60, 64, 67, 0.08)`. Applied to interactive cards, modular tools, and top-level header bars.
- **Level 2 (Active/Hover):** `0px 2px 6px rgba(60, 64, 67, 0.15), 0px 1px 2px rgba(60, 64, 67, 0.3)`. Applied to active dragging topology elements, hovering exercise modules, and contextual menus.
- **Level 3 (Overlay / Modal):** `0px 8px 24px rgba(60, 64, 67, 0.2)`. Dedicated to IP configuration dialogs, sub-netting calculators, and laboratory assessment sheets.

## Shapes
Adhering to roundedness level `2`, the default radius for standard UI elements is `0.5rem` (8px). Medium surfaces and actionable controls leverage this standard, while container groups and structural modular cards scale up to `rounded-lg` (`1rem` / 16px) to maintain a soft, human-centered atmosphere across complex technical workflows.

## Components

### Buttons
- **Primary:** Solid `#0B57D0` fill with `#FFFFFF` text. Height of 36px (or 40px for prominent actions), 8px radius (`roundedness: 2`), `label-md` weight. Hover shifts to `#0842A0` without altering elevation.
- **Secondary / Tonal:** `#E8F0FE` background with `#0B57D0` text. Hover shifts to `#D2E3FC`.
- **Outlined:** Transparent background with 1px border `#DADCE0` and `#0B57D0` text. Hover transitions to `#F8F9FA`.

### Cards & Lab Modules
Cards feature `#FFFFFF` surfaces wrapped in a 1px `#DADCE0` border with a 16px radius (`rounded-lg`). For nested instructional steps, use `#F8F9FA` backgrounds with zero elevation and internal padding mapped to `space-lg`.

### Input Fields & Technical Configulators
Fields must maintain a default 40px height, `#FFFFFF` fill, 1px `#DADCE0` border, and 8px corner radius. Placeholder text takes `#5F6368`. Focused states display a crisp 2px border in `#0B57D0` without layout shift. Monospace fonts are permitted inside configuration fields for terminal emulation and CIDR subnet masking.

### Chips & Badges
Chips maintain a compact 24px to 32px height, 8px corner radius, and subtle status-matched styling:
- **Success Badge:** `#E6F4EA` fill, `#137333` text, optional 6px pulsing dot.
- **Error Badge:** `#FCE8E6` fill, `#C5221F` text.
- **Diagnostic / Protocol Tag:** `#F1F3F4` fill, `#3C4043` text.

### Checkboxes & Radio Controls
20px bounding box with an 8px radius for checkboxes (or circular for radios). Active fill uses `#0B57D0` displaying a white check icon or center dot. Inactive state uses a 1.5px `#5F6368` border with immediate response to pointer events.

### Specialized Components
- **Network Interface Ports:** Port representations on hardware units use 28px square buttons with 4px inner rounding, flanked by a dual-color status LED (green `#1E8E3E` / amber `#F9AB00`).
- **Terminal Console Drawer:** Collapsible bottom-docked viewport in `#202124` with light-contrast text (`#E8EAED`), contrasting against the light-themed educational dashboard.