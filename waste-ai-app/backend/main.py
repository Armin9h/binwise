from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path
from urllib.parse import quote
import tempfile
import os
from io import BytesIO
from PIL import Image, UnidentifiedImageError
import pillow_heif

from prompts import AVC_CATEGORIES

pillow_heif.register_heif_opener()
app = FastAPI()

# -----------------------
# Paths
# -----------------------
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"
IMAGES_DIR = BASE_DIR / "images"

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")
app.mount("/reference-images", StaticFiles(directory=str(IMAGES_DIR)), name="reference-images")

# -----------------------
# Confidence thresholds
# -----------------------
CONFIDENCE_MIN_RAW_SCORE = 0.00
MIN_MARGIN_RAW_SCORE = 0.0

# -----------------------
# Lazy CLIP globals
# -----------------------
_clip = {
    "model": None,
    "preprocess": None,
    "device": None,
    "tokenizer": None,
    "text_features": None,
    "labels": None,
}

# -----------------------
# Reference image mapping
# -----------------------
REFERENCE_IMAGE_MAP = {
    "Tidningar": "tidningar.jpg",
    "Textil": "textil.jpg",
    "Farligt avfall": "farligtavfall.jpg",
    "Elavfall": "elavfall.jpg",
    "Vitvaror (Kyl och frys)": "vitvaror.jpg",
    "Trädgårdsavfall": "tradgardsavfall.jpg",
    "Trä": "tra.jpg",
    "Ej återvinningsbart": "ejatervinningsbart.jpg",
    "Energiåtervinning": "energiatervinning.jpg",
    "Metall": "metall.jpg",
    "Tegel": "tegel.jpg",
    "Betong": "betong.jpg",
    "Wellpapp": "wellpapp.jpg",
    "Ris och grenar": "RIS.jpg",
    "Impregnerat trä": "impregnerattra.jpg",
    "Gips": "gips.jpg",
    "Däck": "dack.jpg",
    "Planglas": "PLANGLAS.jpg",
    "Stoppade möbler": "stoppademobler.jpg",
    "Hårdplast": "hårdplast.jpg",
    "Mjukplast": "mjukplastforpackningar.jpg",
    "Fallfrukt": "fallfrukt.jpg",
    "Böcker": "bocker.jpg",
    "Lastpallar": "lastpallar.jpg",
}

def get_reference_image_url(label: str) -> str | None:
    filename = REFERENCE_IMAGE_MAP.get(label)
    if not filename:
        return None
    return f"/reference-images/{quote(filename)}"

# -----------------------
# Reuse note helper
# -----------------------
def maybe_add_reuse_note(top_labels: list[str]) -> str | None:
    joined = " ".join(label.lower() for label in top_labels)

    if any(word in joined for word in ["elavfall", "böcker", "stoppade möbler", "vitvaror"]):
        return "Den här saken kan även vara lämplig för återbruk om den fortfarande fungerar."
    return None

# -----------------------
# Helpers
# -----------------------
def clamp(x, a, b):
    return max(a, min(b, x))

def normalize_top2(labels: list[str], probs: list[float]) -> list[dict]:
    s = sum(probs) if probs else 0.0
    if s <= 0:
        norm = [0.0 for _ in probs]
    else:
        norm = [p / s for p in probs]

    ranked = []
    for lab, raw_p, n in zip(labels, probs, norm):
        ranked.append({
            "label": lab,
            "raw_score": round(float(raw_p), 3),
            "percent": int(round(n * 100)),
        })

    if ranked:
        total = sum(x["percent"] for x in ranked)
        diff = 100 - total
        ranked[0]["percent"] = clamp(ranked[0]["percent"] + diff, 0, 100)

    return ranked

def should_refuse(raw_top1: float, raw_top2: float) -> bool:
    margin = raw_top1 - raw_top2

    if raw_top1 < CONFIDENCE_MIN_RAW_SCORE:
        return True

    if margin < MIN_MARGIN_RAW_SCORE:
        return True

    return False

def center_crop(img: Image.Image, ratio: float) -> Image.Image:
    w, h = img.size
    new_w = int(w * ratio)
    new_h = int(h * ratio)

    left = (w - new_w) // 2
    top = (h - new_h) // 2
    right = left + new_w
    bottom = top + new_h

    return img.crop((left, top, right, bottom))

