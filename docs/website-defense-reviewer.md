# DeviceIQ Custom Website Defense Reviewer

## Project Inspection Summary

### What The Project Actually Is

- This is a Next.js App Router website written in TypeScript and React 19.
- There are no plain `.html` files in the source. The site uses `.tsx` pages and component JSX.
- Styling is a mix of `app/globals.css` plus many route/component CSS modules.
- The real brand in `lib/site.ts` is `DeviceIQ`, while several page comments still say `AI Phone Matchmaker`. That naming mismatch is a real defense topic.

### Core Frontend Techniques Detected

- Semantic layout: `header`, `main`, `footer`, `nav`, `section`, `article`.
- CSS variables for theme tokens, spacing, radii, shadows, and colors.
- Glassmorphism panels with `backdrop-filter`, gradients, and borders.
- CSS Grid for major page structures and card layouts.
- Flexbox for rows, navs, chip groups, and button clusters.
- Responsive breakpoints at `1180px`, `1024px`, `768px`, `560px`, and `480px`.
- Container queries in the hero, dashboard, and card systems.
- Animated states: hover lift, shimmer loaders, cursor aura, theme modal, and loading overlays.

### Likely Weak Spots In Live Defense

- `app/globals.css` repeats some selectors and media-query blocks, so specificity and override order can be questioned.
- Several pages still use inline `style={{ ... }}` for spacing and layout.
- `InstantNavLink` uses a `button` for navigation, which is convenient but not as semantic as a link.
- `ContactPage` is UI-only and does not actually submit data yet.
- Phone images use raw `<img>` elements instead of `next/image`.
- Modals and sheets have `role="dialog"`, but focus trapping can still be challenged in questioning.

## Table Of Contents

1. Sticky header and shell
2. Desktop navigation and active routes
3. Mobile tab bar
4. Brand lockup and logo mark
5. Hero section structure
6. Hero metrics and count-up cards
7. Scroll story cards
8. About page semantics
9. Contact form structure
10. Services grid
11. Compare selector form
12. Compare hero and VS badge
13. Compare highlights and score rows
14. Compare spec table
15. Dashboard split layout
16. Dashboard filter controls
17. Dashboard mobile filter sheet
18. Dashboard skeleton loading
19. Device card anatomy
20. Device card hover effects
21. Favorite button states
22. Phone detail hero
23. Phone detail summary grid
24. Phone detail specs table
25. Login and signup sharing
26. Auth validation and session checks
27. Auth config notice
28. Theme toggle launcher and modal
29. Cursor aura effect
30. Global glass panel system
31. Button variants
32. Form fields and labels
33. Responsive typography
34. Responsive grid systems
35. Media query behavior
36. Container queries
37. CSS module scoping with `:global`
38. Duplicate global CSS and override order
39. Background gradients and pseudo-elements
40. Z-index layering and overlays
41. Route loading overlay
42. Instant navigation semantics
43. Gallery redirect
44. Semantic heading hierarchy
45. Accessibility focus states
46. Image handling and alt text
47. Empty states
48. Inline style cleanup
49. Shared styling architecture
50. Brand naming inconsistency

## 1. Sticky Header And Shell

### Instructor Question/Task
Why is the top navigation sticky, and how would you keep it readable over the page background?

### Expected Student Answer
It stays visible with `position: sticky`, a translucent background, blur, and a border so users can navigate without losing context.

### Technical Explanation
The header shell in `components/marketing/SiteHeader.module.css` uses sticky positioning and `backdrop-filter`. That makes the navigation float above the content while still letting the page feel layered.

### Step-by-step Solution
1. Keep the header in the root layout so every page gets the same chrome.
2. Apply sticky positioning and a high `z-index`.
3. Add blur and a border so text remains readable.

### Sample HTML
```html
<header class="site-header">
  <div class="header-inner">
    <nav aria-label="Primary navigation">...</nav>
  </div>
</header>
```

### Sample CSS
```css
.site-header {
  position: sticky;
  top: 0;
  z-index: 50;
  backdrop-filter: blur(14px);
}
```

### Why The Solution Works
The navigation never disappears, and the blur prevents the background gradients from making the text hard to read.

### Common Student Mistakes
- Forgetting `z-index`
- Using an opaque header that kills the glass effect
- Leaving the header out of the shared layout

### Alternative Solutions
- Use `position: fixed` instead of sticky
- Add a stronger solid background instead of blur

### Possible Follow-up Question
Why did you choose sticky instead of fixed?

## 2. Desktop Navigation And Active Routes

### Instructor Question/Task
How does the desktop nav show the current page?

### Expected Student Answer
It checks the current pathname and applies an active class to the matching link.

### Technical Explanation
`SiteHeader.tsx` uses `usePathname()` and an `isActivePath()` helper. The CSS then changes the link color and adds an underline effect.

### Step-by-step Solution
1. Read the current route.
2. Compare it against each nav link.
3. Add an `is-active` class to the correct item.

### Sample HTML
```html
<a class="nav-link is-active" href="/dashboard">Dashboard</a>
```

### Sample CSS
```css
.nav-link.is-active {
  color: var(--text);
}
.nav-link.is-active::after {
  transform: scaleX(1);
}
```

### Why The Solution Works
The user sees immediate route feedback, which improves orientation and trust.

### Common Student Mistakes
- Comparing only exact paths and breaking nested pages
- Forgetting hover and active states should look related

### Alternative Solutions
- Use a router helper component
- Highlight active links with a background chip only

### Possible Follow-up Question
How would you handle nested routes like `/phones/[slug]`?

## 3. Mobile Tab Bar

### Instructor Question/Task
Why does the mobile version use a bottom tab bar instead of the desktop nav?

### Expected Student Answer
Because it gives smaller screens larger touch targets and keeps the main routes reachable by thumb.

### Technical Explanation
`MobileTabBar.tsx` is fixed to the bottom on mobile, hidden on desktop, and uses active-state styling so users know where they are.

### Step-by-step Solution
1. Hide the desktop nav under `768px`.
2. Show a fixed bottom bar.
3. Keep labels short and icons clear.

### Sample HTML
```html
<nav class="mobile-tabbar">
  <a class="mobile-tablink is-active" href="/dashboard">Browse</a>
</nav>
```

### Sample CSS
```css
.mobile-tabbar {
  position: fixed;
  bottom: 16px;
  left: 16px;
  right: 16px;
}
```

### Why The Solution Works
The layout stays usable on phones without forcing users to reach the top of the screen.

### Common Student Mistakes
- Making the bar too tall
- Forgetting safe-area spacing
- Hiding the bar on mobile by accident

### Alternative Solutions
- Use a hamburger menu
- Use a drawer instead of tabs

### Possible Follow-up Question
Why did you keep only five tabs?

## 4. Brand Lockup And Logo Mark

### Instructor Question/Task
Explain the brand area in the header. Why is it built as a reusable component?

### Expected Student Answer
It keeps the logo mark, product name, and subtitle consistent in both header and footer.

### Technical Explanation
`BrandLockup.tsx` wraps the mark and text in one link. The CSS builds the small stacked logo using bordered frames and a signal line.

### Step-by-step Solution
1. Put the logo mark in its own component.
2. Reuse the same brand unit in header and footer.
3. Keep the text flexible so the subtitle can change.

### Sample HTML
```html
<a class="brand-lockup" href="/">
  <span class="brand-badge"></span>
  <strong>DeviceIQ</strong>
</a>
```

### Sample CSS
```css
.brand-badge {
  width: 42px;
  height: 42px;
  border: 1px solid var(--border);
  border-radius: 14px;
}
```

### Why The Solution Works
One source for branding prevents visual drift between pages.

### Common Student Mistakes
- Making the logo decorative but not clickable
- Using different text treatments in different places

### Alternative Solutions
- Use an SVG logo
- Use text-only branding with no mark

