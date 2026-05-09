# DeviceIQ Practical HTML/CSS Defense Reviewer

Use this reviewer like a live laboratory exam guide. The tasks below are short, visual, and focused on real-time HTML/CSS edits based on the actual DeviceIQ pages and components.

## Sample 1

**Instructor Task/Question:**  
"Change the homepage hero background to a darker blue."

**What The Student Should Do:**  
Edit the hero panel background in `components/marketing/HeroSection.module.css`.

**HTML To Edit:**  
```html
<section class="hero-panel premium-hero-panel">...</section>
```

**CSS To Edit:**  
```css
.premium-hero-panel {
  background: linear-gradient(135deg, #0b1d3a 0%, #10284d 100%);
}
```

**Expected Visual Result:**  
The hero looks darker and more dramatic.

**Common Mistakes:**  
- Changing the text color instead of the background
- Editing the wrong hero class

**Possible Follow-up Question:**  
"How would you keep the text readable on this background?"

## Sample 2

**Instructor Task/Question:**  
"Increase the padding inside this hero section."

**What The Student Should Do:**  
Add more space inside `.premium-hero-panel` or `.hero-panel`.

**HTML To Edit:**  
```html
<div class="glass-panel hero-panel premium-hero-panel">...</div>
```

**CSS To Edit:**  
```css
.premium-hero-panel {
  padding: 40px;
}
```

**Expected Visual Result:**  
The hero content feels less cramped.

**Common Mistakes:**  
- Changing margin instead of padding
- Adding too much spacing on mobile

**Possible Follow-up Question:**  
"How would you reduce the padding on phones?"

## Sample 3

**Instructor Task/Question:**  
"Put the two buttons in the hero side by side."

**What The Student Should Do:**  
Make the hero button row use flexbox.

**HTML To Edit:**  
```html
<div class="button-row hero-action-row">
  <a class="button" href="/dashboard">Browse phones</a>
  <a class="button-secondary" href="/compare">Watch the compare reveal</a>
</div>
```

**CSS To Edit:**  
```css
.hero-action-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
```

**Expected Visual Result:**  
The buttons appear in one row on desktop.

**Common Mistakes:**  
- Removing the gap
- Forgetting mobile wrapping

**Possible Follow-up Question:**  
"How would you stack them on small screens?"

## Sample 4

**Instructor Task/Question:**  
"Center this hero text on mobile."

**What The Student Should Do:**  
Add a mobile media query and center the hero copy stack.

**HTML To Edit:**  
```html
<div class="hero-copy-stack">
  <h1 class="section-title">Stop guessing. Start comparing.</h1>
</div>
```

**CSS To Edit:**  
```css
@media (max-width: 768px) {
  .hero-copy-stack {
    text-align: center;
  }
}
```

**Expected Visual Result:**  
The hero title and paragraph look centered on phones.

**Common Mistakes:**  
- Centering the whole page instead of the hero only
- Forgetting to test the mobile width

**Possible Follow-up Question:**  
"What else in the hero should align to the center?"

## Sample 5

**Instructor Task/Question:**  
"Add a hover effect to these story cards."

**What The Student Should Do:**  
Edit the `.story-card:hover` rule in the homepage module CSS.

**HTML To Edit:**  
```html
<article class="glass-panel story-card">...</article>
```

**CSS To Edit:**  
```css
.story-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow);
}
```

**Expected Visual Result:**  
The cards lift slightly on hover.

**Common Mistakes:**  
- Using a huge scale effect
- Changing layout size instead of transform

**Possible Follow-up Question:**  
"Why is transform better than changing height?"

## Sample 6

**Instructor Task/Question:**  
"Make all story cards the same height."

**What The Student Should Do:**  
Use grid alignment and consistent card padding.

**HTML To Edit:**  
```html
<div class="story-strip">
  <article class="story-card">...</article>
</div>
```

**CSS To Edit:**  
```css
.story-strip {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
}

.story-card {
  height: 100%;
}
```

**Expected Visual Result:**  
The cards look balanced in one row.

**Common Mistakes:**  
- Hard-coding card heights
- Forgetting the grid container

**Possible Follow-up Question:**  
"What happens if one card has more text than the others?"

## Sample 7

**Instructor Task/Question:**  
"Add more spacing between these feature cards."

**What The Student Should Do:**  
Increase the grid gap in the homepage feature layout.

**HTML To Edit:**  
```html
<div class="home-feature-layout">
  <article class="home-feature-card">...</article>
</div>
```

