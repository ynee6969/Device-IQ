# Defense Reviewer: 50 Basic Questions for Live Editing
## Time Limit: 15 Minutes | Difficulty: Beginner Level

---

### Question 1
Add a dark theme color variable.

**What This Means**
Create a new CSS variable in the dark mode that the app can use for styling.

**Files You Need To Open**
app/globals.css

**Why These Files**
All color variables are defined here in the :root and html[data-theme] selectors.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find the section `html[data-theme="dark"]`.
3. Scroll to the color variables section.
4. Add a new variable: `--custom-color: #1a2332;`
5. Save the file.

**Code Before**
```css
html[data-theme="dark"] {
  --accent: #46b37b;
  --danger: #ff8d8d;
}
```

**Code After**
```css
html[data-theme="dark"] {
  --accent: #46b37b;
  --custom-color: #1a2332;
  --danger: #ff8d8d;
}
```

**What Changed**
A new CSS variable `--custom-color` is now available for use in any CSS rule throughout the app.

**Common Mistakes**
- Forgetting to add the variable to both dark AND light mode selectors.
- Using invalid color formats.
- Placing the variable in the wrong section.

**Extra Notes**
Remember that CSS variables defined at :root are inherited by all elements. If you add a variable to dark mode only, light mode won't have it.

---

### Question 2
Change the button padding.

**What This Means**
Edit the .button class to make buttons have less or more internal padding.

**Files You Need To Open**
app/globals.css

