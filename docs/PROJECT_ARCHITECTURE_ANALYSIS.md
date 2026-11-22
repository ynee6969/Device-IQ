# Project Architecture Analysis

## Overview
This repository is a Next.js 14 frontend-first application for a phone discovery and comparison product called `DeviceIQ`.
The frontend is built with React/Next.js, CSS modules, and a global styling foundation in `app/globals.css`.
The architecture separates:

- Application shell and shared chrome in `app/layout.tsx`
- Page routes in `app/` for public marketing, browsing, compare, authentication, and phone detail pages
- Reusable UI components in `components/`
- Shared styling foundation and page-level style scoping via CSS modules
- Client-side experience and stateful interaction in providers and dashboard components

## Folder Structure

```text
project-root/
│
├── app/
│   ├── layout.tsx
│   │   ├── Root application shell
│   │   ├── Loads global fonts and global CSS
│   │   ├── Wraps pages in BootstrapProvider, ThemeProvider, AppProviders
│   │   └── Renders persistent chrome: CursorAura, SiteHeader, <main>, SiteFooter, MobileTabBar, ThemeToggle
│   │
│   ├── globals.css
│   │   ├── Global token system and color variables
│   │   ├── Fluid typography, spacing, button styles, glass panels
│   │   ├── Main layout containers and utility classes
│   │   ├── Theme-aware CSS variables for dark/light palettes
│   │   └── Responsive utility classes, grid systems, input/button design
│   │
│   ├── page.tsx
│   ├── page.module.css
│   │   ├── Home landing page sections
│   │   ├── Story cards, feature cards, preview grid layout
│   │   └── Container queries and responsive grids
│   │
│   ├── about/page.tsx
│   ├── compare/page.tsx
│   ├── compare/page.module.css
│   ├── contact/page.tsx
│   ├── dashboard/page.tsx
│   ├── dashboard/loading.tsx
│   ├── dashboard/loading.module.css
│   ├── favorites/page.tsx
│   ├── favorites/page.module.css
│   ├── gallery/page.tsx
│   ├── login/page.tsx
│   ├── signup/page.tsx
│   ├── services/page.tsx
│   ├── services/page.module.css
│   ├── phones/[slug]/page.tsx
│   ├── phones/[slug]/page.module.css
│   ├── error.tsx
│
├── components/
│   ├── providers/
│   │   ├── app-providers.tsx
│   │   ├── bootstrap-provider.tsx
│   │   ├── theme-provider.tsx
│   │   └── favorites-provider.tsx
│   │
│   ├── marketing/
│   │   ├── brand-lockup.tsx
│   │   ├── BrandLockup.module.css
│   │   ├── cursor-aura.tsx
│   │   ├── hero-section.tsx
│   │   ├── HeroSection.module.css
│   │   ├── header-auth-controls.tsx
│   │   ├── HeaderAuthControls.module.css
│   │   ├── site-header.tsx
│   │   ├── SiteHeader.module.css
│   │   ├── site-footer.tsx
│   │   ├── SiteFooter.module.css
│   │   ├── theme-toggle.tsx
│   │   ├── ThemeToggle.module.css
│   │   ├── mobile-tabbar.tsx
│   │   └── MobileTabBar.module.css
│   │
│   ├── navigation/
│   │   ├── instant-nav-link.tsx
│   │   └── InstantNavLink.module.css
│   │
│   ├── auth/
│   │   ├── auth-form.tsx
│   │   ├── AuthForm.module.css
│   │   └── auth-config-notice.tsx
│   │
│   ├── dashboard/
│   │   ├── matchmaker-dashboard.tsx
│   │   └── MatchmakerDashboard.module.css
│   │
│   └── phones/
│       ├── device-card.tsx
│       ├── DeviceCard.module.css
│       ├── favorite-button.tsx
│       └── FavoriteButton.module.css
│
├── lib/
│   ├── site.ts
│   ├── utils/
│   │   ├── format.ts
│   │   ├── phone-presentation.ts
│   │   ├── phone-filters.ts
│   │   ├── normalization.ts
│   │   ├── cn.ts
│   ├── types/
│   │   ├── phone-card.ts
│   │   └── phone-reference.ts
│   ├── services/
│   │   ├── phones.ts
│   │   ├── favorites.ts
│   │   ├── comparison.ts
│   │   ├── comparison-history.ts
│   │   ├── gsmarena-reference.ts
│   │   ├── recommendations.ts
│   │   ├── scoring.ts
│   │   ├── cache.ts
│   │   ├── bootstrap.ts
│   └── auth/
│       ├── session.ts
│       ├── config.ts
│       └── validation.ts
│
├── public/
│   └── phone-images/...
├── prisma/
│   └── schema.prisma
└── next.config.mjs
```

