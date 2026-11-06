"""Assemble a local-only ZERO v2 candidate atlas: rows 0-8 from repair-det/rows09.png (+ replacement frames if present),
rows 9-10 from Qwen-generated look images (chroma-keyed, registered to the idle placement)."""
import os
WORK = os.environ.get("PET_WORK", ".")   # 你的工作資料夾（放 inputs、repair、generated、local-run）

import numpy as np
from PIL import Image

D = os.path.join(WORK, "generated")
OUT = os.path.join(WORK, "local-run")
os.makedirs(OUT, exist_ok=True)
CW, CH = 192, 208
rows9 = Image.open(os.path.join(WORK, "repair", "rows09.png")).convert("RGBA")

# ---- input-placement transform (must match run_qwen2.py) ----
idle0 = rows9.crop((0, 0, CW, CH))
bb0 = idle0.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
cw0, ch0 = bb0[2] - bb0[0], bb0[3] - bb0[1]
S = 800 / max(cw0, ch0)                    # cell -> 1024 canvas scale
ow, oh = round(cw0 * S), round(ch0 * S)
ox, oy = (1024 - ow) // 2, 1024 - oh - 60   # where the cropped idle sat on the canvas

def key(img):
    a = np.array(img.convert("RGB")).astype(np.float32)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    m = np.minimum(r, b) - g
    alpha = 1 - np.clip((m - 40) / 150.0, 0, 1)
    spill = np.maximum(0, np.minimum(r, b) - g)
    a[..., 0] -= spill * (1 - alpha * 0.0); a[..., 2] -= spill
    a = np.clip(a, 0, 255)
    out = np.dstack([a, alpha * 255]).astype(np.uint8)
    out[out[..., 3] < 6] = 0
    return Image.fromarray(out, "RGBA")

K = float(os.environ.get("LOOK_SCALE", "0.93"))

def to_cell(gen_path, report, K=K):
    k = key(Image.open(gen_path))
    inv = 1.0 / S
    w, h = round(1024 * inv), round(1024 * inv)
    small = k.resize((w, h), Image.LANCZOS)
    cx, cy = bb0[0] - ox * inv, bb0[1] - oy * inv
    PAD = 100
    big = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    big.alpha_composite(small, (round(cx) + PAD, round(cy) + PAD))
    # pivot = idle foot centre/baseline; scale whole buffer about it, then crop the cell
    ix0, ix1, _, ibot = band(idle0)
    px, py = (ix0 + ix1) / 2 + PAD, ibot + PAD
    bs = big.resize((round(400 * K), round(400 * K)), Image.LANCZOS)
    left, top = round(px * K - (ix0 + ix1) / 2), round(py * K - ibot)
    cell = bs.crop((left, top, left + CW, top + CH))
    bb = cell.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    return cell, bb
def band(cell, frac=0.30):
    al = np.array(cell.getchannel("A")) > 8
    ys = np.where(al.any(1))[0]; top, bot = ys.min(), ys.max()
    y0 = int(bot - (bot - top) * frac)
    xs = np.where(al[y0:bot + 1].any(0))[0]
    return xs.min(), xs.max(), top, bot

ref_x0, ref_x1, _, ref_bot = band(idle0)
ref_w, ref_c = ref_x1 - ref_x0, (ref_x0 + ref_x1) / 2

ORDER = [("c1", "000"), ("m12", "022.5"), ("m12", "045"), ("m12", "067.5"), ("r12", "090"), ("m12", "112.5"), ("m12", "135"), ("m12", "157.5"),
         ("d43", "180"), ("m12", "202.5"), ("m12", "225"), ("m12", "247.5"), ("c2", "270"), ("m12", "292.5"), ("m12", "315"), ("m12", "337.5")]