**Why These Files**
The base .button class is defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.button { padding: 12px 24px; }`.
3. Change 12px to 16px (vertical padding).
4. Save.
5. Refresh the browser to see all buttons change size.

**Code Before**
```css
.button {
  padding: 12px 24px;
}
```

**Code After**
```css
.button {
  padding: 16px 24px;
}
```

**What Changed**
All buttons in the app now have more vertical padding, making them taller.

**Common Mistakes**
- Changing padding in only one CSS module instead of the global class.
- Forgetting to save the file.
- Not refreshing the browser.

**Extra Notes**
The padding syntax is: vertical horizontal. So `12px 24px` means 12px top/bottom and 24px left/right.

---

### Question 3
Make all text larger globally.

**What This Means**
Increase the base font size for the entire app by adjusting the --text-base variable.

**Files You Need To Open**
app/globals.css

**Why These Files**
The :root section defines all typography scale variables.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `--text-base: clamp(1rem, 3vw, 1.125rem);`.
3. Change the maximum value from 1.125rem to 1.5rem.
4. Save and refresh.

**Code Before**
```css
:root {
  --text-base: clamp(1rem, 3vw, 1.125rem);
}
```

**Code After**
```css
:root {
  --text-base: clamp(1rem, 3vw, 1.5rem);
}
```

**What Changed**
The largest size in the clamp() increases, so text on larger screens will be bigger.

**Common Mistakes**
- Changing only one breakpoint instead of the max value.
- Using pixels instead of rem units.

**Extra Notes**
clamp() takes three values: minimum, preferred, maximum. Change the last value to make text bigger.

---

### Question 4
Change the primary button color from green to blue.

**What This Means**
Update the accent color variable and primary button background color.

**Files You Need To Open**
app/globals.css

**Why These Files**
The accent color is defined once in :root and used by .button.primary.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `:root { --accent: #46b37b; }`.
3. Change `#46b37b` to `#5f96ff` (blue).
4. Save and refresh.
5. All green accents across the app turn blue.

**Code Before**
```css
:root {
  --accent: #46b37b;
}
```

**Code After**
```css
:root {
  --accent: #5f96ff;
}
```

**What Changed**
All elements using var(--accent) now display blue instead of green, including primary buttons.

**Common Mistakes**
- Changing color only in dark mode and forgetting light mode.
- Using a color value that doesn't have enough contrast.

**Extra Notes**
Since the accent color is a variable, changing it once updates every element that uses it.

---

### Question 5
Make images responsive.

**What This Means**
Ensure images change size on smaller screens without overflow.

**Files You Need To Open**
app/globals.css

**Why These Files**
The img selector contains global image rules.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find the `img` selector rule.
3. Confirm it has `display: block;` and `max-width: 100%;`.
4. If missing, add both rules.
5. Save and refresh.

**Code Before**
```css
img {
  display: block;
  max-width: 100%;
}
```

**Code After**
```css
img {
  display: block;
  max-width: 100%;
  height: auto;
}
```

**What Changed**
Images shrink gracefully within their containers and maintain their aspect ratio.

**Common Mistakes**
- Leaving height fixed in JSX or CSS.
- Using a parent container with fixed width smaller than the image.

**Extra Notes**
If the page uses next/image, the same rule still works for the generated img element.

---

### Question 6
Remove the box-shadow from buttons.

**What This Means**
Delete or comment out the box-shadow rule on the .button.primary:hover state.

**Files You Need To Open**
app/globals.css

**Why These Files**
The button hover state defines the shadow effect.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.button.primary:hover { box-shadow: 0 8px 25px rgba(...); }`.
3. Delete the entire `box-shadow: ...;` line.
4. Save and refresh.
5. Hover over a primary button and see no shadow.

**Code Before**
```css
.button.primary:hover {
  box-shadow: 0 8px 25px rgba(var(--accent-rgb), 0.3);
}
```

**Code After**
```css
.button.primary:hover {
  transform: translateY(-2px);
}
```

**What Changed**
The button no longer casts a shadow when hovered. Only the transform effect remains.

**Common Mistakes**
- Removing the wrong hover rule.
- Accidentally removing the transform instead.

**Extra Notes**
box-shadow creates depth. Removing it makes the button feel flatter.

---

### Question 7
Add a border-radius to all buttons.

**What This Means**
Make button corners rounder by increasing the border-radius value.

**Files You Need To Open**
app/globals.css

**Why These Files**
The .button base class defines the default border-radius.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.button { border-radius: 12px; }`.
3. Change 12px to 24px.
4. Save and refresh.
5. All buttons now have more rounded corners.

**Code Before**
```css
.button {
  border-radius: 12px;
}
```

**Code After**
```css
.button {
  border-radius: 24px;
}
```

**What Changed**
Buttons have rounder, more pill-like corners instead of slightly rounded rectangles.

**Common Mistakes**
- Using a value that's too large (like 999px) making buttons look too rounded.
- Forgetting to save.

**Extra Notes**
border-radius: 999px creates a perfect pill shape. For buttons, 20-24px works well.

---

### Question 8
Change input field border color on focus.

**What This Means**
Update the focus state border color for form inputs.

**Files You Need To Open**
app/globals.css

**Why These Files**
The input:valid rule defines focus styling for form fields.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `input:valid { border-color: var(--accent); }`.
3. Change to `border-color: var(--accent-secondary);` (blue).
4. Save and refresh.
5. Click an input field to see the new blue border color.

**Code Before**
```css
input:valid {
  border-color: var(--accent);
}
```

**Code After**
```css
input:valid {
  border-color: var(--accent-secondary);
}
```

**What Changed**
When you focus on an input, the border glows blue instead of green.

**Common Mistakes**
- Changing the wrong selector (input:invalid vs input:valid).
- Forgetting to add the display and border rules.

**Extra Notes**
:valid activates when the input is valid. :invalid activates when the input has invalid content.

---

### Question 9
Increase the spacing between navigation items.

**What This Means**
Add more space between header navigation links using a CSS gap property.

**Files You Need To Open**
components/marketing/SiteHeader.module.css

**Why These Files**
The header navigation layout is defined in this component's CSS module.

**Step-by-Step Instructions**
1. Open components/marketing/SiteHeader.module.css.
2. Find the nav selector with `gap: 12px;` or similar.
3. Change the gap value from 12px to 24px.
4. Save and refresh.
5. Nav links are now more spaced out.

**Code Before**
```css
nav {
  display: flex;
  gap: 12px;
}
```

**Code After**
```css
nav {
  display: flex;
  gap: 24px;
}
```

**What Changed**
Navigation items are now further apart horizontally.

**Common Mistakes**
- Changing padding instead of gap.
- Forgetting to save.

**Extra Notes**
gap controls the space between flex or grid items. It only works with flex and grid containers.

---

### Question 10
Make the page background lighter.

**What This Means**
Change the --bg color variable to a lighter shade in dark mode.

**Files You Need To Open**
app/globals.css

**Why These Files**
The background color is defined in the :root section.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `:root { --bg: #0d1117; }`.
3. Change #0d1117 to #1a1f2e (slightly lighter).
4. Save and refresh.
5. The entire page background is now a bit lighter.

**Code Before**
```css
:root {
  --bg: #0d1117;
}
```

**Code After**
```css
:root {
  --bg: #1a1f2e;
}
```

**What Changed**
The background of the entire page shifts from very dark to slightly lighter dark.

**Common Mistakes**
- Only changing it in one theme mode.
- Using a value that loses contrast with text.

**Extra Notes**
Make sure text remains readable. Use a contrast checker if unsure.

---

### Question 11
Add a hover effect to links.

**What This Means**
Create a CSS rule that changes the appearance of links when you hover over them.

**Files You Need To Open**
app/globals.css

**Why These Files**
The global link styling is defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find the `a { color: inherit; }` rule.
3. Add a new rule below it: `a:hover { text-decoration: underline; }`.
4. Save and refresh.
5. Hover over any link to see the underline appear.

**Code Before**
```css
a {
  color: inherit;
  text-decoration: none;
}
```

**Code After**
```css
a {
  color: inherit;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
```

**What Changed**
Links now show an underline when you hover over them, providing visual feedback.

**Common Mistakes**
- Forgetting the colon in :hover.
- Placing the rule in the wrong CSS file.

**Extra Notes**
:hover is a pseudo-class that activates when the user hovers their mouse over the element.

---

### Question 12
Change the card shadow effect.

**What This Means**
Update the --shadow variable to create a different shadow depth for cards.

**Files You Need To Open**
app/globals.css

**Why These Files**
The shadow token is defined in :root.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `--shadow: 0 18px 48px rgba(15, 23, 42, 0.12);`.
3. Change to `--shadow: 0 10px 30px rgba(15, 23, 42, 0.15);` (softer).
4. Save and refresh.
5. All glass-panel cards now have a softer shadow.

**Code Before**
```css
:root {
  --shadow: 0 18px 48px rgba(15, 23, 42, 0.12);
}
```

**Code After**
```css
:root {
  --shadow: 0 10px 30px rgba(15, 23, 42, 0.15);
}
```

**What Changed**
Cards cast a softer, closer shadow instead of a more dramatic distant shadow.

**Common Mistakes**
- Not understanding shadow syntax (x-offset, y-offset, blur, color).
- Changing the opacity without adjusting blur.

**Extra Notes**
Shadow syntax: `offset-x offset-y blur-radius color`. Larger blur = softer shadow.

---

### Question 13
Remove the animation from buttons.

**What This Means**
Delete or comment out the transition property on the .button class.

**Files You Need To Open**
app/globals.css

**Why These Files**
The transition rule is in the base .button class.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.button { transition: all 0.3s cubic-bezier(...); }`.
3. Delete the entire transition line.
4. Save and refresh.
5. Button hover effects are now instant instead of smooth.

**Code Before**
```css
.button {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
```

**Code After**
```css
.button {
  /* transition removed */
}
```

**What Changed**
When you hover or interact with buttons, changes happen instantly instead of animating over 0.3 seconds.

**Common Mistakes**
- Only removing it from one button state.
- Accidentally removing other properties.

**Extra Notes**
transition: all 0.3s means all properties animate over 0.3 seconds. It affects hover, active, and focus states.

---

### Question 14
Adjust the focus outline color.

**What This Means**
Change the outline color that appears when a button or input is focused via keyboard.

**Files You Need To Open**
app/globals.css

**Why These Files**
The .focus-visible class defines focus styling for accessibility.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.focus-visible:focus-visible { outline: 2px solid var(--accent); }`.
3. Change `var(--accent)` to `var(--danger)` (red).
4. Save and refresh.
5. Tab through buttons and inputs to see a red focus outline.

**Code Before**
```css
.focus-visible:focus-visible {
  outline: 2px solid var(--accent);
}
```

**Code After**
```css
.focus-visible:focus-visible {
  outline: 2px solid var(--danger);
}
```

**What Changed**
Keyboard focus indicators are now red instead of green.

**Common Mistakes**
- Removing the :focus-visible pseudo-class entirely (bad for accessibility).
- Changing the wrong selector.

**Extra Notes**
focus-visible is essential for keyboard navigation. Always ensure it's clearly visible.

---

### Question 15
Make the mobile tab bar sticky.

**What This Means**
Add position: fixed to the MobileTabBar so it stays visible when scrolling.

**Files You Need To Open**
components/marketing/MobileTabBar.module.css

**Why These Files**
The mobile navigation is defined in this component's CSS module.

**Step-by-Step Instructions**
1. Open components/marketing/MobileTabBar.module.css.
2. Find the main nav selector (e.g., `.tabbar {`).
3. Add `position: fixed;` if not already there.
4. Add `bottom: 0;` to stick it to the bottom.
5. Add `width: 100%;` to span full width.
6. Save and refresh.
7. Scroll the page and the tab bar stays visible.

**Code Before**
```css
.tabbar {
  display: flex;
  gap: 12px;
}
```

**Code After**
```css
.tabbar {
  display: flex;
  gap: 12px;
  position: fixed;
  bottom: 0;
  width: 100%;
}
```

**What Changed**
The mobile navigation bar is now fixed to the bottom of the viewport and remains visible while scrolling.

**Common Mistakes**
- Forgetting to set bottom: 0 or top: 0.
- Not setting width: 100%.
- Forgetting that fixed positioning removes the element from document flow.

**Extra Notes**
Be careful with position: fixed on large screens. Usually this is for mobile only (wrap in @media).

---

### Question 16
Change the primary text color.

**What This Means**
Modify the --text variable to use a different color for all body text.

**Files You Need To Open**
app/globals.css

**Why These Files**
The text color is defined in :root and inherited by the body element.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `:root { --text: #f5f7fb; }`.
3. Change to `--text: #e0e7ff;` (slightly different shade).
4. Save and refresh.
5. All text color changes globally.

**Code Before**
```css
:root {
  --text: #f5f7fb;
}
```

**Code After**
```css
:root {
  --text: #e0e7ff;
}
```

**What Changed**
All body text shifts to a new color. Make sure it still has good contrast with the background.

**Common Mistakes**
- Using a color too similar to the background.
- Only changing dark mode and forgetting light mode.

**Extra Notes**
The text color cascades to all elements unless explicitly overridden.

---

### Question 17
Add a muted text style.

**What This Means**
Create a new CSS class that styles text in a lighter, secondary color.

**Files You Need To Open**
app/globals.css

**Why These Files**
Reusable text utility classes are defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find the utilities section (after button rules).
3. Add a new class:
   ```css
   .text-muted {
     color: var(--muted);
   }
   ```
4. Save.
5. Use it in any component: `<p class="text-muted">Secondary text</p>`.

**Code Before**
```css
.button { /* ... */ }
```

**Code After**
```css
.button { /* ... */ }

.text-muted {
  color: var(--muted);
}
```

**What Changed**
A new utility class is available for styling secondary text throughout the app.

**Common Mistakes**
- Forgetting to use the CSS variable instead of a hard-coded color.
- Placing it in the wrong CSS file (component module instead of globals).

**Extra Notes**
Utility classes are single-purpose. They should be combined for layout: `<p class="text-muted" style="margin-bottom: 16px;">`.

---

### Question 18
Increase button font size.

**What This Means**
Make the text inside buttons larger by adjusting the font-size property.

**Files You Need To Open**
app/globals.css

**Why These Files**
The base button font size is defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.button { font-size: var(--text-sm); }`.
3. Change to `font-size: var(--text-base);` (one size up).
4. Save and refresh.
5. All buttons have larger text.

**Code Before**
```css
.button {
  font-size: var(--text-sm);
}
```

**Code After**
```css
.button {
  font-size: var(--text-base);
}
```

**What Changed**
Button text scales up from small to base size, making buttons more readable.

**Common Mistakes**
- Changing only one button variant instead of the base class.
- Using absolute pixels instead of responsive clamp() variables.

**Extra Notes**
Using CSS variables for font sizes ensures responsiveness across all screen sizes.

---

### Question 19
Add a dotted border to inputs.

**What This Means**
Change the input border from solid to dotted style.

**Files You Need To Open**
app/globals.css

**Why These Files**
The input element styles are defined in the form element styles section.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Look for input styling rules (search for "input {").
3. Find or add a `border-style: solid;` line.
4. Change to `border-style: dotted;`.
5. Save and refresh.
6. All input fields now have dotted borders.

**Code Before**
```css
input {
  border-style: solid;
}
```

**Code After**
```css
input {
  border-style: dotted;
}
```

**What Changed**
Input field borders are now dotted instead of solid lines.

**Common Mistakes**
- Using `border: dotted;` instead of `border-style: dotted;` (overwrites other border properties).
- Not finding the input styles section.

**Extra Notes**
border-style can be: solid, dotted, dashed, double, groove, ridge, inset, outset.

---

### Question 20
Change the accent color RGB value.

**What This Means**
Update the --accent-rgb variable which is used for rgba() color mixing.

**Files You Need To Open**
app/globals.css

**Why These Files**
RGB values are stored separately for use in color-mix() functions.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `--accent-rgb: 70, 179, 123;`.
3. Change to `--accent-rgb: 95, 150, 255;` (matching the blue accent).
4. Save and refresh.
5. Any color-mix using var(--accent-rgb) updates to blue tones.

**Code Before**
```css
:root {
  --accent-rgb: 70, 179, 123;
}
```

**Code After**
```css
:root {
  --accent-rgb: 95, 150, 255;
}
```

**What Changed**
All color-mix calls that use the accent RGB value now produce blue tones instead of green tones.

**Common Mistakes**
- Forgetting to update both the hex and RGB versions.
- Using the wrong RGB values for the hex color.

**Extra Notes**
The RGB format (R, G, B) is needed for rgba() and color-mix(). It must match the hex color.

---

### Question 21
Remove the border from secondary buttons.

**What This Means**
Delete the border property from the .button.secondary rule.

**Files You Need To Open**
app/globals.css

**Why These Files**
Secondary button styling is defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.button.secondary { border-color: var(--border); }`.
3. Change to `border-color: transparent;` OR delete the entire line.
4. Save and refresh.
5. Secondary buttons no longer have visible borders.

**Code Before**
```css
.button.secondary {
  border-color: var(--border);
}
```

**Code After**
```css
.button.secondary {
  border-color: transparent;
}
```

**What Changed**
Secondary buttons are now borderless (they still have a 1px border, but it's invisible).

**Common Mistakes**
- Deleting the border-width property instead (buttons would still have a border).
- Changing the wrong button variant.

**Extra Notes**
Setting border-color to transparent keeps the border space but makes it invisible.

---

### Question 22
Adjust the border radius on cards.

**What This Means**
Change the --radius-lg variable which is used for rounding card corners.

**Files You Need To Open**
app/globals.css

**Why These Files**
All radius tokens are defined in :root.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `:root { --radius-lg: 22px; }`.
3. Change to `--radius-lg: 32px;` (more rounded).
4. Save and refresh.
5. All cards using var(--radius-lg) are now more rounded.

**Code Before**
```css
:root {
  --radius-lg: 22px;
}
```

**Code After**
```css
:root {
  --radius-lg: 32px;
}
```

**What Changed**
Cards have more pronounced rounded corners instead of subtle rounding.

**Common Mistakes**
- Using a value too large (like 50px) making cards look odd.
- Only changing one radius variable when others might also need updating.

**Extra Notes**
The project uses a radius scale: --radius-xl (largest), --radius-lg, --radius-md (smallest).

---

### Question 23
Make all spacing larger globally.

**What This Means**
Increase all --space-* variables to add more breathing room throughout the page.

**Files You Need To Open**
app/globals.css

**Why These Files**
All spacing tokens are defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find the `:root { --space-1: clamp(...); }` section.
3. Increase the maximum values for each space variable by 50%:
   - --space-1: change max from 0.5rem to 0.75rem
   - --space-2: change max from 1rem to 1.5rem
   - And so on.
4. Save and refresh.
5. The entire page has more generous spacing.

**Code Before**
```css
:root {
  --space-2: clamp(0.5rem, 2vw, 1rem);
  --space-3: clamp(0.75rem, 3vw, 1.5rem);
}
```

**Code After**
```css
:root {
  --space-2: clamp(0.5rem, 2vw, 1.5rem);
  --space-3: clamp(0.75rem, 3vw, 2.25rem);
}
```

**What Changed**
All margins, paddings, and gaps using space variables increase proportionally.

**Common Mistakes**
- Only changing one or two space variables.
- Using absolute values instead of maintaining the clamp() responsive approach.

**Extra Notes**
Increasing spacing improves readability and gives the design a more premium feel.

---

### Question 24
Add a color transition effect.

**What This Means**
Add a transition rule that makes color changes animate smoothly.

**Files You Need To Open**
app/globals.css

**Why These Files**
The a (link) element styling is where you can add a transition for color changes.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find the `a { color: inherit; }` rule.
3. Add `transition: color 0.3s ease;` to the rule.
4. Then add `a:hover { color: var(--accent); }` if not present.
5. Save and refresh.
6. Click a link and the color animates instead of changing instantly.

**Code Before**
```css
a {
  color: inherit;
}

a:hover {
  color: var(--accent);
}
```

**Code After**
```css
a {
  color: inherit;
  transition: color 0.3s ease;
}

a:hover {
  color: var(--accent);
}
```

**What Changed**
Link color changes now animate over 0.3 seconds instead of changing instantly.

**Common Mistakes**
- Putting the transition on hover instead of the base element.
- Using an incorrect easing function.

**Extra Notes**
transition: color specifies only color animates. transition: all makes everything animate.

---

### Question 25
Adjust the muted text color.

**What This Means**
Change the --muted variable to a different secondary text color.

**Files You Need To Open**
app/globals.css

**Why These Files**
The muted color is defined in :root.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `:root { --muted: #9ba7ba; }`.
3. Change to `--muted: #7a8898;` (slightly darker for better contrast).
4. Save and refresh.
5. All secondary/muted text becomes darker.

**Code Before**
```css
:root {
  --muted: #9ba7ba;
}
```

**Code After**
```css
:root {
  --muted: #7a8898;
}
```

**What Changed**
Secondary text (labels, hints, descriptions) is now darker and more visible.

**Common Mistakes**
- Only changing dark mode without updating light mode.
- Using a color too close to the main text color.

**Extra Notes**
Ensure contrast ratio is at least 4.5:1 for accessibility.

---

### Question 26
Add a drop shadow to the header.

**What This Means**
Add a box-shadow property to the SiteHeader to create a subtle shadow below it.

**Files You Need To Open**
components/marketing/SiteHeader.module.css

**Why These Files**
Header-specific styling is in this component's CSS module.

**Step-by-Step Instructions**
1. Open components/marketing/SiteHeader.module.css.
2. Find the main header selector (e.g., `.header {`).
3. Add `box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);`.
4. Save and refresh.
5. The header now has a subtle shadow underneath it.

**Code Before**
```css
.header {
  display: flex;
  padding: 16px;
}
```

**Code After**
```css
.header {
  display: flex;
  padding: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}
```

**What Changed**
The header appears to float above the page with a subtle shadow.

**Common Mistakes**
- Using a shadow too dark or too large (looks overdone).
- Forgetting to save.

**Extra Notes**
Keep shadows subtle on modern designs. Use small blur values (2-12px).

---

### Question 27
Change the compare page card layout.

**What This Means**
Adjust the grid-template-columns in the compare page CSS to change how cards are arranged.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
The compare page layout is defined in this specific CSS module.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-selector-grid) { grid-template-columns: repeat(2, minmax(0, 1fr)); }`.
3. Change `repeat(2, ...)` to `repeat(1, ...)` to stack cards vertically.
4. Save and refresh.
5. Compare cards now stack in a single column instead of two columns.

**Code Before**
```css
.page :global(.compare-selector-grid) {
  grid-template-columns: repeat(2, minmax(0, 1fr));
}
```

**Code After**
```css
.page :global(.compare-selector-grid) {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}
```

**What Changed**
The compare card selector layout changes from 2 columns to 1 column.

**Common Mistakes**
- Confusing repeat() syntax. repeat(2, 1fr) means 2 columns, repeat(3, 1fr) means 3.
- Not understanding that this affects all compare grids.

**Extra Notes**
Use repeat(auto-fit, minmax(300px, 1fr)) for truly responsive grids that don't need media queries.

---

### Question 28
Increase the compare page card padding.

**What This Means**
Change the padding value on compare card selectors.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
Compare card styling is in this module.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-selector-card) { padding: ... }` or add it.
3. Change padding to `padding: 32px;` (or add if missing).
4. Save and refresh.
5. Compare cards now have more internal padding.

**Code Before**
```css
.page :global(.compare-selector-card) {
  display: grid;
  gap: 22px;
}
```

**Code After**
```css
.page :global(.compare-selector-card) {
  display: grid;
  gap: 22px;
  padding: 32px;
}
```

**What Changed**
Content inside compare cards has more breathing room.

**Common Mistakes**
- Using inconsistent padding values across different cards.
- Confusing padding (inside) with margin (outside).

**Extra Notes**
Padding increases space inside an element. Margin increases space outside.

---

### Question 29
Change the compare score card background.

**What This Means**
Modify the background color of the comparison score display card.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
Compare card styling is here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-score-card) {`.
3. Add or modify `background: var(--surface-soft);`.
4. Save and refresh.
5. The score card now uses the secondary surface color.

**Code Before**
```css
.page :global(.compare-score-card) {
  padding: 24px;
}
```

**Code After**
```css
.page :global(.compare-score-card) {
  padding: 24px;
  background: var(--surface-soft);
}
```

**What Changed**
The compare score card has a subtly different background, helping it stand out.

**Common Mistakes**
- Using a color that blends with the main background.
- Forgetting to use a CSS variable (hardcoding instead).

**Extra Notes**
Always use CSS variables for colors so theme changes are consistent.

---

### Question 30
Add overflow hidden to prevent image spillover.

**What This Means**
Add overflow: hidden to a container so images don't exceed its boundaries.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
The compare page image containers are styled here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-phone-media) {`.
3. Confirm `overflow: hidden;` is present.
4. If not, add it.
5. Save and refresh.
6. Images inside phone media containers are clipped to the container bounds.

**Code Before**
```css
.page :global(.compare-phone-media) {
  height: 260px;
  border-radius: 24px;
}
```

**Code After**
```css
.page :global(.compare-phone-media) {
  height: 260px;
  border-radius: 24px;
  overflow: hidden;
}
```

**What Changed**
Images are clipped inside the rounded container instead of spilling outside.

**Common Mistakes**
- Using overflow: scroll (adds unwanted scrollbars).
- Using overflow: visible (defeats the purpose).

**Extra Notes**
overflow: hidden is essential when combining rounded corners with images.

---

### Question 31
Change the badge position in compare cards.

**What This Means**
Adjust the absolute positioning of the versus badge in the compare hero card.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
The badge positioning is in this module.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-versus-badge) { left: 50%; top: 50%; }`.
3. Change `top: 50%;` to `top: 30%;` to move it higher.
4. Save and refresh.
5. The versus badge moves up from the center of the card.

**Code Before**
```css
.page :global(.compare-versus-badge) {
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%);
}
```

**Code After**
```css
.page :global(.compare-versus-badge) {
  left: 50%;
  top: 30%;
  transform: translate(-50%, -50%);
}
```

**What Changed**
The badge position moves up, creating a different visual composition.

**Common Mistakes**
- Forgetting the transform: translate() to center it properly.
- Using wrong percentage values that put it off-screen.

**Extra Notes**
The transform: translate(-50%, -50%) centers an absolutely positioned element perfectly.

---

### Question 32
Increase the insight list padding.

**What This Means**
Add more padding to list items in the insight list.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
The insight list styling is here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.insight-list li) { padding: 14px 16px; }`.
3. Change to `padding: 20px 24px;` (more generous).
4. Save and refresh.
5. Insight list items now have more internal spacing.

