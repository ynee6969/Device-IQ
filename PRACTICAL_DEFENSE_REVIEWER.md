# PRACTICAL DEFENSE REVIEWER

## 1. FULL PROJECT OVERVIEW

### How the website works
- This project is a **Next.js 15** app using the **App Router**. Pages live under `app/` and are built as React components in `.tsx` files.
- The website is not plain HTML files. Instead, it uses **React + Next.js** to generate HTML from component code.
- The main page is `app/page.tsx`. The page imports reusable components such as `HeroSection` from `components/marketing/hero-section.tsx`.
- The app shell is defined in `app/layout.tsx`. This file wraps everything in the header, footer, theme provider, and mobile controls.
- Styling is done by a combination of:
  - `app/globals.css` for shared tokens, layout utilities, and global rules.
  - CSS modules like `components/marketing/SiteHeader.module.css` for component-specific styling.
  - Page-specific modules like `app/page.module.css` and `app/compare/page.module.css`.

### How the files connect together
- `app/layout.tsx` imports `./globals.css` and loads the two fonts used across the site.
- `app/layout.tsx` renders:
  - `CursorAura` (visual effect)
  - `SiteHeader` (top navigation)
  - `main` (content of each page)
  - `SiteFooter`
  - `MobileTabBar`
  - `ThemeToggle`
- Every page file under `app/` becomes a route:
  - `/` → `app/page.tsx`
  - `/about` → `app/about/page.tsx`
  - `/services` → `app/services/page.tsx`
  - `/compare` → `app/compare/page.tsx`
  - `/dashboard` → `app/dashboard/page.tsx`
  - `/favorites` → `app/favorites/page.tsx`
  - `/contact` → `app/contact/page.tsx`
  - `/login`, `/signup` and dynamic `/phones/[slug]` also exist.
- Components use **next/link** and **next/navigation** for navigation.
- The `components/marketing/hero-section.tsx` is the main hero content on the home page.
- CSS module files are imported as `styles from './Something.module.css'` and used as `className={styles.scope}` or `className={styles.header}`.

### Where the styles come from
- `app/globals.css` contains the shared design tokens and utilities:
  - colors: `--bg`, `--surface`, `--accent`, `--text`, `--muted`
  - spacing: `--space-1` through `--space-6`
  - typography sizes: `--text-xs` through `--text-4xl`
  - reusable classes: `.button`, `.button-secondary`, `.button-ghost`, `.glass-panel`, `.section`, `.section-title`, `.page-shell`
- Component CSS modules contain the layout and look for one component only.
  - Example: `components/marketing/SiteHeader.module.css` styles the header and desktop nav.
- Page module CSS files add page-specific layout details.
  - Example: `app/page.module.css` styles home-specific grids.

### How HTML connects to CSS
- In React, `HTML` is created with JSX inside `.tsx` files.
- Classes are set with `className="..."`.
- Reusable global classes like `section`, `glass-panel`, `button` are applied as plain strings.
- CSS module classes are applied using the imported `styles` object, for example:
  - `className={styles.header}`
  - This ensures the style only applies to that component.
- Some component CSS modules use `:global(...)` to style plain class names from JSX.
  - Example: `SiteHeader.module.css` contains `.header :global(.nav-link)` so the `.nav-link` class inside that component gets styled.

### How components are structured
- `app/layout.tsx` is the root wrapper.
- `components/marketing/` contains the top-level UI sections:
  - `site-header.tsx`
  - `hero-section.tsx`
  - `site-footer.tsx`
  - `mobile-tabbar.tsx`
  - `theme-toggle.tsx`
  - `brand-lockup.tsx`
- `components/navigation/instant-nav-link.tsx` is a navigation helper used by buttons to prefetch.
- `components/auth/` contains the login/signup form logic.
- `components/phones/` contains the phone card UI and favorite button.
- Pages import these components as building blocks.

### How responsive behavior works
- The app uses a mix of:
  - **CSS media queries** such as `@media (max-width: 768px)` and `@media (max-width: 480px)`.
  - **CSS container queries** such as `@container (max-width: 768px)` inside component modules.
  - **Grid and flexbox** to rearrange items at different breakpoints.
- Examples:
  - `SiteHeader.module.css` hides desktop nav on mobile and shows mobile auth controls instead.
  - `MobileTabBar.module.css` only shows the bottom mobile navigation for screens under `768px`.
  - `app/page.module.css` uses `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr))` to wrap cards.
- The page shell class `page-shell` provides horizontal padding that adjusts with `clamp()`.

## 2. FILE MAP / EDITING GUIDE

| Website Part | File To Edit | What To Change | Risk Level | Notes |
|---|---|---|---|---|
| Root layout / app shell | `app/layout.tsx` | Add or remove site-wide elements, change header/footer order | High | This file wraps the whole app. Keep edits minimal. |
| Global colors & spacing | `app/globals.css` | Change `--accent`, `--bg`, `--text`, `--space-*` | High | Affects the whole site. Best for theme changes. |
| Navbar container | `components/marketing/site-header.tsx` | Add/remove nav links, change link text | Medium | The header JSX defines nav items. |
| Navbar styles | `components/marketing/SiteHeader.module.css` | Change nav link hover, sticky background | Medium | Controls desktop navigation styling. |
| Hero section layout | `components/marketing/hero-section.tsx` | Change hero heading, buttons, cards | Medium | Primary homepage content. |
| Hero section styles | `components/marketing/HeroSection.module.css` | Adjust hero grid, card backgrounds | Medium | Controls hero responsiveness and hover styles. |
| Homepage sections | `app/page.tsx` | Change home landing content, feature cards | Medium | Edits the home page story. |
| Homepage styles | `app/page.module.css` | Adjust story grid, preview cards | Medium | Controls home-specific page layout. |
| Buttons | `app/globals.css` | Edit `.button`, `.button-secondary`, `.button-ghost` | High | Shared button system used everywhere. |
| Cards / glass panels | `app/globals.css` | Edit `.glass-panel` and its background | High | Affects many content cards globally. |
| Section headings | `app/globals.css` | Edit `.section-title`, `.feature-title` | High | Shared typography for headings. |
| Section layout | `app/globals.css` | Edit `.section`, `.page-shell` | High | Controls vertical spacing and page width. |
| Footer content | `components/marketing/site-footer.tsx` | Edit footer text / brand note | Low | Small area, safe. |
| Footer styles | `components/marketing/SiteFooter.module.css` | Adjust footer alignment, padding | Low | Simple footer-only styles. |
| Mobile bottom nav | `components/marketing/mobile-tabbar.tsx` | Change mobile tab labels/icons | Medium | Only affects mobile screens. |
| Mobile tab styling | `components/marketing/MobileTabBar.module.css` | Change tabbar position, colors | Medium | Controls mobile bottom nav look. |
| Brand logo | `components/marketing/brand-lockup.tsx` | Change site brand text | Low | Branding component used in header/footer. |
| Brand styles | `components/marketing/BrandLockup.module.css` | Adjust logo size and text scale | Low | Simple logo appearance. |
| Auth button area | `components/marketing/header-auth-controls.tsx` | Change login/signup buttons | Medium | Affects header authentication area. |
| Auth mobile sheet | `components/marketing/HeaderAuthControls.module.css` | Adjust mobile overlay | Medium | Strictly mobile auth sheet styling. |
| Theme launcher | `components/marketing/theme-toggle.tsx` | Change theme modal labels | Low | UI chrome for theme settings. |
| Theme styles | `components/marketing/ThemeToggle.module.css` | Edit theme modal layout or launcher | Medium | Complex modal styles. |
| About page content | `app/about/page.tsx` | Change mission statement or list items | Low | Static informational page. |
| Services page | `app/services/page.tsx` | Change tools section content | Low | Service page is page-specific. |
| Compare page layout | `app/compare/page.tsx` | Change comparison card markup | Medium | Complex page with performance layout. |
| Compare page styles | `app/compare/page.module.css` | Edit compare grid and pills | Medium | Controls compare-specific UI. |
| Favorites page | `app/favorites/page.tsx` | Change favorites messaging | Low | Page-specific content only. |
| Dashboard page | `app/dashboard/page.tsx` | Change catalog filters / CTA | Medium | Main app route. |
| Phone detail page | `app/phones/[slug]/page.tsx` | Edit phone detail layout | Medium | Dynamic page with many details. |
| Phone detail styles | `app/phones/[slug]/page.module.css` | Adjust detail action buttons | Medium | Specific to dynamic phone page. |
| Global utilities | `app/globals.css` | Edit `.focus-visible`, `.sr-only`, `.container`, `.animate-...` | Medium | Useful for accessibility / transitions. |
| Common icon buttons | `app/globals.css` | Edit `.chip`, `.pill`, `.theme-toggle` | Medium | Used across many cards and panels. |