### Possible Follow-up Question
Why not keep the logo markup directly in the header?

## 5. Hero Section Structure

### Instructor Question/Task
Walk me through the homepage hero and explain why it is split into two columns.

### Expected Student Answer
The hero uses a strong message on the left and a product preview on the right so the first screen explains the site immediately.

### Technical Explanation
`HeroSection.tsx` combines the main heading, CTA buttons, story cards, and a signature comparison preview. The layout is asymmetric because the text needs more room than the visual theater.

### Step-by-step Solution
1. Put the value proposition first.
2. Place the CTAs immediately under the text.
3. Add a preview card area to show what the app does.

### Sample HTML
```html
<section class="hero-grid">
  <div class="hero-panel">...</div>
  <div class="hero-stack">...</div>
</section>
```

### Sample CSS
```css
.hero-grid {
  display: grid;
  grid-template-columns: minmax(0, 1.15fr) minmax(320px, 0.85fr);
}
```

### Why The Solution Works
The user understands the website value in one glance instead of reading a long intro.

### Common Student Mistakes
- Making both columns equal when the text needs more emphasis
- Overcrowding the hero with too many calls to action

### Alternative Solutions
- Use a single-column hero with a stacked preview
- Replace the right column with a screenshot

### Possible Follow-up Question
Why did you use motion in the hero?

## 6. Hero Metrics And Count-Up Cards

### Instructor Question/Task
How do the number cards in the hero work, and why do they animate?

### Expected Student Answer
They count up to show the catalog feels alive and to make the stats easier to notice.

### Technical Explanation
`CountMetric` in `HeroSection.tsx` uses `requestAnimationFrame` and easing. The cards are simple HTML blocks with labels and values.

### Step-by-step Solution
1. Create a metric card component.
2. Animate the number from 0 to the final value.
3. Keep the animation subtle so it supports the content.

### Sample HTML
```html
<div class="hero-stat-card">
  <span>Phones</span>
  <strong>120</strong>
</div>
```

### Sample CSS
```css
.hero-stat-card {
  padding: 14px 16px;
  border-radius: 20px;
}
```

### Why The Solution Works
It adds energy without changing the structure or making the hero noisy.

### Common Student Mistakes
- Animating too fast
- Making the metric larger than the headline

### Alternative Solutions
- Use static stats
- Use a simple fade-in instead of count-up

### Possible Follow-up Question
What would you do if the numbers changed often?

## 7. Scroll Story Cards

### Instructor Question/Task
Why does the homepage have a "scroll story" section?

### Expected Student Answer
It tells the problem-solution narrative in small cards so the website feels guided instead of random.

### Technical Explanation
The story strip in `app/page.tsx` uses a responsive grid and animated cards. Each card introduces one stage: problem, chaos, solution, and power.

### Step-by-step Solution
1. Break the user journey into stages.
2. Use one small card per stage.
3. Stack the cards on smaller screens.

### Sample HTML
```html
<article class="story-card">
  <span>01</span>
  <h3>Problem</h3>
</article>
```

### Sample CSS
```css
.story-card {
  padding: 22px;
  border-radius: 20px;
}
```

### Why The Solution Works
Users can read the site like a story, which makes the product easier to explain in a defense.

### Common Student Mistakes
- Writing too much copy in each card
- Forgetting the cards need to collapse on mobile

### Alternative Solutions
- Use icons instead of numbered cards
- Turn the story into a horizontal timeline

### Possible Follow-up Question
How would you make this section more accessible?

## 8. About Page Semantics

### Instructor Question/Task
Why did you use a `section` with cards instead of random `div`s on the About page?

### Expected Student Answer
Because the page has one clear topic and the cards separate the mission from the project principles.

### Technical Explanation
`app/about/page.tsx` uses a semantic `section`, a heading, and an unordered list for the values. That makes the structure easier for screen readers and instructors to follow.

### Step-by-step Solution
1. Wrap the page in a `section`.
2. Use one main heading.
3. Put the principles in a list.

### Sample HTML
```html
<section>
  <h1>Built for a cleaner phone search.</h1>
  <ul>
    <li>Compare faster.</li>
  </ul>
</section>
```

### Sample CSS
```css
.marketing-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
```

### Why The Solution Works
The structure mirrors the content, so the page is easy to defend and easy to read.

### Common Student Mistakes
- Using multiple unrelated headings
- Putting list content inside plain paragraphs

### Alternative Solutions
- Use cards with icons
- Turn the values into a checklist

### Possible Follow-up Question
Why did you keep the About page static?

## 9. Contact Page Structure

### Instructor Question/Task
Explain the Contact page layout and what is missing if this were production-ready.

### Expected Student Answer
The left side gives contact info and the right side gives a feedback form, but the form is currently UI-only.

### Technical Explanation
`app/contact/page.tsx` uses fields with labels and a text area. It looks complete visually, but there is no submit handler yet, so it is a placeholder for future backend work.

### Step-by-step Solution
1. Keep the contact details separate from the form.
2. Add labels to every input.
3. If needed, connect the button to a real submit endpoint later.

### Sample HTML
```html
<div class="field">
  <label for="email">Email</label>
  <input id="email" class="input" />
</div>
```

### Sample CSS
```css
.field {
  display: grid;
  gap: 10px;
}
```

### Why The Solution Works
The layout is simple and readable, even if the form still needs real submission logic.

### Common Student Mistakes
- Leaving out `label` elements
- Forgetting the form does nothing yet

### Alternative Solutions
- Convert it into a mailto link
- Replace the form with a support card

### Possible Follow-up Question
What would you add before deploying this page for real users?

## 10. Services Grid

### Instructor Question/Task
Why does the Services page use an asymmetric grid?

### Expected Student Answer
The featured compare card needs more space because it is the signature experience, while the other two cards support it.

### Technical Explanation
`app/services/page.tsx` and `app/services/page.module.css` use a 1.35fr / 1fr / 1fr layout. That makes the featured tool visually dominant without hiding the others.

### Step-by-step Solution
1. Make the most important card larger.
2. Keep supporting cards smaller and lighter.
3. Stack everything on narrow screens.

### Sample HTML
```html
<div class="services-grid">
  <article class="service-card service-card-featured">...</article>
</div>
```

### Sample CSS
```css
.services-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr 1fr;
}
```

### Why The Solution Works
The visual hierarchy matches the product hierarchy.

### Common Student Mistakes
- Making every card equal even when one tool matters more
- Forgetting the grid should collapse on tablets

### Alternative Solutions
- Use a masonry-style layout
- Put the featured card on top instead of left

### Possible Follow-up Question
Why is Compare treated as the lead tool?

## 11. Compare Selector Form

### Instructor Question/Task
How does the comparison selector work, and why is it a form?

### Expected Student Answer
It uses a form because the selected left and right phones are submitted together and the URL updates with query parameters.

### Technical Explanation
The compare page renders two `<select>` elements and a submit button. When the form submits, the route reads `left` and `right` from the search params and builds the comparison.

### Step-by-step Solution
1. Build two select fields.
2. Submit both values together.
3. Use the query string to keep the comparison shareable.

### Sample HTML
```html
<form class="compare-selector-grid">
  <select name="left"></select>
  <select name="right"></select>
</form>
```

### Sample CSS
```css
.compare-selector-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
```

### Why The Solution Works
The comparison can be bookmarked or shared because the selection lives in the URL.

### Common Student Mistakes
- Forgetting the `name` attributes
- Using buttons without a form context

### Alternative Solutions
- Use radio cards instead of selects
- Use a modal picker

### Possible Follow-up Question
How would you prevent invalid pair selections?

## 12. Compare Hero And VS Badge

### Instructor Question/Task
Why does the compare hero place the two phones side by side with a centered VS badge?

### Expected Student Answer
It visually reinforces the comparison idea and makes the two devices feel balanced.