**Code Before**
```css
.page :global(.insight-list li) {
  padding: 14px 16px;
}
```

**Code After**
```css
.page :global(.insight-list li) {
  padding: 20px 24px;
}
```

**What Changed**
List items are taller and have more breathing room inside.

**Common Mistakes**
- Using only one padding value (applies to all sides).
- Confusing padding with margin.

**Extra Notes**
Padding syntax: vertical horizontal. 20px 24px = 20px top/bottom, 24px left/right.

---

### Question 33
Change the compare score row layout.

**What This Means**
Modify the grid-template-columns in the compare score row to adjust the layout.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
The score row layout is in this module.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-score-row) { grid-template-columns: minmax(0, 1fr) 160px minmax(0, 1fr); }`.
3. Change the middle value from 160px to 200px (wider center column).
4. Save and refresh.
5. The center column (label) is now wider.

**Code Before**
```css
.page :global(.compare-score-row) {
  grid-template-columns: minmax(0, 1fr) 160px minmax(0, 1fr);
}
```

**Code After**
```css
.page :global(.compare-score-row) {
  grid-template-columns: minmax(0, 1fr) 200px minmax(0, 1fr);
}
```

**What Changed**
The center comparison label is now wider, giving more space for text.

**Common Mistakes**
- Using fixed widths that make layout fragile.
- Not understanding the three-column layout purpose.

**Extra Notes**
The pattern is: flex column | center label | flex column, for balanced comparison display.

---

### Question 34
Remove border from compare cards.

**What This Means**
Delete or change the border property on compare card selectors.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
Card border styling is here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-selector-card) { border: ... }` or similar.
3. Change `border: 1px solid var(--border);` to `border: none;` OR delete the line.
4. Save and refresh.
5. Compare cards no longer have borders.