### Notes on where to edit
- If you need to change **text**, start in the page `.tsx` file, not CSS.
- If you need to change **size, color, spacing, hover, or layout**, edit CSS.
- If you need to change a **shared look** used on many pages, edit `app/globals.css`.
- If you need to change a **single component**, edit that component's module CSS.

## 3. 50 POSSIBLE PRACTICAL QUESTIONS

Below are 50 real practical teacher-style questions, each with the exact files and classes used in this project.

### Question 1
Change the navbar background color.

#### What This Means
The teacher wants the top header strip to use a different background.

#### Files You Need To Open
- `components/marketing/SiteHeader.module.css`

#### Why These Files
The header background is defined inside the header component CSS.

#### Step-by-Step Instructions
1. Open `components/marketing/SiteHeader.module.css`.
2. Find the `.header` rule near the top.
3. Locate `background: color-mix(in srgb, var(--bg) 88%, transparent);`.
4. Replace it with a new color, for example `background: rgba(10, 20, 25, 0.95);`.
5. Save the file.
6. Refresh the browser.

#### Code Before
```css
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: color-mix(in srgb, var(--bg) 88%, transparent);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border);
}
```

#### Code After
```css
.header {
  position: sticky;
  top: 0;
  z-index: 50;
  background: rgba(10, 20, 25, 0.95);
  backdrop-filter: blur(14px);
  border-bottom: 1px solid var(--border);
}
```

#### What Changed
The header color becomes the new dark overlay instead of the transparent glass effect.

#### Common Mistakes
- Editing the wrong file such as `app/globals.css` instead of `SiteHeader.module.css`.
- Using a fully transparent color and making the header invisible.

#### Extra Notes
If you want a color that matches the accent system, use `background: rgba(var(--accent-rgb), 0.2);`.

### Question 2
Make the hero text bigger.

#### What This Means
The big heading inside the home page hero should use a larger font size.

#### Files You Need To Open
- `components/marketing/hero-section.tsx`
- `components/marketing/HeroSection.module.css`

#### Why These Files
The hero heading is defined in the component markup and styled in the hero CSS module.

#### Step-by-Step Instructions
1. Open `components/marketing/HeroSection.module.css`.
2. Search for `.scope :global(.hero-copy-stack)` or `.section-title` if the title uses that class.
3. If the hero `h1` uses `.section-title`, increase the shared typography in `app/globals.css` or add a specific rule in the hero module.
4. Better: add a new rule in `HeroSection.module.css` for the hero title, such as:
```css
.scope :global(.section-title) {
  font-size: clamp(2.8rem, 6vw, 5rem);
}
```
5. Save and refresh.

#### Code Before
```css
.section-title {
  margin: 18px 0 14px;
  font-family: var(--font-display), sans-serif;
  font-size: clamp(2.4rem, 5vw, 4.5rem);
  line-height: 0.95;
  letter-spacing: -0.05em;
}
```

#### Code After
```css
.section-title {
  margin: 18px 0 14px;
  font-family: var(--font-display), sans-serif;
  font-size: clamp(2.8rem, 6vw, 5rem);
  line-height: 0.95;
  letter-spacing: -0.05em;
}
```

#### What Changed
The hero heading becomes taller and easier to read at larger screen widths.

#### Common Mistakes
- Changing only the desktop size but not mobile. Use `clamp()` or a media query.
- Editing the JSX text instead of the CSS size.

#### Extra Notes
If you need a hero-only size, add a new class in the hero module instead of changing the shared `.section-title`.

### Question 3
Add spacing between cards.

#### What This Means
The teacher wants more gap between card components on a grid.

#### Files You Need To Open
- `app/page.module.css`
- `components/marketing/HeroSection.module.css` or the specific page CSS if cards are on another page.

#### Why These Files
The gap between cards is controlled by the grid `gap` property.

#### Step-by-Step Instructions
1. Open `app/page.module.css` if the cards are on the homepage.
2. Look for `.page :global(.story-strip)` or `.page :global(.home-preview-grid)`.
3. Increase `gap: 20px;` to `gap: 30px;` or `gap: 2.5rem;`.
4. Save.
5. Refresh.

#### Code Before
```css
.page :global(.home-preview-grid) {
  margin-top: var(--space-6);
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: var(--space-4);
}
```

#### Code After
```css
.page :global(.home-preview-grid) {
  margin-top: var(--space-6);
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 32px;
}
```

#### What Changed
Cards move farther apart, reducing visual clutter.

#### Common Mistakes
- Changing `padding` instead of `gap`; padding adds space inside cards, not between them.
- Editing the wrong grid selector.

#### Extra Notes
`gap` is the right property for grid and flex spacing between items.

### Question 4
Align buttons horizontally.

#### What This Means
The buttons in a section should sit side by side instead of stacked.

#### Files You Need To Open
- `app/globals.css`
- `components/marketing/hero-section.tsx` or page-specific JSX if the buttons are on that page.

#### Why These Files
Button layout is managed by row containers like `.button-row`.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find `.button-row`.
3. Ensure it has `display: flex; flex-wrap: wrap; gap: 12px;`.
4. If buttons are stacking on mobile, add `flex-wrap: nowrap;` in the parent component or add a desktop-only rule.
5. Save.

#### Code Before
```css
.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}
```

#### Code After
```css
.button-row {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  align-items: center;
}
```

#### What Changed
Buttons align on a single horizontal row when space allows.

#### Common Mistakes
- Setting `display: block` on buttons instead of the container.
- Forgetting `flex-wrap` if there are many buttons.

#### Extra Notes
On mobile, a row may still wrap naturally. Use `.button-row-stack` for full-width stacked buttons.

### Question 5
Make images responsive.

#### What This Means
Ensure images change size on smaller screens without overflow.

#### Files You Need To Open
- `app/globals.css`
- Any page or component file with `<img>` markup.

#### Why These Files
`app/globals.css` already has general responsive image rules.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find the `img` rule.
3. Confirm it has `display: block; max-width: 100%;`.
4. If not, add it.
5. Save and refresh.

#### Code Before
```css
img {
  display: block;
  max-width: 100%;
}
```

#### Code After
```css
img {
  display: block;
  max-width: 100%;
  height: auto;
}
```

#### What Changed
Images shrink gracefully within their containers.

#### Common Mistakes
- Leaving `height` fixed in JSX or CSS.
- Using a parent container with fixed width smaller than the image.

#### Extra Notes
If the page uses `next/image`, the same rule still works for the generated `img` element.

### Question 6
Center the footer text.

#### What This Means
Footer text should be horizontally centered on the page.

#### Files You Need To Open
- `components/marketing/SiteFooter.module.css`

#### Why These Files
The footer layout is defined there.

#### Step-by-Step Instructions
1. Open `components/marketing/SiteFooter.module.css`.
2. Find the `.inner` rule.
3. Add `text-align: center; justify-content: center;`.
4. Save.

#### Code Before
```css
.inner {
  width: 100%;
  margin: 0 auto;
  padding-inline: clamp(16px, 3vw, 36px);
  padding-block: 16px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}
```

#### Code After
```css
.inner {
  width: 100%;
  margin: 0 auto;
  padding-inline: clamp(16px, 3vw, 36px);
  padding-block: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  gap: 18px;
}
```

#### What Changed
Footer content is centered horizontally; note that if there are multiple items, they will sit next to each other.

#### Common Mistakes
- Forgetting `justify-content`.
- Adding `align-items` only.

#### Extra Notes
For a single column on mobile, add a `@media` rule to change to `flex-direction: column;`.

### Question 7
Change hover color.

#### What This Means
Alter the hover effect for buttons or links.

#### Files You Need To Open
- `app/globals.css`
- `components/marketing/SiteHeader.module.css` if the hover is for nav.