## Root Application Shell

### `app/layout.tsx`
- The entry point for the frontend shell.
- Imports Google fonts via `next/font/google` and exposes them as CSS variables `--font-body` and `--font-display`.
- Loads global reset and design foundation from `app/globals.css`.
- Wraps every page in:
  - `BootstrapProvider` for app initialization and caching.
  - `ThemeProvider` for appearance state and CSS variable updates.
  - `AppProviders` for React context providers including `SessionProvider` and `FavoritesProvider`.
- Renders persistent UI chrome:
  - `CursorAura` for pointer-driven glow.
  - `SiteHeader` sticky desktop header.
  - `<main>{children}</main>` for page content.
  - `SiteFooter` global footer.
  - `MobileTabBar` fixed mobile navigation.
  - `ThemeToggle` floating theme modal launcher.
- Sets metadata using `site` values from `lib/site.ts`.

### `app/globals.css`
- The global style foundation for the entire app.
- Defines:
  - design tokens: `--bg`, `--surface`, `--accent`, `--text`, `--muted`, `--border`, `--shadow`, radius values
  - fluid typography and spacing via `clamp()`
  - global resets for `*, *::before, *::after`, anchor reset, button/input resets, image responsiveness
  - utility classes: `.container`, `.button`, `.pill`, `.chip`, `.stack`, `.field`, `.input`, `.textarea`
  - layout helpers: `.page-shell`, `.glass-panel`, `.section`, `.section-label`, `.section-title`, `.feature-title`
  - CSS grid systems: `.hero-grid`, `.marketing-grid`, `.phone-grid`, `.comparison-grid`, `.recommendation-grid`
  - dark/light theme mode tokens under `html[data-theme="dark"]` and `html[data-theme="light"]`
- Enables advanced UI patterns:
  - glass-morphism surfaces with `backdrop-filter`
  - hover and transition states for button/interactive controls
  - animation keyframes: `fadeInUp`, `slideInFromLeft`, `bounceIn`
  - responsive utility classes and container queries.

## Page and Route Architecture

### Home landing page
- `app/page.tsx`
  - Uses `HeroSection` for the above-the-fold experience.
  - Renders marketing sections using shared utilities and home-specific CSS classes.
  - Uses `page.module.css` to control:
    - story card grid
    - featured home feature layout
    - home preview card grid
    - responsive breakpoints and container query adaptations
  - imports curated data from `lib/data/seed-phones.ts`.

### Marketing and static pages
- `app/about/page.tsx`
  - Simple two-panel marketing layout with static content.

- `app/services/page.tsx`
  - Asymmetric 3-column feature layout.
  - Uses `services/page.module.css` for the featured compare hero and responsive service cards.

- `app/contact/page.tsx`
  - Two-column contact form and information layout.
  - Uses global form field styles and cards from the foundation.

- `app/gallery/page.tsx`
  - Redirect route to `/dashboard`.
  - Maintains backward compatibility for legacy navigation.

### Authentication pages
- `app/login/page.tsx` and `app/signup/page.tsx`
  - Both delegate UI to `components/auth/auth-form.tsx`.
  - Use `AuthForm` as a reusable login/signup shell.
  - Client-side form submission, validations, and NextAuth integration live in `AuthForm`.
  - Authentication config guard displayed by `AuthConfigNotice`.

### Browsing and product discovery
- `app/dashboard/page.tsx`
  - Fetches initial phone catalog with `listPhones`.
  - Uses `unstable_cache` and `revalidate = 120` for server-side caching.
  - Renders interactive client component `MatchmakerDashboard`.

- `components/dashboard/matchmaker-dashboard.tsx`
  - Core client-side browsing surface.
  - Maintains filter state in React and fetches `/api/phones` on change.
  - Supports mobile sheet filters and desktop sticky sidebar filters.
  - Uses `DeviceCard` to render each phone card, preserving visual consistency.

- `components/phones/device-card.tsx`
  - Responsible for the phone card presentation in dashboard and favorites.
  - Uses pointer-based hover tilt via CSS variables and `onPointerMove`.
  - Renders primary actions, marketplace links, favorite button, stat bars, and spec chips.

- `components/phones/favorite-button.tsx`
  - Encapsulates save/remove favorite behavior.
  - Reads current account favorites from `FavoritesProvider`.
  - Exposes optimistic UI state and pending request handling.

- `app/favorites/page.tsx`
  - Protected route requiring authenticated session.
  - Uses `listFavoritesByUserId` to fetch user-specific saved phones.
  - Renders `DeviceCard` list or empty state.