### Technical Explanation
The hero section uses a two-column grid and an absolutely positioned badge in the center. On mobile, the badge shifts lower so the cards do not overlap awkwardly.

### Step-by-step Solution
1. Create two equal phone panels.
2. Position the VS circle in the center.
3. Reposition it on smaller screens.

### Sample HTML
```html
<div class="compare-hero-card">
  <article class="compare-phone-hero">A</article>
  <div class="compare-versus-badge">VS</div>
  <article class="compare-phone-hero">B</article>
</div>
```

### Sample CSS
```css
.compare-versus-badge {
  position: absolute;
  left: 50%;
  top: 50%;
}
```

### Why The Solution Works
The page instantly communicates "A vs B" without needing extra explanation.

### Common Student Mistakes
- Making the badge too large
- Forgetting to change its position on mobile

### Alternative Solutions
- Put a vertical divider between the cards
- Use a top-centered comparison label

### Possible Follow-up Question
Why not make the hero a single wide table?

## 13. Compare Highlights And Score Rows

### Instructor Question/Task
How do the highlight cards and score snapshot support the comparison?

### Expected Student Answer
They give a quick summary of the strengths and winning values before the user reads the detailed spec table.

### Technical Explanation
The compare page separates human-readable reasons from the structured score rows. That keeps the page from feeling like a raw spec dump.

### Step-by-step Solution
1. Show summary highlights first.
2. Show score rows next.
3. Send detailed specs below that.

### Sample HTML
```html
<ul class="insight-list">
  <li>Better battery</li>
</ul>
```

### Sample CSS
```css
.insight-list li {
  padding: 14px 16px;
  border-radius: 18px;
}
```

### Why The Solution Works
The page reduces decision fatigue by moving from summary to detail.

### Common Student Mistakes
- Putting the detailed table before the summary
- Overusing badges so the page feels noisy

### Alternative Solutions
- Use a chart instead of score rows
- Convert highlights into icons

### Possible Follow-up Question
How would you make the winner state more obvious without adding more color?

## 14. Compare Spec Table

### Instructor Question/Task
Show me how the compare table stays readable on desktop and mobile.

### Expected Student Answer
It uses a three-column table on desktop and collapses each row into a stacked card on mobile.

### Technical Explanation
`app/compare/page.module.css` hides the header row on small screens, changes the row grid to one column, and reveals the device name inside each value cell.

### Step-by-step Solution
1. Build the three-column comparison table.
2. Highlight the winning values.
3. Collapse each row into a single stacked card on mobile.

### Sample HTML
```html
<div class="compare-table-row">
  <div class="compare-label-cell">Battery</div>
  <div class="compare-value-cell">5000 mAh</div>
  <div class="compare-value-cell">4800 mAh</div>
</div>
```

### Sample CSS
```css
.compare-table-row {
  display: grid;
  grid-template-columns: minmax(180px, 0.8fr) repeat(2, minmax(0, 1fr));
}
```

### Why The Solution Works
The same information works at different screen widths without losing context.

### Common Student Mistakes
- Keeping the desktop grid on mobile
- Forgetting to label which value belongs to which phone

### Alternative Solutions
- Use a horizontal scroll table
- Use stacked definition lists instead

### Possible Follow-up Question
How do you decide which values are winners?

## 15. Dashboard Split Layout

### Instructor Question/Task
Why does the dashboard use a sidebar on desktop and a stack on smaller screens?

### Expected Student Answer
Because filters need space on large screens, but on mobile they would waste space, so they move into a more compact flow.

### Technical Explanation
`MatchmakerDashboard.tsx` uses a left filter column and a right results stack. The CSS collapses that into one column below `1024px`.

### Step-by-step Solution
1. Keep filters visible on desktop.
2. Keep results dominant.
3. Stack everything on smaller screens.

### Sample HTML
```html
<div class="dashboard-layout">
  <aside class="sidebar"></aside>
  <section class="results-stack"></section>
</div>
```

### Sample CSS
```css
.dashboard-layout {
  display: grid;
  grid-template-columns: minmax(290px, 340px) minmax(0, 1fr);
}
```

### Why The Solution Works
It gives the catalog room to breathe while keeping filters within easy reach.

### Common Student Mistakes
- Letting the sidebar become too wide
- Forgetting to remove the sticky behavior on mobile

### Alternative Solutions
- Use an off-canvas sidebar
- Put filters above the results

### Possible Follow-up Question
Why is the sidebar sticky?

## 16. Dashboard Filter Controls

### Instructor Question/Task
How do the dashboard filters work, and why are they reusable?

### Expected Student Answer
They are reusable select fields that filter by brand, price, performance, camera, and battery.

### Technical Explanation
The dashboard uses one shared filter body for desktop and mobile. That keeps the UI consistent and prevents two different filter implementations from drifting apart.

### Step-by-step Solution
1. Create one filter component.
2. Pass it the current state and setter.
3. Reuse it in both desktop and mobile shells.

### Sample HTML
```html
<label for="brand">Brand</label>
<select id="brand" class="select"></select>
```

### Sample CSS
```css
.select {
  width: 100%;
  padding: 13px 14px;
  border-radius: 18px;
}
```

### Why The Solution Works
One filter source means one place to debug and one visual style to defend.

### Common Student Mistakes
- Duplicating filter markup in different places
- Forgetting the reset button state

### Alternative Solutions
- Use checkbox groups
- Use chips for quick filters

### Possible Follow-up Question
How would you persist filters across reloads?

## 17. Dashboard Mobile Filter Sheet

### Instructor Question/Task
Why does the dashboard open filters in a sheet on mobile?

### Expected Student Answer
Because it keeps the page readable while still giving users a comfortable place to edit filters.

### Technical Explanation
The mobile sheet is a centered dialog overlay. It reuses the same filter body and closes when the user taps the backdrop or the close button.

### Step-by-step Solution
1. Hide the desktop sidebar on smaller screens.
2. Open a dialog when the user taps Filters.
3. Reuse the same filter controls inside the dialog.

### Sample HTML
```html
<div class="sheet-overlay">
  <div class="sheet-panel" role="dialog">...</div>
</div>
```

### Sample CSS
```css
.sheet-overlay {
  position: fixed;
  inset: 0;
  display: grid;
  place-items: center;
}
```

### Why The Solution Works
It protects horizontal space and makes the controls touch-friendly.

### Common Student Mistakes
- Forgetting the backdrop click handler
- Letting the panel grow too tall without scrolling

### Alternative Solutions
- Use a slide-up drawer
- Use a full-screen filter page

### Possible Follow-up Question
How would you add focus trapping?

## 18. Dashboard Skeleton Loading

### Instructor Question/Task
Why did you build a skeleton loader instead of a blank loading screen?

### Expected Student Answer
Because it shows the layout immediately and makes loading feel faster.

### Technical Explanation
The dashboard loading state mirrors the real layout with skeleton lines, media blocks, and card placeholders. That reduces layout shift and gives users a preview of the page structure.

### Step-by-step Solution
1. Match the skeleton structure to the real layout.
2. Animate the shimmer effect.
3. Hide it from screen readers with `aria-hidden`.

### Sample HTML
```html
<div class="phone-card phone-card-skeleton" aria-hidden="true"></div>
```

### Sample CSS
```css
.skeleton-line::after {
  animation: shimmer 1.2s infinite;
}
```

### Why The Solution Works
The user sees the page forming instead of staring at empty space.

### Common Student Mistakes
- Making the skeleton unrelated to the final layout
- Forgetting to keep it non-interactive

### Alternative Solutions
- Use a spinner
- Use static loading text

### Possible Follow-up Question
Why is skeleton loading usually better than a spinner?

## 19. Device Card Anatomy

### Instructor Question/Task
Break down the phone card structure for me.

### Expected Student Answer
It has a top row, score strip, image, headline, quick chips, stat bars, detail chips, and action buttons.