#### Why These Files
Button hover styles are global; nav hover styles are in the header module.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find `.button:hover`, `.button-secondary:hover`, `.button-ghost:hover`.
3. Update the background or border color.
4. For nav, open `SiteHeader.module.css` and update `.nav-link:hover`.
5. Save.

#### Code Before
```css
.button:hover,
.button-secondary:hover,
.button-ghost:hover,
.theme-toggle:hover {
  transform: translateY(-1px);
}
```

#### Code After
```css
.button:hover,
.button-secondary:hover,
.button-ghost:hover,
.theme-toggle:hover {
  transform: translateY(-1px);
  background: rgba(var(--accent-rgb), 0.18);
}
```

#### What Changed
Hover states become brighter and more visible.

#### Common Mistakes
- Adding `background` to `.button-ghost:hover` without also setting `color`.

#### Extra Notes
Use `color-mix(in srgb, var(--accent) 20%, var(--surface))` for subtler hover tones.

### Question 8
Add border radius.

#### What This Means
Make a card or button corners rounder.

#### Files You Need To Open
- If it is a shared card, `app/globals.css`.
- If it is a component card, that component's CSS module.

#### Why These Files
Rounded corners are applied by `border-radius`.

#### Step-by-Step Instructions
1. Find the selector for the card or button you want.
2. Add or increase `border-radius: 32px;` or `border-radius: 1.5rem;`.
3. Save.

#### Code Before
```css
.glass-panel {
  border-radius: var(--radius-xl);
}
```

#### Code After
```css
.glass-panel {
  border-radius: 36px;
}
```

#### What Changed
The selected element appears softer with rounder corners.

#### Common Mistakes
- Using `border-radius` on a parent wrapper when the visible card is a child.

#### Extra Notes
If a component uses a special card class like `.hero-story-card`, update that class instead of `.glass-panel`.

### Question 9
Make layout mobile responsive.

#### What This Means
Fix layout overflow or stacking issues on small screen sizes.

#### Files You Need To Open
- `app/globals.css`
- The page CSS module for the page showing the layout problem.

#### Why These Files
Responsive breakpoints are handled by media queries here.

#### Step-by-Step Instructions
1. Identify the broken layout container in the browser inspector.
2. Open `app/globals.css` and page CSS.
3. Add or modify `@media (max-width: 768px)` rules for grid/flex containers.
4. Use `grid-template-columns: 1fr;` or `flex-direction: column;`.
5. Save.

#### Code Before
```css
.marketing-grid {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
```

#### Code After
```css
@media (max-width: 768px) {
  .marketing-grid {
    grid-template-columns: 1fr;
  }
}
```

#### What Changed
The layout stacks vertically on phones.

#### Common Mistakes
- Only resizing one column and not both.
- Forgetting `minmax(0, 1fr)` inside grid columns.

#### Extra Notes
Use `repeat(auto-fit, minmax(...))` when possible to make grids adapt automatically.

### Question 10
Change font family.

#### What This Means
Switch the main heading or body font used by the site.

#### Files You Need To Open
- `app/layout.tsx`
- `app/globals.css`

#### Why These Files
`app/layout.tsx` loads the fonts. `app/globals.css` applies them.

#### Step-by-Step Instructions
1. In `app/layout.tsx`, look at `Space_Grotesk` and `Manrope` imports.
2. If you want a new font, install or import it using `next/font/google`.
3. Update `variable: "--font-body"` or `--font-display` as needed.
4. In `app/globals.css`, update `body { font-family: var(--font-body), sans-serif; }` and `.section-title { font-family: var(--font-display), sans-serif; }`.
5. Save.

#### Code Before
```ts
const display = Space_Grotesk({ variable: "--font-display" });
const body = Manrope({ variable: "--font-body" });
```

#### Code After
```ts
const display = Space_Grotesk({ variable: "--font-display" });
const body = Inter({ subsets: ["latin"], variable: "--font-body" });
```

#### What Changed
The entire site uses the new body font.

#### Common Mistakes
- Changing CSS `font-family` without importing the new font in `layout.tsx`.
- Forgetting the fallback `sans-serif`.

#### Extra Notes
The site already uses `--font-body` for text and `--font-display` for headings.

### Question 11
Adjust tablet spacing.

#### What This Means
Change margins or padding for mid-sized screens.

#### Files You Need To Open
- `app/globals.css`
- The page or component CSS with the broken spacing.

#### Why These Files
Tablet breakpoints are controlled by `@media (max-width: 768px)` or container queries.

#### Step-by-Step Instructions
1. Identify which spacing feels wrong in the browser.
2. Open the relevant CSS file.
3. Add an `@media (max-width: 900px)` or `@media (max-width: 768px)` section.
4. Adjust `padding-inline`, `margin-top`, or `gap`.
5. Save.

#### Code Before
```css
.header :global(.header-inner) {
  padding-inline: clamp(16px, 3vw, 36px);
}
```

#### Code After
```css
@media (max-width: 768px) {
  .header :global(.header-inner) {
    padding-inline: 16px;
  }
}
```

#### What Changed
Tablet/mobile gets a consistent smaller padding.

#### Common Mistakes
- Editing only desktop values and not adding a responsive override.
- Using fixed pixel values that break on smaller tablets.

#### Extra Notes
`clamp()` already gives responsive spacing. Use media queries when you need a hard breakpoint.

### Question 12
Fix overflowing content.

#### What This Means
A section is wider than the screen and causes horizontal scroll.

#### Files You Need To Open
- The page/component CSS file where overflow appears.
- `app/globals.css` if the break is global.

#### Why These Files
Overflow is usually caused by fixed widths or missing `max-width`.

#### Step-by-Step Instructions
1. Inspect the element in the browser and find the overflowing container.
2. Open the corresponding CSS file.
3. Add `max-width: 100%;` and/or `overflow-wrap: break-word;` to the text or container.
4. For grids, change `grid-template-columns` to `minmax(0, 1fr)`.
5. Save.

#### Code Before
```css
.hero-grid {
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
}
```

#### Code After
```css
.hero-grid {
  grid-template-columns: minmax(0, 1.15fr) minmax(0, 0.85fr);
}
```

#### What Changed
Grid columns now shrink properly and no longer force horizontal scroll.

#### Common Mistakes
- Using `minmax(320px, ...)` inside narrow containers without a mobile override.
- Forgetting to set `min-width: 0` on grid children.

#### Extra Notes
`min-width: 0` on grid/flex children is often needed to allow text to shrink.

### Question 13
Add animation.

#### What This Means
Introduce a transition or entrance effect on a card or section.

#### Files You Need To Open
- `app/globals.css`
- The component CSS that contains the target element.

#### Why These Files
Animations have shared keyframes in `globals.css`.

#### Step-by-Step Instructions
1. Open `app/globals.css` and find `@keyframes fadeInUp` or `slideInFromLeft`.
2. Note the class names `.animate-fade-in-up`, `.animate-slide-in-left`, `.animate-bounce-in`.
3. In the target component JSX, add `className="animate-fade-in-up"` to the element.
4. If the element is in a CSS module, use `className={
  `existing-classes animate-fade-in-up`
}`.
5. Save.

#### Code Before
```tsx
<div className="glass-panel card">
  ...
</div>
```

#### Code After
```tsx
<div className="glass-panel card animate-fade-in-up">
  ...
</div>
```

#### What Changed
The element now fades in and slides up into view.

#### Common Mistakes
- Adding animation classes to an element that is hidden or not rendered yet.
- Forgetting to import or use plain string class names if inside a CSS module component.

#### Extra Notes
You can combine animations with hover transitions for polished motion.

### Question 14
Modify flexbox alignment.

#### What This Means
Change how items are aligned along a row or column.

#### Files You Need To Open
- `app/globals.css`
- Relevant page/component CSS.

#### Why These Files
Flexbox alignment uses `align-items` and `justify-content`.

#### Step-by-Step Instructions
1. Find the container with `display: flex;`.
2. Change `align-items: center;` or `justify-content: space-between;`.
3. Save.

#### Code Before
```css
.header :global(.header-inner) {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
```

#### Code After
```css
.header :global(.header-inner) {
  display: flex;
  align-items: center;
  justify-content: flex-start;
}
```

#### What Changed
Header items will shift to the left instead of stretching across the top.

#### Common Mistakes
- Confusing `align-items` (cross-axis) with `justify-content` (main axis).

