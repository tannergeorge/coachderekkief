# Coach Derek Kief site

Static HTML + one `style.css`. No build step: open `index.html` in a browser.

- Pages: `index.html` (landing), `resume.html`, `recruiting.html`. Unleashed PSA (training) page is next; its landing tile links to a placeholder.
- Recruiting map: state silhouettes in `img/recruiting_imgs/state_shapes/` are generated from `state_outlines/` by `python3 img/recruiting_imgs/make_web_images.py` (numpy + ImageMagick), which also makes the web-sized `school_logos_web/*.webp`, `commits_web/*.webp` (player photos) and `header.webp` the page loads; rerun it after adding any logo or photo.
- Photos live in `img/`. Every photo is a `.ph` element with `style="--img:url(img/x.jpg)"`; a missing file shows a gray gradient with its filename, so the layout never breaks.
- Resume facts come from Derek's resume PDF; anything marked VERIFY needs Derek's confirmation.

## Ponytails (smallest thing that works; each tagged `ponytail:` in code)
- Nav + footer copy-pasted per page → JS include or static-site generator past ~5 pages.
- Single stylesheet, no framework → split per page if it passes ~400 lines.
- Liquid glass = CSS blur + specular rim, no SVG refraction (Chromium-only) → add behind `@supports` if wanted. Glass only on nav, hero buttons and the video pause control (HIG: functional layer only); never on photos, video, text or cards. Design reviews use the apple-design skill in .agents/skills.