### Technical Explanation
`DeviceCard.tsx` is a self-contained card that shows the important purchase info and actions in one place so the dashboard stays self-sufficient.

### Step-by-step Solution
1. Put the segment badge and favorite button at the top.
2. Show price and score quickly.
3. Add the image, chips, stats, and actions below.

### Sample HTML
```html
<article class="phone-card">
  <div class="phone-card-top">...</div>
  <div class="phone-media">...</div>
</article>
```

### Sample CSS
```css
.phone-card {
  display: grid;
  gap: 18px;
  padding: 20px;
}
```

### Why The Solution Works
The user can scan the card in a few seconds and decide what to do next.

### Common Student Mistakes
- Putting too much text under the title
- Hiding the action buttons too deep

### Alternative Solutions
- Use a compact list view
- Use a denser product card

### Possible Follow-up Question
Why are the chips and stat bars both present?

## 20. Device Card Hover Effects

### Instructor Question/Task
How does the card hover effect work without breaking the layout?

### Expected Student Answer
The card changes transform, shadow, and glow on hover, but the underlying grid stays the same.

### Technical Explanation
The card uses CSS variables for pointer position and a 3D hover transform. The glow is decorative, so it does not interfere with the content.

### Step-by-step Solution
1. Track pointer position on fine pointers only.
2. Update CSS variables for tilt and glow.
3. Reset the values when the pointer leaves.

### Sample HTML
```html
<article class="phone-card">
  <div class="phone-card-glow" aria-hidden="true"></div>
</article>
```

### Sample CSS
```css
.phone-card:hover {
  transform: perspective(1100px) translateY(-6px);
}
```

### Why The Solution Works
The effect feels premium, but it still respects touch devices and keeps the card readable.

### Common Student Mistakes
- Animating width or height instead of transform
- Keeping the effect active on touch devices

### Alternative Solutions
- Use a simple shadow lift only
- Add a scale effect without tilt

### Possible Follow-up Question
Why did you hide the cursor aura on mobile?

## 21. Favorite Button States

### Instructor Question/Task
How does the Favorite button communicate saved, pending, and unsaved states?

### Expected Student Answer
It changes icon fill, label text, and disabled state depending on whether the phone is saved or still updating.

### Technical Explanation
`FavoriteButton.tsx` reads from the favorites provider and updates its own UI. The CSS turns the saved state into an accent pill with a softer background.

### Step-by-step Solution
1. Read favorite state from the provider.
2. Show "Save" or "Saved".
3. Disable the control while the request is pending.

### Sample HTML
```html
<button class="favorite-button" aria-pressed="true">
  <span>Saved</span>
</button>
```

### Sample CSS
```css
.favorite-button.active {
  background: var(--accent-soft);
  color: var(--accent);
}
```

### Why The Solution Works
The user gets instant feedback and can tell when the action is already applied.

### Common Student Mistakes
- Forgetting `aria-pressed`
- Letting users click repeatedly during loading

### Alternative Solutions
- Use a bookmark icon only
- Use a toast message after saving

### Possible Follow-up Question
How would you show favorite counts per route?

## 22. Phone Detail Hero

### Instructor Question/Task
Explain the phone detail hero layout and how it differs from the dashboard card.

### Expected Student Answer
It gives one phone a large media block, a title, chips, summary metrics, and action buttons because the page is about depth, not browsing.

### Technical Explanation
`app/phones/[slug]/page.tsx` turns the selected phone into a larger editorial layout. The image and the specs are separated so the top of the page feels like a product spotlight.

### Step-by-step Solution
1. Show the image first.
2. Add the title and summary chips.
3. Place actions after the summary so they are easy to find.

### Sample HTML
```html
<div class="phone-detail-hero">
  <div class="phone-detail-media"></div>
  <div class="stack"></div>
</div>
```

### Sample CSS
```css
.phone-detail-hero {
  display: grid;
  grid-template-columns: minmax(260px, 360px) minmax(0, 1fr);
}
```

### Why The Solution Works
The layout makes one device feel important and easy to evaluate.

### Common Student Mistakes
- Making the hero too small
- Putting the action buttons before the summary

### Alternative Solutions
- Use a centered single-column hero
- Put the specs in a side panel

### Possible Follow-up Question
Why did you keep the summary chips separate from the spec table?

## 23. Phone Detail Summary Grid

### Instructor Question/Task
How does the summary metric grid help the phone detail page?

### Expected Student Answer
It gives fast facts like display, chipset, and battery before the user scrolls into the full spec list.

### Technical Explanation
The detail page maps over `reference.summary` and renders metric blocks only when values exist. That keeps the hero compact and avoids empty boxes.

### Step-by-step Solution
1. Gather the summary fields.
2. Remove empty values.
3. Render only the metrics that exist.

### Sample HTML
```html
<div class="detail-summary-grid">
  <div class="metric"><span>Display</span><strong>6.8"</strong></div>
</div>
```

### Sample CSS
```css
.detail-summary-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
}
```

### Why The Solution Works
The grid adapts to the amount of data without looking broken.

### Common Student Mistakes
- Showing empty summary cards
- Overcrowding the hero with too many values

### Alternative Solutions
- Use a compact list instead of cards
- Show the metrics in a sidebar

### Possible Follow-up Question
What happens if the reference data is incomplete?

## 24. Phone Detail Specs Table

### Instructor Question/Task
Why is the spec table split into section titles and rows?

### Expected Student Answer
Because the phone detail page has a lot of information, and section grouping makes it easier to scan.

### Technical Explanation
The specs page uses a two-column section grid with a labeled section title on the left and rows on the right. On mobile, the layout collapses to one column.

### Step-by-step Solution
1. Group related specs under one category.
2. Use rows for label/value pairs.
3. Stack them on mobile.

### Sample HTML
```html
<section class="specs-section">
  <div class="specs-section-title">Battery</div>
  <div class="spec-row"><div>Capacity</div><div>5000 mAh</div></div>
</section>
```

### Sample CSS
```css
.specs-section {
  display: grid;
  grid-template-columns: 220px minmax(0, 1fr);
}
```

### Why The Solution Works
The hierarchy is obvious, so users do not get lost in a wall of text.

### Common Student Mistakes
- Using the same weight for labels and values
- Forgetting to stack the sections on mobile

### Alternative Solutions
- Use a definition list
- Use accordion sections

### Possible Follow-up Question
Why did you choose a table-like structure instead of cards?

## 25. Login And Signup Sharing

### Instructor Question/Task
Why do login and signup share the same form component?

### Expected Student Answer
Because both pages have the same layout and mostly the same fields, so one reusable component avoids duplication.

### Technical Explanation
`AuthForm.tsx` switches content based on `mode`. Signup includes the name field, while login skips it. The rest of the form, spacing, and button styling stay the same.

### Step-by-step Solution
1. Create a shared auth component.
2. Pass the mode as a prop.
3. Change the copy, fields, and links based on that mode.

### Sample HTML
```html
<div class="auth-card">
  <form class="stack">...</form>
</div>
```

### Sample CSS
```css
.auth-card {
  width: min(100%, 560px);
  padding: clamp(22px, 4vw, 32px);
}
```

### Why The Solution Works
The UI stays consistent and maintenance is easier.

### Common Student Mistakes
- Copy-pasting two separate auth layouts
- Forgetting the callback URL flow

### Alternative Solutions
- Split login and signup into two components
- Use a single modal instead of pages

### Possible Follow-up Question
Why is the signup page slightly different from login?

## 26. Auth Validation And Session Checks

### Instructor Question/Task
Explain the session check after sign-in. Why not redirect immediately?

### Expected Student Answer
Because the form verifies that the session really exists before redirecting, which avoids a false login state.

### Technical Explanation
The auth flow performs credentials sign-in and then polls `/api/auth/session` to confirm that the session cookie is active. That prevents the UI from moving too early.

