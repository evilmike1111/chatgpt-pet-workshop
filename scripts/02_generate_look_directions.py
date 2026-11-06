"""Local-only look-direction generator for ZERO using Qwen-Image-2.1 edit (single input image = repaired idle frame on magenta).
usage: run_qwen2.py <result.json> <tag> <seed> <dir1,dir2,...>"""
import os
WORK = os.environ.get("PET_WORK", ".")   # 你的工作資料夾（放 inputs、repair、generated、local-run）

from PIL import Image

API = "http://127.0.0.1:8188"
SRC_ATLAS = os.path.join(WORK, "repair", "rows09.png")
COMFY = os.environ.get("COMFYUI_DIR", r"C:\ComfyUI")
GEN = os.path.join(WORK, "generated"); os.makedirs(GEN, exist_ok=True)
import os
IN_NAME = os.environ.get("IN_NAME", "zero_idle0_on_magenta.png")
# build the input once: idle frame 0 on pure magenta, scaled up
SR, SC = int(os.environ.get("SRC_ROW", "0")), int(os.environ.get("SRC_COL", "0"))
cell = Image.open(SRC_ATLAS).convert("RGBA").crop((SC*192, SR*208, SC*192+192, SR*208+208))
bb = cell.getchannel("A").point(lambda v: 255 if v > 8 else 0).getbbox()
cell = cell.crop(bb)
s = 800 / max(cell.size)
cell = cell.resize((round(cell.width * s), round(cell.height * s)), Image.LANCZOS)
canvas = Image.new("RGBA", (1024, 1024), (255, 0, 255, 255))
canvas.alpha_composite(cell, ((1024 - cell.width) // 2, 1024 - cell.height - 60))
canvas.convert("RGB").save(os.path.join(COMFY, "input", IN_NAME))
canvas.convert("RGB").save(os.path.join(GEN, "qwen_input.png"))

KEEP = ("Keep everything else pixel-identical: the same black-and-gold chibi mechanical baby dragon, same body, same sitting pose, same legs, same wings, "
        "same tail, same chest crystal, same size and position in the frame, same flat solid pure magenta #FF00FF background. Draw only ONE dragon, no extra views, no text. ")
DIRS = {
    "000": "Change only the head: tilt the head and eyes straight UP toward the top of the picture, chin raised, both amber pupils at the top of the eyes.",
    "090": "Change only the head: turn the head strongly to the RIGHT, three-quarter view, the snout points toward the right edge of the picture, the right side of the face is hidden, both pupils at the far right corners of the eyes; the body stays facing the viewer.",
    "180": "Change only the head: bow the head forward and down so the chin tucks toward the chest and the top of the head and horns face the viewer; both amber pupils look straight down at the ground. The body, legs, wings and tail keep exactly the same size and position as the input.",
    "270": "Change only the head: turn the head strongly to the LEFT, three-quarter view, the snout points toward the left edge of the picture, the left side of the face is hidden, both pupils at the far left corners of the eyes; the body stays facing the viewer.",
    "022.5": "Change only the head: tilt the head up a lot and turn it only slightly to the right; pupils look up and a little to the right; the body stays facing the viewer.",
    "067.5": "Change only the head: turn the head clearly to the right and tilt it slightly up; pupils look right and a little up; the body stays facing the viewer.",
    "112.5": "Change only the head: turn the head clearly to the right and tilt it slightly down; pupils look right and a little down; the body stays facing the viewer.",
    "157.5": "Change only the head: lower the head a lot and turn it only slightly to the right; pupils look down and a little to the right; the body stays facing the viewer.",
    "202.5": "Change only the head: lower the head a lot and turn it only slightly to the left; pupils look down and a little to the left; the body stays facing the viewer.",
    "247.5": "Change only the head: turn the head clearly to the left and tilt it slightly down; pupils look left and a little down; the body stays facing the viewer.",
    "292.5": "Change only the head: turn the head clearly to the left and tilt it slightly up; pupils look left and a little up; the body stays facing the viewer.",
    "337.5": "Change only the head: tilt the head up a lot and turn it only slightly to the left; pupils look up and a little to the left; the body stays facing the viewer.",    "nod": "Change only the head: tilt the head very slightly down and a little to the left, as a small friendly acknowledging nod; both amber eyes open and looking at the viewer; the expression stays calm.",
    "tiltR": "Change only the head: tilt the head a little to the viewer's right side in a curious, attentive way; both amber eyes open looking at the viewer.",
    "proud": "Change only the head: raise the head slightly with a confident satisfied look, eyes open and bright, a tiny smile.",
    "blink": "Change only the face: both eyes gently closed in a calm content blink, head level, tiny smile.",
    "045": "Change only the head: tilt the head up and turn it toward the upper right corner; pupils look toward the upper right; the body stays facing the viewer.",
    "135": "Change only the head: lower the head and turn it toward the lower right corner; pupils look toward the lower right; the body stays facing the viewer.",
    "225": "Change only the head: lower the head and turn it toward the lower left corner; pupils look toward the lower left; the body stays facing the viewer.",
    "315": "Change only the head: tilt the head up and turn it toward the upper left corner; pupils look toward the upper left; the body stays facing the viewer.",
}

def graph(prompt, seed, prefix):
    return {
        "1": {"class_type": "UNETLoader", "inputs": {"unet_name": "qwen_image_2.1_int8_convrot.safetensors", "weight_dtype": "default"}},
        "2": {"class_type": "CLIPLoader", "inputs": {"clip_name": "qwen3vl_8b_int8_convrot.safetensors", "type": "qwen_image", "device": "default"}},
        "3": {"class_type": "VAELoader", "inputs": {"vae_name": "qwen_image_2.1_vae_bf16.safetensors"}},
        "4": {"class_type": "QwenImage21Cache", "inputs": {"model": ["1", 0], "device": "auto", "dtype": "default"}},
        "6": {"class_type": "LoadImage", "inputs": {"image": IN_NAME}},
        "8": {"class_type": "TextEncodeQwenImage21", "inputs": {"clip": ["2", 0], "prompt": prompt, "negative_prompt": "multiple views, grid, collage, sheet, text, shadow", "resolution": 1024,
              "vae": ["3", 0], "images.image_1": ["6", 0]}},
        "10": {"class_type": "EmptyLatentImage", "inputs": {"width": 1024, "height": 1024, "batch_size": 1}},
        "11": {"class_type": "KSampler", "inputs": {"model": ["4", 0], "positive": ["8", 0], "negative": ["8", 1], "latent_image": ["10", 0],
               "seed": seed, "steps": 25, "cfg": 1.0, "sampler_name": "euler", "scheduler": "simple", "denoise": 1.0}},
        "12": {"class_type": "VAEDecode", "inputs": {"samples": ["11", 0], "vae": ["3", 0]}},
        "13": {"class_type": "SaveImage", "inputs": {"images": ["12", 0], "filename_prefix": prefix}},
    }

def post(g):
    req = urllib.request.Request(API + "/prompt", data=json.dumps({"prompt": g}).encode(), headers={"Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8", "replace")[:2000]}

def wait(pid):
    t0 = time.time()
    while True:
        h = json.load(urllib.request.urlopen(f"{API}/history/{pid}"))
        if pid in h:
            st = h[pid].get("status", {})
            outs = [im["filename"] for o in h[pid]["outputs"].values() for im in o.get("images", [])]
            return st.get("status_str"), outs, round(time.time() - t0)
        time.sleep(3)

out_json, tag, seed, dirs = sys.argv[1], sys.argv[2], int(sys.argv[3]), sys.argv[4].split(",")
res = {}
for d in dirs:
    r = post(graph(KEEP + DIRS[d], seed, f"zq_{tag}_{d}"))
    if "prompt_id" not in r:
        print(d, "SUBMIT_FAIL", r); break
    res[d] = wait(r["prompt_id"]); print(d, res[d], flush=True)
    for f in res[d][1]:
        shutil.copy(os.path.join(COMFY, "output", f), os.path.join(GEN, f))
json.dump(res, open(out_json, "w"), indent=1)