**CSS To Edit:**  
```css
.home-feature-layout {
  gap: 28px;
}
```

**Expected Visual Result:**  
The feature cards feel less crowded.

**Common Mistakes:**  
- Adding margin to only one card
- Increasing gap too much

**Possible Follow-up Question:**  
"Would you change the gap on mobile too?"

## Sample 8

**Instructor Task/Question:**  
"Make the feature cards stack into one column on tablet."

**What The Student Should Do:**  
Use a media query for `.home-feature-layout`.

**HTML To Edit:**  
```html
<div class="home-feature-layout">...</div>
```

**CSS To Edit:**  
```css
@media (max-width: 900px) {
  .home-feature-layout {
    grid-template-columns: 1fr;
  }
}
```

**Expected Visual Result:**  
The cards become a single column on smaller screens.

**Common Mistakes:**  
- Forgetting the breakpoint
- Leaving the 3-column layout on tablets

**Possible Follow-up Question:**  
"Why is one column easier to read on a tablet?"

## Sample 9

**Instructor Task/Question:**  
"Make the featured card stand out more."

**What The Student Should Do:**  
Add a stronger border or shadow to the accent feature card.

**HTML To Edit:**  
```html
<article class="glass-panel home-feature-card accent">...</article>
```

**CSS To Edit:**  
```css
.home-feature-card.accent {
  border-color: rgba(var(--accent-rgb), 0.28);
  box-shadow: 0 22px 60px rgba(4, 10, 18, 0.3);
}
```

**Expected Visual Result:**  
The middle feature card looks more important.

**Common Mistakes:**  
- Making every card equally strong
- Using a border that is too bright

**Possible Follow-up Question:**  
"How would you emphasize it without changing the size?"

## Sample 10

**Instructor Task/Question:**  
"Change the navbar to a darker tone."

**What The Student Should Do:**  
Edit the header background in `SiteHeader.module.css`.

**HTML To Edit:**  
```html
<header class="site-header">...</header>
```

**CSS To Edit:**  
```css
.header {
  background: rgba(8, 12, 20, 0.96);
}
```

**Expected Visual Result:**  
The header looks deeper and more solid.

**Common Mistakes:**  
- Removing the blur entirely
- Making the header too opaque

**Possible Follow-up Question:**  
"How would you keep the glass effect while darkening it?"

## Sample 11

**Instructor Task/Question:**  
"Make the navbar sticky."

**What The Student Should Do:**  
Add sticky positioning to the header.

**HTML To Edit:**  
```html
<header class="site-header">...</header>
```

**CSS To Edit:**  
```css
.header {
  position: sticky;
  top: 0;
  z-index: 50;
}
```

**Expected Visual Result:**  
The navbar stays visible while scrolling.

**Common Mistakes:**  
- Forgetting `top: 0`
- Using the wrong stacking order

**Possible Follow-up Question:**  
"What can hide a sticky header on top of other elements?"

## Sample 12

**Instructor Task/Question:**  
"Hide the desktop navbar on mobile."

**What The Student Should Do:**  
Use the existing mobile breakpoint in the header CSS.

**HTML To Edit:**  
```html
<nav class="nav-row desktop-nav">...</nav>
```

**CSS To Edit:**  
```css
@media (max-width: 768px) {
  .desktop-nav {
    display: none;
  }
}
```

**Expected Visual Result:**  
The top links disappear on phones.

**Common Mistakes:**  
- Hiding the wrong nav
- Forgetting the mobile tab bar still needs to show

**Possible Follow-up Question:**  
"What replaces the desktop nav on mobile?"

## Sample 13

**Instructor Task/Question:**  
"Make the mobile bottom navigation more visible."

**What The Student Should Do:**  
Darken the background and add a stronger border or shadow.

**HTML To Edit:**  
```html
<nav class="mobile-tabbar">...</nav>
```

**CSS To Edit:**  
```css
.scope {
  background: rgba(12, 16, 24, 0.98);
  box-shadow: 0 18px 40px rgba(0, 0, 0, 0.3);
}
```

**Expected Visual Result:**  
The tab bar is easier to see over the page.

**Common Mistakes:**  
- Making the bar too bright
- Forgetting the rounded corners

**Possible Follow-up Question:**  
"Why should the mobile nav stay inside the safe area?"

## Sample 14

**Instructor Task/Question:**  
"Make the mobile tab labels smaller."

**What The Student Should Do:**  
Reduce the font size inside the mobile tab button.

**HTML To Edit:**  
```html
<a class="mobile-tablink" href="/compare">
  <span>Compare</span>
</a>
```