### Step-by-step Solution
1. Submit the form.
2. Attempt sign-in.
3. Verify the session endpoint before redirecting.

### Sample HTML
```html
<button type="submit" class="button auth-submit">Log in</button>
```

### Sample CSS
```css
.auth-submit {
  width: 100%;
}
```

### Why The Solution Works
It protects the user from being sent forward before the account is actually authenticated.

### Common Student Mistakes
- Redirecting after the first response only
- Not showing an error when the session check fails

### Alternative Solutions
- Redirect and then let the destination page confirm auth
- Use server actions for the whole flow

### Possible Follow-up Question
What would you do if the session endpoint is slow?

## 27. Auth Config Notice

### Instructor Question/Task
What happens if the auth secret is missing?

### Expected Student Answer
The page shows a friendly setup notice instead of crashing the form.

### Technical Explanation
`AuthConfigNotice.tsx` is the fallback UI when authentication is not configured. It keeps the public dashboard accessible and explains what needs to be fixed.

### Step-by-step Solution
1. Check whether auth is configured.
2. If not, render a notice component.
3. Give the user a safe path back to the dashboard.

### Sample HTML
```html
<div class="auth-card">
  <h1>Authentication is not configured yet.</h1>
</div>
```

### Sample CSS
```css
.auth-message-error {
  border-color: color-mix(in srgb, var(--danger) 34%, transparent);
}
```

### Why The Solution Works
The site stays usable even when the environment is incomplete.

### Common Student Mistakes
- Showing a blank page
- Exposing a raw error stack to users

### Alternative Solutions
- Hide auth pages entirely
- Show a maintenance banner

### Possible Follow-up Question
Why is graceful failure important in a defense demo?

## 28. Theme Toggle Launcher And Modal

### Instructor Question/Task
Why is the theme picker a floating button with a modal instead of a simple switch in the header?

### Expected Student Answer
Because the site offers more than light and dark mode. It also lets the user browse preset themes in one focused panel.

### Technical Explanation
`ThemeToggle.tsx` opens a centered dialog, locks body scroll, supports Escape to close, and lets the user edit light and dark presets separately.

### Step-by-step Solution
1. Place a floating launcher on every page.
2. Open a modal when the user clicks it.
3. Let the user search and choose theme presets inside the modal.

### Sample HTML
```html
<button class="theme-launcher">Theme</button>
<div class="theme-modal-backdrop" role="dialog"></div>
```

### Sample CSS
```css
.theme-launcher {
  position: fixed;
  right: 24px;
  bottom: 24px;
}
```

### Why The Solution Works
The theme controls are always reachable, but they do not clutter the main navigation.

### Common Student Mistakes
- Forgetting to close the modal on route change
- Not locking scroll behind the modal

### Alternative Solutions
- Put theme controls inside the header
- Use a dropdown instead of a modal

### Possible Follow-up Question
How would you improve keyboard accessibility in this modal?

## 29. Cursor Aura Effect

### Instructor Question/Task
Why does the site show a cursor aura on desktop only?

### Expected Student Answer
Because the effect depends on a fine pointer, and mobile users do not have the same hover behavior.

### Technical Explanation
`CursorAura.tsx` tracks pointer movement and feeds CSS variables into a fixed blurred glow. It is disabled on coarse pointers so it does not waste performance or create clutter on mobile.

### Step-by-step Solution
1. Detect a fine pointer.
2. Update the glow position on pointer move.
3. Hide the effect when the pointer leaves the window.

### Sample HTML
```html
<div class="cursor-aura" aria-hidden="true"></div>
```

### Sample CSS
```css
.cursor-aura {
  position: fixed;
  width: 520px;
  height: 520px;
}
```

### Why The Solution Works
The glow adds polish without interfering with content or touch usability.

### Common Student Mistakes
- Leaving it visible on phones
- Letting it cover the text layer

### Alternative Solutions
- Remove the effect entirely
- Use a static ambient background instead

### Possible Follow-up Question
Is this effect decorative or functional?

## 30. Global Glass Panel System

### Instructor Question/Task
What is the purpose of the shared `glass-panel` class?

### Expected Student Answer
It gives cards and panels a consistent frosted surface, shadow, and border so the whole site feels unified.

### Technical Explanation
`app/globals.css` defines `.glass-panel` once and many pages build on it. The class uses translucent surfaces, blur, rounded corners, and layered shadows.

### Step-by-step Solution
1. Define the shared panel style in the global file.
2. Reuse it in the homepage, compare page, dashboard, and auth pages.
3. Add route-specific classes on top of it.

### Sample HTML
```html
<article class="glass-panel card">...</article>
```

### Sample CSS
```css
.glass-panel {
  background: var(--surface);
  backdrop-filter: blur(14px);
  border-radius: 28px;
}
```

### Why The Solution Works
One visual system makes the site look intentional, not patched together.

### Common Student Mistakes
- Recreating the same card styles in every file
- Forgetting the border and shadow work together

### Alternative Solutions
- Use flat cards instead of glassmorphism
- Use a lighter editorial style

### Possible Follow-up Question
Why might too much glassmorphism become a problem?

## 31. Button Variants

### Instructor Question/Task
Explain the difference between the primary, secondary, and ghost buttons.

### Expected Student Answer
Primary is for the main action, secondary is for supportive actions, and ghost is the least prominent option.

### Technical Explanation
The global CSS defines `.button`, `.button-secondary`, and `.button-ghost` with different fills, borders, and emphasis levels.

### Step-by-step Solution
1. Use the primary button for the main conversion action.
2. Use secondary buttons for supporting actions.
3. Use ghost buttons for lightweight or optional actions.

### Sample HTML
```html
<a class="button" href="/dashboard">Browse</a>
<a class="button-secondary" href="/compare">Compare</a>
```

### Sample CSS
```css
.button {
  background: var(--accent);
  color: var(--accent-contrast);
}
```

### Why The Solution Works
The visual hierarchy matches the importance of the action.

### Common Student Mistakes
- Making all buttons look equally important
- Using ghost buttons for critical actions

### Alternative Solutions
- Use outline buttons only
- Use filled buttons only for all actions

### Possible Follow-up Question
Why do some buttons also have the magnetic hover effect?

## 32. Form Fields And Labels

### Instructor Question/Task
Why do the form inputs need labels, and why do they have consistent spacing?

### Expected Student Answer
Labels make the form understandable and accessible, while consistent spacing helps the user scan the form faster.

### Technical Explanation
The global `.field`, `.input`, `.select`, and `.textarea` styles create one form system used across contact and auth pages.

### Step-by-step Solution
1. Put the label above the field.
2. Keep widths and padding consistent.
3. Style focus and invalid states clearly.

### Sample HTML
```html
<div class="field">
  <label for="password">Password</label>
  <input id="password" class="input" type="password" />
</div>
```

### Sample CSS
```css
.input,
.select,
.textarea {
  border-radius: 18px;
  padding: 13px 14px;
}
```

### Why The Solution Works
The form feels trustworthy and easy to complete.

### Common Student Mistakes
- Relying on placeholders instead of labels
- Making all fields different sizes

### Alternative Solutions
- Use floating labels
- Use compact inline forms

### Possible Follow-up Question
How do invalid and valid styles help users?

## 33. Responsive Typography

### Instructor Question/Task
How do your headings stay readable on different screen sizes?

### Expected Student Answer
They use `clamp()` so the font size scales smoothly without needing lots of manual breakpoints.

### Technical Explanation
The global stylesheet defines a fluid type scale for sections, features, and body text. That keeps large headings bold on desktop and still readable on small screens.

### Step-by-step Solution
1. Define a fluid font scale.
2. Use the scale for titles and labels.
3. Adjust line height and letter spacing for display headings.

