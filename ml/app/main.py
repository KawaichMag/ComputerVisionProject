import base64
import io
import json
import logging
import os
from contextlib import asynccontextmanager

import numpy as np
import torch
import torch.nn.functional as F
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from PIL import Image
from torchvision import transforms
from transformers import SegformerForSemanticSegmentation

from .app_state import init_models
from .recipe_retrieval import router

app = FastAPI()

app.include_router(router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models(app)
    yield


app.router.lifespan_context = lifespan

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()],
)
logger = logging.getLogger("food_detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "segmentation_b0")
CONFIG_PATH = os.path.join(MODEL_PATH, "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

id2label = {int(k): v for k, v in config["id2label"].items()}

IMG_SIZE = config.get("image_size", 224)

transform = transforms.Compose(
    [
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ]
)

model = SegformerForSemanticSegmentation.from_pretrained(MODEL_PATH)
model.eval()

"""
Принимает файл с изображением

Возвращает json
{
  "predictions": [
    {
      "class_name": "tomato",
      "mask": "<Base64 PNG>"
    },
    {
      "class_name": "broccoli",
      "mask": "<Base64 PNG>"
    }
  ]
}
"""


@app.post("/predict_segment")
async def predict_image_segment(file: UploadFile = File(...)):
    image = Image.open(file.file).convert("RGB")
    original_size = image.size
    input_tensor = transform(image).unsqueeze(0)

    with torch.no_grad():
        outputs = model(input_tensor)

    logits = outputs.logits
    upsampled_logits = F.interpolate(
        logits, size=original_size[::-1], mode="bilinear", align_corners=False
    )
    preds = upsampled_logits.argmax(dim=1)[0].cpu().numpy()

    unique_labels = np.unique(preds)
    result = []

    for label in unique_labels:
        if label == 0:
            continue
        mask = (preds == label).astype(np.uint8) * 255
        mask_image = Image.fromarray(mask)
        buffered = io.BytesIO()
        mask_image.save(buffered, format="PNG")
        mask_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

        result.append(
            {"class_name": id2label.get(label, f"class_{label}"), "mask": mask_base64}
        )

    return JSONResponse(content={"predictions": result})


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    result = app.state.model.query(
        image,
        "List all food products in this image as comma separated values. Only product names, no descriptions.",
    )
    products_text = result["answer"]
    products_list = [p.strip() for p in products_text.split(",") if p.strip()]
    logger.info(f"Распознано продуктов: {len(products_list)}")
    logger.info(f"Список продуктов: {products_list}")
    logger.info(f"Сырой ответ модели: {products_text}")

    return {"predictions": products_list}


@app.post("/predict_with_number")
async def predict_with_number(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    prompt = """<image>
Count food items. Output exactly:
item_name: count(number)
One per line. Only food. No plates."""

    result = app.state.model.query(image, prompt)
    answer = result["answer"]

    predictions = {}
    for line in answer.strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            predictions[key.strip()] = value.strip()

    return {"predictions": predictions}


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": "moondream2"}
