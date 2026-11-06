"""Deterministic repair candidate for ZERO v6 rows 0-8 (no new imagery is drawn):
 1. remove pink/red/magenta residue pixels (hue outside the black-gold palette) -> alpha 0
 2. rescale the jumping row to idle scale (shared scale) and re-register baseline, keeping a visible lift
Source atlas is never modified. Output: rows09.png (1536x1872) + report.json + before/after sheets."""
import os
WORK = os.environ.get("PET_WORK", ".")   # 你的工作資料夾（放 inputs、repair、generated、local-run）

import json
from PIL import Image, ImageFilter
import numpy as np

SRC = os.path.join(WORK, "inputs", "source_atlas.png")   # 1536x1872 以上的舊圖集（至少含前 9 列）
OUT = os.path.join(WORK, "repair"); os.makedirs(OUT, exist_ok=True)
COUNTS = [6, 8, 8, 4, 5, 8, 6, 6, 6]
NAMES = ["idle", "running-right", "running-left", "waving", "jumping", "failed", "waiting", "running", "review"]
CW, CH = 192, 208
atlas = Image.open(SRC).convert("RGBA")
report = {"despill_removed_pixels": {}, "jump": {}}


def bbox(img):
    return img.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()


def despill(cell):
    a = np.array(cell).astype(np.float32)
    r, g, b, al = a[..., 0] / 255, a[..., 1] / 255, a[..., 2] / 255, a[..., 3]
    mx, mn = np.maximum.reduce([r, g, b]), np.minimum.reduce([r, g, b])
    d = mx - mn + 1e-6
    h = np.zeros_like(mx)
    m = mx == r; h[m] = ((g - b)[m] / d[m]) % 6
    m = (mx == g) & ~(mx == r); h[m] = ((b - r)[m] / d[m]) + 2
    m = (mx == b) & ~(mx == r) & ~(mx == g); h[m] = ((r - g)[m] / d[m]) + 4
    h = h * 60
    s = d / (mx + 1e-6)
    # pink / red / magenta: hue 285..360 or 0..18, clearly saturated and not dark
    bad = ((h >= 285) | (h <= 18)) & (s > 0.22) & (mx > 0.35) & (al > 0)
    removed = int(bad.sum())
    a[bad, 3] = 0
    out = Image.fromarray(a.astype(np.uint8), "RGBA")
    # kill 1px fringe that touches removed area and is semi-transparent
    al2 = np.array(out.getchannel("A"))
    return out, removed


rows_img = []
for r, (name, c) in enumerate(zip(NAMES, COUNTS)):
    cells, removed = [], 0
    for i in range(c):
        cell = atlas.crop((i * CW, r * CH, (i + 1) * CW, (r + 1) * CH))
        cell, n = despill(cell)
        removed += n
        cells.append(cell)
    report["despill_removed_pixels"][name] = removed
    rows_img.append(cells)

# idle reference
idle_bb = [bbox(c) for c in rows_img[0]]
idle_h = float(np.median([b[3] - b[1] for b in idle_bb]))
idle_w = float(np.median([b[2] - b[0] for b in idle_bb]))
idle_base = int(np.median([b[3] for b in idle_bb]))
jump = rows_img[4]
jb = [bbox(c) for c in jump]
# shared scale from the grounded frames (0 and 4) so width/height match idle
scale = float(np.mean([idle_w / (jb[0][2] - jb[0][0]), idle_w / (jb[4][2] - jb[4][0])]))
scale = min(scale, 1.10)
MARGIN_TOP = 8
new_jump = []
orig_ground = max(b[3] for b in jb)
for k, (cell, b) in enumerate(zip(jump, jb)):
    crop = cell.crop(b)
    w, h = round(crop.width * scale), round(crop.height * scale)
    # premultiplied resize to avoid halos
    arr = np.array(crop).astype(np.float32)
    arr[..., :3] *= arr[..., 3:4] / 255
    pm = Image.fromarray(arr.astype(np.uint8), "RGBA").resize((w, h), Image.LANCZOS)
    p = np.array(pm).astype(np.float32)
    al = np.maximum(p[..., 3:4], 1)
    p[..., :3] = np.clip(p[..., :3] * 255 / al, 0, 255)
    sized = Image.fromarray(p.astype(np.uint8), "RGBA")
    lift = orig_ground - b[3]
    bottom = idle_base - lift
    top = bottom - h
    if top < MARGIN_TOP:
        bottom += MARGIN_TOP - top
    # keep horizontal centre of the original frame
    cx = (b[0] + b[2]) / 2
    left = round(cx - w / 2)
    left = max(2, min(CW - w - 2, left))
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    canvas.alpha_composite(sized, (left, int(bottom - h)))
    new_jump.append(canvas)
rows_img[4] = new_jump
nb = [bbox(c) for c in new_jump]
report["jump"] = {"scale": round(scale, 4), "idle_median_wh": [idle_w, idle_h], "idle_baseline": idle_base,
                  "before_bbox": jb, "after_bbox": nb,
                  "after_baselines": [b[3] for b in nb],
                  "airborne_lift_px": max(b[3] for b in nb) - min(b[3] for b in nb),
                  "landing_delta_px": abs(nb[-1][3] - idle_base),
                  "min_top_px": min(b[1] for b in nb)}

sheet = Image.new("RGBA", (8 * CW, 9 * CH), (0, 0, 0, 0))
for r, cells in enumerate(rows_img):
    for i, c in enumerate(cells):
        sheet.alpha_composite(c, (i * CW, r * CH))
# clear RGB under fully transparent pixels
arr = np.array(sheet)
arr[arr[..., 3] == 0] = 0
Image.fromarray(arr, "RGBA").save(f"{OUT}\\rows09.png")
json.dump(report, open(f"{OUT}\\report.json", "w", ensure_ascii=False, indent=1) if False else open(f"{OUT}\\report.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)

# before/after comparison for jumping + review
def strip(img_getter, r, n):
    s = Image.new("RGBA", (n * CW, CH), (205, 205, 205, 255))
    for i in range(n):
        c = img_getter(r, i)
        bg = Image.new("RGBA", (CW, CH), (205, 205, 205, 255)); bg.alpha_composite(c); s.paste(bg, (i * CW, 0))
    return s
before = lambda r, i: atlas.crop((i * CW, r * CH, (i + 1) * CW, (r + 1) * CH))
after = lambda r, i: rows_img[r][i]
parts = [strip(before, 0, 6), strip(before, 4, 5), strip(after, 4, 5), strip(before, 8, 6), strip(after, 8, 6)]
W = max(p.width for p in parts)
cmp_ = Image.new("RGBA", (W, CH * len(parts)), (255, 255, 255, 255))
for k, p in enumerate(parts):
    cmp_.paste(p, (0, k * CH))
cmp_.convert("RGB").save(f"{OUT}\\compare.png")
print(json.dumps(report, ensure_ascii=False))
