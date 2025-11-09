from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .app_state import init_models
from PIL import Image
import io
import logging

app = FastAPI()

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_models(app)
    yield

app.router.lifespan_context = lifespan

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("food_detector")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/predict")
async def predict_image(file: UploadFile = File(...)):
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))
    result = app.state.model.query(
        image,
        "List all food products in this image as comma separated values. Only product names, no descriptions."
    )
    products_text = result["answer"]
    products_list = [p.strip() for p in products_text.split(",") if p.strip()]
    logger.info(f"Распознано продуктов: {len(products_list)}")
    logger.info(f"Список продуктов: {products_list}")
    logger.info(f"Сырой ответ модели: {products_text}")
        
    return JSONResponse(content={"predictions": products_list})


@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": "moondream2"}
