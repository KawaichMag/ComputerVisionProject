from datetime import datetime
import hashlib
import os
import zipfile
import io
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
        return f"{photo_dir}/{photo_name}"
        
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


def get_photo_file(photo_path: str):
    """
    Проверяет существование файла фотографии по указанному пути.
    
    Args:
        photo_path: Полный путь к файлу фотографии
        
    Returns:
        file object if exists, None otherwise
    """
    if not os.path.exists(photo_path):
        return None
    
    return open(photo_path, 'rb')


def create_zip_archive(files: list) -> io.BytesIO:
    """
    Создает ZIP архив из списка файловых объектов.
    
    Args:
        files: Список файловых объектов (открытых в бинарном режиме)
        
    Returns:
        BytesIO объект с ZIP архивом
    """
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for file_obj in files:
            try:
                # Получаем имя файла из пути
                filename = os.path.basename(file_obj.name)
                # Читаем содержимое файла
                content = file_obj.read()
                # Добавляем файл в архив
                zip_file.writestr(filename, content)
                # Закрываем файл
                file_obj.close()
            except Exception as e:
                # Пропускаем файлы с ошибками
                continue
    
    zip_buffer.seek(0)
    return zip_buffer
