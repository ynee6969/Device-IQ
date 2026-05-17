import { addBg, addBulletCard, addFooterLine, addFrame, addKicker, addPill, addRule, addSlideNumber, addText, fonts, palette } from "./_shared.mjs";

export async function slide02(presentation, ctx) {
  const slide = presentation.slides.add();
  addBg(slide, ctx);

  addKicker(slide, ctx, "WEBSITE RATIONALE");
  addText(slide, ctx, {
    x: 58,
    y: 98,
    w: 930,
    h: 118,
    text: "- Sticky header on desktop\n- Bottom tab bar on mobile\n- Homepage introduces the idea\n- Dashboard handles browsing\n- Compare page handles decisions",
    size: 17,
    color: palette.text,
    bold: true,
    face: fonts.title
  });
  addText(slide, ctx, {
    x: 60,
    y: 220,
    w: 840,
    h: 34,
    text: "Clear sections, easy navigation, mobile-friendly flow.",
    size: 14.5,
    color: palette.muted
  });

  addBulletCard(slide, ctx, {
    x: 58,
    y: 250,
    w: 350,
    h: 132,
    title: "Purpose",
    body: "Make phone selection simpler and faster."
  });
  addBulletCard(slide, ctx, {
    x: 58,
    y: 396,
    w: 350,
    h: 132,
    title: "Target users",
    body: "Phone shoppers, students, and casual visitors."
  });
  addBulletCard(slide, ctx, {
    x: 58,
    y: 542,
    w: 350,
    h: 118,
    title: "HTML + CSS idea",
    body: "Semantic sections, Grid, Flexbox, and media queries.",
    accent: palette.accent2
  });

  // Flow rail on the right
  addFrame(slide, ctx, 450, 250, 772, 410, palette.surface, palette.border, 28);
  addText(slide, ctx, {
    x: 476,
    y: 274,
    w: 240,
    h: 24,
    text: "Navigation logic",
    size: 16,
    color: palette.accent,
    bold: true
  });
  addText(slide, ctx, {
    x: 476,
    y: 302,
    w: 340,
    h: 52,
    text: "Desktop uses a sticky header, while mobile uses a bottom tab bar so the main actions stay easy to reach.",
    size: 13.2,
    color: palette.muted
  });
  addPill(slide, ctx, {
    x: 476,
    y: 344,
    w: 118,
    h: 26,
    text: "Homepage",
    fill: "rgba(70,179,123,0.10)",
    line: "rgba(70,179,123,0.18)",
    color: palette.accent,
    size: 10.2
  });
  addPill(slide, ctx, {
    x: 604,
    y: 344,
    w: 118,
    h: 26,
    text: "Dashboard",
    fill: "rgba(95,150,255,0.10)",
    line: "rgba(95,150,255,0.18)",
    color: palette.accent2,
    size: 10.2
  });
  addPill(slide, ctx, {
    x: 732,
    y: 344,
    w: 118,
    h: 26,
    text: "Compare page",
    fill: "rgba(184,217,202,0.10)",
    line: "rgba(184,217,202,0.18)",
    color: palette.accent3,
    size: 10.2
  });

  const steps = [
    ["Browse", "Start with a clean catalog."],
    ["Compare", "See important details side by side."],
    ["Save", "Keep favorites for later."],
    ["Return", "Come back to an organized layout."]
  ];
  steps.forEach((step, index) => {
    const x = 476 + (index % 2) * 288;
    const y = 376 + Math.floor(index / 2) * 126;
    addFrame(slide, ctx, x, y, 250, 100, palette.surfaceSoft, "rgba(255,255,255,0.09)", 20);
    addPill(slide, ctx, {
      x: x + 16,
      y: y + 14,
      w: 86,
      h: 26,
      text: `0${index + 1}`,
      fill: index % 2 === 0 ? palette.accentSoft : palette.accentSoft2,
      line: index % 2 === 0 ? "rgba(70,179,123,0.24)" : "rgba(95,150,255,0.22)",
      color: index % 2 === 0 ? palette.accent : palette.accent2,
      size: 11
    });
    addText(slide, ctx, {
      x: x + 16,
      y: y + 48,
      w: 200,
      h: 18,
      text: step[0],
      size: 18,
      color: palette.text,
      bold: true,
      face: fonts.title
    });
    addText(slide, ctx, {
      x: x + 16,
      y: y + 72,
      w: 220,
      h: 22,
      text: step[1],
      size: 11.8,
      color: palette.muted
    });
  });

  // Responsiveness and CSS cue row
  addText(slide, ctx, {
    x: 478,
    y: 606,
    w: 220,
    h: 20,
    text: "Responsiveness strategy",
    size: 12,
    color: palette.accent3,
    bold: true
  });
  ["Stack on mobile", "Adjust spacing", "Keep touch targets clear", "Use flexible grids"].forEach((label, index) => {
    addPill(slide, ctx, {
      x: 678 + index * 142,
      y: 596,
      w: 132,
      h: 30,
      text: label,
      fill: "rgba(255,255,255,0.04)",
      line: "rgba(255,255,255,0.08)",
      color: palette.text,
      size: 10.2,
      bold: false
    });
  });

  addFooterLine(slide, ctx, "Simple path: browse, compare, save, return.", 58, 676, 1140);
  addSlideNumber(slide, ctx, 2);
  return slide;
}
