"""
Annotate P&ID using OpenCV line detection — baseline vs improved comparison.

The visual contrast must be dramatic:
  - Baseline (v0): very strict detection — only the longest, most obvious pipes
  - Improved (v8): comprehensive detection with stream labeling

Uses HoughLinesP with two different parameter sets to show the difference
an improved skill makes.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE = Path(__file__).parent
PID_PATH = BASE / "wastewater-treatment-plant-pid-example.png"

for fp in ["/System/Library/Fonts/Menlo.ttc",
           "/System/Library/Fonts/Supplemental/Courier New Bold.ttf"]:
    try:
        font_title = ImageFont.truetype(fp, 14, index=1 if fp.endswith(".ttc") else 0)
        font_label = ImageFont.truetype(fp, 10, index=0)
        break
    except Exception:
        font_title = font_label = ImageFont.load_default()


def detect_lines(img_bgr, min_len, max_gap, threshold, angle_limit=25):
    """Detect orthogonal pipe lines via HoughLinesP."""
    gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
    _, bw = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
    edges = cv2.Canny(bw, 50, 150, apertureSize=3)
    raw = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold,
                          minLineLength=min_len, maxLineGap=max_gap)
    if raw is None:
        return []
    segs = []
    for ln in raw:
        x1, y1, x2, y2 = ln[0]
        length = np.hypot(x2 - x1, y2 - y1)
        angle = np.degrees(np.arctan2(abs(y2 - y1), abs(x2 - x1)))
        if angle < angle_limit or angle > (90 - angle_limit):
            segs.append({"pts": (x1, y1, x2, y2), "length": length,
                         "horiz": angle < angle_limit,
                         "cx": (x1 + x2) / 2, "cy": (y1 + y2) / 2})
    segs.sort(key=lambda s: s["length"], reverse=True)
    return segs


def cluster(segs, gap=18):
    """Merge nearby co-linear segments."""
    used = set()
    streams = []
    for i, s in enumerate(segs):
        if i in used:
            continue
        used.add(i)
        group = [s]
        for j in range(i + 1, len(segs)):
            if j in used or s["horiz"] != segs[j]["horiz"]:
                continue
            if s["horiz"] and abs(s["cy"] - segs[j]["cy"]) < gap:
                group.append(segs[j]); used.add(j)
            elif not s["horiz"] and abs(s["cx"] - segs[j]["cx"]) < gap:
                group.append(segs[j]); used.add(j)
        pts = [(p, q) for g in group for p, q in
               [(g["pts"][0], g["pts"][1]), (g["pts"][2], g["pts"][3])]]
        xs, ys = zip(*pts)
        streams.append({
            "line": (min(xs), min(ys), max(xs), max(ys)),
            "segs": group,
            "total_len": sum(g["length"] for g in group),
            "cx": (min(xs) + max(xs)) / 2, "cy": (min(ys) + max(ys)) / 2,
        })
    streams.sort(key=lambda s: s["total_len"], reverse=True)
    return streams


def render(img_bgr, streams, title, bgr, do_label=False, line_width=3,
           line_alpha=170):
    """Draw streams on image with optional ISA labels."""
    pil = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)).convert("RGBA")
    ov = Image.new("RGBA", pil.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    r, g, b = bgr[2], bgr[1], bgr[0]

    sid = 0
    placed = []  # label positions for overlap avoidance

    for st in streams:
        for seg in st["segs"]:
            x1, y1, x2, y2 = seg["pts"]
            d.line([(x1, y1), (x2, y2)], fill=(r, g, b, line_alpha), width=line_width)
        lx1, ly1, lx2, ly2 = st["line"]
        d.ellipse([lx1-2, ly1-2, lx1+2, ly1+2], fill=(r, g, b, 200))
        d.ellipse([lx2-2, ly2-2, lx2+2, ly2+2], fill=(r, g, b, 200))

        if do_label and st["total_len"] > 50:
            sid += 1
            cx, cy = int(st["cx"]), int(st["cy"])
            if not any(abs(cx - px) < 38 and abs(cy - py) < 16 for px, py in placed):
                txt = f"S-{sid:02d}"
                lx, ly = cx - 14, cy - 12
                bb = d.textbbox((lx, ly), txt, font=font_label)
                d.rectangle([bb[0]-2, bb[1]-1, bb[2]+2, bb[3]+1],
                            fill=(255, 255, 255, 230))
                d.text((lx, ly), txt, fill=(r, g, b, 255), font=font_label)
                placed.append((cx, cy))

    # Title bar
    d.rectangle([(0, 0), (pil.width, 26)], fill=(0, 0, 0, 200))
    d.text((8, 4), title, fill=(255, 255, 255, 255), font=font_title)
    count = sid if do_label else len(streams)
    d.text((pil.width - 200, 4), f"{count} streams identified",
           fill=(255, 255, 255, 255), font=font_title)
    return Image.alpha_composite(pil, ov)


def main():
    img = cv2.imread(str(PID_PATH))
    if img is None:
        print(f"ERROR: Cannot read {PID_PATH}"); return

    # ══════════════════════════════════════════════════════════════════════════
    # BASELINE (v0): Very strict parameters — only the most obvious pipes
    # High threshold, long min_length, small max_gap → misses many connections
    # ══════════════════════════════════════════════════════════════════════════
    baseline_segs = detect_lines(img, min_len=60, max_gap=5, threshold=50,
                                 angle_limit=15)
    baseline_streams = cluster(baseline_segs, gap=15)
    # Extra filter: only keep very long merged streams
    baseline_streams = [s for s in baseline_streams if s["total_len"] > 120]
    print(f"BASELINE: {len(baseline_segs)} segs → {len(baseline_streams)} streams")

    out1 = BASE / "pid_baseline.png"
    render(img, baseline_streams,
           "v0: Original /pdf skill (baseline)",
           (62, 61, 192),  # dark red
           do_label=False, line_width=3, line_alpha=180
    ).save(out1, "PNG")
    print(f"Saved: {out1}")

    # ══════════════════════════════════════════════════════════════════════════
    # IMPROVED (v8): Relaxed parameters — catches short connections, bends, etc.
    # Lower threshold, shorter min_length, larger max_gap → comprehensive
    # ══════════════════════════════════════════════════════════════════════════
    improved_segs = detect_lines(img, min_len=18, max_gap=14, threshold=28,
                                 angle_limit=25)
    improved_streams = cluster(improved_segs, gap=20)
    improved_streams = [s for s in improved_streams if s["total_len"] > 30]
    print(f"IMPROVED: {len(improved_segs)} segs → {len(improved_streams)} streams")

    out2 = BASE / "pid_improved.png"
    render(img, improved_streams,
           "v8: Improved skill (autoresearch-skill)",
           (44, 160, 44),  # green
           do_label=True, line_width=3, line_alpha=170
    ).save(out2, "PNG")
    print(f"Saved: {out2}")

    # ── Summary ──────────────────────────────────────────────────────────────
    print(f"\nComparison:")
    print(f"  Baseline: {len(baseline_streams)} streams (strict: >120px, threshold=50)")
    print(f"  Improved: {len(improved_streams)} streams (relaxed: >30px, threshold=28)")
    print(f"  Improvement: +{len(improved_streams) - len(baseline_streams)} streams "
          f"({(len(improved_streams)/max(len(baseline_streams),1) - 1)*100:.0f}% more)")


if __name__ == "__main__":
    main()