**CSS To Edit:**  
```css
@media (max-width: 560px) {
  .mobile-tablink {
    font-size: 0.68rem;
  }
}
```

**Expected Visual Result:**  
The labels fit better on small screens.

**Common Mistakes:**  
- Making the text too tiny
- Changing the icon size instead of the label size

**Possible Follow-up Question:**  
"What if the labels still overlap?"

## Sample 15

**Instructor Task/Question:**  
"Add an active state to this nav link."

**What The Student Should Do:**  
Style the `.nav-link.is-active` state.

**HTML To Edit:**  
```html
<a class="nav-link is-active" href="/dashboard">Dashboard</a>
```

**CSS To Edit:**  
```css
.nav-link.is-active {
  color: var(--text);
  background: rgba(var(--accent-rgb), 0.12);
}
```

**Expected Visual Result:**  
The current page link looks highlighted.

**Common Mistakes:**  
- Using only hover styles
- Forgetting the active class on mobile too

**Possible Follow-up Question:**  
"How can you show active state without a background?"

## Sample 16

**Instructor Task/Question:**  
"Increase the size of this brand logo box."

**What The Student Should Do:**  
Edit the `.brand-badge` dimensions.

**HTML To Edit:**  
```html
<a class="brand-lockup" href="/">
  <span class="brand-badge"></span>
</a>
```

**CSS To Edit:**  
```css
.brand-badge {
  width: 48px;
  height: 48px;
}
```

**Expected Visual Result:**  
The logo mark looks bigger and easier to notice.

**Common Mistakes:**  
- Stretching the whole brand lockup unevenly
- Breaking the alignment with the text

**Possible Follow-up Question:**  
"Would you also increase the text size?"

## Sample 17

**Instructor Task/Question:**  
"Make the footer content align better."

**What The Student Should Do:**  
Use flex alignment and increase spacing inside the footer.

**HTML To Edit:**  
```html
<footer class="footer">
  <div class="inner">...</div>
</footer>
```

**CSS To Edit:**  
```css
.inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 18px;
}
```

**Expected Visual Result:**  
The footer looks cleaner and balanced.

**Common Mistakes:**  
- Using too much horizontal spacing
- Forgetting the footer note is hidden on mobile

**Possible Follow-up Question:**  
"How would you stack this on a phone?"

## Sample 18

**Instructor Task/Question:**  
"Make the about page into two columns."

**What The Student Should Do:**  
Use the existing `marketing-grid` layout.

**HTML To Edit:**  
```html
<div class="page-shell marketing-grid">
  <div class="glass-panel card">...</div>
  <div class="glass-panel card">...</div>
</div>
```

**CSS To Edit:**  
```css
.marketing-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}
```

**Expected Visual Result:**  
The About page shows two balanced cards.

**Common Mistakes:**  
- Using fixed widths
- Forgetting the mobile stack

**Possible Follow-up Question:**  
"What happens to this layout on small screens?"

## Sample 19

**Instructor Task/Question:**  
"Increase the padding inside the about cards."

**What The Student Should Do:**  
Add more space inside `.card`.

**HTML To Edit:**  
```html
<div class="glass-panel card">...</div>
```

**CSS To Edit:**  
```css
.card {
  padding: 32px;
}
```

**Expected Visual Result:**  
The text does not feel cramped.

**Common Mistakes:**  
- Changing the outer section spacing instead
- Adding too much padding on mobile

**Possible Follow-up Question:**  
"How would you keep the card compact on phones?"

## Sample 20

**Instructor Task/Question:**  
"Make this contact form look cleaner."

**What The Student Should Do:**  
Increase spacing between fields and keep inputs consistent.

**HTML To Edit:**  
```html
<div class="stack">
  <div class="field">...</div>
</div>
```

**CSS To Edit:**  
```css
.stack {
  gap: 18px;
}

.input,
.textarea {
  border-radius: 18px;
}
```

**Expected Visual Result:**  
The form looks neater and easier to scan.

**Common Mistakes:**  
- Making fields different heights
- Removing label spacing

**Possible Follow-up Question:**  
"What would you change in the button row?"

## Sample 21

**Instructor Task/Question:**  
"Add another input field to this contact form."

**What The Student Should Do:**  
Insert one more `.field` block, such as a subject field.

**HTML To Edit:**  
```html
<div class="field">
  <label for="subject">Subject</label>
  <input id="subject" class="input" placeholder="What is this about?" />
</div>
```

**CSS To Edit:**  
```css
.field {
  display: grid;
  gap: 10px;
}
```