**Code Before**
```css
.page :global(.compare-selector-card) {
  border: 1px solid var(--border);
}
```

**Code After**
```css
.page :global(.compare-selector-card) {
  border: none;
}
```

**What Changed**
Compare cards appear without borders, giving a cleaner appearance.

**Common Mistakes**
- Using `border: transparent;` instead of `border: none;`.
- Only removing it from one card type.

**Extra Notes**
Use `border: none;` to completely remove borders. `border: transparent;` still reserves space.

---

### Question 35
Adjust the compare phone hero card border-radius.

**What This Means**
Change the border-radius on the phone hero cards to make them rounder or sharper.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
Phone card styling is here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-phone-hero) { border-radius: 26px; }`.
3. Change to `border-radius: 32px;` (rounder).
4. Save and refresh.
5. Phone hero cards are now more rounded.

**Code Before**
```css
.page :global(.compare-phone-hero) {
  border-radius: 26px;
}
```

**Code After**
```css
.page :global(.compare-phone-hero) {
  border-radius: 32px;
}
```

**What Changed**
The phone card corners are more pronounced/rounded.

**Common Mistakes**
- Using a value that's too large (>50px for cards).
- Forgetting to save.

**Extra Notes**
Keep border-radius consistent with your design system. Usually 16-32px for cards.

---

### Question 36
Add a gap between compare sections.

**What This Means**
Increase the gap value in the compare sections grid.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
The compare sections grid is defined here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-sections) { gap: 24px; }`.
3. Change to `gap: 32px;` (more space between sections).
4. Save and refresh.
5. More space appears between compare sections.