### Sample HTML
```html
<h1 class="section-title">Stop guessing. Start comparing.</h1>
```

### Sample CSS
```css
.section-title {
  font-size: clamp(2.4rem, 5vw, 4.5rem);
  line-height: 0.95;
}
```

### Why The Solution Works
Typography feels consistent across devices instead of jumping at breakpoints.

### Common Student Mistakes
- Using fixed pixel sizes everywhere
- Making every heading the same size

### Alternative Solutions
- Use rem-only sizing
- Use fewer heading levels

### Possible Follow-up Question
Why is line-height so tight on the hero title?

## 34. Responsive Grid Systems

### Instructor Question/Task
Explain how your grids adapt from desktop to mobile.

### Expected Student Answer
The site uses `minmax()` and `auto-fit`, then collapses columns with media queries when needed.

### Technical Explanation
The project combines fixed multi-column grids for structure with auto-fitting grids for cards and summary blocks.

### Step-by-step Solution
1. Choose the right grid pattern for the section.
2. Set minimum widths with `minmax()`.
3. Collapse the grid in mobile breakpoints.

### Sample HTML
```html
<div class="phone-grid">
  <article class="phone-card"></article>
</div>
```

### Sample CSS
```css
.phone-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 280px), 1fr));
}
```

### Why The Solution Works
The layout keeps its shape on wide screens and stays readable on narrow screens.

### Common Student Mistakes
- Hard-coding column counts that fail on small devices
- Forgetting to test card overflow

### Alternative Solutions
- Use Flexbox wrapping
- Use a masonry layout

### Possible Follow-up Question
When would you choose Flexbox instead of Grid here?

## 35. Media Query Behavior

### Instructor Question/Task
What happens at your main breakpoints, and why are they there?

### Expected Student Answer
The dashboard, compare page, header, hero, and card layouts all tighten and stack at specific widths so the content stays usable.

### Technical Explanation
The project uses `1180px`, `1024px`, `768px`, `560px`, and `480px` to progressively simplify the layout. That lets each page stay comfortable on laptop, tablet, and mobile.

### Step-by-step Solution
1. Start with desktop layouts.
2. Reduce columns at tablet widths.
3. Stack or simplify on mobile widths.

### Sample HTML
```html
<div class="marketing-grid">...</div>
```

### Sample CSS
```css
@media (max-width: 768px) {
  .marketing-grid {
    grid-template-columns: 1fr;
  }
}
```

### Why The Solution Works
The page adapts instead of shrinking into unreadable tiny columns.

### Common Student Mistakes
- Using too many breakpoints without a plan
- Leaving the desktop grid intact on mobile

### Alternative Solutions
- Use only container queries
- Use mobile-first min-width queries instead

### Possible Follow-up Question
Why did you mix media queries and container queries?

## 36. Container Queries

### Instructor Question/Task
Why did you use container queries in the hero and dashboard instead of only media queries?

### Expected Student Answer
Because some components need to react to the width of their own container, not the entire screen.

### Technical Explanation
The hero, story strip, feature layout, and phone cards use `container-type: inline-size`. That lets the layout respond to the space available in a section rather than only viewport width.

### Step-by-step Solution
1. Mark the container.
2. Write a query against the container width.
3. Change the component layout inside that container.

### Sample HTML
```html
<section class="home-feature-layout">...</section>
```

### Sample CSS
```css
.home-feature-layout {
  container-type: inline-size;
}
@container (max-width: 900px) {
  .home-feature-layout { grid-template-columns: 1fr; }
}
```

### Why The Solution Works
Components become more reusable because they adapt to their own space.

### Common Student Mistakes
- Forgetting to set `container-type`
- Expecting the query to work on the whole page

### Alternative Solutions
- Use only media queries
- Use component-specific class toggles in JS

### Possible Follow-up Question
Where in this project do container queries help the most?

## 37. CSS Module Scoping With `:global`

### Instructor Question/Task
Why do so many CSS module files use `:global` selectors?

### Expected Student Answer
Because the module scopes only part of the styling, while shared structural classes are still defined globally.

### Technical Explanation
The project often gives a wrapper component a local class and then styles globally named inner elements inside it. That saves duplication, but it also makes the styles more coupled to the markup.

### Step-by-step Solution
1. Keep the wrapper class local.
2. Style the shared child class through `:global`.
3. Be careful not to overuse it.

### Sample HTML
```html
<div class="scope">
  <div class="phone-card-top">...</div>
</div>
```

### Sample CSS
```css
.scope :global(.phone-card-top) {
  display: grid;
}
```

### Why The Solution Works
It lets route-specific modules fine-tune shared markup without rewriting every component.

### Common Student Mistakes
- Using `:global` everywhere and losing the benefit of modules
- Forgetting the local wrapper class

### Alternative Solutions
- Use fully local class names only
- Use BEM-style naming across the whole app

### Possible Follow-up Question
What risk comes from too much `:global` usage?

## 38. Duplicate Global CSS And Override Order

### Instructor Question/Task
I noticed some repeated selectors in `app/globals.css`. How would you explain that?

### Expected Student Answer
The file has foundational rules near the top and later overrides for visual refinement, but the repetition should be cleaned up for maintainability.

### Technical Explanation
There are multiple blocks for `body`, `main`, `.glass-panel`, `.nav-link`, `.phone-grid`, and responsive breakpoints. That works because of cascade order, but it is harder to defend than a cleaner single-source setup.

### Step-by-step Solution
1. Keep base tokens and resets at the top.
2. Move shared component styles into one block.
3. Remove duplicate media-query definitions.

### Sample HTML
```html
<body class="site-shell"></body>
```

### Sample CSS
```css
/* Prefer one glass-panel definition */
.glass-panel { ... }
```

### Why The Solution Works
Cleaner CSS is easier to debug and easier to explain in a defense.

### Common Student Mistakes
- Relying on later overrides without realizing it
- Forgetting which rule is actually winning

### Alternative Solutions
- Split globals into base and utilities files
- Move more styling into CSS modules

### Possible Follow-up Question
If the same selector appears twice, which one wins?

## 39. Background Gradients And Pseudo-Elements

### Instructor Question/Task
What is the purpose of the layered background on `body`?

### Expected Student Answer
It creates depth with gradients, a grid pattern, and a soft glow so the site feels premium instead of flat.

### Technical Explanation
`app/globals.css` uses `body::before` and `body::after` to add a faint grid and blurred ambient light. These layers sit behind the content and do not block interaction.

### Step-by-step Solution
1. Set a base background color.
2. Add layered gradients.
3. Put decorative pseudo-elements behind the content.

### Sample HTML
```html
<body class="site-shell"></body>
```

### Sample CSS
```css
body::before,
body::after {
  content: "";
  position: fixed;
  inset: 0;
}
```

### Why The Solution Works
The background feels richer while the text still remains legible.

### Common Student Mistakes
- Making the decorative layers too strong
- Accidentally covering the content with them

### Alternative Solutions
- Use a flat background
- Use an SVG noise texture instead

### Possible Follow-up Question
Why is `overflow-x: hidden` used on the body?

## 40. Z-Index Layering And Overlays

### Instructor Question/Task
How do you keep the header, mobile tab bar, theme modal, and loading overlays from fighting each other?

### Expected Student Answer
Each layer gets a clear `z-index` strategy so the active overlay appears above the base chrome.

### Technical Explanation
The sticky header, mobile tab bar, theme modal, account sheet, and route overlays all have different stacking values. That prevents the modal from hiding behind the header or tab bar.

### Step-by-step Solution
1. Assign a low-but-consistent z-index to persistent chrome.
2. Assign higher values to overlays and dialogs.
3. Test the stack on mobile and desktop.

### Sample HTML
```html
<div class="theme-modal-backdrop"></div>
<nav class="mobile-tabbar"></nav>
```

