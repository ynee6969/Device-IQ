import { addBg, addBulletCard, addFooterLine, addFrame, addKicker, addPill, addRule, addSlideNumber, addText, fonts, palette } from "./_shared.mjs";

export async function slide01(presentation, ctx) {
  const slide = presentation.slides.add();
  addBg(slide, ctx);

  addKicker(slide, ctx, "TITLE SLIDE");
  addText(slide, ctx, {
    x: 58,
    y: 98,
    w: 510,
    h: 110,
    text: "DeviceIQ",
    size: 60,
    color: palette.text,
    bold: true,
    face: fonts.title
  });
  addText(slide, ctx, {
    x: 60,
    y: 202,
    w: 520,
    h: 72,
    text: "A cleaner way to choose a phone.",
    size: 24,
    color: palette.muted
  });
  addText(slide, ctx, {
    x: 60,
    y: 270,
    w: 530,
    h: 150,
    text: "- Browse and compare phones in one place\n- Reduce confusion from too many tabs and spec sheets\n- Designed for phone shoppers, students, and casual visitors\n- Sign-in is optional for browsing, but useful for saving favorites",
    size: 16,
    color: palette.text
  });

  addPill(slide, ctx, { x: 60, y: 404, w: 122, text: "Problem", fill: palette.accentSoft, line: "rgba(70,179,123,0.24)", color: palette.accent });
  addPill(slide, ctx, { x: 194, y: 404, w: 122, text: "Solution", fill: "rgba(95,150,255,0.12)", line: "rgba(95,150,255,0.22)", color: palette.accent2 });
  addPill(slide, ctx, { x: 328, y: 404, w: 122, text: "Users", fill: "rgba(184,217,202,0.12)", line: "rgba(184,217,202,0.22)", color: palette.accent3 });

  addText(slide, ctx, {
    x: 60,
    y: 448,
    w: 460,
    h: 18,
    text: "Key idea: fewer tabs, clearer choices, easier saving.",
    size: 12.2,
    color: palette.muted
  });

  // Right-side hero mockup inspired by the site card system.
  addFrame(slide, ctx, 716, 96, 482, 500, palette.surface, palette.border, 28);
  addRule(slide, ctx, 716, 96, 482, "rgba(255,255,255,0.04)", 1);

  addFrame(slide, ctx, 748, 126, 182, 248, palette.surfaceStrong, "rgba(70,179,123,0.24)", 24);
  addText(slide, ctx, {
    x: 770,
    y: 148,
    w: 120,
    h: 18,
    text: "Dashboard",
    size: 12,
    color: palette.accent,
    bold: true
  });
  addText(slide, ctx, {
    x: 770,
    y: 176,
    w: 128,
    h: 84,
    text: "Easy to scan\nphone cards.",
    size: 22,
    color: palette.text,
    bold: true,
    face: fonts.title
  });
  addPill(slide, ctx, { x: 770, y: 278, w: 112, h: 26, text: "Responsive", size: 10, fill: "rgba(70,179,123,0.10)", line: "rgba(70,179,123,0.18)", color: palette.accent });
  addPill(slide, ctx, { x: 770, y: 312, w: 112, h: 26, text: "Glass cards", size: 10, fill: "rgba(95,150,255,0.10)", line: "rgba(95,150,255,0.18)", color: palette.accent2 });

  addFrame(slide, ctx, 956, 156, 178, 208, palette.surfaceSoft, palette.borderStrong, 24);
  addText(slide, ctx, {
    x: 978,
    y: 178,
    w: 122,
    h: 22,
    text: "Compare",
    size: 12,
    color: palette.accent2,
    bold: true
  });
  addText(slide, ctx, {
    x: 978,
    y: 206,
    w: 116,
    h: 56,
    text: "Phone details\nside by side.",
    size: 21,
    color: palette.text,
    bold: true,
    face: fonts.title
  });
  addRule(slide, ctx, 978, 280, 128, "rgba(255,255,255,0.10)", 6);
  addRule(slide, ctx, 978, 298, 104, "rgba(70,179,123,0.95)", 6);
  addRule(slide, ctx, 978, 318, 116, "rgba(95,150,255,0.86)", 6);
  addText(slide, ctx, {
    x: 978,
    y: 340,
    w: 110,
    h: 20,
    text: "Decision-first UI",
    size: 11.5,
    color: palette.muted,
    bold: true
  });

  // Bottom rhythm cards
  addBulletCard(slide, ctx, {
    x: 60,
    y: 498,
    w: 194,
    h: 118,
    title: "Clear flow",
    body: "One path from browsing to comparing."
  });
  addBulletCard(slide, ctx, {
    x: 270,
    y: 498,
    w: 194,
    h: 118,
    title: "Fast decisions",
    body: "Less clutter, less second-guessing.",
    accent: palette.accent2
  });
  addBulletCard(slide, ctx, {
    x: 480,
    y: 498,
    w: 194,
    h: 118,
    title: "Target users",
    body: "Helpful for students and casual visitors.",
    accent: palette.accent3
  });

  addFooterLine(slide, ctx, "Website defense deck | minimal, card-based, and visually aligned to the site", 58, 648, 870);
  addSlideNumber(slide, ctx, 1);
  return slide;
}