**Code Before**
```css
.page :global(.compare-sections) {
  gap: 24px;
}
```

**Code After**
```css
.page :global(.compare-sections) {
  gap: 32px;
}
```

**What Changed**
The vertical spacing between compare sections increases.

**Common Mistakes**
- Confusing gap (flex/grid spacing) with padding (internal spacing).
- Changing it to a value too large (>48px usually looks odd).

**Extra Notes**
gap only works on flex and grid containers.

---

### Question 37
Change the compare phone label color.

**What This Means**
Modify the color property of the compare phone label text.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
Phone label styling is here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-phone-label) { color: var(--muted); }`.
3. Change to `color: var(--accent);` (accent color).
4. Save and refresh.
5. The "Phone 1" and "Phone 2" labels are now green instead of gray.

**Code Before**
```css
.page :global(.compare-phone-label) {
  color: var(--muted);
}
```

**Code After**
```css
.page :global(.compare-phone-label) {
  color: var(--accent);
}
```

**What Changed**
Phone labels (e.g., "Phone 1") are now colored with the accent green instead of muted gray.

**Common Mistakes**
- Using a color that blends with the background.
- Not checking contrast for accessibility.

**Extra Notes**
Always use CSS variables for colors to ensure theme consistency.

---

### Question 38
Adjust font weight of compare titles.

**What This Means**
Change the font-weight property on compare section titles.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
Title styling for compare sections is here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-phone-hero h2) { font-weight: ... }` or add it.
3. Change or add `font-weight: 700;` to make it bolder, or try 600 for lighter.
4. Save and refresh.
5. Compare titles are now bolder or lighter.