### Comparison lab and phone detail
- `app/compare/page.tsx`
  - Server route that builds comparison from query string parameters.
  - Uses `buildDetailedComparison`, `rememberComparisonSnapshot`, and recent history.
  - Renders a multi-stage comparison layout: selector, hero comparison card, highlights, scores, table sections.
  - Uses `compare/page.module.css` for table structure and responsive stacking.

- `app/phones/[slug]/page.tsx`
  - Dynamic phone detail route.
  - Fetches phone record and GSMArena reference specs via `unstable_cache` and `revalidate = 300`.
  - Renders hero media, key metrics, actions, and full spec table.
  - Uses `page.module.css` for detail layout and spec table responsiveness.

## Component Relationships and Flow

### Persistent UI relationship
- App shell in `app/layout.tsx` is the root of the render tree.
- Shared providers and chrome are placed outside page content.
- The route render tree follows:
  - `app/layout.tsx`
    - `BootstrapProvider` -> `ThemeProvider` -> `AppProviders`
      - `CursorAura`
      - `SiteHeader`
      - `<main>` -> page component
      - `SiteFooter`
      - `MobileTabBar`
      - `ThemeToggle`

### Route-level rendering
- `HomePage` renders `HeroSection` and static marketing sections.
- `ComparePage` renders server-side comparison data; if logged in, it also updates comparison history.
- `DashboardPage` passes initial phone data to `MatchmakerDashboard` for client-side interactivity.
- `PhoneDetailPage` renders a server-generated detail view with spec sections and action buttons.

### Data and interaction flow (frontend only)
- `ThemeProvider` sets `html[data-theme]`, CSS variables, and exposes palette state.
- `MobileTabBar` and `SiteHeader` use `usePathname()` to determine active route for highlighting.
- `FavoritesProvider` fetches `/api/favorites` and supplies `useFavorites()` to `FavoriteButton` and header auth.
- `MatchmakerDashboard` uses browser fetch to `/api/phones` on filter changes and merges results.
- `FavoriteButton` triggers POST/DELETE to `/api/favorites` and updates provider state optimistically.
- `AuthForm` uses `fetch("/api/auth/signup")` and `signIn("credentials")`, then polls `/api/auth/session`.

## Styling and Layout Systems

### Global styling architecture
- `app/globals.css` is the foundation of the style system.
- It defines:
  - token-based color and spacing system
  - responsive typography via `clamp()`
  - global layout helpers for sections, containers, cards, buttons, inputs
  - theme-aware CSS variables and light/dark mode state
- Utility classes are reused across pages and component CSS modules.

### Component styling architecture
- CSS modules are used for page and component-scoped styles.
- Each component file imports a module with `.scope` or targeted `.scope :global(...)` selectors.
- Example:
  - `HeroSection.module.css` scopes hero-specific layout while reusing global `.glass-panel`, `.section-copy`, `.button`.
  - `MatchmakerDashboard.module.css` scopes dashboard layout and mobile sheet behavior.
  - `DeviceCard.module.css` defines card-specific hover tilt, glow, and stat bar styling.

### Layout hierarchy
- The app uses a combination of CSS Grid and Flexbox.
- Primary layout patterns:
  - 2-column hero layouts in home, dashboard, and detail pages
  - 3-column feature grid on services page
  - responsive stacking via `@media` and `@container` queries
  - fixed bottom mobile tab bar for phone viewports

### Responsive systems
- The codebase uses explicit breakpoints at:
  - `1024px` for laptop/tablet transitions
  - `768px` for tablet/mobile stack-down
  - `560px` for compact phones
- Additionally, `container-type: inline-size` and `@container` queries appear in home and card styles.
- Fluid spacing and typography via `clamp()` reduce the need for many media queries.

## File Responsibility Map

