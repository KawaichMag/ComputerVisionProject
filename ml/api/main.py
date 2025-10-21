from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from PIL import Image
import torch
from torchvision import transforms
import torch.nn.functional as F
import numpy as np
import io
import base64
import json
import os
from transformers import SegformerForSemanticSegmentation

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "..", "models", "segmentation_b0")
CONFIG_PATH = os.path.join(MODEL_PATH, "config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    config = json.load(f)

id2label = {int(k): v for k, v in config["id2label"].items()}

IMG_SIZE = config.get("image_size", 224)

transform = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

model = SegformerForSemanticSegmentation.from_pretrained(MODEL_PATH)
model.eval()

app = FastAPI()

'''
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
'''

@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
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

        result.append({
            "class_name": id2label.get(label, f"class_{label}"),
            "mask": mask_base64
        })

    return JSONResponse(content={"predictions": result})
