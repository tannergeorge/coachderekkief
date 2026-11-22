"""Make the light, web-sized images recruiting.html loads. Originals stay untouched; run after adding or replacing any:
    python3 make_web_images.py        (from this folder; needs numpy + ImageMagick `magick`)

- state_outlines/<state>.png (gray state on white, watermark underneath) -> state_shapes/<state>.png:
  white silhouette on transparency, trimmed, 600px. The page uses them as CSS masks and fills them with any color.
- school_logos/<school>.* -> school_logos_web/<school>.webp, at most 400px (tiles show ~190px; 2x for retina).
  A 3000px logo decodes to ~27 MB of memory; at 400px it is under 1 MB.
- commits/<player>.* -> commits_web/<player>.webp, just big enough to cover a player card at 2x (640x854).
- header.jpg -> header.webp, at most 1800px wide."""
import pathlib, subprocess, numpy as np

here = pathlib.Path(__file__).parent

def magick(*args, **kw):
    return subprocess.run(["magick", *map(str, args)], check=True, capture_output=True, **kw).stdout

shapes = here / "state_shapes"; shapes.mkdir(exist_ok=True)
for src in sorted((here / "state_outlines").glob("*.png")):
    pgm = magick(src, "-colorspace", "gray", "-depth", "8", "pgm:-")
    # binary PGM: "P5\n<w> <h>\n255\n" then pixels
    head = pgm.split(b"\n", 3); w, h = map(int, head[1].split()); px = np.frombuffer(head[3], np.uint8).reshape(h, w)
    alpha = np.clip((255 - px.astype(int)) * 8, 0, 255).astype(np.uint8)  # anything not white is the state (interior gray #ddd -> opaque)
    # drop the watermark: the last band of inked rows, if it's thin and separated from the state by blank rows
    inked = np.flatnonzero(alpha.max(1) > 40)
    breaks = np.flatnonzero(np.diff(inked) > 1)
    if len(breaks) and inked[-1] - inked[breaks[-1] + 1] < h * 0.03:
        alpha[inked[breaks[-1] + 1]:] = 0
    mask = b"P5\n%d %d\n255\n" % (w, h) + alpha.tobytes()
    magick("-size", f"{w}x{h}", "xc:white", "(", "pgm:-", ")", "-compose", "CopyOpacity", "-composite",
           "-trim", "+repage", "-resize", "600x600", "-strip", shapes / src.name, input=mask)
    print("shape", src.name)

logos = here / "school_logos_web"; logos.mkdir(exist_ok=True)
for src in sorted((here / "school_logos").iterdir()):
    if src.name.startswith("."): continue
    density = ["-density", "300", "-background", "none"] if src.suffix == ".svg" else []
    magick(*density, f"{src}[0]", "-resize", "400x400>", "-strip", "-quality", "88", logos / (src.stem + ".webp"))
    print("logo ", src.name)

commits = here / "commits_web"; commits.mkdir(exist_ok=True)
for src in sorted((here / "commits").iterdir()):
    if src.name.startswith("."): continue
    magick(f"{src}[0]", "-auto-orient", "-resize", "640x854^>", "-strip", "-quality", "80", commits / (src.stem + ".webp"))
    print("commit", src.name)

if (here / "header.jpg").exists():
    magick(here / "header.jpg", "-resize", "1800x>", "-strip", "-quality", "78", here / "header.webp")
    print("header")