#### Extra Notes
A row uses `justify-content` horizontally and `align-items` vertically.

### Question 15
Convert grid columns.

#### What This Means
Change a multi-column layout into a different column count.

#### Files You Need To Open
- `app/page.module.css`
- Any page CSS module with `grid-template-columns`.

#### Why These Files
Grid layout is defined by `grid-template-columns`.

#### Step-by-Step Instructions
1. Find the grid selector, like `.story-strip`.
2. Change `grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));` to a new value.
3. For 2 columns, use `repeat(2, minmax(0, 1fr));`.
4. Save.

#### Code Before
```css
.page :global(.story-strip) {
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}
```

#### Code After
```css
.page :global(.story-strip) {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
```

#### What Changed
The story cards now display in exactly two columns on large screens.

#### Common Mistakes
- Using fixed columns without checking mobile behavior.
- Forgetting to update responsive media queries.

#### Extra Notes
`auto-fit` is usually better for responsive grids.

### Question 16
Hide element on mobile.

#### What This Means
Make an element disappear for small screens.

#### Files You Need To Open
- `app/globals.css` or the component CSS with the target class.

#### Why These Files
Responsive display rules go inside media queries.

#### Step-by-Step Instructions
1. Identify the class of the element you want to hide.
2. Add an `@media (max-width: 768px)` rule.
3. Set `display: none;` for that class.
4. Save.

#### Code Before
```css
.header :global(.desktop-nav) {
  margin-left: auto;
  margin-right: 18px;
}
```

#### Code After
```css
@media (max-width: 768px) {
  .header :global(.desktop-nav) {
    display: none;
  }
}
```

#### What Changed
The desktop navigation is hidden on phones.

#### Common Mistakes
- Using `visibility: hidden;` instead of `display: none;`.
- Forgetting the media query.

#### Extra Notes
The header already hides `.desktop-nav` at mobile width.

### Question 17
Make button wider.

#### What This Means
Increase a button's width so it is easier to click.

#### Files You Need To Open
- `app/globals.css`
- Relevant component page if the button has a special wrapper.

#### Why These Files
Button width is controlled by padding or explicit width.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find the `.button`, `.button-secondary`, or `.button-ghost` rule.
3. Increase `padding: 13px 24px;`.
4. If you want a full-width button, add `.button { width: 100%; }` in a wrapper context.
5. Save.

#### Code Before
```css
.button,
.button-secondary,
.button-ghost {
  padding: 13px 18px;
}
```

#### Code After
```css
.button,
.button-secondary,
.button-ghost {
  padding: 13px 24px;
}
```

#### What Changed
Buttons become wider and easier to tap.

#### Common Mistakes
- Changing only the button text width and not padding.

#### Extra Notes
Use `.button-row-stack .button { width: 100%; }` for stacked full-width buttons.

### Question 18
Change hero height.

#### What This Means
Adjust the vertical size of the hero section container.

#### Files You Need To Open
- `components/marketing/HeroSection.module.css`

#### Why These Files
The hero panel height is defined in the hero CSS module.

#### Step-by-Step Instructions
1. Open `HeroSection.module.css`.
2. Find `.scope :global(.premium-hero-panel)`.
3. Update `min-height: 620px;` to another value.
4. Save.

#### Code Before
```css
.scope :global(.premium-hero-panel) {
  min-height: 620px;
}
```

#### Code After
```css
.scope :global(.premium-hero-panel) {
  min-height: 720px;
}
```

#### What Changed
The hero becomes taller, giving more space inside the main panel.

#### Common Mistakes
- Changing the wrong `.headline` selector.

#### Extra Notes
If the hero is too tall on mobile, add a media query to lower the height.

### Question 19
Adjust z-index.

#### What This Means
Ensure one overlay appears above another.

#### Files You Need To Open
- The CSS module of the overlay or floating component.

#### Why These Files
`z-index` controls stacking order.

#### Step-by-Step Instructions
1. Find the overlay or floating element class.
2. Add or increase `z-index`, for example `z-index: 100;`.
3. Save.

#### Code Before
```css
.scope {
  position: fixed;
  z-index: 45;
}
```

#### Code After
```css
.scope {
  position: fixed;
  z-index: 105;
}
```

#### What Changed
That element is forced above lower z-index items.

#### Common Mistakes
- Setting `z-index` without `position: relative/absolute/fixed`.

#### Extra Notes
The header uses `z-index: 50`; the mobile theme modal likely needs more.

### Question 20
Add shadow to cards.

#### What This Means
Give card panels a stronger drop shadow.

#### Files You Need To Open
- `app/globals.css`
- The component CSS module for specific cards.

#### Why These Files
Card shadows may rely on `.glass-panel` or component-specific panels.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find `.glass-panel`.
3. Update `box-shadow: var(--shadow);` to a stronger value, or add a custom shadow.
4. Save.

#### Code Before
```css
.glass-panel {
  box-shadow: var(--shadow);
}
```

#### Code After
```css
.glass-panel {
  box-shadow: 0 22px 65px rgba(0, 0, 0, 0.2);
}
```

#### What Changed
Cards appear more lifted and prominent.

#### Common Mistakes
- Adding only `border` without stronger shadow.

#### Extra Notes
Use `box-shadow` with low opacity for modern effect.

### Question 21
Change the hero button text.

#### What This Means
Update the CTA copy inside the hero.

#### Files You Need To Open
- `components/marketing/hero-section.tsx`

#### Why These Files
The button labels are in the hero JSX.

#### Step-by-Step Instructions
1. Open `components/marketing/hero-section.tsx`.
2. Find `<InstantNavLink href="/dashboard" ...>Browse phones <ArrowRight ... /></InstantNavLink>`.
3. Replace the text content: `Browse phones` → `Start browsing`.
4. Save.

#### Code Before
```tsx
<InstantNavLink href="/dashboard" className="button magnetic-button" loadingLabel="Opening phone browser...">
  Browse phones <ArrowRight size={16} />
</InstantNavLink>
```

#### Code After
```tsx
<InstantNavLink href="/dashboard" className="button magnetic-button" loadingLabel="Opening phone browser...">
  Start browsing <ArrowRight size={16} />
</InstantNavLink>
```

#### What Changed
The call-to-action label changes directly in the hero.

#### Common Mistakes
- Changing the `href` accidentally.

#### Extra Notes
Text edits do not require CSS changes.

### Question 22
Move the hero CTA buttons lower.

#### What This Means
Add vertical spacing between the hero copy and the buttons.

#### Files You Need To Open
- `components/marketing/HeroSection.module.css`

#### Why These Files
The button container is styled in the hero module.

#### Step-by-Step Instructions
1. Open `HeroSection.module.css`.
2. Find `.scope :global(.hero-action-row)`.
3. Increase `margin-top` from `28px` to `40px`.
4. Save.

#### Code Before
```css
.scope :global(.hero-action-row) {
  margin-top: 28px;
}
```

#### Code After
```css
.scope :global(.hero-action-row) {
  margin-top: 40px;
}
```

#### What Changed
The CTA block sits further below the hero paragraph.

#### Common Mistakes
- Editing `padding` instead of `margin-top`.

#### Extra Notes
Spacing changes are safer than size changes for readability.

### Question 23
Change the hero panel background gradient.

#### What This Means
Modify the hero card's background appearance.

#### Files You Need To Open
- `components/marketing/HeroSection.module.css`

#### Why These Files
The hero panel background is defined there.

#### Step-by-Step Instructions
1. Open `HeroSection.module.css`.
2. Find `.scope :global(.premium-hero-panel)`.
3. Replace the `background:` property with a new gradient.
4. Save.

#### Code Before
```css
.scope :global(.premium-hero-panel) {
  background: 
    radial-gradient(circle at 20% 30%, rgba(var(--accent-rgb), 0.15), transparent 50%),
    radial-gradient(circle at 80% 70%, rgba(95, 150, 255, 0.1), transparent 50%),
    linear-gradient(135deg, var(--surface) 0%, var(--surface-soft) 100%);
}
```

#### Code After
```css
.scope :global(.premium-hero-panel) {
  background:
    radial-gradient(circle at 20% 30%, rgba(var(--accent-rgb), 0.2), transparent 40%),
    radial-gradient(circle at 80% 70%, rgba(var(--accent-secondary-rgb), 0.18), transparent 45%),
    linear-gradient(135deg, var(--surface-soft) 0%, var(--surface-strong) 100%);
}
```