**Expected Visual Result:**  
The form has one more clean input row.

**Common Mistakes:**  
- Forgetting the label
- Making the new input style different from the others

**Possible Follow-up Question:**  
"Where should this field be placed in the form?"

## Sample 22

**Instructor Task/Question:**  
"Make the contact button full width."

**What The Student Should Do:**  
Change the button display or width in the form area.

**HTML To Edit:**  
```html
<button class="button" type="button">Send message</button>
```

**CSS To Edit:**  
```css
.button {
  width: 100%;
}
```

**Expected Visual Result:**  
The button stretches across the form width.

**Common Mistakes:**  
- Applying the style to every button on the site
- Forgetting to adjust button padding if needed

**Possible Follow-up Question:**  
"When is full width a good choice for buttons?"

## Sample 23

**Instructor Task/Question:**  
"Make the textarea taller."

**What The Student Should Do:**  
Increase the textarea height in the global input styles.

**HTML To Edit:**  
```html
<textarea id="message" class="textarea"></textarea>
```

**CSS To Edit:**  
```css
.textarea {
  min-height: 180px;
}
```

**Expected Visual Result:**  
The message box is easier to type in.

**Common Mistakes:**  
- Making it too tall on mobile
- Using fixed height when minimum height is enough

**Possible Follow-up Question:**  
"Would you let the user resize it?"

## Sample 24

**Instructor Task/Question:**  
"Make the services page look more balanced."

**What The Student Should Do:**  
Adjust the grid columns in `services-grid`.

**HTML To Edit:**  
```html
<div class="services-grid">
  <article class="service-card service-card-featured">...</article>
</div>
```

**CSS To Edit:**  
```css
.services-grid {
  display: grid;
  grid-template-columns: 1.35fr 1fr 1fr;
  gap: 20px;
}
```

**Expected Visual Result:**  
The featured card stays larger and the other cards stay aligned.

**Common Mistakes:**  
- Making all columns equal by accident
- Forgetting the tablet breakpoint

**Possible Follow-up Question:**  
"Which card should be the biggest and why?"

## Sample 25

**Instructor Task/Question:**  
"Make the featured services card more obvious."

**What The Student Should Do:**  
Add a stronger border and shadow to `.service-card-featured`.

**HTML To Edit:**  
```html
<article class="glass-panel service-card service-card-featured">...</article>
```

**CSS To Edit:**  
```css
.service-card-featured {
  border-color: rgba(var(--accent-rgb), 0.28);
  box-shadow: 0 22px 60px rgba(4, 10, 18, 0.3);
}
```

**Expected Visual Result:**  
The compare tool card stands out more.

**Common Mistakes:**  
- Overdoing the shadow
- Making the accent too bright

**Possible Follow-up Question:**  
"How would you make it stand out only with color?"

## Sample 26

**Instructor Task/Question:**  
"Make the compare selector fields the same width."

**What The Student Should Do:**  
Keep the selector grid at two equal columns.

**HTML To Edit:**  
```html
<form class="compare-selector-grid">
  <div class="field">...</div>
  <div class="field">...</div>
</form>
```

**CSS To Edit:**  
```css
.compare-selector-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 16px;
}
```

**Expected Visual Result:**  
Both dropdowns look balanced.

**Common Mistakes:**  
- Letting one field stretch more than the other
- Forgetting the mobile stack

**Possible Follow-up Question:**  
"What would you change on very small screens?"

## Sample 27

**Instructor Task/Question:**  
"Put the VS badge exactly in the middle."

**What The Student Should Do:**  
Center `.compare-versus-badge` inside the hero card.

**HTML To Edit:**  
```html
<div class="compare-versus-badge">VS</div>
```

**CSS To Edit:**  
```css
.compare-versus-badge {
  position: absolute;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
```

**Expected Visual Result:**  
The badge sits between both phone cards.

**Common Mistakes:**  
- Forgetting the parent needs `position: relative`
- Off-centering it with wrong transform values

**Possible Follow-up Question:**  
"How does this change on mobile?"

## Sample 28

**Instructor Task/Question:**  
"Make the compare cards stack on mobile."

**What The Student Should Do:**  
Change the compare hero grid to one column on small screens.

**HTML To Edit:**  
```html
<div class="compare-hero-phones">
  <article class="compare-phone-hero">...</article>
  <article class="compare-phone-hero">...</article>
</div>
```

**CSS To Edit:**  
```css
@media (max-width: 768px) {
  .compare-hero-phones {
    grid-template-columns: 1fr;
  }
}
```