### Sample CSS
```css
.theme-modal-backdrop { z-index: 120; }
.mobile-tabbar { z-index: 45; }
```

### Why The Solution Works
Users always interact with the layer they expect to be on top.

### Common Student Mistakes
- Giving everything a huge `z-index`
- Not testing overlays with fixed nav elements

### Alternative Solutions
- Use a dedicated z-index scale in variables
- Render overlays in a portal

### Possible Follow-up Question
What bug would happen if the tab bar had a higher z-index than the modal?

## 41. Route Loading Overlay

### Instructor Question/Task
What is `InstantNavLink`, and why does it show a loading overlay?

### Expected Student Answer
It is a custom navigation helper that prefetches a route and shows feedback while the route is being opened.

### Technical Explanation
`InstantNavLink.tsx` uses `router.prefetch()` and `router.push()` inside a transition, then displays a loading card. It is useful for the dashboard because that route does more work than the others.

### Step-by-step Solution
1. Prefetch the target route.
2. Start a transition on click.
3. Show a short loading state while navigation happens.

### Sample HTML
```html
<button type="button" class="button">Browse phones</button>
<div class="route-loading-overlay"></div>
```

### Sample CSS
```css
.route-loading-overlay {
  position: fixed;
  inset: 0;
}
```

### Why The Solution Works
The user gets immediate feedback instead of wondering whether the click registered.

### Common Student Mistakes
- Using a button when a link is more semantic and not explaining why
- Forgetting to skip navigation when already on the same route

### Alternative Solutions
- Use a plain `Link` with no overlay
- Add a global page loader only

### Possible Follow-up Question
Why would an instructor question the use of a button here?

## 42. Instant Navigation Semantics

### Instructor Question/Task
Why might the `InstantNavLink` component be questioned in a defense?

### Expected Student Answer
Because it behaves like a link but is implemented as a button, so the semantics deserve an explanation.

### Technical Explanation
The component is a navigation control with prefetch and overlay behavior. It works well, but from an HTML perspective a real anchor is usually more semantic for navigation.

### Step-by-step Solution
1. Decide whether the element is a link or an action.
2. If it navigates, prefer an anchor when possible.
3. If extra behavior is required, explain why the wrapper exists.

### Sample HTML
```html
<a href="/dashboard" class="button">Browse phones</a>
```

### Sample CSS
```css
.button {
  display: inline-flex;
  align-items: center;
}
```

### Why The Solution Works
The markup matches the user intent more clearly.

### Common Student Mistakes
- Treating all clickable things as buttons
- Ignoring keyboard and screen reader expectations

### Alternative Solutions
- Keep the custom component and explain the tradeoff
- Use `Link` with a separate loading UI

### Possible Follow-up Question
How would you preserve the loading overlay while keeping anchor semantics?

## 43. Gallery Redirect

### Instructor Question/Task
Why does the gallery page immediately redirect to the dashboard?

### Expected Student Answer
Because the dashboard replaced the old browsing experience, and the redirect preserves old links without keeping duplicate UI.

### Technical Explanation
`app/gallery/page.tsx` calls `redirect("/dashboard")`. It is a clean compatibility layer and reduces route clutter.

### Step-by-step Solution
1. Keep the old route alive.
2. Redirect it to the new canonical route.
3. Avoid rendering a duplicate page.

### Sample HTML
```html
<!-- No page UI; redirect only -->
```

### Sample CSS
```css
/* None needed */
```

### Why The Solution Works
Old links still work, but the app keeps one browsing destination.

### Common Student Mistakes
- Leaving old pages alive forever
- Building duplicate layouts for the same feature

### Alternative Solutions
- Show a deprecation message
- Keep an alias page with a notice

### Possible Follow-up Question
Why is route cleanup important in a growing app?

## 44. Semantic Heading Hierarchy

### Instructor Question/Task
How do you keep heading levels organized across the site?

### Expected Student Answer
Each page starts with one main heading and then moves to smaller headings for sections and cards.

### Technical Explanation
The site uses `h1` for page titles, `h2` for section groups, and `h3` for card titles. That keeps the outline easy to follow both visually and semantically.

### Step-by-step Solution
1. Reserve `h1` for the page-level topic.
2. Use `h2` for section blocks.
3. Use `h3` for cards or feature titles.

### Sample HTML
```html
<h1 class="section-title">Built for a cleaner phone search.</h1>
<h2 class="feature-title">Three tools, one clear decision flow.</h2>
```

### Sample CSS
```css
.section-title, .feature-title {
  font-family: var(--font-display), sans-serif;
}
```

### Why The Solution Works
The content outline mirrors the page structure.

### Common Student Mistakes
- Using multiple h1s without a reason
- Skipping heading levels

### Alternative Solutions
- Use fewer heading levels on simpler pages
- Use `h2` cards inside a smaller page

### Possible Follow-up Question
Why is heading order important for accessibility?

## 45. Accessibility Focus States

### Instructor Question/Task
How do users who keyboard-navigate know where they are?

### Expected Student Answer
The site adds visible focus states to important links, buttons, and form controls.

### Technical Explanation
The global CSS uses `:focus-visible` on key interactive elements. That keeps the focus ring available for keyboard users without showing it constantly during mouse use.

### Step-by-step Solution
1. Style focus only when it is visible.
2. Keep the outline color consistent with the theme.
3. Test tab order across header, cards, forms, and dialogs.

### Sample HTML
```html
<a class="nav-link" href="/compare">Compare</a>
```

### Sample CSS
```css
.nav-link:focus-visible {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}
```

### Why The Solution Works
Keyboard users get a clear map of where they are on the page.

### Common Student Mistakes
- Removing outlines globally
- Using a focus color that is too subtle

### Alternative Solutions
- Use a background highlight instead of an outline
- Use a thicker underline for focus

### Possible Follow-up Question
Why use `:focus-visible` instead of `:focus`?

## 46. Image Handling And Alt Text

### Instructor Question/Task
Why do the cards and detail pages use `alt` text, and what would you improve about the image handling?

### Expected Student Answer
Alt text makes the image understandable to assistive tech, and the current code could still be improved by using `next/image` for optimization.

### Technical Explanation
The project uses `<img>` with meaningful `alt` text on product images and placeholders when no image exists. That is semantically correct, but it still leaves room for better image optimization.

### Step-by-step Solution
1. Always provide descriptive alt text.
2. Use a fallback when no image exists.
3. Consider `next/image` later if optimization is needed.

### Sample HTML
```html
<img src="/phone.jpg" alt="Galaxy S24 Ultra" />
```

### Sample CSS
```css
.phone-media img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
```

### Why The Solution Works
The content remains understandable even if the image fails to load.

### Common Student Mistakes
- Using empty alt text for meaningful product images
- Stretching images with no `object-fit`

### Alternative Solutions
- Use `next/image`
- Use an SVG placeholder illustration

### Possible Follow-up Question
Why might the project still choose raw `<img>` right now?

## 47. Empty States

### Instructor Question/Task
How do you handle pages with no favorites or no matching results?

### Expected Student Answer
The site shows a clear empty state and gives the user a next step instead of leaving a blank screen.

### Technical Explanation
Favorites and dashboard results both render `empty-state` panels. That keeps the user from getting stuck when there is no data.

### Step-by-step Solution
1. Detect the empty condition.
2. Show a short message.
3. Provide a button back to browsing.

### Sample HTML
```html
<div class="glass-panel empty-state">
  <p>No phones match the current filters.</p>
</div>
```

### Sample CSS
```css
.empty-state {
  padding: 42px 24px;
  text-align: center;
}
```

### Why The Solution Works
The page still guides the user forward even when there are no results.

### Common Student Mistakes
- Showing nothing at all
- Making the empty state too long and apologetic

### Alternative Solutions
- Add a reset filters button
- Show recommended phones instead

### Possible Follow-up Question
What would you add to the empty favorites state?

