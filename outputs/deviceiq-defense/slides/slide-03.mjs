import { addBg, addFooterLine, addFrame, addPill, addRule, addSlideNumber, addText, fonts, palette } from "./_shared.mjs";

export async function slide03(presentation, ctx) {
  const slide = presentation.slides.add();
  addBg(slide, ctx);

  addText(slide, ctx, {
    x: 18,
    y: 10,
    w: 1220,
    h: 42,
    text: "Slide 3: Why The Design Feels Modern And Responsive",
    size: 30,
    color: palette.text,
    bold: true,
    face: fonts.title
  });
  addRule(slide, ctx, 18, 70, 1244, "rgba(255,255,255,0.12)", 1);

  addText(slide, ctx, {
    x: 16,
    y: 108,
    w: 440,
    h: 54,
    text: "Slide Title",
    size: 28,
    color: palette.text,
    bold: true,
    face: fonts.title
  });
  addText(slide, ctx, {
    x: 16,
    y: 180,
    w: 320,
    h: 38,
    text: "Style and responsiveness",
    size: 18,
    color: palette.text,
    bold: true
  });

  addText(slide, ctx, {
    x: 16,
    y: 258,
    w: 260,
    h: 32,
    text: "Bullet Points",
    size: 28,
    color: palette.text,
    bold: true,
    face: fonts.title
  });

  addPill(slide, ctx, {
    x: 16,
    y: 318,
    w: 314,
    h: 36,
    text: "Style and responsiveness",
    fill: palette.surfaceSoft,
    line: "rgba(255,255,255,0.08)",
    color: palette.text,
    size: 13,
    bold: true,
    align: "left"
  });

  const bullets = [
    ["Dark background with green accent for a modern tech feel", 810],
    ["Glassmorphism panels and soft shadows create depth", 690],
    ["Manrope and Space Grotesk give clear body text and strong headings", 960],
    ["Grid and Flexbox help the layout adapt to different screen sizes", 900],
    ["Mobile layout stacks sections so the page stays readable", 780],
  ];

  bullets.forEach((item, index) => {
    const y = 382 + index * 52;
    addText(slide, ctx, {
      x: 42,
      y: y + 8,
      w: 18,
      h: 18,
      text: "•",
      size: 24,
      color: palette.text,
      bold: true
    });
    addFrame(slide, ctx, 80, y, item[1], 38, "rgba(19, 82, 215, 0.96)", "rgba(19, 82, 215, 0.96)", 3);
    addText(slide, ctx, {
      x: 84,
      y: y + 5,
      w: item[1] - 12,
      h: 26,
      text: item[0],
      size: 24,
      color: palette.white,
      bold: false,
      face: fonts.body
    });
  });

  addFooterLine(slide, ctx, "Modern feel + responsive structure + clear text hierarchy.", 18, 678, 700);
  addSlideNumber(slide, ctx, 3);
  return slide;
}
