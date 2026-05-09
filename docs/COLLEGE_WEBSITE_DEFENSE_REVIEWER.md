# College Website Presentation Defense Reviewer

## Frontend Live-Coding and Oral Defense Manual

This reviewer is designed for a college-level website defense with a 15-minute Q&A and live coding exam. It focuses on the kinds of HTML and CSS tasks instructors usually give when they want to test whether you really understand how a website is built, styled, debugged, and made responsive.

Use this document as:
- a study guide before the defense
- a live-coding reference during practice
- a quick troubleshooting manual during the exam

---

## Table of Contents

- [How To Use This Reviewer](#how-to-use-this-reviewer)
- [Defense Mindset](#defense-mindset)
- [50 Sample Instructor Questions And Coding Tasks](#50-sample-instructor-questions-and-coding-tasks)
  - [HTML Structure And Semantic Tags](#1-html-structure-and-semantic-tags)
  - [Layout, Flexbox, And Grid](#2-layout-flexbox-and-grid)
  - [Responsive Design And Media Queries](#3-responsive-design-and-media-queries)
  - [Forms, Navigation, And Accessibility](#4-forms-navigation-and-accessibility)
  - [Debugging, Specificity, And Advanced CSS](#5-debugging-specificity-and-advanced-css)
- [Rapid Fire Practice Questions](#rapid-fire-practice-questions)
- [Common Defense Tips](#common-defense-tips)
- [Most Important CSS Properties To Memorize](#most-important-css-properties-to-memorize)
- [Most Common HTML Tags Used In Website Defenses](#most-common-html-tags-used-in-website-defenses)
- [Emergency Debugging Checklist](#emergency-debugging-checklist)

---

## How To Use This Reviewer

- Read the question like an instructor would ask it in real time.
- Say the expected answer first, then show the code.
- Explain the logic out loud while you edit.
- If you do not remember the exact syntax, build the layout step by step.
- Keep your solution simple before making it fancy.

---

## Defense Mindset

- Instructors usually test one of three things:
  - whether you understand HTML structure
  - whether you can style and align things with CSS
  - whether you can debug layout problems quickly
- During live coding, do not panic if the first attempt is not perfect.
- Talk through your thinking:
  - "I will first identify the container."
  - "Then I will check the display type."
  - "After that I will adjust spacing and responsiveness."
- A good defense answer is not only the final code. It is the reasoning behind the code.

---

## 50 Sample Instructor Questions And Coding Tasks

### 1. HTML Structure And Semantic Tags

#### 1. Center this div on the page
- **Question/Task:** "Center this login box both horizontally and vertically."
- **Expected Answer:** Use a parent wrapper with Flexbox or Grid and align the child to the center.
- **Step-by-step Explanation:**
  1. Wrap the box in a full-height parent container.
  2. Set the parent to `display: flex`.
  3. Use `justify-content: center` and `align-items: center`.
- **Sample HTML code:**
```html
<main class="page">
  <div class="login-box">
    <h1>Login</h1>
  </div>
</main>
```
- **Sample CSS code:**
```css
.page {
  min-height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-box {
  width: min(100%, 420px);
}
```
- **Why the solution works:** The parent controls the layout, so the child is centered in both directions without manual margins.
- **Common mistakes students make:** Adding `margin: auto` without giving the parent height; centering only horizontally.
- **Alternative solutions if applicable:** Use CSS Grid with `place-items: center`.

#### 2. Make the navbar sticky
- **Question/Task:** "Make the navigation stay at the top while scrolling."
- **Expected Answer:** Use `position: sticky` with `top: 0` and a higher `z-index`.
- **Step-by-step Explanation:**
  1. Select the header or nav container.
  2. Set sticky positioning.
  3. Add a background so content does not show through.
- **Sample HTML code:**
```html
<header class="site-header">
  <nav class="nav">Home | About | Contact</nav>
</header>
```
- **Sample CSS code:**
```css
.site-header {
  position: sticky;
  top: 0;
  z-index: 1000;
  background: #111827;
}
```
- **Why the solution works:** Sticky positioning keeps the element in normal flow until the page scrolls, then pins it at the top.
- **Common mistakes students make:** Forgetting `top: 0`; not setting a background color.
- **Alternative solutions if applicable:** Use `position: fixed`, but that removes it from normal document flow.

#### 3. Use semantic tags instead of generic divs
- **Question/Task:** "Rewrite this layout using semantic HTML."
- **Expected Answer:** Replace generic containers with `header`, `nav`, `main`, `section`, `article`, and `footer`.
- **Step-by-step Explanation:**
  1. Identify the role of each section.
  2. Use the HTML element that matches the purpose.
  3. Keep one clear main content area.
- **Sample HTML code:**
```html
<header>
  <nav>...</nav>
</header>
<main>
  <section>
    <article>Phone card</article>
  </section>
</main>
<footer>...</footer>
```
- **Sample CSS code:**
```css
header, main, footer {
  width: 100%;
}
```
- **Why the solution works:** Semantic tags improve readability, accessibility, and SEO.
- **Common mistakes students make:** Using only `div` elements for everything.
- **Alternative solutions if applicable:** Use `aside` for side content or filters.

#### 4. Add a hero section with a heading and call-to-action
- **Question/Task:** "Create a proper hero section for the homepage."
- **Expected Answer:** Use a `section` with an `h1`, supporting text, and a button or link.
- **Step-by-step Explanation:**
  1. Build a semantic hero section.
  2. Add a strong headline.
  3. Add a CTA link or button.
- **Sample HTML code:**
```html
<section class="hero">
  <div class="hero-content">
    <h1>Find the right phone faster</h1>
    <p>Compare features, save favorites, and browse smarter.</p>
    <a class="btn" href="#browse">Start browsing</a>
  </div>
</section>
```
- **Sample CSS code:**
```css
.hero {
  min-height: 70vh;
  display: flex;
  align-items: center;
  padding: 2rem;
}
```
- **Why the solution works:** It creates a clear visual hierarchy and tells users what to do next.
- **Common mistakes students make:** Using multiple `h1` elements without purpose; placing the CTA too far from the headline.
- **Alternative solutions if applicable:** Use a split hero with text on one side and image on the other.

#### 5. Add a footer with links
- **Question/Task:** "Make a footer that contains site links and copyright text."
- **Expected Answer:** Use a `footer` element with a nav or list for links.
- **Step-by-step Explanation:**
  1. Group footer content in one semantic area.
  2. Use a list of links for clean structure.
  3. Style it with spacing and contrast.
- **Sample HTML code:**
```html
<footer class="site-footer">
  <nav>
    <a href="/">Home</a>
    <a href="/about">About</a>
  </nav>
  <p>&copy; 2026 Dialed</p>
</footer>
```
- **Sample CSS code:**
```css
.site-footer {
  padding: 1.5rem;
  display: flex;
  justify-content: space-between;
  gap: 1rem;
}
```
- **Why the solution works:** The footer is clearly separated from the main content and remains easy to navigate.
- **Common mistakes students make:** Mixing footer and main content together.
- **Alternative solutions if applicable:** Stack links vertically on mobile.

#### 6. Make a card semantic and reusable
- **Question/Task:** "Convert this product block into a reusable card."
- **Expected Answer:** Wrap the content in an `article` with a title, image, and action.
- **Step-by-step Explanation:**
  1. Identify the self-contained unit.
  2. Use `article` so each item can stand on its own.
  3. Keep the card structure consistent.
- **Sample HTML code:**
```html
<article class="card">
  <img src="phone.jpg" alt="Phone model">
  <h3>Phone Name</h3>
  <p>Short description</p>
</article>
```
- **Sample CSS code:**
```css
.card {
  border: 1px solid #e5e7eb;
  border-radius: 16px;
  padding: 1rem;
}
```
- **Why the solution works:** Cards become modular and easier to repeat in grids.
- **Common mistakes students make:** Using `div` with no content grouping; missing alt text.
- **Alternative solutions if applicable:** Use `figure` and `figcaption` when the image is the main content.

#### 7. Fix broken heading hierarchy
- **Question/Task:** "The page has heading levels that are out of order. Fix it."
- **Expected Answer:** Use one `h1` for the main title, then `h2` for major sections, `h3` for subsections.
- **Step-by-step Explanation:**
  1. Identify the page title.
  2. Check sections beneath it.
  3. Make headings follow a logical order.
- **Sample HTML code:**
```html
<h1>Dialed</h1>
<h2>Featured Phones</h2>
<h3>Top Choice</h3>
```
- **Sample CSS code:**
```css
h1 { font-size: 2.5rem; }
h2 { font-size: 1.75rem; }
h3 { font-size: 1.25rem; }
```
- **Why the solution works:** Screen readers and browsers understand the content structure better.
- **Common mistakes students make:** Jumping from `h1` to `h4`; styling headings only by size.
- **Alternative solutions if applicable:** Use section headings within each card when needed.

#### 8. Add a section for FAQs
- **Question/Task:** "Create a frequently asked questions section."
- **Expected Answer:** Use a `section` with grouped question and answer blocks.
- **Step-by-step Explanation:**
  1. Wrap the FAQ area in a semantic section.
  2. Use article-like blocks for each question.
  3. Style the questions clearly.
- **Sample HTML code:**
```html
<section class="faq">
  <h2>Frequently Asked Questions</h2>
  <article>
    <h3>How do I compare phones?</h3>
    <p>Choose two phones and open the compare page.</p>
  </article>
</section>
```
- **Sample CSS code:**
```css
.faq article {
  margin-top: 1rem;
  padding: 1rem;
  border-radius: 12px;
}
```
- **Why the solution works:** The content becomes easier to scan and reuse.
- **Common mistakes students make:** Using one huge paragraph for all answers.
- **Alternative solutions if applicable:** Use `<details>` and `<summary>` for collapsible FAQs.

#### 9. Make a list of features accessible
- **Question/Task:** "Show the website features in a semantic list."
- **Expected Answer:** Use `ul` and `li` instead of plain text blocks.
- **Step-by-step Explanation:**
  1. Identify repeated items.
  2. Wrap them in a list.
  3. Style the list for spacing and readability.
- **Sample HTML code:**
```html
<ul class="features">
  <li>Search phones</li>
  <li>Compare devices</li>
  <li>Save favorites</li>
</ul>
```
- **Sample CSS code:**
```css
.features {
  display: grid;
  gap: 0.75rem;
}
```
- **Why the solution works:** Lists are semantically correct for repeated items and help assistive technology.
- **Common mistakes students make:** Using multiple `div`s without list semantics.
- **Alternative solutions if applicable:** Use an icon list with flex alignment.

#### 10. Improve image accessibility
- **Question/Task:** "Why is this image not accessible, and how do you fix it?"
- **Expected Answer:** Add meaningful `alt` text, and make decorative images empty alt if they are not informative.
- **Step-by-step Explanation:**
  1. Decide whether the image is informative or decorative.
  2. Write the correct `alt` text.
  3. Make sure the image size is responsive.
- **Sample HTML code:**
```html
<img src="phone.jpg" alt="Black smartphone shown on a table">
```
- **Sample CSS code:**
```css
img {
  max-width: 100%;
  height: auto;
  display: block;
}
```
- **Why the solution works:** Screen readers can describe the image, and the image scales correctly.
- **Common mistakes students make:** Writing `alt="image"` or leaving alt text empty for important images.
- **Alternative solutions if applicable:** Use `figure` and `figcaption` for richer image context.

### 2. Layout, Flexbox, And Grid

#### 11. Convert a horizontal menu into Flexbox
- **Question/Task:** "Make these navigation links sit in one row."
- **Expected Answer:** Put the links inside a flex container.
- **Step-by-step Explanation:**
  1. Wrap the links in a nav container.
  2. Set `display: flex`.
  3. Add `gap` for spacing.
- **Sample HTML code:**
```html
<nav class="menu">
  <a href="/">Home</a>
  <a href="/about">About</a>
  <a href="/contact">Contact</a>
</nav>
```
- **Sample CSS code:**
```css
.menu {
  display: flex;
  gap: 1rem;
  align-items: center;
}
```
- **Why the solution works:** Flexbox is ideal for one-dimensional alignment.
- **Common mistakes students make:** Using margins instead of `gap` or forgetting flex container display.
- **Alternative solutions if applicable:** Use `inline-flex` for smaller components.

#### 12. Create a 3-column services grid
- **Question/Task:** "Show three service cards across the page."
- **Expected Answer:** Use CSS Grid for structured columns.
- **Step-by-step Explanation:**
  1. Wrap the service cards in a grid container.
  2. Define 3 columns.
  3. Add a gap between cards.
- **Sample HTML code:**
```html
<section class="services">
  <article>Service 1</article>
  <article>Service 2</article>
  <article>Service 3</article>
</section>
```
- **Sample CSS code:**
```css
.services {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}
```
- **Why the solution works:** Grid handles multi-column layouts cleanly and evenly.
- **Common mistakes students make:** Using float-based layouts or fixed widths.
- **Alternative solutions if applicable:** `repeat(auto-fit, minmax(240px, 1fr))` for responsive grids.

#### 13. Make card heights equal
- **Question/Task:** "These cards look uneven. Make them the same height."
- **Expected Answer:** Use grid alignment or flex stretching.
- **Step-by-step Explanation:**
  1. Put cards in a grid or flex container.
  2. Make the items stretch.
  3. Let content flow naturally inside each card.
- **Sample HTML code:**
```html
<div class="grid">
  <article class="card">Short content</article>
  <article class="card">Longer content with more text</article>
</div>
```
- **Sample CSS code:**
```css
.grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.card {
  height: 100%;
}
```
- **Why the solution works:** Grid items naturally align within the same row height.
- **Common mistakes students make:** Giving each card a fixed height that causes overflow.
- **Alternative solutions if applicable:** Use flex containers with `align-stretch`.

#### 14. Center content using CSS Grid
- **Question/Task:** "Center this modal or box perfectly."
- **Expected Answer:** Use `place-items: center` on the parent grid.
- **Step-by-step Explanation:**
  1. Turn the parent into a grid.
  2. Use `place-items: center`.
  3. Limit the child width.
- **Sample HTML code:**
```html
<div class="overlay">
  <div class="modal">Centered content</div>
</div>
```
- **Sample CSS code:**
```css
.overlay {
  min-height: 100vh;
  display: grid;
  place-items: center;
}
```
- **Why the solution works:** Grid makes two-axis centering simple and clean.
- **Common mistakes students make:** Using `position: absolute` when simple centering is enough.
- **Alternative solutions if applicable:** Flexbox centering.

#### 15. Split layout into two columns
- **Question/Task:** "Create a two-column layout for text and image."
- **Expected Answer:** Use Grid or Flexbox depending on the design.
- **Step-by-step Explanation:**
  1. Create a container for both columns.
  2. Define equal or unequal widths.
  3. Add spacing between the columns.
- **Sample HTML code:**
```html
<section class="split">
  <div>Text content</div>
  <img src="phone.jpg" alt="Phone">
</section>
```
- **Sample CSS code:**
```css
.split {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}
```
- **Why the solution works:** Grid gives precise control over column widths and spacing.
- **Common mistakes students make:** Hardcoding widths that break on smaller screens.
- **Alternative solutions if applicable:** Flexbox with `flex: 1`.

#### 16. Make a layout with a sidebar and main content
- **Question/Task:** "Build a page with a sidebar filter and a content area."
- **Expected Answer:** Use a two-column grid where the sidebar has a fixed or smaller width.
- **Step-by-step Explanation:**
  1. Wrap sidebar and content in one container.
  2. Set a grid with two columns.
  3. Adjust widths for desktop and stack on mobile.
- **Sample HTML code:**
```html
<div class="layout">
  <aside class="sidebar">Filters</aside>
  <main class="content">Results</main>
</div>
```
- **Sample CSS code:**
```css
.layout {
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 1.5rem;
}
```
- **Why the solution works:** The sidebar stays separate from the main content and remains easy to scan.
- **Common mistakes students make:** Using fixed positioning for layout instead of content flow.
- **Alternative solutions if applicable:** Flexbox with `flex-basis` on the sidebar.

#### 17. Add spacing between buttons
- **Question/Task:** "Space out these action buttons."
- **Expected Answer:** Use Flexbox `gap` rather than manual margins.
- **Step-by-step Explanation:**
  1. Group the buttons in a flex container.
  2. Add `gap`.
  3. Ensure wrapping works if needed.
- **Sample HTML code:**
```html
<div class="actions">
  <button>Save</button>
  <button>Compare</button>
</div>
```
- **Sample CSS code:**
```css
.actions {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
}
```
- **Why the solution works:** `gap` keeps spacing consistent and easier to manage.
- **Common mistakes students make:** Adding margins to every button separately.
- **Alternative solutions if applicable:** Use CSS Grid for evenly spaced button groups.

#### 18. Make equal width navigation items
- **Question/Task:** "The nav items should have equal width."
- **Expected Answer:** Use Flexbox with `flex: 1` or Grid with equal columns.
- **Step-by-step Explanation:**
  1. Place nav items inside a parent.
  2. Let each item share the same width.
  3. Center the text.
- **Sample HTML code:**
```html
<nav class="nav-links">
  <a href="/">Home</a>
  <a href="/services">Services</a>
  <a href="/contact">Contact</a>
</nav>
```
- **Sample CSS code:**
```css
.nav-links {
  display: flex;
}

.nav-links a {
  flex: 1;
  text-align: center;
}
```
- **Why the solution works:** Every link gets the same flex share, so the row looks balanced.
- **Common mistakes students make:** Assuming text alignment alone will equalize widths.
- **Alternative solutions if applicable:** `display: grid; grid-template-columns: repeat(3, 1fr);`

#### 19. Make a page full-height with footer at the bottom
- **Question/Task:** "The footer should stay at the bottom even when content is short."
- **Expected Answer:** Use a column flex layout on the body or page wrapper.
- **Step-by-step Explanation:**
  1. Make the page wrapper full height.
  2. Use column Flexbox.
  3. Push the footer down with `margin-top: auto`.
- **Sample HTML code:**
```html
<body>
  <div class="page">
    <main>Content</main>
    <footer>Footer</footer>
  </div>
</body>
```
- **Sample CSS code:**
```css
.page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

footer {
  margin-top: auto;
}
```
- **Why the solution works:** The footer occupies the remaining space at the bottom of the viewport.
- **Common mistakes students make:** Giving the footer `position: fixed` when it is not needed.
- **Alternative solutions if applicable:** CSS Grid with `grid-template-rows: auto 1fr auto`.

#### 20. Build a responsive gallery
- **Question/Task:** "Make a gallery of images or cards that adapts to screen size."
- **Expected Answer:** Use `repeat(auto-fit, minmax(...))` in CSS Grid.
- **Step-by-step Explanation:**
  1. Wrap all items in a grid.
  2. Use auto-fit to allow wrapping.
  3. Set a minimum width for each card.
- **Sample HTML code:**
```html
<section class="gallery">
  <img src="1.jpg" alt="Sample 1">
  <img src="2.jpg" alt="Sample 2">
</section>
```
- **Sample CSS code:**
```css
.gallery {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 1rem;
}
```
- **Why the solution works:** The layout automatically changes the number of columns based on available width.
- **Common mistakes students make:** Hardcoding exact column counts for all screens.
- **Alternative solutions if applicable:** Flexbox with wrapping.

### 3. Responsive Design And Media Queries

#### 21. Make this layout responsive on mobile
- **Question/Task:** "The desktop layout breaks on phones. Make it responsive."
- **Expected Answer:** Add a media query that stacks the content and reduces spacing.
- **Step-by-step Explanation:**
  1. Check the widest breakpoint where it breaks.
  2. Switch to a single column.
  3. Shrink spacing and font sizes if needed.
- **Sample HTML code:**
```html
<div class="wrapper">
  <section>Left</section>
  <section>Right</section>
</div>
```
- **Sample CSS code:**
```css
.wrapper {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 2rem;
}

@media (max-width: 768px) {
  .wrapper {
    grid-template-columns: 1fr;
  }
}
```
- **Why the solution works:** It changes the layout at the exact screen size where the desktop version becomes too narrow.
- **Common mistakes students make:** Only shrinking fonts and not changing layout.
- **Alternative solutions if applicable:** Use `clamp()` for fluid sizing.

#### 22. Create a hamburger menu
- **Question/Task:** "Make the navigation collapse into a hamburger menu on mobile."
- **Expected Answer:** Use a button, a hidden menu, and a mobile media query.
- **Step-by-step Explanation:**
  1. Show the normal menu on desktop.
  2. Hide it on mobile.
  3. Show a menu button instead.
- **Sample HTML code:**
```html
<header class="header">
  <button class="menu-btn" aria-label="Open menu">Menu</button>
  <nav class="nav">Links</nav>
</header>
```
- **Sample CSS code:**
```css
.menu-btn {
  display: none;
}

@media (max-width: 768px) {
  .menu-btn {
    display: block;
  }

  .nav {
    display: none;
  }
}
```
- **Why the solution works:** Mobile users get a simpler navigation pattern that fits the screen.
- **Common mistakes students make:** Hiding navigation without providing an accessible replacement.
- **Alternative solutions if applicable:** Use a checkbox toggle or JavaScript for open/close behavior.

#### 23. Make the text scale smoothly
- **Question/Task:** "The typography feels too large on small screens. Fix it."
- **Expected Answer:** Use `clamp()` so font size scales with the viewport.
- **Step-by-step Explanation:**
  1. Choose a minimum and maximum size.
  2. Add a fluid middle value.
  3. Apply it to headings and paragraphs.
- **Sample HTML code:**
```html
<h1 class="title">Find Your Phone</h1>
```
- **Sample CSS code:**
```css
.title {
  font-size: clamp(2rem, 5vw, 4rem);
}
```
- **Why the solution works:** The font adapts without needing many breakpoints.
- **Common mistakes students make:** Setting only fixed font sizes.
- **Alternative solutions if applicable:** Use responsive rem values in media queries.

#### 24. Stack columns on smaller screens
- **Question/Task:** "The two-column layout should become one column on mobile."
- **Expected Answer:** Change the grid or flex direction in a media query.
- **Step-by-step Explanation:**
  1. Identify the desktop layout.
  2. Override it in the mobile breakpoint.
  3. Keep spacing consistent.
- **Sample HTML code:**
```html
<div class="columns">
  <div>Column A</div>
  <div>Column B</div>
</div>
```
- **Sample CSS code:**
```css
.columns {
  display: flex;
  gap: 1rem;
}

@media (max-width: 640px) {
  .columns {
    flex-direction: column;
  }
}
```
- **Why the solution works:** Mobile screens become easier to read when content is vertical.
- **Common mistakes students make:** Forgetting to override the desktop display value.
- **Alternative solutions if applicable:** Use grid column changes instead of flex direction.

#### 25. Make a mobile-friendly form
- **Question/Task:** "The signup form is too wide on phones. Improve it."
- **Expected Answer:** Limit form width, use full-width inputs, and reduce padding on small screens.
- **Step-by-step Explanation:**
  1. Put the form in a centered container.
  2. Make fields stretch to 100%.
  3. Reduce padding for smaller screens.
- **Sample HTML code:**
```html
<form class="form">
  <input type="text" placeholder="Name">
  <input type="email" placeholder="Email">
</form>
```
- **Sample CSS code:**
```css
.form {
  width: min(100%, 420px);
}

.form input {
  width: 100%;
}
```
- **Why the solution works:** The form remains readable and touch-friendly on small devices.
- **Common mistakes students make:** Leaving fixed widths on inputs.
- **Alternative solutions if applicable:** Add `max-width` and responsive padding.

#### 26. Hide or simplify content on mobile
- **Question/Task:** "This extra section makes mobile cluttered. Simplify it."
- **Expected Answer:** Hide decorative content or collapse it with a breakpoint.
- **Step-by-step Explanation:**
  1. Decide what is essential.
  2. Hide nonessential content on small screens.
  3. Keep the core action visible.
- **Sample HTML code:**
```html
<div class="promo">Promotional banner</div>
```
- **Sample CSS code:**
```css
@media (max-width: 768px) {
  .promo {
    display: none;
  }
}
```
- **Why the solution works:** The user focuses on important content first.
- **Common mistakes students make:** Hiding important navigation or forms.
- **Alternative solutions if applicable:** Reduce the size instead of fully hiding.

#### 27. Make a button full width on mobile
- **Question/Task:** "The CTA button should fill the width on phones."
- **Expected Answer:** Set the button to `width: 100%` inside a mobile media query.
- **Step-by-step Explanation:**
  1. Keep the desktop style.
  2. Override button width on mobile.
  3. Preserve padding and touch target size.
- **Sample HTML code:**
```html
<button class="cta">Sign Up</button>
```
- **Sample CSS code:**
```css
@media (max-width: 640px) {
  .cta {
    width: 100%;
  }
}
```
- **Why the solution works:** Full-width buttons are easier to tap and more visually balanced.
- **Common mistakes students make:** Making buttons too tall or removing their spacing.
- **Alternative solutions if applicable:** Make only the primary button full width.

#### 28. Build a responsive navbar alignment
- **Question/Task:** "On mobile, the navbar items are too cramped. Fix the alignment."
- **Expected Answer:** Use `flex-wrap` or switch the nav to a vertical stack.
- **Step-by-step Explanation:**
  1. Check where the overflow happens.
  2. Decide whether to wrap or stack.
  3. Add spacing and center alignment.
- **Sample HTML code:**
```html
<nav class="nav">
  <a href="/">Home</a>
  <a href="/about">About</a>
</nav>
```
- **Sample CSS code:**
```css
.nav {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
```
- **Why the solution works:** Wrapping prevents overflow and keeps items readable.
- **Common mistakes students make:** Forcing a row even when the screen is too narrow.
- **Alternative solutions if applicable:** Use a column layout on mobile.

#### 29. Make images responsive in a card layout
- **Question/Task:** "The images overflow the cards on mobile."
- **Expected Answer:** Use `max-width: 100%`, `height: auto`, and `object-fit` if needed.
- **Step-by-step Explanation:**
  1. Ensure the image cannot exceed its container.
  2. Keep aspect ratio.
  3. Crop responsibly if the design requires it.
- **Sample HTML code:**
```html
<article class="card">
  <img src="phone.jpg" alt="Phone">
</article>
```
- **Sample CSS code:**
```css
.card img {
  width: 100%;
  height: auto;
  object-fit: cover;
}
```
- **Why the solution works:** The image adapts to the card without distortion.
- **Common mistakes students make:** Forcing fixed widths and heights without object fit.
- **Alternative solutions if applicable:** Use background images for purely decorative visuals.

#### 30. Make spacing responsive with clamp
- **Question/Task:** "The layout spacing looks too tight on mobile and too loose on desktop."
- **Expected Answer:** Use `clamp()` for padding, margin, or gap values.
- **Step-by-step Explanation:**
  1. Pick a minimum value.
  2. Add a fluid viewport-based value.
  3. Set a maximum value.
- **Sample HTML code:**
```html
<section class="section">Content</section>
```
- **Sample CSS code:**
```css
.section {
  padding: clamp(1rem, 3vw, 3rem);
}
```
- **Why the solution works:** The spacing changes smoothly across screen sizes.
- **Common mistakes students make:** Using only fixed pixels for all devices.
- **Alternative solutions if applicable:** Use media query spacing scales.

### 4. Forms, Navigation, And Accessibility

#### 31. Improve a form with labels
- **Question/Task:** "This form only uses placeholders. Improve it for accessibility."
- **Expected Answer:** Add `label` elements and connect them with `for` and `id`.
- **Step-by-step Explanation:**
  1. Assign an `id` to each input.
  2. Create a matching label.
  3. Keep labels visible at all times.
- **Sample HTML code:**
```html
<label for="email">Email</label>
<input id="email" type="email">
```
- **Sample CSS code:**
```css
label {
  display: block;
  margin-bottom: 0.5rem;
}
```
- **Why the solution works:** Labels help screen readers and improve form clarity.
- **Common mistakes students make:** Relying only on placeholders.
- **Alternative solutions if applicable:** Use `aria-label` when a visible label is not possible.

#### 32. Create a clear focus state
- **Question/Task:** "Make keyboard focus visible."
- **Expected Answer:** Add a strong `:focus-visible` style.
- **Step-by-step Explanation:**
  1. Select interactive elements.
  2. Add outline or box-shadow.
  3. Make the focus state easy to see.
- **Sample HTML code:**
```html
<button class="btn">Submit</button>
```
- **Sample CSS code:**
```css
.btn:focus-visible {
  outline: 3px solid #f472b6;
  outline-offset: 3px;
}
```
- **Why the solution works:** Keyboard users can track where they are on the page.
- **Common mistakes students make:** Removing outlines without replacement.
- **Alternative solutions if applicable:** Use a glow or border change.

#### 33. Style an active navigation link
- **Question/Task:** "Highlight the current page in the navbar."
- **Expected Answer:** Add a class like `active` or use an attribute selector.
- **Step-by-step Explanation:**
  1. Mark the current link in HTML.
  2. Style it differently.
  3. Make the state obvious but not overpowering.
- **Sample HTML code:**
```html
<a class="nav-link active" href="/dashboard">Dashboard</a>
```
- **Sample CSS code:**
```css
.nav-link.active {
  font-weight: 700;
  color: #ffffff;
}
```
- **Why the solution works:** Users can instantly see which page they are on.
- **Common mistakes students make:** Using the same style for every link.
- **Alternative solutions if applicable:** Add a bottom border or background highlight.

#### 34. Build an accessible button
- **Question/Task:** "Make this clickable element keyboard-friendly."
- **Expected Answer:** Use a real `<button>` or `<a>` when appropriate, not a fake clickable `div`.
- **Step-by-step Explanation:**
  1. Use the correct element for the action.
  2. Keep text descriptive.
  3. Add focus and hover states.
- **Sample HTML code:**
```html
<button type="button" class="btn">Compare</button>
```
- **Sample CSS code:**
```css
.btn {
  cursor: pointer;
  transition: transform 0.2s ease;
}
```
- **Why the solution works:** Native buttons are accessible by default and easier to use.
- **Common mistakes students make:** Using `div` with click handlers for buttons.
- **Alternative solutions if applicable:** Use `<a>` for navigation and `<button>` for actions.

#### 35. Make a clean login form layout
- **Question/Task:** "Arrange the login form so it looks professional."
- **Expected Answer:** Use spacing, labels, input fields, and a clear CTA.
- **Step-by-step Explanation:**
  1. Group the form controls vertically.
  2. Add even spacing.
  3. Make the submit button visually strong.
- **Sample HTML code:**
```html
<form class="login-form">
  <label for="user">Username</label>
  <input id="user" type="text">
  <button type="submit">Login</button>
</form>
```
- **Sample CSS code:**
```css
.login-form {
  display: grid;
  gap: 1rem;
}
```
- **Why the solution works:** The form is easy to scan and use.
- **Common mistakes students make:** Crowding inputs and buttons together.
- **Alternative solutions if applicable:** Flex column layout.

#### 36. Add hover states to links and buttons
- **Question/Task:** "Add a visible hover effect."
- **Expected Answer:** Use `:hover` with subtle color or movement changes.
- **Step-by-step Explanation:**
  1. Select interactive elements.
  2. Change color, background, or transform.
  3. Keep the effect smooth.
- **Sample HTML code:**
```html
<a class="link" href="/shop">Shop now</a>
```
- **Sample CSS code:**
```css
.link:hover {
  color: #ec4899;
  text-decoration: underline;
}
```
- **Why the solution works:** Hover states give clear visual feedback.
- **Common mistakes students make:** Making hover effects too flashy.
- **Alternative solutions if applicable:** Add shadow or border-color transitions.

#### 37. Improve form validation styles
- **Question/Task:** "Make invalid fields obvious to the user."
- **Expected Answer:** Use `:invalid`, `:required`, or custom error classes.
- **Step-by-step Explanation:**
  1. Mark required inputs.
  2. Style invalid states carefully.
  3. Keep error messages readable.
- **Sample HTML code:**
```html
<input type="email" required>
```
- **Sample CSS code:**
```css
input:invalid {
  border-color: #ef4444;
}
```
- **Why the solution works:** Users can see which fields need attention.
- **Common mistakes students make:** Showing errors only after form submission with no visual cue.
- **Alternative solutions if applicable:** Add a custom error message container.

#### 38. Fix a navigation bar that is too crowded
- **Question/Task:** "The navbar has too many items and looks messy."
- **Expected Answer:** Group the items, reduce text clutter, or move extra links into a menu.
- **Step-by-step Explanation:**
  1. Identify the essential links.
  2. Hide secondary actions behind a menu.
  3. Use spacing and wrapping.
- **Sample HTML code:**
```html
<nav class="nav">
  <a href="/">Home</a>
  <a href="/compare">Compare</a>
  <a href="/favorites">Favorites</a>
</nav>
```
- **Sample CSS code:**
```css
.nav {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}
```
- **Why the solution works:** Less clutter means better usability and cleaner design.
- **Common mistakes students make:** Trying to show every possible link at once.
- **Alternative solutions if applicable:** Use a dropdown menu or hamburger toggle.

#### 39. Improve accessibility with skip links
- **Question/Task:** "How do you help keyboard users skip the navigation?"
- **Expected Answer:** Add a skip link at the top of the page.
- **Step-by-step Explanation:**
  1. Put a hidden skip link early in the DOM.
  2. Reveal it on focus.
  3. Link it to the main content.
- **Sample HTML code:**
```html
<a class="skip-link" href="#main">Skip to content</a>
<main id="main">...</main>
```
- **Sample CSS code:**
```css
.skip-link {
  position: absolute;
  left: -999px;
}

.skip-link:focus {
  left: 1rem;
  top: 1rem;
}
```
- **Why the solution works:** Keyboard users can jump directly to the main content.
- **Common mistakes students make:** Leaving the skip link visible all the time or not linking it properly.
- **Alternative solutions if applicable:** Use ARIA landmarks in addition to the skip link.

#### 40. Make buttons and links visually distinct
- **Question/Task:** "Users cannot tell what is a link and what is a button."
- **Expected Answer:** Style links and buttons differently based on their roles.
- **Step-by-step Explanation:**
  1. Use proper HTML elements.
  2. Give buttons a filled style.
  3. Give links a text or outline style when appropriate.
- **Sample HTML code:**
```html
<a class="link-btn" href="/compare">Compare</a>
<button class="solid-btn" type="button">Save</button>
```
- **Sample CSS code:**
```css
.solid-btn {
  background: #111827;
  color: white;
}

.link-btn {
  color: #111827;
}
```
- **Why the solution works:** Users can quickly understand the difference between navigation and actions.
- **Common mistakes students make:** Making all interactive elements look identical.
- **Alternative solutions if applicable:** Use icons or underline treatment for links.

### 5. Debugging, Specificity, And Advanced CSS

#### 41. Fix CSS that is not applying
- **Question/Task:** "Why is this CSS not working?"
- **Expected Answer:** Check the selector, import path, class name spelling, and CSS specificity.
- **Step-by-step Explanation:**
  1. Confirm the CSS file is imported.
  2. Check that the class name matches the HTML or JSX.
  3. Look for overrides from more specific selectors.
- **Sample HTML code:**
```html
<div class="box">Content</div>
```
- **Sample CSS code:**
```css
.box {
  background: #f3f4f6;
}
```
- **Why the solution works:** Correct selector matching is required for CSS to take effect.
- **Common mistakes students make:** Typing `.Box` instead of `.box`; forgetting to import the stylesheet.
- **Alternative solutions if applicable:** Use inline styles temporarily to confirm the issue.

#### 42. Fix overlapping elements
- **Question/Task:** "Two sections overlap on the page. Fix the layout."
- **Expected Answer:** Check positioning, margins, heights, and z-index.
- **Step-by-step Explanation:**
  1. Inspect whether one element is absolutely positioned.
  2. Check if the parent has enough space.
  3. Adjust stacking and flow.
- **Sample HTML code:**
```html
<div class="hero">
  <div class="badge">New</div>
  <div class="content">Text</div>
</div>
```
- **Sample CSS code:**
```css
.hero {
  position: relative;
  padding-top: 2rem;
}

.badge {
  position: absolute;
  top: 1rem;
  right: 1rem;
}
```
- **Why the solution works:** The parent becomes the positioning context and prevents random overlap.
- **Common mistakes students make:** Using absolute positioning without a relative parent.
- **Alternative solutions if applicable:** Use Flexbox or Grid instead of positioning.

#### 43. Explain class vs id usage
- **Question/Task:** "When should you use a class instead of an id?"
- **Expected Answer:** Use classes for repeated styling and ids for unique page elements or anchors.
- **Step-by-step Explanation:**
  1. Ask whether the style will be reused.
  2. If yes, use a class.
  3. Keep ids unique and limited.
- **Sample HTML code:**
```html
<section id="main-hero" class="hero-card"></section>
```
- **Sample CSS code:**
```css
.hero-card {
  padding: 2rem;
}
```
- **Why the solution works:** Classes scale better and keep styles reusable.
- **Common mistakes students make:** Using ids for every style and creating specificity problems.
- **Alternative solutions if applicable:** Combine an id for anchor linking and a class for styling.

#### 44. Use transitions and transforms on hover
- **Question/Task:** "Add a hover animation to this card."
- **Expected Answer:** Animate `transform` and maybe `box-shadow` or `border-color`.
- **Step-by-step Explanation:**
  1. Define the base state.
  2. Add a transition.
  3. Change transform on hover.
- **Sample HTML code:**
```html
<article class="card">Hover me</article>
```
- **Sample CSS code:**
```css
.card {
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card:hover {
  transform: translateY(-4px);
}
```
- **Why the solution works:** Transforms are smooth and perform well.
- **Common mistakes students make:** Animating layout properties like width or height unnecessarily.
- **Alternative solutions if applicable:** Add scale instead of translateY.

#### 45. Make z-index work correctly
- **Question/Task:** "The modal is behind the header. Fix it."
- **Expected Answer:** Give the modal a higher z-index and ensure the element is positioned.
- **Step-by-step Explanation:**
  1. Check the stacking context.
  2. Set `position` on the element.
  3. Increase `z-index` above competing elements.
- **Sample HTML code:**
```html
<div class="modal">Modal content</div>
```
- **Sample CSS code:**
```css
.modal {
  position: fixed;
  inset: 0;
  z-index: 2000;
}
```
- **Why the solution works:** z-index only works inside positioned stacking contexts.
- **Common mistakes students make:** Changing z-index without positioning.
- **Alternative solutions if applicable:** Lower the z-index of the header if appropriate.

#### 46. Add a dark mode with CSS variables
- **Question/Task:** "Create a dark mode switch."
- **Expected Answer:** Use CSS custom properties on `:root` and a theme attribute.
- **Step-by-step Explanation:**
  1. Define default variables.
  2. Override them under a theme selector.
  3. Toggle the attribute in the page or script.
- **Sample HTML code:**
```html
<html data-theme="dark">
```
- **Sample CSS code:**
```css
:root {
  --bg: #ffffff;
  --text: #111827;
}

html[data-theme="dark"] {
  --bg: #111827;
  --text: #f9fafb;
}
```
- **Why the solution works:** One variable system can update the whole site consistently.
- **Common mistakes students make:** Hardcoding colors in many separate selectors.
- **Alternative solutions if applicable:** Use `prefers-color-scheme` for automatic system-based theme.

#### 47. Debug CSS specificity
- **Question/Task:** "Why is my class style being overridden?"
- **Expected Answer:** A more specific selector, later rule, or inline style is winning.
- **Step-by-step Explanation:**
  1. Check the cascade order.
  2. Inspect the winning selector in devtools.
  3. Refactor the CSS rather than overusing `!important`.
- **Sample HTML code:**
```html
<button class="btn primary">Save</button>
```
- **Sample CSS code:**
```css
.btn {
  background: gray;
}

.primary {
  background: blue;
}
```
- **Why the solution works:** Understanding specificity helps you predict which style wins.
- **Common mistakes students make:** Using `!important` everywhere without understanding why.
- **Alternative solutions if applicable:** Reorder the CSS or simplify selector structure.

#### 48. Fix layout caused by a missing display property
- **Question/Task:** "This row should be horizontal, but it is stacking."
- **Expected Answer:** Apply `display: flex` or `display: grid` to the correct parent container.
- **Step-by-step Explanation:**
  1. Identify the parent that controls the children.
  2. Add the correct display property.
  3. Verify spacing and alignment.
- **Sample HTML code:**
```html
<div class="row">
  <span>Left</span>
  <span>Right</span>
</div>
```
- **Sample CSS code:**
```css
.row {
  display: flex;
  justify-content: space-between;
}
```
- **Why the solution works:** The parent layout model determines how its children behave.
- **Common mistakes students make:** Styling the child elements instead of the parent container.
- **Alternative solutions if applicable:** Use grid columns.

#### 49. Add a sticky sidebar
- **Question/Task:** "Keep the filter sidebar visible while scrolling."
- **Expected Answer:** Use `position: sticky` with a top offset.
- **Step-by-step Explanation:**
  1. Set sticky positioning on the sidebar.
  2. Add `top`.
  3. Make sure the parent allows scrolling.
- **Sample HTML code:**
```html
<aside class="filters">Filters</aside>
```
- **Sample CSS code:**
```css
.filters {
  position: sticky;
  top: 1rem;
}
```
- **Why the solution works:** The sidebar stays visible without leaving the normal flow.
- **Common mistakes students make:** Using fixed positioning when sticky is better.
- **Alternative solutions if applicable:** `position: fixed` for always-visible panels.

#### 50. Fix a broken layout quickly during live coding
- **Question/Task:** "The page suddenly looks broken. Diagnose and fix it live."
- **Expected Answer:** Check the parent container, display mode, width, overflow, positioning, and media query conflicts.
- **Step-by-step Explanation:**
  1. Identify the section that changed.
  2. Inspect the parent and child styles.
  3. Restore the layout step by step.
- **Sample HTML code:**
```html
<section class="problem-section">
  <div class="panel">Panel A</div>
  <div class="panel">Panel B</div>
</section>
```
- **Sample CSS code:**
```css
.problem-section {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1rem;
}
```
- **Why the solution works:** A structured checklist helps you isolate the exact cause of the bug.
- **Common mistakes students make:** Changing random styles without isolating the issue.
- **Alternative solutions if applicable:** Temporarily comment out conflicting CSS to identify the broken rule.

---

## Rapid Fire Practice Questions

1. What is semantic HTML?
2. Why is `main` important?
3. What is the difference between `section` and `div`?
4. When should you use Flexbox?
5. When should you use CSS Grid?
6. What does `display: flex` do?
7. What does `gap` control?
8. Why is `position: relative` important?
9. What does `z-index` control?
10. Why is `position: sticky` useful?
11. What is the purpose of `alt` text?
12. What makes a button accessible?
13. Why use labels in forms?
14. What is the difference between `button` and `a`?
15. What is CSS specificity?
16. Why can `!important` be dangerous?
17. What is a media query?
18. Why use mobile-first design?
19. What does `max-width: 100%` do?
20. What is `box-sizing: border-box`?
21. Why do we use CSS variables?
22. What is a hover state?
23. What is a focus state?
24. What is the difference between inline, internal, and external CSS?
25. How do you center a div?
26. How do you make a navbar sticky?
27. How do you create a responsive grid?
28. How do you make cards equal height?
29. How do you hide a section on mobile?
30. How do you improve page accessibility?

---

## Common Defense Tips

- Always speak clearly before typing.
- Identify the parent container first.
- Use semantic tags whenever possible.
- Prefer classes for reusable styles.
- Keep your code changes small and visible.
- If the instructor asks "why", answer with purpose, not just syntax.
- If you are stuck, explain your debugging process out loud.
- Keep a calm pace and avoid overcomplicating the fix.
- If one solution fails, offer a simpler alternative.
- Remember that live coding is about reasoning, not memorization.

---

## Most Important CSS Properties To Memorize

- `display`
- `position`
- `top`, `right`, `bottom`, `left`
- `z-index`
- `justify-content`
- `align-items`
- `gap`
- `flex-direction`
- `flex-wrap`
- `grid-template-columns`
- `grid-template-rows`
- `padding`
- `margin`
- `width`
- `max-width`
- `height`
- `min-height`
- `border-radius`
- `box-shadow`
- `overflow`
- `object-fit`
- `text-align`
- `font-size`
- `font-weight`
- `line-height`
- `color`
- `background`
- `transition`
- `transform`
- `opacity`

---

## Most Common HTML Tags Used In Website Defenses

- `html`
- `head`
- `body`
- `header`
- `nav`
- `main`
- `section`
- `article`
- `aside`
- `footer`
- `div`
- `span`
- `h1` to `h6`
- `p`
- `a`
- `button`
- `form`
- `label`
- `input`
- `textarea`
- `select`
- `ul`
- `ol`
- `li`
- `img`
- `figure`
- `figcaption`
- `strong`
- `em`

---

## Emergency Debugging Checklist

- Check whether the correct stylesheet is imported.
- Verify class names and element names for spelling errors.
- Inspect the parent container first, not just the child.
- Confirm whether the element is flex, grid, block, or inline.
- Check for conflicting media queries.
- Look for overflow caused by fixed widths.
- Check whether `position: absolute` is breaking the layout.
- Confirm that `z-index` is applied to a positioned element.
- Verify `alt`, `for`, `id`, and `aria-label` attributes where needed.
- Remove `!important` if it is hiding the real problem.
- Use browser devtools to inspect the computed styles.
- Disable one rule at a time until the bug disappears.
- Test the layout at desktop and mobile widths.
- Save your work after each small fix.

---

## Closing Note

The best way to win a website defense is to understand the purpose of every element and every CSS rule. If you can explain what the code does, why it exists, and how it behaves on mobile, you are already ahead of most students.