**Expected Visual Result:**  
The cards stack nicely on phones.

**Common Mistakes:**  
- Keeping the two-column layout on mobile
- Forgetting to reduce the badge size

**Possible Follow-up Question:**  
"Why is stacking better here?"

## Sample 29

**Instructor Task/Question:**  
"Make the compare table easier to read on mobile."

**What The Student Should Do:**  
Hide the header row and stack each row into a card.

**HTML To Edit:**  
```html
<div class="compare-table-row">...</div>
```

**CSS To Edit:**  
```css
@media (max-width: 768px) {
  .compare-table-row {
    grid-template-columns: 1fr;
    padding: 12px;
  }
}
```

**Expected Visual Result:**  
Each spec row becomes a neat stacked block.

**Common Mistakes:**  
- Leaving the table too wide
- Forgetting to show which value belongs to which phone

**Possible Follow-up Question:**  
"What makes the row still understandable after stacking?"

## Sample 30

**Instructor Task/Question:**  
"Reduce the spacing in the compare score rows."

**What The Student Should Do:**  
Lower the gap and padding in the score snapshot area.

**HTML To Edit:**  
```html
<div class="compare-score-row">
  <div class="compare-score-cell">...</div>
</div>
```

**CSS To Edit:**  
```css
.compare-score-row {
  gap: 8px;
}

.compare-score-cell {
  padding: 12px 14px;
}
```

**Expected Visual Result:**  
The score section feels tighter and cleaner.

**Common Mistakes:**  
- Making the cells too small
- Compressing the text too much

**Possible Follow-up Question:**  
"When does tighter spacing become a problem?"

## Sample 31

**Instructor Task/Question:**  
"Make the compare highlight cards into two columns."

**What The Student Should Do:**  
Keep the highlight grid at two equal columns on desktop.

**HTML To Edit:**  
```html
<div class="compare-highlights-grid">
  <div class="compare-highlight-card">...</div>
  <div class="compare-highlight-card">...</div>
</div>
```

**CSS To Edit:**  
```css
.compare-highlights-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 20px;
}
```

**Expected Visual Result:**  
The two highlight boxes sit side by side.

**Common Mistakes:**  
- Forgetting to collapse to one column on mobile
- Making one card visibly smaller

**Possible Follow-up Question:**  
"Why are there two highlight cards?"

## Sample 32

**Instructor Task/Question:**  
"Make the phone image responsive."

**What The Student Should Do:**  
Ensure the image fits inside the media box without distortion.

**HTML To Edit:**  
```html
<div class="phone-media">
  <img src="..." alt="Phone" />
</div>
```

**CSS To Edit:**  
```css
.phone-media img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
```

**Expected Visual Result:**  
The phone image scales cleanly inside the card.

**Common Mistakes:**  
- Stretching the image
- Forgetting `object-fit`

**Possible Follow-up Question:**  
"What should happen if the image is missing?"

## Sample 33

**Instructor Task/Question:**  
"Make the phone card buttons equal size."

**What The Student Should Do:**  
Set the action buttons to full width in the card action grid.

**HTML To Edit:**  
```html
<div class="phone-card-actions">
  <a class="button-secondary">View full specs</a>
  <a class="button">Compare</a>
</div>
```

**CSS To Edit:**  
```css
.card-primary-actions {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}
```

**Expected Visual Result:**  
The buttons line up evenly.

**Common Mistakes:**  
- Leaving one button shorter than the other
- Forgetting the mobile stack

**Possible Follow-up Question:**  
"Why is equal button size important?"

## Sample 34

**Instructor Task/Question:**  
"Add hover effect to the phone card."

**What The Student Should Do:**  
Edit the card hover state in `DeviceCard.module.css`.

**HTML To Edit:**  
```html
<article class="glass-panel phone-card">...</article>
```

**CSS To Edit:**  
```css
.scope:hover {
  transform: translateY(-6px);
  border-color: rgba(var(--accent-rgb), 0.28);
}
```

**Expected Visual Result:**  
The card feels interactive when hovered.

**Common Mistakes:**  
- Using a harsh zoom effect
- Changing the layout size

**Possible Follow-up Question:**  
"How would you make the hover effect softer?"

## Sample 35

**Instructor Task/Question:**  
"Make the favorite button bigger."

**What The Student Should Do:**  
Increase the min-width or padding in the favorite button style.

**HTML To Edit:**  
```html
<button class="button favorite-button">Save</button>
```

**CSS To Edit:**  
```css
.full {
  min-width: 140px;
}
```

