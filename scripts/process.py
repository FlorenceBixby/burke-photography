"""Curated originals -> web sizes in public/img/<set>/. Drops all metadata
(GPS included) by re-encoding; keeps camera settings in public/data.json for
the placards."""
import json, os, glob
from fractions import Fraction
from PIL import Image, ImageOps, ExifTags
Image.MAX_IMAGE_PIXELS = None
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cur = json.load(open(os.path.join(ROOT, "scripts/curation.json")))
TAGS = {v: k for k, v in ExifTags.TAGS.items()}

def meta(im):
    ex = im.getexif(); sub = ex.get_ifd(0x8769)
    g = lambda t: sub.get(TAGS[t]) or ex.get(TAGS[t])
    def fmt_exp(v):
        if not v: return None
        v = float(v); return f"1/{round(1/v)}s" if v < 1 else f"{v:g}s"
    f = g("FNumber"); fl = g("FocalLength"); iso = g("ISOSpeedRatings") or g("PhotographicSensitivity")
    return {"camera": (ex.get(TAGS["Model"]) or "").strip() or None, "lens": (sub.get(0xA434) or "").strip() or None,
            "focal": f"{float(fl):g}mm" if fl else None, "aperture": f"f/{float(f):g}" if f else None,
            "shutter": fmt_exp(g("ExposureTime")), "iso": f"ISO {iso}" if iso else None,
            "date": (g("DateTimeOriginal") or "")[:10].replace(":", "-") or None}

data = {}
for name, c in cur.items():
    files = sorted(f for f in glob.glob(os.path.expanduser(c["src"]) + "/*") if f.lower().endswith((".jpg", ".jpeg")))
    out = os.path.join(ROOT, "public/img", name); os.makedirs(out, exist_ok=True)
    data[name] = []
    for n, i in enumerate(c["pick"], 1):
        im = Image.open(files[i]); m = meta(im)
        im = ImageOps.exif_transpose(im).convert("RGB")
        slug = f"{n:02d}"
        for w, suffix in ((2400, ""), (900, "-s")):
            t = im.copy(); t.thumbnail((w, w), Image.LANCZOS)
            t.save(f"{out}/{slug}{suffix}.jpg", "JPEG", quality=84 if w > 1000 else 80, progressive=True, optimize=True)
        data[name].append({"file": f"/img/{name}/{slug}", "w": t.width, "h": t.height, "src": os.path.basename(files[i]), **m})
        print(name, slug, os.path.basename(files[i]), m["date"], m["focal"], m["aperture"])
json.dump(data, open(os.path.join(ROOT, "scripts/photos.json"), "w"), indent=1)