**Code Before**
```css
.page :global(.compare-phone-hero h2) {
  font-size: clamp(1.45rem, 2.4vw, 2.1rem);
}
```

**Code After**
```css
.page :global(.compare-phone-hero h2) {
  font-size: clamp(1.45rem, 2.4vw, 2.1rem);
  font-weight: 700;
}
```

**What Changed**
Compare titles are now bold (weight 700) for more emphasis.

**Common Mistakes**
- Using invalid font-weight values (must be 100-900, in steps of 100).
- Overriding important font rendering.

**Extra Notes**
Font weights: 400=normal, 500=medium, 700=bold, 900=extra bold.

---

### Question 39
Change the compare score cell background.

**What This Means**
Modify the background color of score cells in the comparison table.

**Files You Need To Open**
app/compare/page.module.css

**Why These Files**
Score cell styling is here.

**Step-by-Step Instructions**
1. Open app/compare/page.module.css.
2. Find `.page :global(.compare-score-cell) {`.
3. Add or change `background: var(--surface);` to use a different background.
4. Save and refresh.
5. Score cells now have a different background than surrounding elements.

**Code Before**
```css
.page :global(.compare-score-cell) {
  font-weight: 700;
  text-align: center;
}
```

**Code After**
```css
.page :global(.compare-score-cell) {
  font-weight: 700;
  text-align: center;
  background: var(--surface);
}
```