**Expected Visual Result:**  
The favorite control is easier to tap and read.

**Common Mistakes:**  
- Making it too wide in card layouts
- Forgetting the icon and text spacing

**Possible Follow-up Question:**  
"Would you keep the same size on mobile?"

## Sample 36

**Instructor Task/Question:**  
"Make the phone detail image area taller."

**What The Student Should Do:**  
Increase the height of `.phone-detail-media`.

**HTML To Edit:**  
```html
<div class="phone-detail-media">
  <img src="..." alt="Phone image" />
</div>
```

**CSS To Edit:**  
```css
.phone-detail-media {
  min-height: 420px;
}
```

**Expected Visual Result:**  
The product image becomes more prominent.

**Common Mistakes:**  
- Making it too tall on mobile
- Forgetting the container already has padding

**Possible Follow-up Question:**  
"How would you shrink it on phones?"

## Sample 37

**Instructor Task/Question:**  
"Turn the phone detail summary into a cleaner grid."

**What The Student Should Do:**  
Use the existing summary grid and keep each metric box equal.

**HTML To Edit:**  
```html
<div class="detail-summary-grid">
  <div class="metric">...</div>
</div>
```

**CSS To Edit:**  
```css
.detail-summary-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
}
```

**Expected Visual Result:**  
The summary boxes line up neatly.

**Common Mistakes:**  
- Making the boxes uneven
- Using too many columns on small screens

**Possible Follow-up Question:**  
"What happens if one metric is missing?"

## Sample 38

**Instructor Task/Question:**  
"Make the spec table easier to scan."

**What The Student Should Do:**  
Increase spacing between labels and values and strengthen section titles.

**HTML To Edit:**  
```html
<section class="specs-section">
  <div class="specs-section-title">Display</div>
</section>
```

**CSS To Edit:**  
```css
.specs-section-title {
  padding: 18px 24px;
  font-weight: 700;
}

.spec-row {
  gap: 18px;
}
```

**Expected Visual Result:**  
The long spec page feels less dense.

**Common Mistakes:**  
- Making all rows look the same
- Forgetting the mobile stacked version

**Possible Follow-up Question:**  
"Why is this page allowed to be more text-heavy?"

## Sample 39

**Instructor Task/Question:**  
"Add a border radius to this compare card."

**What The Student Should Do:**  
Round the corners of the card or panel.

**HTML To Edit:**  
```html
<article class="glass-panel compare-highlight-card">...</article>
```

**CSS To Edit:**  
```css
.compare-highlight-card {
  border-radius: 24px;
}
```

**Expected Visual Result:**  
The card looks softer and more modern.

**Common Mistakes:**  
- Forgetting the card already inherits a radius
- Making the radius too large

**Possible Follow-up Question:**  
"Which elements on the site use the largest radius?"

## Sample 40

**Instructor Task/Question:**  
"Add a shadow to this section."

**What The Student Should Do:**  
Apply a deeper shadow to the selected panel.

**HTML To Edit:**  
```html
<div class="glass-panel final-cta-card">...</div>
```

**CSS To Edit:**  
```css
.final-cta-card {
  box-shadow: 0 22px 60px rgba(4, 10, 18, 0.28);
}
```

**Expected Visual Result:**  
The section feels lifted from the background.

**Common Mistakes:**  
- Using too much blur
- Forgetting the shadow should match the site style

**Possible Follow-up Question:**  
"How would you make the shadow lighter on mobile?"

## Sample 41

**Instructor Task/Question:**  
"Make the compare buttons stack on mobile."

**What The Student Should Do:**  
Change the button row to one column on small screens.

**HTML To Edit:**  
```html
<div class="button-row">
  <a class="button">Open compare lab</a>
  <a class="button-secondary">Start from dashboard</a>
</div>
```

**CSS To Edit:**  
```css
@media (max-width: 768px) {
  .button-row {
    flex-direction: column;
  }
}
```

**Expected Visual Result:**  
The buttons become easier to tap.

**Common Mistakes:**  
- Leaving the buttons too wide side by side
- Forgetting to stretch them to full width

**Possible Follow-up Question:**  
"Why is stacking better for phone users?"

## Sample 42

**Instructor Task/Question:**  
"Reduce the spacing around these chips."

**What The Student Should Do:**  
Tighten the chip gap and padding slightly.

**HTML To Edit:**  
```html
<div class="chip-row">
  <span class="chip">Price</span>
  <span class="chip">Camera</span>
</div>
```

