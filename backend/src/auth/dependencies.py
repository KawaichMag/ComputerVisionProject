from typing import Annotated
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.service import AuthService
from src.core.db_session import get_db
from src.core.service_factory import ServiceFactory
from src.user.schemas import UserInDB
from src.auth.service import oauth2_scheme

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[AsyncSession, Depends(get_db)]
) -> UserInDB:
    """Зависимость для получения текущего пользователя по токену"""
    auth_service = ServiceFactory.create(AuthService, db)
    user = await auth_service.get_current_user(token)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
