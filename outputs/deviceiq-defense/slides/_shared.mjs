export const palette = {
  bg: "#0d1117",
  bgAlt: "#0b1016",
  surface: "rgba(20, 25, 32, 0.92)",
  surfaceSoft: "rgba(22, 29, 38, 0.96)",
  surfaceStrong: "rgba(29, 38, 49, 0.96)",
  border: "rgba(255, 255, 255, 0.08)",
  borderStrong: "rgba(255, 255, 255, 0.14)",
  text: "#f5f7fb",
  muted: "#9ba7ba",
  accent: "#46b37b",
  accentStrong: "#2d8d5c",
  accent2: "#5f96ff",
  accent3: "#b8d9ca",
  accentSoft: "rgba(70, 179, 123, 0.14)",
  accentSoft2: "rgba(95, 150, 255, 0.14)",
  dark: "rgba(8, 12, 17, 0.94)",
  white: "#ffffff"
};

export const fonts = {
  title: "Aptos Display",
  body: "Aptos",
  mono: "Aptos Mono"
};

export function addBg(slide, ctx) {
  ctx.addShape(slide, {
    geometry: "rect",
    left: 0,
    top: 0,
    width: ctx.W,
    height: ctx.H,
    fill: palette.bg,
    line: { width: 0, fill: "#00000000" }
  });

  ctx.addShape(slide, {
    geometry: "ellipse",
    left: -130,
    top: -110,
    width: 520,
    height: 520,
    fill: "rgba(70, 179, 123, 0.18)",
    line: { width: 0, fill: "#00000000" }
  });

  ctx.addShape(slide, {
    geometry: "ellipse",
    left: 910,
    top: -70,
    width: 390,
    height: 390,
    fill: "rgba(95, 150, 255, 0.12)",
    line: { width: 0, fill: "#00000000" }
  });

  ctx.addShape(slide, {
    geometry: "ellipse",
    left: 420,
    top: 520,
    width: 620,
    height: 300,
    fill: "rgba(255, 255, 255, 0.04)",
    line: { width: 0, fill: "#00000000" }
  });

  ctx.addShape(slide, {
    geometry: "rect",
    left: 0,
    top: 0,
    width: ctx.W,
    height: ctx.H,
    fill: "rgba(13, 17, 23, 0.12)",
    line: { width: 0, fill: "#00000000" }
  });
}

export function addFrame(slide, ctx, x, y, w, h, fill = palette.surface, line = palette.border, radius = 24) {
  const shape = ctx.addShape(slide, {
    geometry: "rect",
    left: x,
    top: y,
    width: w,
    height: h,
    fill,
    line: { width: 1, fill: line }
  });
  shape.borderRadius = radius;
  return shape;
}

export function addText(slide, ctx, { x, y, w, h, text, size, color = palette.text, bold = false, align = "left", valign = "top", face = fonts.body, insets = { left: 0, right: 0, top: 0, bottom: 0 } }) {
  const shape = ctx.addText(slide, {
    left: x,
    top: y,
    width: w,
    height: h,
    text,
    fontSize: size,
    color,
    bold,
    align,
    valign,
    face,
    fill: "#00000000",
    line: { width: 0, fill: "#00000000" },
    insets
  });
  return shape;
}

export function addRule(slide, ctx, x, y, w, fill = palette.border, h = 1) {
  return ctx.addShape(slide, {
    geometry: "rect",
    left: x,
    top: y,
    width: w,
    height: h,
    fill,
    line: { width: 0, fill: "#00000000" }
  });
}

export function addPill(slide, ctx, { x, y, w, h = 34, text, fill = palette.surfaceSoft, line = palette.border, color = palette.text, size = 12, bold = true, align = "center" }) {
  const pill = addFrame(slide, ctx, x, y, w, h, fill, line, 999);
  addText(slide, ctx, {
    x: x + 8,
    y: y + 5,
    w: w - 16,
    h: h - 10,
    text,
    size,
    color,
    bold,
    align,
    valign: "mid",
    face: fonts.body
  });
  return pill;
}

export function addKicker(slide, ctx, label, x = 58, y = 44) {
  addPill(slide, ctx, {
    x,
    y,
    w: 176,
    h: 34,
    text: label,
    fill: palette.accentSoft,
    line: "rgba(70, 179, 123, 0.24)",
    color: palette.accent,
    size: 11
  });
}

export function addSlideNumber(slide, ctx, num) {
  addText(slide, ctx, {
    x: 1180,
    y: 668,
    w: 42,
    h: 24,
    text: String(num).padStart(2, "0"),
    size: 12,
    color: palette.muted,
    bold: true,
    align: "right",
    face: fonts.mono
  });
}

export function addFooterLine(slide, ctx, text, x = 58, y = 648, w = 670) {
  addRule(slide, ctx, x, y, w, "rgba(255,255,255,0.12)", 1);
  addText(slide, ctx, {
    x,
    y: y + 12,
    w,
    h: 20,
    text,
    size: 11,
    color: palette.muted
  });
}

export function addBulletCard(slide, ctx, { x, y, w, h, title, body, accent = palette.accent }) {
  addFrame(slide, ctx, x, y, w, h, palette.surfaceSoft, "rgba(255,255,255,0.10)", 22);
  addRule(slide, ctx, x, y, w, accent, 3);
  addText(slide, ctx, {
    x: x + 18,
    y: y + 18,
    w: w - 36,
    h: 24,
    text: title,
    size: 20,
    color: palette.text,
    bold: true,
    face: fonts.title
  });
  addText(slide, ctx, {
    x: x + 18,
    y: y + 52,
    w: w - 36,
    h: h - 62,
    text: body,
    size: 13.5,
    color: palette.muted
  });
}

export function addQuestionCard(slide, ctx, { x, y, w, h, kicker, question, answer, accent = palette.accent2 }) {
  addFrame(slide, ctx, x, y, w, h, palette.surface, "rgba(255,255,255,0.09)", 20);
  addPill(slide, ctx, {
    x: x + 16,
    y: y + 14,
    w: 88,
    h: 26,
    text: kicker,
    fill: "rgba(95, 150, 255, 0.12)",
    line: "rgba(95, 150, 255, 0.24)",
    color: palette.accent2,
    size: 10
  });
  addText(slide, ctx, {
    x: x + 16,
    y: y + 44,
    w: w - 32,
    h: 44,
    text: question,
    size: 16,
    color: palette.text,
    bold: true,
    face: fonts.title
  });
  addText(slide, ctx, {
    x: x + 16,
    y: y + 88,
    w: w - 32,
    h: h - 100,
    text: answer,
    size: 11.8,
    color: palette.muted
  });
}