**CSS To Edit:**  
```css
.chip-row {
  gap: 8px;
}

.chip {
  padding: 8px 12px;
}
```

**Expected Visual Result:**  
The chips look more compact.

**Common Mistakes:**  
- Making the chips too small to tap
- Removing the gap completely

**Possible Follow-up Question:**  
"Where else in the site do chips appear?"

## Sample 43

**Instructor Task/Question:**  
"Add another card to the homepage preview grid."

**What The Student Should Do:**  
Duplicate one preview card and place it inside `.home-preview-grid`.

**HTML To Edit:**  
```html
<div class="home-preview-grid">
  <article class="home-preview-card">...</article>
</div>
```

**CSS To Edit:**  
```css
.home-preview-grid {
  display: grid;
  gap: 20px;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}
```

**Expected Visual Result:**  
The preview area shows one more phone card.

**Common Mistakes:**  
- Adding the card but not matching the same styles
- Letting the grid overflow on small screens

**Possible Follow-up Question:**  
"How would you keep the cards visually consistent?"

## Sample 44

**Instructor Task/Question:**  
"Make this footer note disappear on mobile."

**What The Student Should Do:**  
Hide `.note` in the footer mobile media query.

**HTML To Edit:**  
```html
<p class="note">Phone search, full specs, and compare mode in one place.</p>
```

**CSS To Edit:**  
```css
@media (max-width: 768px) {
  .note {
    display: none;
  }
}
```

**Expected Visual Result:**  
The footer becomes cleaner on small screens.

**Common Mistakes:**  
- Hiding the whole footer
- Forgetting the note still shows on desktop

**Possible Follow-up Question:**  
"Why is removing extra text helpful on phones?"

## Sample 45

**Instructor Task/Question:**  
"Make the loading skeleton match the real card better."

**What The Student Should Do:**  
Adjust the skeleton blocks to resemble the phone card layout more closely.

**HTML To Edit:**  
```html
<div class="phone-card phone-card-skeleton" aria-hidden="true"></div>
```

**CSS To Edit:**  
```css
.phone-card-skeleton {
  display: grid;
  gap: 14px;
  padding: 20px;
}
```

**Expected Visual Result:**  
The loading state looks like the real card shape.

**Common Mistakes:**  
- Making the skeleton random
- Forgetting the media block height

**Possible Follow-up Question:**  
"Why is matching the real layout important?"

## Sample 46

**Instructor Task/Question:**  
"Fix this overflowing card on small screens."

**What The Student Should Do:**  
Check the card width, image height, and grid layout for mobile overflow.

**HTML To Edit:**  
```html
<article class="glass-panel phone-card">...</article>
```

**CSS To Edit:**  
```css
@media (max-width: 480px) {
  .phone-card {
    padding: 16px;
  }
}
```

**Expected Visual Result:**  
The card fits neatly inside the phone screen.

**Common Mistakes:**  
- Ignoring the parent grid
- Only shrinking the text and not the container

**Possible Follow-up Question:**  
"What would you inspect first if it still overflows?"

## Sample 47

**Instructor Task/Question:**  
"Move this image beside the text."

**What The Student Should Do:**  
Change the layout to a two-column grid for the section.

**HTML To Edit:**  
```html
<div class="phone-detail-hero">
  <div class="phone-detail-media"></div>
  <div class="stack"></div>
</div>
```

**CSS To Edit:**  
```css
.phone-detail-hero {
  display: grid;
  grid-template-columns: 360px 1fr;
  gap: 28px;
}
```

**Expected Visual Result:**  
The image sits beside the text on desktop.

**Common Mistakes:**  
- Using float instead of grid
- Forgetting the mobile stack

**Possible Follow-up Question:**  
"How would you change this on mobile?"

## Sample 48

**Instructor Task/Question:**  
"Make the compare page a bit cleaner."

**What The Student Should Do:**  
Reduce padding and tighten spacing in the compare cards.

**HTML To Edit:**  
```html
<div class="compare-page">
  <div class="compare-hero-card">...</div>
</div>
```

**CSS To Edit:**  
```css
.compare-page {
  gap: 20px;
}

.compare-hero-card {
  padding: 20px;
}
```

**Expected Visual Result:**  
The page feels less crowded.

**Common Mistakes:**  
- Overcompressing the layout
- Making the page look empty

**Possible Follow-up Question:**  
"What would you keep large so the page still feels important?"

## Sample 49

**Instructor Task/Question:**  
"Change this button color on hover."

**What The Student Should Do:**  
Update the hover state for `.button`, `.button-secondary`, or `.button-ghost`.