**What Changed**
Score cells now have a distinct background, helping them stand out in the comparison table.

**Common Mistakes**
- Using a background color that doesn't contrast with text.
- Forgetting to use a CSS variable.

**Extra Notes**
Use --surface or --surface-soft for subtle differentiation.

---

### Question 40
Increase border width on glass panels.

**What This Means**
Add or modify the border-width property on glass panel cards.

**Files You Need To Open**
app/globals.css

**Why These Files**
The .glass-panel utility class is defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.glass-panel { border: 1px solid var(--border); }` or similar.
3. Change `1px` to `2px` (thicker border).
4. Save and refresh.
5. All glass panels now have thicker borders.

**Code Before**
```css
.glass-panel {
  border: 1px solid var(--border);
}
```

**Code After**
```css
.glass-panel {
  border: 2px solid var(--border);
}
```

**What Changed**
Glass panels are outlined with a thicker, more prominent border.

**Common Mistakes**
- Using values >3px (usually too thick for subtlety).
- Changing the border-color by accident.

**Extra Notes**
Borders add visual definition. Thicker borders (2px) work for modern glassmorphism designs.

---

### Question 41
Add text-shadow to headings.

**What This Means**
Add a text-shadow property to h2 or h3 elements for depth.

**Files You Need To Open**
app/globals.css

**Why These Files**
Base heading styles are here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find the heading styles or add one: `h2 { ... }`.
3. Add `text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);`.
4. Save and refresh.
5. Headings now have a subtle shadow behind the text.

**Code Before**
```css
h2 {
  font-size: var(--text-2xl);
}
```

**Code After**
```css
h2 {
  font-size: var(--text-2xl);
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
```

**What Changed**
Headings appear to have depth with a subtle text shadow.

**Common Mistakes**
- Using shadows too strong (looks blurry).
- Applying to body text (only use on headings for emphasis).

**Extra Notes**
Text shadows should be subtle. Use small blur values (2-4px) and low opacity (0.1-0.2).

---

### Question 42
Change the page section gap.

**What This Means**
Adjust the gap property in the .section class to change spacing between sections.

**Files You Need To Open**
app/globals.css

**Why These Files**
The .section utility class is defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.section { gap: ... }` or add the property.
3. Change or add `gap: 48px;` (vertical spacing between sections).
4. Save and refresh.
5. More or less space appears between page sections.

**Code Before**
```css
.section {
  display: grid;
}
```

**Code After**
```css
.section {
  display: grid;
  gap: 48px;
}
```

**What Changed**
Vertical spacing between page sections increases, improving readability.

**Common Mistakes**
- Using values too large (>80px) creating excessive gaps.
- Forgetting that sections need to be grid or flex to use gap.

**Extra Notes**
Use a consistent gap value (24px, 32px, 48px) throughout the design for visual harmony.

---

### Question 43
Make the container full width.

**What This Means**
Remove max-width constraint on the main content container.

**Files You Need To Open**
app/globals.css

**Why These Files**
The .page-shell or .container max-width is defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.page-shell { max-width: 1200px; }` or similar.
3. Change to `max-width: none;` or delete the property.
4. Save and refresh.
5. Content now spans the full viewport width.

**Code Before**
```css
.page-shell {
  max-width: 1200px;
  margin: 0 auto;
}
```

**Code After**
```css
.page-shell {
  max-width: none;
  margin: 0 auto;
}
```

**What Changed**
The page content is no longer constrained to a max-width and fills the entire screen.

**Common Mistakes**
- Removing max-width without removing margin: 0 auto.
- Forgetting to add horizontal padding for edge content.

**Extra Notes**
Without max-width, add horizontal padding (padding: 0 24px) to prevent text touching screen edges.

---

### Question 44
Add a gradient background to the page.

**What This Means**
Replace the solid background color with a linear or radial gradient.

**Files You Need To Open**
app/globals.css

**Why These Files**
The body background is set here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `body { background: var(--bg); }`.
3. Change to `background: linear-gradient(135deg, var(--bg) 0%, var(--surface-strong) 100%);`.
4. Save and refresh.
5. The page now has a subtle gradient background.

**Code Before**
```css
body {
  background: var(--bg);
}
```

**Code After**
```css
body {
  background: linear-gradient(135deg, var(--bg) 0%, var(--surface-strong) 100%);
}
```

**What Changed**
The page background transitions from one color to another diagonally.

**Common Mistakes**
- Using colors with low contrast (gradient is invisible).
- Making the gradient too steep or colorful (distracting).

**Extra Notes**
Keep gradients subtle. Use colors from your palette. Use 135deg (diagonal) for modern look.

---

### Question 45
Change input field styling.

**What This Means**
Modify the input element's padding, border, or background properties.

**Files You Need To Open**
app/globals.css

**Why These Files**
Form element styles are defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find the `input {` rule (in form element styles section).
3. Change or add `padding: 12px 16px;`.
4. Change or add `background: var(--surface-soft);`.
5. Save and refresh.
6. Input fields now have more padding and a distinct background.

**Code Before**
```css
input {
  border: 1px solid var(--border);
}
```

**Code After**
```css
input {
  border: 1px solid var(--border);
  padding: 12px 16px;
  background: var(--surface-soft);
}
```

**What Changed**
Input fields now have more generous padding and a slightly darker background for better visibility.

**Common Mistakes**
- Using padding that's too large (makes inputs tall and awkward).
- Not setting a background (inputs blend with page).

**Extra Notes**
Input padding should match button padding for visual consistency.

---

### Question 46
Add letter-spacing to titles.

**What This Means**
Add space between letters in headings for a more premium, spread-out look.

**Files You Need To Open**
app/globals.css

**Why These Files**
Heading styles are defined here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find or create an `h2 {` rule.
3. Add `letter-spacing: -0.02em;` (negative spacing tightens; positive spreads).
4. Save and refresh.
5. Titles now have adjusted letter spacing.

**Code Before**
```css
h2 {
  font-size: var(--text-2xl);
}
```

**Code After**
```css
h2 {
  font-size: var(--text-2xl);
  letter-spacing: -0.02em;
}
```

**What Changed**
Letters in headings are now tighter/closer together (with negative letter-spacing).

**Common Mistakes**
- Using positive values too large (>0.1em) making text hard to read.
- Applying to body text (use only on headings).

**Extra Notes**
em units are relative to font size. 0.02em = 2% of current font size.

---

### Question 47
Change the focus outline width.

**What This Means**
Adjust the outline width on focused elements for keyboard navigation.

**Files You Need To Open**
app/globals.css

**Why These Files**
The .focus-visible class defines focus styling.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `.focus-visible:focus-visible { outline: 2px solid ... }`.
3. Change `2px` to `3px` (thicker outline).
4. Save and refresh.
5. Tab through the page and see a thicker focus outline.

**Code Before**
```css
.focus-visible:focus-visible {
  outline: 2px solid var(--accent);
}
```

**Code After**
```css
.focus-visible:focus-visible {
  outline: 3px solid var(--accent);
}
```

**What Changed**
The focus outline is now thicker and more visible, improving accessibility.

**Common Mistakes**
- Using values >4px (too visually aggressive).
- Removing the outline entirely (bad for keyboard users).

**Extra Notes**
A thicker outline (2-3px) is essential for accessibility. Never remove it.

---

### Question 48
Add min-height to the body.

**What This Means**
Ensure the body always takes up at least full viewport height.

**Files You Need To Open**
app/globals.css

**Why These Files**
Body element baseline styles are here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `body { ... }`.
3. Confirm `min-height: 100vh;` is present.
4. If not, add it.
5. Save and refresh.
6. The page always fills the viewport, pushing footer to bottom on short pages.

**Code Before**
```css
body {
  margin: 0;
  background: var(--bg);
}
```

**Code After**
```css
body {
  margin: 0;
  background: var(--bg);
  min-height: 100vh;
}
```

**What Changed**
The body ensures the page is always at least 100% viewport height, improving footer positioning.

**Common Mistakes**
- Using height: 100vh (causes overflow on small devices).
- Forgetting to set min-height (footer can float mid-page).

**Extra Notes**
100vh = 100% of viewport height. Use min-height to allow content taller than viewport.

---

### Question 49
Change line-height for better readability.

**What This Means**
Adjust the line-height property on body text for more or less spacing between lines.

**Files You Need To Open**
app/globals.css

**Why These Files**
Body text line-height is set here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find or add `body { line-height: 1.5; }`.
3. Change to `line-height: 1.6;` (more space between lines).
4. Save and refresh.
5. Text is now more spaced vertically, easier to read.

**Code Before**
```css
body {
  line-height: 1.5;
}
```

**Code After**
```css
body {
  line-height: 1.6;
}
```

**What Changed**
The vertical spacing between lines of text increases, improving readability.

**Common Mistakes**
- Using values too large (>2.0 makes text feel disconnected).
- Using absolute values like 20px (won't scale with font size).

**Extra Notes**
Recommended line-height for body text: 1.5 to 1.8. Use unitless numbers for best results.

---

### Question 50
Adjust the scroll behavior.

**What This Means**
Change the scroll-behavior property to control how the page scrolls to anchor links.

**Files You Need To Open**
app/globals.css

**Why These Files**
The html element scroll behavior is set here.

**Step-by-Step Instructions**
1. Open app/globals.css.
2. Find `html { scroll-behavior: smooth; }`.
3. Change to `scroll-behavior: auto;` for instant jumping (or keep smooth).
4. Save and refresh.
5. Click an anchor link to see if it scrolls smoothly or jumps instantly.

**Code Before**
```css
html {
  scroll-behavior: smooth;
}
```

**Code After**
```css
html {
  scroll-behavior: auto;
}
```

**What Changed**
The page now jumps instantly to anchor links instead of scrolling smoothly (or vice versa).

**Common Mistakes**
- Using invalid values (only smooth and auto are standard).
- Causing performance issues with smooth (avoid on very long pages).

**Extra Notes**
smooth scroll provides a polished UX but uses more CPU. auto is instant and lightweight.

---

## How to Use This Reviewer

1. **Print or Display**: Open this file in VS Code or a markdown viewer.
2. **Teacher Reviews**: A teacher can ask any of these 50 questions in random order.
3. **Live Editing**: For each question, you have ~18 seconds to:
   - Understand the file location
   - Find the relevant CSS rule
   - Make the change
   - Save and refresh the browser
4. **Demonstration**: Show the teacher the change working in the browser.

## Tips for Success

- **Familiarize yourself** with the file structure of app/globals.css and component CSS modules.
- **Practice finding code** quickly using Ctrl+F to search for specific selectors.
- **Understand CSS units**: px, rem, em, clamp(), %, vw, vh.
- **Know CSS properties**: display, gap, padding, margin, border-radius, color, background, etc.
- **Theme-aware changes**: Always check if a change needs to be made in both dark and light mode selectors.
- **Save and refresh**: Always save (Ctrl+S) and refresh the browser (Ctrl+R) to see changes.

Good luck on your defense! 🎯
