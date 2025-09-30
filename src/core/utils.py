from datetime import datetime
import hashlib
import os
from fastapi import UploadFile, HTTPException
from src.core.config import settings


def photo_hashed_name(email: str, format: str = "jpg") -> str:
    """
    Генерирует уникальное хешированное имя для фотографии пользователя.
    
    Имя формируется на основе email пользователя и текущего времени,
    что гарантирует уникальность для каждого пользователя и загрузки.
    
    Args:
        email: Email пользователя
        format: Формат изображения (по умолчанию jpg)
        
    Returns:
        Строка с хешированным именем файла в формате:
        <хэш_sha256>.<формат>
    """
    hash_input = f"{email}_{datetime.now()}"
    hash_output = hashlib.sha256(hash_input.encode())
    return f"{hash_output.hexdigest()}.{format}"


def save_photo(photo_file: UploadFile, photo_name: str) -> str:
    """
    Сохраняет загруженное фото в указанную директорию с валидацией.
    
    Args:
        photo_file: Загруженный файл из запроса
        photo_name: Имя, под которым нужно сохранить файл
        
    Returns:
        Путь к директории, в которую было сохранено фото
        
    Raises:
        HTTPException: При ошибках валидации или записи файла
    """
    try:
        # Валидация типа файла
        if photo_file.content_type not in ["image/jpeg", "image/png"]:
            raise HTTPException(
                status_code=415,
                detail="Unsupported media type. Allowed: image/jpeg, image/png"
            )

        # Сохранение файла
        photo_dir = os.path.expanduser(settings.PHOTO_FOLDER_FULL_NAME)
        os.makedirs(photo_dir, exist_ok=True)
        
        file_path = os.path.join(photo_dir, photo_name)
        
        with open(file_path, "wb") as buffer:
            buffer.write(photo_file.file.read())
            
        return photo_dir
        
    except OSError as e:
        raise HTTPException(
            status_code=500,
            detail=f"File save error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}"
        )