#### What Changed
The hero background uses a new blend of colors.

#### Common Mistakes
- Removing all gradient layers and making it flat.

#### Extra Notes
Use `var(--surface-soft)` and `var(--surface-strong)` for consistent theme.

### Question 24
Increase card hover lift.

#### What This Means
Make hover animation more pronounced on cards.

#### Files You Need To Open
- `app/page.module.css`
- Or the component CSS where the card is defined.

#### Why These Files
Card hover styles are local to the card container.

#### Step-by-Step Instructions
1. Open the code for the target card's CSS module.
2. Find the `:hover` selector such as `.page :global(.story-card:hover)`.
3. Increase `transform: translateY(-4px);` to `translateY(-8px);` and intensify `box-shadow`.
4. Save.

#### Code Before
```css
.page :global(.story-card:hover) {
  transform: translateY(-4px);
  border-color: color-mix(in srgb, var(--accent) 30%, var(--border));
  box-shadow: var(--shadow);
}
```

#### Code After
```css
.page :global(.story-card:hover) {
  transform: translateY(-8px);
  border-color: color-mix(in srgb, var(--accent) 30%, var(--border));
  box-shadow: 0 26px 60px rgba(15, 23, 42, 0.18);
}
```

#### What Changed
Hover movement is stronger and the card pops more.

#### Common Mistakes
- Adding too much lift and making the UI feel jittery.

#### Extra Notes
Try to keep hover shift subtle on production pages.

### Question 25
Change the mobile tab icon.

#### What This Means
Swap one of the bottom nav icons on mobile.

#### Files You Need To Open
- `components/marketing/mobile-tabbar.tsx`

#### Why These Files
This file defines mobile tab items and icons.

#### Step-by-Step Instructions
1. Open `mobile-tabbar.tsx`.
2. Find the `tabs` array at the top.
3. Replace an imported icon name with another from `lucide-react`.
4. Ensure the icon is also imported at the top.
5. Save.

#### Code Before
```ts
import { GitCompareArrows, Heart, House, LayoutDashboard, Sparkles } from "lucide-react";
const tabs = [
  { href: "/", label: "Home", icon: House },
  ...
];
```

#### Code After
```ts
import { ArrowRight, Heart, House, LayoutDashboard, Sparkles } from "lucide-react";
const tabs = [
  { href: "/", label: "Home", icon: House },
  { href: "/compare", label: "Compare", icon: ArrowRight },
  ...
];
```

#### What Changed
The selected mobile tab uses the new icon.

#### Common Mistakes
- Forgetting to update the import line when adding a new icon.

#### Extra Notes
Mobile tabs use the `span` label and icon inside each link.

### Question 26
Add a new navbar link.

#### What This Means
Add a new route link to the desktop header.

#### Files You Need To Open
- `components/marketing/site-header.tsx`

#### Why These Files
The `links` array defines header navigation.

#### Step-by-Step Instructions
1. Open `site-header.tsx`.
2. Find the `links = [...]` array.
3. Add a new object, for example `{ href: "/blog", label: "Blog" }`.
4. Save.

#### Code Before
```ts
const links = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  ...
];
```

#### Code After
```ts
const links = [
  { href: "/", label: "Home" },
  { href: "/about", label: "About" },
  { href: "/blog", label: "Blog" },
  ...
];
```

#### What Changed
A new link appears in the desktop navigation.

#### Common Mistakes
- Adding the link outside of the array.
- Using the wrong route format.

#### Extra Notes
The mobile tab bar is separate and does not automatically get this link.

### Question 27
Make the footer sticky.

#### What This Means
Keep the footer at the bottom of the viewport when content is short.

#### Files You Need To Open
- `app/globals.css`
- `components/marketing/site-footer.tsx`

#### Why These Files
The body and footer container determine sticky behavior.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Ensure `body { min-height: 100vh; }` is present.
3. Add `footer { position: relative; }` if needed.
4. Save.

#### Code Before
```css
body {
  min-height: 100vh;
}
```

#### Code After
```css
body {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
main {
  flex: 1;
}
```

#### What Changed
The footer sits at the bottom when the page is short.

#### Common Mistakes
- Forgetting `main { flex: 1; }` so the content area expands.

#### Extra Notes
This can affect all pages, so test multiple routes.

### Question 28
Change the default text color.

#### What This Means
Update the main body text color across the site.

#### Files You Need To Open
- `app/globals.css`

#### Why These Files
The body text color is defined by `--text`.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find `:root { --text: #f5f7fb; }` and/or `html[data-theme="light"] { --text: #111827; }`.
3. Replace the value.
4. Save.

#### Code Before
```css
:root {
  --text: #f5f7fb;
}

html[data-theme="light"] {
  --text: #111827;
}
```

#### Code After
```css
:root {
  --text: #e6e9f2;
}

html[data-theme="light"] {
  --text: #0f172a;
}
```

#### What Changed
The body text color changes depending on the theme.

#### Common Mistakes
- Changing the color in one theme only and not both dark/light.

#### Extra Notes
`--text` is used by many elements, so the change is global.

### Question 29
Change button border color.

#### What This Means
Update the border on secondary or ghost buttons.

#### Files You Need To Open
- `app/globals.css`

#### Why These Files
Button borders are defined in the global button styles.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find `.button-secondary` or `.button-ghost`.
3. Update `border-color: var(--border);` to another variable.
4. Save.

#### Code Before
```css
.button-secondary {
  background: var(--surface-soft);
  border-color: var(--border);
  color: var(--text);
}
```

#### Code After
```css
.button-secondary {
  background: var(--surface-soft);
  border-color: rgba(var(--accent-rgb), 0.35);
  color: var(--text);
}
```

#### What Changed
Secondary buttons now have an accent-colored border.

#### Common Mistakes
- Using a border color with too little contrast.

#### Extra Notes
Ghost buttons are great when you want a subtle outline effect.

### Question 30
Debug a missing section label.

#### What This Means
A section label like `Scroll Story` disappeared.

#### Files You Need To Open
- `app/page.tsx` or the specific page file.

#### Why These Files
The label is plain JSX text inside a `span`.

#### Step-by-Step Instructions
1. Open the page file.
2. Find the `span className="section-label"` for the missing label.
3. Confirm the text is not commented out.
4. If the label is present but invisible, inspect CSS for `color: transparent;`.
5. Fix the text or CSS.

#### Code Before
```tsx
<span className="section-label">Scroll Story</span>
```

#### Code After
```tsx
<span className="section-label">Scroll Story</span>
```

#### What Changed
No code change if it was already correct; the fix may be style-related.

#### Common Mistakes
- Assuming the label is missing in JSX when it is simply hidden by CSS.

#### Extra Notes
`section-label` is shared and uses accent styling.

### Question 31
Change the section title color.

#### What This Means
Update a large heading color for one section.

#### Files You Need To Open
- `app/globals.css`
- Or page CSS if the section has a custom title.

#### Why These Files
Section titles use the shared `.section-title` class.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find `.section-title`.
3. Add `color: var(--text);` or `color: var(--accent);`.
4. Save.

#### Code Before
```css
.section-title {
  font-size: clamp(2.4rem, 5vw, 4.5rem);
  line-height: 0.95;
}
```

#### Code After
```css
.section-title {
  font-size: clamp(2.4rem, 5vw, 4.5rem);
  line-height: 0.95;
  color: var(--accent-secondary);
}
```

#### What Changed
The title now uses the accent secondary color.

#### Common Mistakes
- Overriding `color` without a fallback.

#### Extra Notes
If only one section should change, use a new class on the heading.

### Question 32
Fix a dark mode issue.

#### What This Means
The site may be displaying incorrect colors in dark theme.

#### Files You Need To Open
- `app/globals.css`
- `components/providers/theme-provider.tsx`

#### Why These Files
Dark mode tokens and theme switching logic live there.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Review `html[data-theme="dark"] { ... }` and `html[data-theme="light"] { ... }`.
3. Check whether the variable that is wrong is defined in the correct block.
4. If the logic is wrong, open `theme-provider.tsx` and verify `data-theme` is set correctly.
5. Save.

#### Code Before
```css
html[data-theme="dark"] {
  --text: #f5f7fb;
}
```

