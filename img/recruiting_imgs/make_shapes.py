"""Turn state_outlines/<state>.png (gray state on white, watermark underneath) into
state_shapes/<state>.png: a white silhouette on transparency, trimmed, ~1000px.
recruiting.html uses the shapes as CSS masks, so the page can fill them with any color.

Adding a state: drop its outline PNG in state_outlines/, then run from this folder:
    python3 make_shapes.py
Needs numpy and ImageMagick (`magick`)."""
import pathlib, subprocess, numpy as np

here = pathlib.Path(__file__).parent
out = here / "state_shapes"; out.mkdir(exist_ok=True)

for src in sorted((here / "state_outlines").glob("*.png")):
    pgm = subprocess.run(["magick", src, "-colorspace", "gray", "-depth", "8", "pgm:-"], capture_output=True, check=True).stdout
    # binary PGM: "P5\n<w> <h>\n255\n" then pixels
    head = pgm.split(b"\n", 3); w, h = map(int, head[1].split()); px = np.frombuffer(head[3], np.uint8).reshape(h, w)
    alpha = np.clip((255 - px.astype(int)) * 8, 0, 255).astype(np.uint8)  # anything not white is the state (interior gray #ddd -> opaque)
    # drop the watermark: the last band of inked rows, if it's thin and separated from the state by blank rows
    inked = np.flatnonzero(alpha.max(1) > 40)
    breaks = np.flatnonzero(np.diff(inked) > 1)
    if len(breaks) and inked[-1] - inked[breaks[-1] + 1] < h * 0.03:
        alpha[inked[breaks[-1] + 1]:] = 0
    mask = b"P5\n%d %d\n255\n" % (w, h) + alpha.tobytes()
    subprocess.run(["magick", "-size", f"{w}x{h}", "xc:white", "(", "pgm:-", ")", "-compose", "CopyOpacity", "-composite",
                    "-trim", "+repage", "-resize", "1000x1000", "-strip", out / src.name], input=mask, check=True)
    print(src.name, subprocess.run(["magick", "identify", "-format", "%wx%h", out / src.name], capture_output=True, text=True).stdout)
