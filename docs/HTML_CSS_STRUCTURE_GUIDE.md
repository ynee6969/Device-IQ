# HTML and CSS Structure Guide

## How the Frontend Works

### Application structure
- `app/layout.tsx` is the global root for every route.
- It defines the overall HTML shell and wraps all content in providers and persistent UI components.
- Each route file inside `app/` renders one page section inside `<main>`.
- The top-level shell includes both desktop and mobile navigation, a footer, and a theme launcher.
- The app mixes server-rendered pages with client-side interactive components.

### Hierarchy of rendering
- The root shell is rendered first.
- Then the route component renders under `<main>`.
- Shared components are imported from `components/marketing` and `components/phones`.
- Page-specific styles are handled through CSS modules.
- Global design tokens and utilities in `app/globals.css` provide the base styling.

## How HTML Connects to CSS

### Global foundation
- `app/globals.css` declares core CSS variables and global element rules.
- All pages and components inherit the theme variables from the `<html>` root.
- Shared classes such as `.section`, `.glass-panel`, `.button`, `.chip`, and `.input` are defined once and reused.
- Component markup uses these global classes for consistent spacing and visual rhythm.

### Scoped component styling
- CSS modules are imported next to their component file.
- Example: `components/phones/DeviceCard.tsx` imports `DeviceCard.module.css`.
- The module typically exports `.scope` to wrap a component root and keep local layout rules isolated.
- Inside the module, `:global(...)` is used when styling shared classes from the global foundation.

### Theme and token flow
- `ThemeProvider` manages theme mode and palette selection.
- It writes CSS variables to `document.documentElement` and sets `html[data-theme]`.
- Global CSS uses those variables and defines alternate values for light/dark modes.
- This means color, surface, and accent styles are inherited consistently across the page.

## Layout Control

### Main containers
- `.page-shell` is the primary inner wrapper for horizontal padding.
- `.section` defines vertical spacing for page blocks.
- `.glass-panel` is the reusable card surface giving the glassmorphism look.
- `.stack` and `.button-row` are used to create vertical or horizontal spacing patterns.

### Grids and cards
- The app relies on CSS Grid for the majority of page layouts.
- Example grids:
  - `.hero-grid` for the landing hero section.
  - `.services-grid` for the feature showcase.
  - `.compare-table` for side-by-side spec comparison.
  - `.phone-grid` for dashboard and favorites lists.
- `DeviceCard.module.css` uses grid for internal card layout and also uses `container-type` to adapt to card width.

### Responsive layout
- The project uses both media queries and container queries.
- Breakpoints exist at 1024px, 768px, and 560px.
- `clamp()` is used extensively for font size, spacing, and padding.
- Grid layouts typically move from multiple columns to a single column on smaller screens.
- Mobile-only elements such as `MobileTabBar` appear through CSS module `@media (max-width: 768px)`.

## Reusable Component Structure

### Persistent marketing chrome
- `SiteHeader` contains the brand and desktop links.
- `MobileTabBar` contains mobile primary navigation.
- `ThemeToggle` handles the floating theme launcher and modal.
- `SiteFooter` closes the page with branded summary content.

### Reusable UI primitives
- `BrandLockup` delivers a logo mark + brand text block.
- `HeroSection` encapsulates the landing hero layout and metric cards.
- `FavoriteButton` encapsulates save/remove state and visual styling.
- `DeviceCard` is the reusable phone preview card used in dashboard and favorites.
- `AuthForm` is the shared login/signup form.

### Shared form and interactive patterns
- Inputs use `.input`, `.select`, `.textarea`, and `.field`.
- Buttons use `.button`, `.button-secondary`, `.button-ghost`.
- Interactive states include `:hover`, `:focus-visible`, and transition easing.
- Wide form sections and skeleton states use the same glass-panel surface.

## Styling Inheritance

### Token inheritance
- Root custom properties are inherited by every child element.
- Example: `.glass-panel` uses `var(--surface)` and `var(--border)`.
- When theme mode changes, those variables update and all components refresh automatically.

### Class inheritance
- Global utility classes are layered first.
- Page modules extend or override global defaults with more specific layout rules.
- Example: `.button` is global but `.phone-card-actions .button-secondary` is module-specific.

### Specificity strategy
- The style system stays simple with few nested selectors.
- CSS modules isolate route-specific styles, preventing cross-page collisions.
- Shared global classes define low-specificity foundational style.
- Module rules use `:global()` only to adjust shared utility classes in their local context.

## Responsive Systems

### Fluid typography
- `app/globals.css` defines text sizes using `clamp()`.
- This allows text to scale smoothly between viewport sizes without explicit breakpoints.

### Adaptive grids
- `.hero-grid` uses a combination of `minmax()` and fixed minimum widths.
- `.service-preview-compare` and `.compare-table` adjust columns based on screen width.
- `.phone-grid` and `.dashboard-grid` use repeat patterns for responsive card layouts.

### Mobile-specific behaviors
- `SiteHeader.module.css` hides desktop nav for smaller screens.
- `MobileTabBar.module.css` only displays on mobile and is hidden on larger breakpoints.
- `MatchmakerDashboard` includes a mobile filter sheet overlay instead of a desktop sidebar.

## Why the structure is organized this way

### Separation of concerns
- `app/` defines routes and top-level rendering logic.
- `components/` contains reusable, visually consistent UI blocks.
- Styles are split between global foundation and local modules.
- This gives each page the ability to share core design tokens while preserving route-specific layout.

### Maintainability
- Global classes are intentionally minimal and composable.
- Page modules scope only what is necessary for that route.
- Provider components centralize theme and favorite state so multiple UI elements can consume them.

### Performance
- `ThemeProvider` writes only the required CSS variables, reducing style recalculation.
- `DeviceCard` uses `contain-intrinsic-size` and `content-visibility` for card performance.
- `DashboardPage` hydrates only the interactive dashboard after server render.

## Practical guide for contributors

### To add a new page
1. Add `app/<route>/page.tsx`.
2. Wrap content in `section.section` and `div.page-shell`.
3. Use `glass-panel` for card surfaces.
4. Reuse global classes before creating new ones.
5. If necessary, add a CSS module for route-specific layout.

### To add a new reusable component
1. Create `components/<area>/<component>.tsx`.
2. Add a CSS module with `.scope` around the component root.
3. Use global utilities and tokens from `app/globals.css`.
4. Keep component markup semantic: `article`, `nav`, `section`, `form`.

### To add responsive behavior
- Prefer `clamp()` and `repeat(auto-fit, minmax())`.
- Use CSS modules and `@media` when layout shifts are required.
- Use `container-type` and `@container` only when the component needs to adapt to its container width.

## Summary
The frontend is a modern Next.js architecture that balances global design tokens and utilities with component-scoped layout. HTML structure is semantic and modular, CSS architecture is token-driven and responsive, and the component flow is rooted in the root shell plus targeted route-level rendering. This produces an enterprise-level UI system that is predictable, theme-aware, and easy to reason about.