#### Code After
```css
html[data-theme="dark"] {
  --text: #f5f7fb;
  --bg: #0d1117;
}
```

#### What Changed
Dark mode variables are restored.

#### Common Mistakes
- Fixing the CSS but not the theme provider logic.

#### Extra Notes
This app uses theme variables; switch by updating `data-theme`.

### Question 33
Add a new section to the homepage.

#### What This Means
Insert a new content block below or above existing sections.

#### Files You Need To Open
- `app/page.tsx`
- `app/page.module.css` if styling is needed.

#### Why These Files
The home page structure is defined in `app/page.tsx`.

#### Step-by-Step Instructions
1. Open `app/page.tsx`.
2. Copy one existing `<section className="section">...</section>` block.
3. Paste it where you want the new section.
4. Update the text and links inside.
5. If you need a new style, add it to `app/page.module.css`.
6. Save.

#### Code Before
```tsx
<section className="section">
  <div className="page-shell">
    ...
  </div>
</section>
```

#### Code After
```tsx
<section className="section">
  <div className="page-shell">
    <span className="section-label">New Section</span>
    <h2 className="feature-title">This is a new homepage feature.</h2>
    <p className="section-copy">...</p>
  </div>
</section>
```

#### What Changed
A new content block appears on the home page.

#### Common Mistakes
- Forgetting to wrap content in `page-shell`.
- Using duplicate IDs if you add anchors.

#### Extra Notes
`section` and `page-shell` are the standard home page wrappers.

### Question 34
Change the mobile bottom nav text.

#### What This Means
Update one of the labels in the tab bar.

#### Files You Need To Open
- `components/marketing/mobile-tabbar.tsx`

#### Why These Files
The labels are defined in the `tabs` array.

#### Step-by-Step Instructions
1. Open `mobile-tabbar.tsx`.
2. In the `tabs` array, change `label: "Saved"` to `label: "Favorites"` or similar.
3. Save.

#### Code Before
```ts
{ href: "/favorites", label: "Saved", icon: Heart }
```

#### Code After
```ts
{ href: "/favorites", label: "Favorites", icon: Heart }
```

#### What Changed
The text under the mobile icon updates.

#### Common Mistakes
- Changing `href` accidentally.

#### Extra Notes
Mobile labels are short due to space.

### Question 35
Change the hero badge style.

#### What This Means
Modify the little pill badges below the hero buttons.

#### Files You Need To Open
- `HeroSection.module.css`

#### Why These Files
The `.hero-badge-row .pill` rule controls these badges.

#### Step-by-Step Instructions
1. Open `HeroSection.module.css`.
2. Find `.scope :global(.hero-badge-row .pill)`.
3. Update `background`, `border`, or `padding`.
4. Save.

#### Code Before
```css
.scope :global(.hero-badge-row .pill) {
  min-height: 48px;
  padding: 12px 16px;
  background: color-mix(in srgb, var(--surface-soft) 80%, rgba(255, 255, 255, 0.05));
}
```

#### Code After
```css
.scope :global(.hero-badge-row .pill) {
  min-height: 48px;
  padding: 12px 16px;
  background: var(--surface);
  border: 1px solid rgba(var(--accent-rgb), 0.18);
}
```

#### What Changed
Hero badges become more visible and refined.

#### Common Mistakes
- Removing the border and making them disappear.

#### Extra Notes
Pill styles are shared with other small badges.

### Question 36
Make the mobile tab bar sticky on small screens.

#### What This Means
Ensure the bottom mobile nav stays fixed.

#### Files You Need To Open
- `components/marketing/MobileTabBar.module.css`

#### Why These Files
This file defines the fixed position and display rules.

#### Step-by-Step Instructions
1. Open `MobileTabBar.module.css`.
2. Confirm `.scope` has `position: fixed; left: 16px; right: 16px; bottom: 16px;`.
3. Save.

#### Code Before
```css
.scope {
  position: fixed;
  left: 16px;
  right: 16px;
  bottom: 16px;
  z-index: 45;
  display: none;
}
```

#### Code After
```css
.scope {
  position: fixed;
  left: 16px;
  right: 16px;
  bottom: 16px;
  z-index: 45;
  display: none;
}
```

#### What Changed
The tab bar remains fixed; this is already set.

#### Common Mistakes
- Deleting `position: fixed;`.

#### Extra Notes
The bar appears only on screens `max-width: 768px`.

### Question 37
Update the site logo text.

#### What This Means
Change the brand name or subtitle shown in header/footer.

#### Files You Need To Open
- `components/marketing/brand-lockup.tsx`
- `lib/site.ts`

#### Why These Files
The brand text comes from the reusable brand component and site config.

#### Step-by-Step Instructions
1. Open `lib/site.ts`.
2. Change `site.name` or `site.tagline`.
3. Save.
4. If needed, open `brand-lockup.tsx` to override `subtitle`.

#### Code Before
```ts
const site = {
  name: "Dialed",
  tagline: "Search, compare, and get to a short list."
};
```

#### Code After
```ts
const site = {
  name: "Dialed",
  tagline: "Phone search made simple."
};
```

#### What Changed
The brand subtitle text updates across header and footer.

#### Common Mistakes
- Editing `brand-lockup.tsx` text directly when the shared config is used.

#### Extra Notes
`BrandLockup` renders the same brand unit in header and footer.

### Question 38
Change the mobile action sheet button color.

#### What This Means
Update the button styles inside the mobile auth sheet.

#### Files You Need To Open
- `components/marketing/HeaderAuthControls.module.css`

#### Why These Files
Mobile sheet button styling is defined here.

#### Step-by-Step Instructions
1. Open `HeaderAuthControls.module.css`.
2. Find `.panel :global(.header-account-link)` or `.panel :global(.header-account-close)`.
3. Add `background: var(--accent); color: var(--accent-contrast);` or similar.
4. Save.

#### Code Before
```css
.panel :global(.header-account-link) {
  width: 100%;
  justify-content: center;
  gap: 10px;
}
```

#### Code After
```css
.panel :global(.header-account-link) {
  width: 100%;
  justify-content: center;
  gap: 10px;
  background: var(--accent);
  color: var(--accent-contrast);
}
```

#### What Changed
Buttons in the mobile auth sheet now use the accent background.

#### Common Mistakes
- Forgetting that `.button-secondary` or `.button-ghost` already provide styling.

#### Extra Notes
Use `button` classes carefully because the component already applies them.

### Question 39
Reduce the hero text line height.

#### What This Means
Tighten the spacing between lines in the hero description.

#### Files You Need To Open
- `components/marketing/HeroSection.module.css` or `app/globals.css`.

#### Why These Files
Line height is a typography property on text elements.

#### Step-by-Step Instructions
1. Open `HeroSection.module.css`.
2. Find `.scope :global(.hero-copy-stack) p` or `.scope :global(.hero-story-card p)`.
3. Add `line-height: 1.5;` or lower.
4. Save.

#### Code Before
```css
.scope :global(.hero-story-card p) {
  margin: 0;
  color: var(--muted);
  line-height: 1.62;
}
```

#### Code After
```css
.scope :global(.hero-story-card p) {
  margin: 0;
  color: var(--muted);
  line-height: 1.45;
}
```

#### What Changed
Text becomes more compact and tighter.

#### Common Mistakes
- Making line height too small, which hurts readability.

#### Extra Notes
Body text usually works best between `1.4` and `1.75`.

### Question 40
Make the hero cards stack on tablet.

#### What This Means
Force the hero preview cards to become one column on tablets.

#### Files You Need To Open
- `app/page.module.css`

#### Why These Files
The homepage grid is controlled there.

#### Step-by-Step Instructions
1. Open `app/page.module.css`.
2. Find `.page :global(.home-preview-grid)`.
3. Add a media query:
```css
@media (max-width: 900px) {
  .page :global(.home-preview-grid) {
    grid-template-columns: 1fr;
  }
}
```
4. Save.

#### Code Before
```css
.page :global(.home-preview-grid) {
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}
```

#### Code After
```css
.page :global(.home-preview-grid) {
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

@media (max-width: 900px) {
  .page :global(.home-preview-grid) {
    grid-template-columns: 1fr;
  }
}
```

#### What Changed
The cards stack vertically on tablets.

#### Common Mistakes
- Using `max-width: 768px` only; tablet might need 900px.

