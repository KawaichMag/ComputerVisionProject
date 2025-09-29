from datetime import datetime
import hashlib
import os
from fastapi import UploadFile
from src.core.config import settings

def photo_hashed_name(email: str, format: str = "jpg") -> str:
    hash_input = f"{email}_{datetime.now()}"
    hash_output =  hashlib.sha256(hash_input.encode())
    return f"{hash_output.hexdigest()}.{format}"
    


def save_photo(photo_file: UploadFile, photo_name: str) -> str:
    """Сохраняет файл фото в заданную директорию"""
    # Получаем абсолютный путь к папке с фото
    photo_dir = os.path.expanduser(settings.PHOTO_FOLDER_FULL_NAME)
    
    # Создаем директорию, если она не существует
    os.makedirs(photo_dir, exist_ok=True)
    
    # Формируем полный путь к файлу
    file_path = os.path.join(photo_dir, photo_name)
    
    # Сохраняем файл
    with open(file_path, "wb") as buffer:
        buffer.write(photo_file.file.read())
    return photo_dir