## 48. Inline Style Cleanup

### Instructor Question/Task
Why do some pages use inline styles, and what would you improve?

### Expected Student Answer
Inline styles are used for small one-off spacing fixes, but they should be reduced in favor of reusable classes.

### Technical Explanation
Pages like About, Contact, Favorites, Compare, and Auth use inline margins or width tweaks in a few places. That is okay for quick work, but too many inline styles make the code harder to maintain.

### Step-by-step Solution
1. Move repeated spacing to a class.
2. Keep only truly unique one-off styles inline.
3. Reuse the utility classes in global CSS or a module.

### Sample HTML
```html
<div class="stack mt-4"></div>
```

### Sample CSS
```css
.mt-4 {
  margin-top: 24px;
}
```

### Why The Solution Works
The code becomes easier to scan and easier to change later.

### Common Student Mistakes
- Leaving every spacing tweak inline
- Creating too many one-off utility classes

### Alternative Solutions
- Use module classes only
- Use CSS variables for spacing helpers

### Possible Follow-up Question
When is an inline style acceptable in a defense project?

## 49. Shared Styling Architecture

### Instructor Question/Task
How would you explain the split between global CSS and module CSS in this project?

### Expected Student Answer
Global CSS holds the design tokens and shared utilities, while module CSS handles route-specific and component-specific layouts.

### Technical Explanation
`app/globals.css` is the foundation. Modules like `DeviceCard.module.css`, `HeroSection.module.css`, `MatchmakerDashboard.module.css`, and `page.module.css` files customize the specific screens.

### Step-by-step Solution
1. Put reusable tokens and resets in one global file.
2. Put component layouts next to the component.
3. Avoid repeating the same styles in multiple files.

### Sample HTML
```html
<div class="glass-panel card"></div>
```

### Sample CSS
```css
.card {
  padding: 24px;
}
```

### Why The Solution Works
The architecture scales without turning into one giant tangled stylesheet.

### Common Student Mistakes
- Putting everything in globals
- Overusing module overrides instead of shared utilities

### Alternative Solutions
- Use a full design system package
- Split globals into tokens and utilities files

### Possible Follow-up Question
Which styles would you never move into a module?

## 50. Brand Naming Inconsistency

### Instructor Question/Task
Your root site config says `DeviceIQ`, but some comments and docs say `AI Phone Matchmaker`. How would you handle that?

### Expected Student Answer
I would standardize the brand name everywhere so the UI, metadata, comments, and presentation materials all match.

### Technical Explanation
The actual site chrome uses `DeviceIQ`, but the homepage hero and older docs still reference the older label. That is not a layout bug, but it is a real defense question because consistency matters in product design.

### Step-by-step Solution
1. Pick one brand name.
2. Update comments, metadata, and UI copy.
3. Make the presentation script use the same wording.

### Sample HTML
```html
<strong>DeviceIQ</strong>
```

### Sample CSS
```css
.brand-text strong {
  font-family: var(--font-display), sans-serif;
}
```

### Why The Solution Works
Users and instructors see one clear identity instead of two competing names.

### Common Student Mistakes
- Treating naming as unimportant
- Leaving old copy in comments and slides

### Alternative Solutions
- Keep the product name and use the hero tagline only
- Mention both names once and then standardize

### Possible Follow-up Question
If the panel asks which name is final, what would you say?

## Rapid Fire Oral Questions

1. Why use `header`, `main`, and `footer` instead of only `div`?
2. Why is `nav` used in both the top header and mobile bar?
3. Why does the homepage use a story section after the hero?
4. Why is Compare treated as the signature feature?
5. Why does the dashboard have a sidebar on desktop?
6. Why is the dashboard filter sheet hidden on larger screens?
7. Why are CSS variables better than hardcoded colors here?
8. Why did you choose a green accent instead of a random bright color?
9. Why is the site dark by default?
10. Why use `clamp()` for heading sizes?
11. Why do phone cards use Grid and some rows use Flexbox?
12. Why does the mobile tab bar stay fixed to the bottom?
13. Why does `main` need extra bottom padding?
14. Why is the theme launcher floating?
15. Why does the gallery route redirect?
16. Why is the auth flow optional for browsing?
17. Why does the contact form still need backend wiring?
18. Why is the compare table more useful than a plain list?
19. Why are the spec sections grouped by category?
20. Why are favorites protected by authentication?
21. Why does the dashboard skeleton match the real layout?
22. Why is the mobile VS badge repositioned?
23. Why do some pages use `section-copy` and `feature-title`?
24. Why is `:global` used so often in CSS modules?
25. Why is the cursor aura disabled on mobile?
26. Why are the header and footer brand units reusable?
27. Why are some buttons primary and others ghost?
28. Why is the brand name inconsistent in the source right now?
29. Why is `InstantNavLink` more complex than a normal link?
30. Why would an instructor ask you to refactor the global CSS?

## Most Important HTML Concepts To Memorize

- Semantic elements: `header`, `nav`, `main`, `section`, `article`, `footer`.
- Proper heading order: one `h1` per page, then `h2`, `h3`.
- Labels for inputs and selects.
- `alt` text for meaningful images.
- Forms, button types, and anchor links.
- `aria-label`, `aria-expanded`, `aria-pressed`, and `aria-modal`.
- Why navigation should use links when possible.
- Why cards can be articles when they represent standalone content.

## Most Important CSS Concepts To Memorize

- CSS variables for colors, spacing, radii, and shadows.
- Grid versus Flexbox.
- `clamp()` for fluid typography.
- `minmax()` and `auto-fit` for responsive grids.
- `backdrop-filter` for the glass effect.
- `:focus-visible` for keyboard accessibility.
- Media queries and container queries.
- `z-index` stacking order.
- Pseudo-elements like `::before` and `::after`.
- Animation timing and when to keep motion subtle.

## Most Common Live Coding Tasks

- Stack a two-column section on mobile.
- Fix a sticky header overlap.
- Convert a card row from Flexbox to Grid.
- Add a hover effect without moving the layout.
- Clean up spacing in a form.
- Improve the active state of a nav link.
- Turn a blank loading screen into a skeleton.
- Rework a compare table for small screens.
- Center a modal and close it with a backdrop click.
- Simplify a global class that is being repeated too much.

## Emergency Debugging Checklist

1. Check the route name first.
2. Verify the HTML structure and heading order.
3. Inspect the applied CSS class names.
4. Check whether a media query is overriding the style.
5. Check `z-index` if something is hidden.
6. Check `overflow` if content is clipped.
7. Check `display` and `position` if alignment breaks.
8. Check whether the page is using the right wrapper class.
9. Confirm whether the mobile layout is hiding the desktop version.
10. Reload after changing the theme or modal state if needed.

## Common Instructor Traps

- "Why did you use a button instead of a link here?"
- "Why is this page using inline styles?"
- "Why did you hide the desktop nav on mobile?"
- "Why is this card not using `next/image`?"
- "Why do some styles live in globals instead of modules?"
- "Why are there duplicate selectors in the global stylesheet?"
- "Why is the site name different in the hero and metadata?"
- "Why does the modal not trap focus yet?"
- "Why does the compare layout change so much on mobile?"
- "What would break if the bottom nav overlay was removed?"

## Defense Survival Tips

- Answer the user benefit first, then the CSS detail.
- If you forget the exact class name, describe the layout role clearly.
- When asked to debug, inspect structure before guessing at styling.
- Use the words "semantic", "responsive", "reusable", and "accessible" naturally.
- Keep your explanations tied to a specific page in the project.

## Confidence Tips During Live Coding

- Start by making the smallest safe change.
- Refresh after every layout edit.
- Use the browser at different widths if the instructor asks for responsiveness.
- If the layout breaks, inspect the wrapper first, not the button first.
- Speak in terms of the exact project sections: hero, dashboard, compare, favorites, and detail pages.