**HTML To Edit:**  
```html
<a class="button" href="/dashboard">Start browsing</a>
```

**CSS To Edit:**  
```css
.button:hover {
  background: var(--accent-strong);
}
```

**Expected Visual Result:**  
The button changes color when hovered.

**Common Mistakes:**  
- Changing the base state instead of hover
- Using a hover color with poor contrast

**Possible Follow-up Question:**  
"How would you make the hover feel smoother?"

## Sample 50

**Instructor Task/Question:**  
"What happens if you remove this CSS rule?"

**What The Student Should Do:**  
Explain the layout effect, then test it if asked.

**HTML To Edit:**  
```html
<section class="section">
  <div class="page-shell">...</div>
</section>
```

**CSS To Edit:**  
```css
.page-shell {
  padding-inline: clamp(16px, 3vw, 36px);
}
```

**Expected Visual Result:**  
Without the rule, the content loses its side spacing.

**Common Mistakes:**  
- Guessing instead of checking the result
- Saying the rule does something unrelated

**Possible Follow-up Question:**  
"Why is `page-shell` useful across many pages?"

## Sample 51

**Instructor Task/Question:**  
"Make the theme launcher a little bigger and more visible."

**What The Student Should Do:**  
Increase the padding and shadow on the floating theme button.

**HTML To Edit:**  
```html
<button class="theme-launcher">Theme</button>
```

**CSS To Edit:**  
```css
.theme-launcher {
  padding: 12px 18px;
  box-shadow: 0 20px 44px rgba(4, 10, 18, 0.32);
}
```

**Expected Visual Result:**  
The launcher stands out more in the corner.

**Common Mistakes:**  
- Making it too large for mobile
- Forgetting to keep it circular or pill-shaped

**Possible Follow-up Question:**  
"How would you hide the text on very small screens?"

## Sample 52

**Instructor Task/Question:**  
"Add a second column to this dashboard section."

**What The Student Should Do:**  
Turn the section into a grid with two columns on desktop.

**HTML To Edit:**  
```html
<div class="dashboard-topbar dashboard-topbar-split">
  <div class="stack dashboard-copy-stack">...</div>
  <div class="button-row dashboard-cta-row">...</div>
</div>
```

**CSS To Edit:**  
```css
.dashboard-topbar-split {
  display: flex;
  justify-content: space-between;
  gap: 18px;
}
```

**Expected Visual Result:**  
The intro text and buttons sit side by side on wide screens.

**Common Mistakes:**  
- Forgetting to switch back to column on mobile
- Using a fixed width that breaks the layout

**Possible Follow-up Question:**  
"Why is a single column better on mobile?"

## Sample 53

**Instructor Task/Question:**  
"Add a border radius to this contact card."

**What The Student Should Do:**  
Round the corner values in the card style.

**HTML To Edit:**  
```html
<div class="glass-panel card">...</div>
```

**CSS To Edit:**  
```css
.card {
  border-radius: 22px;
}
```

**Expected Visual Result:**  
The card looks smoother and matches the rest of the site.

**Common Mistakes:**  
- Making the radius inconsistent with other cards
- Changing the radius on the wrong selector

**Possible Follow-up Question:**  
"Which other elements use the same radius?"

## Sample 54

**Instructor Task/Question:**  
"Make the phone cards equal size in the preview grid."

**What The Student Should Do:**  
Keep the preview cards on the same grid and let them stretch evenly.

**HTML To Edit:**  
```html
<div class="home-preview-grid">
  <article class="home-preview-card">...</article>
</div>
```

**CSS To Edit:**  
```css
.home-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
}

.home-preview-card {
  height: 100%;
}
```

**Expected Visual Result:**  
All preview cards feel balanced.

**Common Mistakes:**  
- Using different heights for different cards
- Forgetting the grid container

**Possible Follow-up Question:**  
"What would you do if one card has much longer text?"

## Sample 55

**Instructor Task/Question:**  
"Fix this text that is not centered."

**What The Student Should Do:**  
Check the parent container and apply `text-align: center` or flex alignment if needed.

**HTML To Edit:**  
```html
<div class="services-hint">
  <span>Hover each card to explore the interaction previews.</span>
</div>
```

**CSS To Edit:**  
```css
.services-hint {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}
```

**Expected Visual Result:**  
The text sits properly with its icon and feels aligned.

**Common Mistakes:**  
- Centering the text when it should stay left-aligned
- Forgetting the icon spacing

**Possible Follow-up Question:**  
"How do you decide whether something should be centered or aligned left?"