#### Extra Notes
`auto-fit` already helps, but explicit rules are useful for specific breakpoints.

### Question 41
Add a secondary headline under the hero.

#### What This Means
Insert a small subtitle below the hero title.

#### Files You Need To Open
- `components/marketing/hero-section.tsx`
- `HeroSection.module.css` if style is needed.

#### Why These Files
The hero markup defines the title structure.

#### Step-by-Step Instructions
1. Open `hero-section.tsx`.
2. Find the hero heading `<h1 className="section-title">...</h1>`.
3. Add a `<p className="section-copy">...</p>` after it.
4. If needed, add spacing in `HeroSection.module.css`.
5. Save.

#### Code Before
```tsx
<h1 className="section-title">Stop guessing. Start comparing.</h1>
<p className="section-copy">...</p>
```

#### Code After
```tsx
<h1 className="section-title">Stop guessing. Start comparing.</h1>
<p className="section-copy">The cleanest phone comparison flow built for fast shoppers.</p>
<p className="section-copy">No clutter, no decoy tabs, just the phones that matter.</p>
```

#### What Changed
A new subtitle appears below the main hero heading.

#### Common Mistakes
- Using the wrong class name and losing the shared typography.

#### Extra Notes
`section-copy` is the standard body text class.

### Question 42
Change the hero CTA button order.

#### What This Means
Swap the primary and secondary hero buttons.

#### Files You Need To Open
- `components/marketing/hero-section.tsx`

#### Why These Files
Button order is set in the JSX.

#### Step-by-Step Instructions
1. Open `hero-section.tsx`.
2. Locate the two buttons in `.hero-action-row`.
3. Swap the two JSX blocks.
4. Save.

#### Code Before
```tsx
<InstantNavLink ...>Browse phones</InstantNavLink>
<Link href="/compare" className="button-secondary ...">Watch the compare reveal</Link>
```

#### Code After
```tsx
<Link href="/compare" className="button-secondary ...">Watch the compare reveal</Link>
<InstantNavLink ...>Browse phones</InstantNavLink>
```

#### What Changed
The secondary button appears before the primary button.

#### Common Mistakes
- Breaking the closing tags when moving JSX blocks.

#### Extra Notes
The order affects both design and accessibility.

### Question 43
Change the floating theme button icon.

#### What This Means
Update the icon inside the theme launcher.

#### Files You Need To Open
- `components/marketing/theme-toggle.tsx`
- `components/marketing/ThemeToggle.module.css` if style is needed.

#### Why These Files
The icon is imported and rendered in the theme launcher.

#### Step-by-Step Instructions
1. Open `theme-toggle.tsx`.
2. Replace `Palette` with a different `lucide-react` icon such as `SunMedium`.
3. Update the import line accordingly.
4. Save.

#### Code Before
```ts
import { Check, Monitor, MoonStar, Palette, Search, SunMedium, X } from "lucide-react";
...
<Palette size={16} />
```

#### Code After
```ts
import { Check, Monitor, MoonStar, Search, SunMedium, X } from "lucide-react";
...
<SunMedium size={16} />
```

#### What Changed
The floating theme button uses a different icon.

#### Common Mistakes
- Removing the import and causing a build error.

#### Extra Notes
This changes only the icon, not the modal behavior.

### Question 44
Make the hero stat cards two columns on mobile.

#### What This Means
Change the stats grid from 2 columns to 1 on smartphones.

#### Files You Need To Open
- `HeroSection.module.css`

#### Why These Files
The hero stats grid rule is defined there.

#### Step-by-Step Instructions
1. Open `HeroSection.module.css`.
2. Find `.scope :global(.hero-stats-grid)`.
3. Add a media query:
```css
@media (max-width: 640px) {
  .scope :global(.hero-stats-grid) {
    grid-template-columns: 1fr;
  }
}
```
4. Save.

#### Code Before
```css
.scope :global(.hero-stats-grid) {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
```

#### Code After
```css
.scope :global(.hero-stats-grid) {
  display: grid;
  gap: 14px;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}

@media (max-width: 640px) {
  .scope :global(.hero-stats-grid) {
    grid-template-columns: 1fr;
  }
}
```

#### What Changed
Stat cards stack vertically on small phones.

#### Common Mistakes
- Using `flex-direction` on a grid container.

#### Extra Notes
The existing layout already changes at `768px`; this makes it even more mobile-friendly.

### Question 45
Change the compare page card background.

#### What This Means
Update the background of panels on `/compare`.

#### Files You Need To Open
- `app/compare/page.module.css`

#### Why These Files
Compare page panel styles live there.

#### Step-by-Step Instructions
1. Open `app/compare/page.module.css`.
2. Find a panel rule like `.page :global(.compare-panel)` or `.glass-panel` usage.
3. Replace the `background:` property.
4. Save.

#### Code Before
```css
.page :global(.glass-panel) {
  background: var(--surface);
}
```

#### Code After
```css
.page :global(.glass-panel) {
  background: rgba(255, 255, 255, 0.08);
}
```

#### What Changed
Compare cards appear lighter or darker depending on the new value.

#### Common Mistakes
- Editing `page.tsx` markup rather than CSS.

#### Extra Notes
Use `var(--surface)` for consistency with theming.

### Question 46
Add a CTA button to the about page.

#### What This Means
Place a new button in the about page content.

#### Files You Need To Open
- `app/about/page.tsx`

#### Why These Files
The about page JSX defines content.

#### Step-by-Step Instructions
1. Open `app/about/page.tsx`.
2. Inside one of the `<div className="glass-panel card">` blocks, add:
```tsx
<Link href="/dashboard" className="button">
  Open dashboard
</Link>
```
3. Save.

#### Code Before
```tsx
<div className="glass-panel card">
  <span className="section-label">About</span>
  <h1 className="section-title">Built for a cleaner phone search.</h1>
  <p className="section-copy">...</p>
</div>
```

#### Code After
```tsx
<div className="glass-panel card">
  <span className="section-label">About</span>
  <h1 className="section-title">Built for a cleaner phone search.</h1>
  <p className="section-copy">...</p>
  <Link href="/dashboard" className="button">
    Open dashboard
  </Link>
</div>
```

#### What Changed
A new CTA button appears on the about page.

#### Common Mistakes
- Not importing `Link` from `next/link` if it is not already imported.

#### Extra Notes
Use `button-secondary` if you want a less intense CTA.

### Question 47
Change the `section-copy` color for one page.

#### What This Means
Only one page's body paragraphs should use a different text color.

#### Files You Need To Open
- The page-specific CSS file.

#### Why These Files
The page module can override global copy styling locally.

#### Step-by-Step Instructions
1. Open the relevant page module, for example `app/about/page.tsx` has no module, so use `app/globals.css` or add inline style.
2. If the page has a module CSS file, add:
```css
.page :global(.section-copy) {
  color: #cbd5e1;
}
```
3. If the page does not have a module, add a new class to the JSX and style it.
4. Save.

#### Code Before
```tsx
<p className="section-copy">...</p>
```

#### Code After
```tsx
<p className="section-copy about-copy">...</p>
```

#### What Changed
Only the about copy uses the new color.

#### Common Mistakes
- Editing the global `.section-copy` and changing it everywhere.

#### Extra Notes
Use a specific class like `about-copy` for page-only overrides.

### Question 48
Change the card outline color.

#### What This Means
Update the border color around glass panels.

#### Files You Need To Open
- `app/globals.css`

#### Why These Files
`glass-panel` borders are shared globally.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find `.glass-panel`.
3. Replace `border: 1px solid var(--border);` with `border: 1px solid rgba(var(--accent-rgb), 0.18);`.
4. Save.

#### Code Before
```css
.glass-panel {
  border: 1px solid var(--border);
}
```

#### Code After
```css
.glass-panel {
  border: 1px solid rgba(var(--accent-rgb), 0.18);
}
```

#### What Changed
Glass panels now have an accent-tinged border.

#### Common Mistakes
- Choosing a border color with low contrast.

#### Extra Notes
Use `color-mix` if you want soft blending.

### Question 49
Change site spacing tokens.

#### What This Means
Adjust the design system distances globally.

#### Files You Need To Open
- `app/globals.css`

#### Why These Files
Spacing tokens are defined there.

