# Frontend Workflow Diagrams

## 1. Folder Structure Diagram

```text
project-root/
├── app/
│   ├── layout.tsx
│   ├── globals.css
│   ├── page.tsx
│   ├── about/page.tsx
│   ├── compare/page.tsx
│   ├── contact/page.tsx
│   ├── dashboard/page.tsx
│   ├── dashboard/loading.tsx
│   ├── favorites/page.tsx
│   ├── gallery/page.tsx
│   ├── login/page.tsx
│   ├── signup/page.tsx
│   ├── services/page.tsx
│   └── phones/[slug]/page.tsx
├── components/
│   ├── providers/
│   ├── marketing/
│   ├── navigation/
│   ├── auth/
│   ├── dashboard/
│   └── phones/
├── lib/
│   ├── utils/
│   ├── services/
│   ├── auth/
│   └── types/
└── public/
```

## 2. Frontend Component Flow Diagram

```text
app/layout.tsx
  ↓ wraps
ThemeProvider → sets html[data-theme] and CSS variables
  ↓ wraps
AppProviders → SessionProvider + FavoritesProvider
  ↓ renders
SiteHeader ────────────────────────────┐
  ↓                                 │
main → route page component           │
  ↓                                 │
SiteFooter                            │
  ↓                                 │
MobileTabBar                          │
  ↓                                 │
ThemeToggle                           │
  ↓                                 │
CursorAura                            │
```

### Route-specific component flow

```text
Home page
  app/page.tsx
    ↓ imports
  HeroSection
    ↓ imports
  InstantNavLink

Dashboard page
  app/dashboard/page.tsx
    ↓ renders
  MatchmakerDashboard
    ↓ renders
  DeviceCard ─── FavoriteButton
    ↓ reads
  FavoritesProvider

Compare page
  app/compare/page.tsx
    ↓ server logic
  buildDetailedComparison
    ↓ renders
  compare cards, compare table

Phone detail page
  app/phones/[slug]/page.tsx
    ↓ renders
  FavoriteButton
    ↓ reads
  FavoritesProvider
```

## 3. HTML Layout Hierarchy Diagram

```text
<html lang="en">
  <body class="site-shell ...">
    <div class="cursor-aura" aria-hidden="true" />
    <header class="site-header">
      <div class="header-inner">
        <BrandLockup />
        <nav class="nav-row desktop-nav"> ... </nav>
        <div class="header-actions"> ... </div>
      </div>
    </header>

    <main>
      <section class="section">
        <div class="page-shell">
          <div class="glass-panel"> ... </div>
        </div>
      </section>
    </main>

    <footer class="footer">
      <div class="inner"> ... </div>
    </footer>
    <nav class="mobile-tabbar"> ... </nav>
    <button class="theme-launcher"> ... </button>
  </body>
</html>
```

## 4. CSS Styling Flow Diagram

```text
app/globals.css
  ↓ defines
  - tokens: colors, space, radius, shadows
  - layout helpers: .page-shell, .section, .glass-panel
  - interactive utilities: .button, .pill, .chip
  - typography: .section-title, .feature-title
  - responsive grid systems: .hero-grid, .phone-grid

Component CSS modules
  ↓ scope
  - HeroSection.module.css: hero presentation and preview grid
  - SiteHeader.module.css: sticky header + desktop nav
  - MatchmakerDashboard.module.css: sidebar + content grid + mobile sheet
  - DeviceCard.module.css: interactive card tilt + stat bars
  - compare/page.module.css: comparison table and mobile stacking
  - phones/[slug]/page.module.css: spec layout and details page

ThemeProvider
  ↓ updates
  html[data-theme] tokens
  ↓ cascades into
  app/globals.css + all CSS modules
```

## 5. Responsive Design Workflow

```text
Base design in globals.css
  ↓ uses clamp() for typography and spacing
  ↓ uses CSS Grid and flex containers

Component rules add breakpoints:
  - 1024px: collapse dashboard sidebar and adjust card sizing
  - 768px: stack multi-column layouts to single columns
  - 560px: compact mobile padding and hide desktop nav

Home page uses container queries:
  .story-strip, .home-feature-layout, .home-preview-grid
  ↓ adapt to available container width

Dashboard uses mobile sheet:
  button opens <MobileSheet>
  ↓ sheetOverlay + sheetPanel handle touch layout
```

## 6. Page Rendering Workflow

```text
User requests route
  ↓ resolved by Next.js route in app/
  ↓ app/layout.tsx builds root wrapper
  ↓ if route is server-rendered, gather data first
    - /dashboard: getDashboardCatalog → listPhones
    - /compare: buildDetailedComparison → services/comparison
    - /phones/[slug]: getPhoneDetail → getPhoneBySlugWithPreviewSource + getPhoneReferenceBySlug
  ↓ render route page markup
  ↓ client hydration
    - Dashboard page hydrates MatchmakerDashboard
    - Auth pages hydrate AuthForm
    - SiteHeader hydrates auth and route highlighting
  ↓ theme and favorite providers hydrate
  ↓ interactive components (favorite toggles, filters, modal launcher) become active
```