| Feature | Main File | Related CSS | Purpose |
| --- | --- | --- | --- |
| Root shell | `app/layout.tsx` | `app/globals.css` | Application wrapper, global providers, persistent chrome, metadata |
| Global styles | `app/globals.css` | N/A | Theme tokens, typography, spacing, card/panel utilities, responsive utilities |
| Home landing page | `app/page.tsx` | `app/page.module.css` | Marketing landing page, hero story, feature cards, preview grid |
| Hero section | `components/marketing/hero-section.tsx` | `components/marketing/HeroSection.module.css` | Landing hero UX, CTA actions, animated metric cards |
| Header | `components/marketing/site-header.tsx` | `components/marketing/SiteHeader.module.css` | Sticky top navigation, route highlights, desktop nav layout |
| Footer | `components/marketing/site-footer.tsx` | `components/marketing/SiteFooter.module.css` | Global footer branding and note text |
| Brand lockup | `components/marketing/brand-lockup.tsx` | `components/marketing/BrandLockup.module.css` | Logo mark and brand text unit |
| Mobile navigation | `components/marketing/mobile-tabbar.tsx` | `components/marketing/MobileTabBar.module.css` | Fixed bottom tab bar on phones |
| Theme settings | `components/marketing/theme-toggle.tsx` | `components/marketing/ThemeToggle.module.css` | Theme launcher, modal, palette selection |
| Auth forms | `components/auth/auth-form.tsx` | `components/auth/AuthForm.module.css` | Login/signup form and session polling |
| Auth notice | `components/auth/auth-config-notice.tsx` | `components/auth/AuthForm.module.css` | Auth configuration fallback message |
| Dashboard browser | `components/dashboard/matchmaker-dashboard.tsx` | `components/dashboard/MatchmakerDashboard.module.css` | Client-side browse surface, filters, phone grid |
| Dashboard loading state | `app/dashboard/loading.tsx` | `app/dashboard/loading.module.css` | Skeleton page while dashboard content loads |
| Phone card | `components/phones/device-card.tsx` | `components/phones/DeviceCard.module.css` | Individual phone presentation, action buttons, market links |
| Favorite button | `components/phones/favorite-button.tsx` | `components/phones/FavoriteButton.module.css` | Favorite toggle UI and state management |
| Compare lab | `app/compare/page.tsx` | `app/compare/page.module.css` | Phone comparison page with selectors, score table, responsive layout |
| Phone detail | `app/phones/[slug]/page.tsx` | `app/phones/[slug]/page.module.css` | Phone specs page, hero summary, detailed table |
| Static marketing | `app/about/page.tsx` | N/A | Mission and core principles page |
| Feature overview | `app/services/page.tsx` | `app/services/page.module.css` | Tool and feature showcase page |
| Contact | `app/contact/page.tsx` | N/A | Contact and feedback form page |

## Component Import Graph

- `app/layout.tsx`
  - `CursorAura`
  - `SiteHeader`
    - `BrandLockup`
    - `HeaderAuthControls`
      - `useFavorites()` from `FavoritesProvider`
  - `ThemeToggle`
    - `useThemeValue()` from `ThemeProvider`
  - `MobileTabBar`
    - `InstantNavLink`
  - `SiteFooter`

- `app/page.tsx`
  - `HeroSection`

- `app/dashboard/page.tsx`
  - `MatchmakerDashboard`
    - `DeviceCard`
      - `FavoriteButton`
    - `DashboardFilters`
    - `MobileSheet`

- `app/compare/page.tsx`
  - `Link`

- `app/phones/[slug]/page.tsx`
  - `FavoriteButton`
  - `Link`

- `app/login/page.tsx` and `app/signup/page.tsx`
  - `AuthForm`
  - `AuthConfigNotice`

## HTML Structure Summary

### Persistent app structure
- `<html lang="en" suppressHydrationWarning>`
- `<body className="site-shell ...">`
- `<CursorAura />` renders a non-interactive glow element
- `<header className="site-header ...">` sticky top navigation
- `<main>` page route content
- `<footer>` site footer
- `<nav className="mobile-tabbar ...">` mobile bottom navigation
- Theme launcher and modal are rendered at the root shell level

### Page structure conventions
- All pages use a top-level `<section className="section">` for consistent vertical rhythm.
- `.page-shell` is the inner horizontal padding container for content width control.
- `glass-panel` is the reusable surface wrapper for cards and panels.
- Many route UIs use nested `<div className="stack">` / `<div className="button-row">` to build vertical/horizontal spacing.
- Reusable semantic elements:
  - `<article>` for cards and phone tiles
  - `<nav>` for navigation sections
  - `<form>` for auth and compare selector pages
  - `<section>` for spec groups and page sections

## Styling Inheritance and Cascade

- Global CSS variables in `app/globals.css` are the source of truth.
- Theme provider mutates document root CSS custom properties, which cascade into all components.
- Shared classes like `.glass-panel`, `.button`, `.section`, `.stack`, `.field` are defined globally and reused in module-scoped markup.
- CSS modules use `:global(...)` when they need to style shared structural classes across pages and components.
- Scoped modules keep route-specific layout details near the view logic while still inheriting global tokens.

## Key Architecture Observations

- **Layered styling**: `app/globals.css` for foundation, CSS modules for page/component-specific layout.
- **Modular page design**: Each route is self-contained, with either no module or a local module for layout details.
- **Responsive-first approach**: Most components scale with `clamp()`, `auto-fit`, `repeat(minmax)` and media queries.
- **Data-driven client interactivity**: The dashboard is the primary interactive client-side surface; the rest of the app is largely server-rendered marketing and detail pages.
- **Provider-backed state**: `ThemeProvider` and `FavoritesProvider` are centralized, making UI state available to cross-cutting components.
- **Accessibility attention**: `aria-hidden`, `role="dialog"`, focus-visible styles, and proper semantic wrappers are present.