#### Step-by-Step Instructions
1. Open `app/globals.css`.
2. Find `--space-1` through `--space-6` under `:root`.
3. Increase or decrease values, for example `--space-4: clamp(1rem, 4vw, 2.5rem);`.
4. Save.

#### Code Before
```css
:root {
  --space-4: clamp(1rem, 4vw, 2rem);
}
```

#### Code After
```css
:root {
  --space-4: clamp(1.25rem, 4vw, 2.5rem);
}
```

#### What Changed
Many gaps and paddings using `var(--space-4)` adjust globally.

#### Common Mistakes
- Changing a single component when the app uses the token in many places.

#### Extra Notes
This is powerful; use with care.

### Question 50
Fix a broken route link in the navbar.

#### What This Means
One of the header links navigates to the wrong page.

#### Files You Need To Open
- `components/marketing/site-header.tsx`

#### Why These Files
Navigation routes are defined in the `links` array.

#### Step-by-Step Instructions
1. Open `site-header.tsx`.
2. Find the `links` array.
3. Locate the wrong `href` and correct it.
4. Save.

#### Code Before
```ts
{ href: "/services", label: "Services" },
{ href: "/contact", label: "Contact" },
```

#### Code After
```ts
{ href: "/services", label: "Services" },
{ href: "/contact", label: "Contact" },
```

#### What Changed
The correct route is restored. If it was a real mistake, the wrong path is replaced.

#### Common Mistakes
- Changing the route label instead of the `href`.

#### Extra Notes
Make sure the route exists under `app/`.

## 4. HTML + CSS CHEAT SHEET

### Common CSS properties
- `color`: text color.
- `background`, `background-color`: element background.
- `border`, `border-radius`: edge styling.
- `padding`: inside spacing.
- `margin`: outside spacing.
- `width`, `height`: element size.
- `max-width`, `max-height`: limit size.
- `display`: layout type (`block`, `inline-flex`, `grid`).
- `position`: placement mode (`static`, `relative`, `absolute`, `fixed`, `sticky`).
- `z-index`: stacking order.
- `opacity`: transparency.
- `transform`: move/scale/rotate.
- `transition`: smooth animation on property change.

### Flexbox
- `display: flex;` turns a container into a flex layout.
- `flex-direction: row;` aligns items horizontally.
- `flex-direction: column;` aligns items vertically.
- `justify-content`: horizontal spacing in a row.
- `align-items`: vertical alignment in a row.
- `gap`: spacing between flex items.
- `flex-wrap: wrap;` allows items to move to the next line.

### Grid
- `display: grid;` creates a grid layout.
- `grid-template-columns: repeat(3, 1fr);` creates 3 equal columns.
- `gap: 20px;` spaces both rows and columns.
- `grid-template-columns: minmax(0, 1fr);` prevents overflow and makes content shrink.
- `auto-fit` and `auto-fill` allow responsive column counts.

### Positioning
- `position: relative;` allows child absolute positioning.
- `position: absolute;` positions relative to nearest positioned ancestor.
- `position: fixed;` pins an element relative to the viewport.
- `position: sticky;` keeps an element fixed after it scrolls past a point.

### Margins and paddings
- `margin`: outside spacing.
- `padding`: inside spacing.
- `margin-top`, `margin-bottom`, `margin-inline`: directional control.
- `padding-block`, `padding-inline`: block/inline axis support.
- `gap`: spacing between grid/flex children.

### Font styling
- `font-family`: chooses the typeface.
- `font-weight`: boldness.
- `font-size`: text size.
- `line-height`: spacing between lines.
- `letter-spacing`: spacing between letters.
- `text-transform`: uppercase/lowercase.

### Responsive design
- `@media (max-width: 768px) { ... }` for mobile/tablet breakpoints.
- `clamp(min, preferred, max)` for fluid values.
- `max-width: 100%` to prevent overflow.
- `container-type: inline-size` to enable container queries.
- `@container (max-width: 768px) { ... }` to respond to component width.

### Hover effects
- `:hover` triggers when the pointer is over an element.
- Example:
```css
.button:hover {
  background: var(--accent-strong);
}
```

### Transitions
- `transition: all 0.3s ease;` makes property changes smooth.
- Common on hover: `transition: transform 0.3s ease, background 0.3s ease;`

### Animations
- `@keyframes name { from { ... } to { ... } }`
- Apply with `animation: name duration ease;`.
- Example in this project: `fadeInUp`, `slideInFromLeft`, `bounceIn`.

### z-index
- Higher `z-index` values appear above lower ones.
- `position` must be set to use z-index.

### Display types
- `block`: full-width element.
- `inline`: width matched to content.
- `inline-flex`: inline-level flex container.
- `flex`: flex container.
- `grid`: grid container.
- `none`: hidden element.

### Width vs max-width
- `width` sets the element size.
- `max-width` limits expansion but allows shrinking.
- Use `max-width: 100%;` for responsive images and containers.

### rem vs px
- `px` is fixed pixels.
- `rem` is relative to root font size (usually 16px).
- `clamp()` combines responsive `rem`, `vw`, and fixed values.

### Absolute vs relative
- `relative` keeps the element in normal flow and allows child positioning.
- `absolute` removes the element from normal flow and positions it by top/left/right/bottom.

### Semantic HTML tags
- `<section>` groups related page sections.
- `<article>` is for self-contained content blocks.
- `<header>` is for page or section headers.
- `<footer>` is for footer content.
- `<nav>` is for navigation links.
- `<strong>` means important text.
- `<span>` is an inline wrapper for styling.

## 5. LIVE CODING SURVIVAL GUIDE

### How to quickly identify files
1. Look at the route in the browser.
   - `/about` → `app/about/page.tsx`
   - `/compare` → `app/compare/page.tsx`
2. The root shell is always `app/layout.tsx`.
3. Shared UI is in `components/marketing/` for header/footer/hero.
4. Global styling is in `app/globals.css`.

### How to debug CSS
- Use browser developer tools and inspect the element.
- Look for the class names on the selected element.
- Check which CSS file is applying the rule.
- If a rule is crossed out, a more specific rule is winning.
- Use the search feature in VS Code for the class name.

### How to inspect elements
- Right-click in the browser and choose Inspect (or use F12).
- In the Elements panel, note the `class` attribute.
- In the Styles panel, see which selector and file are active.
- The URL near the selector tells you the source file.

### How to search classes
- Use VS Code search (`Ctrl+Shift+F`) for a class like `section-title`.
- Search in `app/` and `components/` first.
- For class names with `:global`, search the visible class string.

### How to trace components
- Find the route file in `app/`.
- Open the page JSX and follow imported component names.
- Use the component file to locate its CSS module.
- Repeat until you reach the exact component.

### How to avoid breaking layouts
- Edit CSS in small steps.
- Prefer adding overrides instead of changing shared tokens if uncertain.
- Keep text edits separate from layout edits.
- Save and refresh after each change.

### How to confidently explain edits
- Say which file you changed and why.
- Example: "I opened `components/marketing/SiteHeader.module.css` because the header’s background and nav styles are defined there."
- Mention whether it is a component-specific style or a shared global style.
- If asked why, explain the path: `layout.tsx` → shared header → header CSS.

### What teachers usually ask
- "Where do I edit the navbar?" → `components/marketing/site-header.tsx` + `SiteHeader.module.css`
- "Where are the hero styles?" → `components/marketing/HeroSection.module.css`
- "Where is the global button styling?" → `app/globals.css`
- "Why is mobile nav different?" → `MobileTabBar.module.css`

### How to answer when nervous
- Keep the answer short and factual.
- Use the file path and the class name.
- Example: "The hero title uses `.section-title` in `app/globals.css`, and the hero panel layout is in `components/marketing/HeroSection.module.css`."
- If you are unsure, say: "I’ll confirm in the component file." and then verify quickly.

---

## IMPORTANT REMINDERS FOR THIS PROJECT

- The strongest styling rules are in `app/globals.css`.
- Shared components use global classes like `.button`, `.glass-panel`, `.section-title`.
- Component-specific modules use `:global(...)` to style plain class names inside their scoped CSS.
- The mobile nav is separate from the desktop header.
- Responsive behavior is handled with both media queries and container queries.
- If a change affects many pages, edit `app/globals.css`. If it affects one component, edit its module CSS.
- Always save and reload after each edit during live coding.

Good luck with your practical defense!
