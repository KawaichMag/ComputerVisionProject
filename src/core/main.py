from fastapi import FastAPI
from src.core.db_session import create_db_and_tables
from src.auth.router import router as auth_router
from src.user.handlers import router as user_router
from src.cards.handlers import router as cards_router

app = FastAPI(
    title="CV Project API",
    description="API для работы с карточками пользователей",
    version="0.1.0"
)

# Подключаем роутеры с префиксом /api
app.include_router(auth_router, prefix="/api")
app.include_router(user_router, prefix="/api")
app.include_router(cards_router, prefix="/api")

@app.on_event("startup")
async def on_startup():
    """Инициализация при старте приложения"""
    await create_db_and_tables()