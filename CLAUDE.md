# Coach Derek Kief site

Static HTML + one `style.css`. No build step: open `index.html` in a browser.

- Pages: `index.html` (landing), `resume.html`. Recruiting + Unleashed PSA (training) pages are next; landing tiles link to placeholders.
- Photos live in `img/`. Every photo is a `.ph` element with `style="--img:url(img/x.jpg)"`; a missing file shows a gray gradient with its filename, so the layout never breaks.
- Resume facts come from public school bios; anything marked VERIFY needs Derek's confirmation.

## Ponytails (smallest thing that works; each tagged `ponytail:` in code)
- Nav + footer copy-pasted per page → JS include or static-site generator past ~5 pages.
- Single stylesheet, no framework → split per page if it passes ~400 lines.
- Liquid glass = CSS blur + specular rim, no SVG refraction (Chromium-only) → add behind `@supports` if wanted. Glass only on nav, hero buttons and the video pause control (HIG: functional layer only); never on photos, video, text or cards. Design reviews use the apple-design skill in .agents/skills.