report = {"transform": {"S": S, "ox": ox, "oy": oy}, "frames": []}
frames = []
for tag, name in ORDER:
    p = f"{D}\\zq_{tag}_{name}_00001_.png"
    cell, bb = to_cell(p, report)
    x0, x1, top, bot = band(cell)
    w, c = x1 - x0, (x0 + x1) / 2
    sc = ref_w / max(w, 1)
    sc = min(max(sc, 0.9), 1.1)
    # rescale around bottom-center then shift to idle foot position
    if abs(sc - 1) > 0.015:
        nw, nh = round(CW * sc), round(CH * sc)
        sm = cell.resize((nw, nh), Image.LANCZOS)
        big = Image.new("RGBA", (CW * 2, CH * 2), (0, 0, 0, 0)); big.alpha_composite(sm, (CW // 2, CH // 2))
        cell = big.crop((CW // 2 + round((nw - CW) / 2), CH // 2 + (nh - CH)), (CW // 2 + round((nw - CW) / 2) + CW, CH // 2 + (nh - CH) + CH)) if False else cell
    x0, x1, top, bot = band(cell)
    dx, dy = round(ref_c - (x0 + x1) / 2), ref_bot - bot
    shifted = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); shifted.alpha_composite(cell, (max(dx, 0), max(dy, 0))) if dx >= 0 and dy >= 0 else shifted.paste(cell, (dx, dy))
    arr = np.array(shifted); arr[arr[..., 3] == 0] = 0
    shifted = Image.fromarray(arr, "RGBA")
    a = shifted.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
    report["frames"].append({"dir": name, "scale_hint": round(sc, 3), "dx": dx, "dy": dy, "bbox": a, "band_w": int(w)})
    frames.append(shifted)

# ---- review row (row 8): idle0, nod, tiltR, proud, blink, idle1 ; frames 1-4 generated locally from idle0 ----
def idle_cell(c): return rows9.crop((c * CW, 0, (c + 1) * CW, CH))
review = [idle_cell(0)]
for nm in ("nod", "tiltR", "proud", "blink"):
    c, _ = to_cell(f"{D}\\zq_rv_{nm}_00001_.png", report, K=1.0)
    x0, x1, top, bot = band(c)
    dx, dy = round(ref_c - (x0 + x1) / 2), ref_bot - bot
    sh = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); sh.paste(c, (dx, dy)); review.append(sh)
review.append(idle_cell(1))
rows9 = rows9.copy()
blank = Image.new("RGBA", (8 * CW, CH), (0, 0, 0, 0)); rows9.paste(blank, (0, 8 * CH))
for i, c in enumerate(review): rows9.alpha_composite(c, (i * CW, 8 * CH))
atlas = Image.new("RGBA", (8 * CW, 11 * CH), (0, 0, 0, 0))
atlas.alpha_composite(rows9, (0, 0))
for i, f in enumerate(frames):
    atlas.alpha_composite(f, ((i % 8) * CW, (9 + i // 8) * CH))
arr = np.array(atlas).astype(np.int32)
sp = np.maximum(0, np.minimum(arr[..., 0], arr[..., 2]) - arr[..., 1] - 12)
arr[..., 0] -= sp; arr[..., 2] -= sp
arr = np.clip(arr, 0, 255).astype(np.uint8); arr[arr[..., 3] == 0] = 0
atlas = Image.fromarray(arr, "RGBA")
atlas.save(f"{OUT}\\atlas_candidate.png")
json.dump(report, open(f"{OUT}\\assemble-report.json", "w"), indent=1, default=int)

# preview: 16-direction loop gif (180 ms/frame) and contact sheet on grey
bgc = (205, 205, 205, 255)
gifs = []
for f in frames:
    g = Image.new("RGBA", (CW, CH), bgc); g.alpha_composite(f); gifs.append(g.convert("P", palette=Image.ADAPTIVE))
gifs[0].save(f"{OUT}\\look16.gif", save_all=True, append_images=gifs[1:], duration=180, loop=0, disposal=2)
sheet = Image.new("RGB", (8 * CW, 2 * CH), bgc[:3])
for i, f in enumerate(frames):
    g = Image.new("RGBA", (CW, CH), bgc); g.alpha_composite(f); sheet.paste(g.convert("RGB"), ((i % 8) * CW, (i // 8) * CH))
sheet.save(f"{OUT}\\look16-cells.png")
print(json.dumps(report["frames"], default=int))






