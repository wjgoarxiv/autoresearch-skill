"""
Generate autoresearch-skill cover image (2560x1280).
Dark navy canvas, scientific blue/cyan/violet blobs, bold monospace title, rounded corners.
"""

from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 2560, 1280
CORNER_RADIUS = 80

# ── 1. Base canvas (dark navy) ────────────────────────────────────────────────
base = Image.new("RGBA", (W, H), (10, 13, 26, 255))  # #0a0d1a

# ── 2. Color blobs ────────────────────────────────────────────────────────────
def make_blob(size, color_rgba, cx, cy, rx, ry):
    """Paint an elliptical color blob on a transparent layer."""
    layer = Image.new("RGBA", size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    draw.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=color_rgba)
    return layer

blobs = [
    # (r, g, b, alpha,  cx,    cy,   rx,   ry,  blur)
    (0,   60, 180, 200,   700,  600, 700, 500, 120),   # deep blue, centered-left
    (0,  160, 200, 160,  1900,  200, 600, 400, 100),   # electric cyan, top-right
    (80,   0, 160, 180,  1280, 1150, 900, 350,  90),   # violet, bottom
    (0,  120, 100, 120,  1400,  640, 500, 350,  80),   # teal, center
]

canvas = base.copy()
for r, g, b, a, cx, cy, rx, ry, blur in blobs:
    blob = make_blob((W, H), (r, g, b, a), cx, cy, rx, ry)
    blob = blob.filter(ImageFilter.GaussianBlur(radius=blur))
    canvas = Image.alpha_composite(canvas, blob)

# Extra full-image blend pass for silky smoothness
canvas = canvas.filter(ImageFilter.GaussianBlur(radius=8))

# ── 3. Film grain ─────────────────────────────────────────────────────────────
rng = np.random.default_rng(42)
noise = rng.integers(0, 255, (H, W), dtype=np.uint8)
grain_alpha = (noise * 0.22).astype(np.uint8)   # ~22% opacity
grain_layer = np.stack([noise, noise, noise, grain_alpha], axis=-1).astype(np.uint8)
grain_img = Image.fromarray(grain_layer, "RGBA")
canvas = Image.alpha_composite(canvas, grain_img)

# ── 4. Fonts ──────────────────────────────────────────────────────────────────
TITLE_SIZE = 220
SUBTITLE_SIZE = 70

# Try Menlo Bold (index 1 in the TTC), fallback to Courier New Bold
try:
    font_title = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", TITLE_SIZE, index=1)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Menlo.ttc", SUBTITLE_SIZE, index=0)
except Exception:
    font_title = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", TITLE_SIZE)
    font_subtitle = ImageFont.truetype("/System/Library/Fonts/Supplemental/Courier New Bold.ttf", SUBTITLE_SIZE)

TITLE_TEXT = "autoresearch-skill"
SUBTITLE_TEXT = "Define a goal. Let the agent iterate."

# ── 5. Measure text ───────────────────────────────────────────────────────────
tmp = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(tmp)

t_bbox = d.textbbox((0, 0), TITLE_TEXT, font=font_title)
t_w = t_bbox[2] - t_bbox[0]
t_h = t_bbox[3] - t_bbox[1]

s_bbox = d.textbbox((0, 0), SUBTITLE_TEXT, font=font_subtitle)
s_w = s_bbox[2] - s_bbox[0]
s_h = s_bbox[3] - s_bbox[1]

GAP = 100 # between title and subtitle
total_h = t_h + GAP + s_h
block_top = (H - total_h) // 2 - 30   # slightly above true center

title_x = (W - t_w) // 2 - t_bbox[0]
title_y = block_top - t_bbox[1]

subtitle_x = (W - s_w) // 2 - s_bbox[0]
subtitle_y = title_y + t_h + GAP

# ── 6. Title with glow ────────────────────────────────────────────────────────
def draw_text_layer(text, x, y, font, color):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(layer).text((x, y), text, font=font, fill=color)
    return layer

# Glow: 3 blurred copies (wide → narrow), then sharp white on top
glow_specs = [
    ((80, 160, 255, 60),  18),    # outer glow, blue
    ((120, 180, 255, 90), 9),     # mid glow
    ((180, 220, 255, 120), 4),    # tight glow, near-white
]
for color, blur_r in glow_specs:
    glow = draw_text_layer(TITLE_TEXT, title_x, title_y, font_title, color)
    glow = glow.filter(ImageFilter.GaussianBlur(radius=blur_r))
    canvas = Image.alpha_composite(canvas, glow)

# Sharp white title
title_layer = draw_text_layer(TITLE_TEXT, title_x, title_y, font_title, (255, 255, 255, 245))
canvas = Image.alpha_composite(canvas, title_layer)

# ── 7. Subtitle ───────────────────────────────────────────────────────────────
subtitle_layer = draw_text_layer(
    SUBTITLE_TEXT, subtitle_x, subtitle_y, font_subtitle, (160, 170, 192, 210)
)
canvas = Image.alpha_composite(canvas, subtitle_layer)

# ── 8. Rounded corner mask ────────────────────────────────────────────────────
mask = Image.new("L", (W, H), 0)
ImageDraw.Draw(mask).rounded_rectangle([(0, 0), (W - 1, H - 1)], radius=CORNER_RADIUS, fill=255)
canvas.putalpha(mask)

# ── 9. Final polish blur (radius=1) ──────────────────────────────────────────
canvas = canvas.filter(ImageFilter.GaussianBlur(radius=1))

# ── 10. Save ──────────────────────────────────────────────────────────────────
out_path = str(Path(__file__).parent / "cover.png")
canvas.save(out_path, "PNG", dpi=(400, 400))
print(f"Saved: {out_path}")
print(f"Size: {canvas.size}")
print(f"Mode: {canvas.mode}")
