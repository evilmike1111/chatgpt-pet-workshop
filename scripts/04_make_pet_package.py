import json, os, hashlib
from PIL import Image
WORK=os.environ.get("PET_WORK",".")
o=os.path.join(WORK,"local-run"); pk=o+r"\pet-package"; os.makedirs(pk,exist_ok=True)
a=Image.open(o+r"\atlas_candidate.png").convert("RGBA")
a.save(pk+r"\spritesheet.webp",lossless=True,quality=100,method=6,exact=True)
b=Image.open(pk+r"\spritesheet.webp").convert("RGBA")
same=(list(a.getdata())==list(b.getdata())) if False else (a.tobytes()==b.tobytes())
json.dump({"id":"zero","displayName":"玄龍 ZERO","description":"黑金玄晶機械龍，聰明、傲嬌、忠誠。","spriteVersionNumber":2,"spritesheetPath":"spritesheet.webp"},open(pk+r"\pet.json","w",encoding="utf-8"),ensure_ascii=False,indent=2)
print("size",b.size,"lossless_roundtrip",same,"bytes",os.path.getsize(pk+r"\spritesheet.webp"),hashlib.sha256(open(pk+r"\spritesheet.webp","rb").read()).hexdigest())