# -----------------------
# CLIP (lazy loader)
# -----------------------
def get_clip_bundle():
    if _clip["model"] is None:
        import torch
        import open_clip

        device = "cuda" if torch.cuda.is_available() else "cpu"

        model, _, preprocess = open_clip.create_model_and_transforms(
            "ViT-B-32",
            pretrained="laion2b_s34b_b79k"
        )
        model = model.to(device)
        model.eval()

        tokenizer = open_clip.get_tokenizer("ViT-B-32")

        labels = [item["label"] for item in AVC_CATEGORIES]
        prompts = [item["prompt"] for item in AVC_CATEGORIES]

        with torch.no_grad():
            tokens = tokenizer(prompts).to(device)
            text_features = model.encode_text(tokens)
            text_features /= text_features.norm(dim=-1, keepdim=True)

        _clip["model"] = model
        _clip["preprocess"] = preprocess
        _clip["device"] = device
        _clip["tokenizer"] = tokenizer
        _clip["text_features"] = text_features
        _clip["labels"] = labels

    return _clip

def classify_avc_ensemble(pil_image: Image.Image, top_k=2) -> tuple[list[dict], float, float]:
    import torch

    bundle = get_clip_bundle()
    model = bundle["model"]
    preprocess = bundle["preprocess"]
    device = bundle["device"]
    text_features = bundle["text_features"]
    labels = bundle["labels"]

    views = [
        pil_image,
        center_crop(pil_image, 0.85),
        center_crop(pil_image, 0.70),
    ]

    probs_list = []

    with torch.no_grad():
        for view in views:
            image_input = preprocess(view).unsqueeze(0).to(device)
            image_features = model.encode_image(image_input)
            image_features /= image_features.norm(dim=-1, keepdim=True)

            probs = (image_features @ text_features.T).softmax(dim=-1)[0]
            probs_list.append(probs)

        avg_probs = torch.stack(probs_list, dim=0).mean(dim=0)

    k = min(top_k, len(labels))
    values, indices = avg_probs.topk(k)

    probs = values.tolist()
    chosen_labels = [labels[i] for i in indices.tolist()]

    ranked = normalize_top2(chosen_labels, probs)

    raw_top1 = probs[0] if len(probs) > 0 else 0.0
    raw_top2 = probs[1] if len(probs) > 1 else 0.0

    return ranked, raw_top1, raw_top2

# -----------------------
# Pages
# -----------------------
@app.get("/")
def serve_home():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/hem")
def serve_hem():
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/analys")
def serve_analys():
    return FileResponse(str(FRONTEND_DIR / "analys.html"))

@app.get("/om-oss")
def serve_about():
    return FileResponse(str(FRONTEND_DIR / "om-oss.html"))

@app.get("/api/health")
def health():
    return {"status": "ok", "message": "Backend is alive ✅"}

@app.post("/analyze")
async def analyze_image(file: UploadFile = File(...)):
    content = await file.read()
    suffix = os.path.splitext(file.filename or "")[1] or ".jpg"

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(content)
        tmp_path = tmp.name

    try:
        try:
            img = Image.open(BytesIO(content)).convert("RGB")
        except UnidentifiedImageError:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Bildformatet stöds inte. Testa att använda JPG eller PNG."
                }
            )
        except Exception:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "message": "Kunde inte läsa bilden. Testa att ta bilden igen eller välj en bild från galleriet."
                }
            )
        ranked, raw_top1, raw_top2 = classify_avc_ensemble(img, top_k=2)

        if should_refuse(raw_top1, raw_top2):
            return JSONResponse({
                "filename": file.filename,
                "status": "no_guess",
                "message": "Jag kan inte avgöra vad det är. Ta en tydligare bild.",
                "tips": [
                    "Ta en närmare bild",
                    "Mer ljus",
                    "Enklare bakgrund",
                    "Låt objektet fylla mer av bilden",
                    "Undvik suddiga bilder"
                ]
            })

        reuse_note = maybe_add_reuse_note([item["label"] for item in ranked])
        best_label = ranked[0]["label"] if ranked else None
        reference_image = get_reference_image_url(best_label) if best_label else None

        return JSONResponse({
            "filename": file.filename,
            "status": "ok",
            "predictions": ranked,
            "note": reuse_note,
            "reference_image": reference_image
        })

    finally:
        try:
            os.remove(tmp_path)
        except Exception:
            pass