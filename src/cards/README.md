# Cards Package

Пакет для работы с карточками в системе.

## Структура пакета

```
cards/
├── __init__.py       # Инициализация пакета
├── handlers.py       # API роутеры FastAPI
├── model.py          # Модель SQLAlchemy
├── repository.py     # Репозиторий для работы с БД
├── schemas.py        # Pydantic схемы
└── service.py        # Бизнес-логика
```

## Основные компоненты

### Модель (model.py)
```python
class Card(BaseModel):
    __tablename__ = "cards"
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100))
    description: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    photo_path: Mapped[str] = mapped_column(String(255))
    price: Mapped[float] = mapped_column(Float)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
```

### Схемы (schemas.py)
```python
class CardBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    photo_path: str = Field(..., max_length=255)
    price: float = Field(..., gt=0)
    user_id: int

class CardCreate(CardBase):
    pass

class CardInDB(CardBase):
    id: int
    created_at: datetime
    updated_at: datetime
```

## API Documentation

### Cards API

#### Создание карточки с фото
**Endpoint:** `POST /cards/`

**Request Format:** `multipart/form-data`

**Parameters:**
- `title` (string, required): Название карточки
- `description` (string, optional): Описание карточки
- `photo` (file, required): Файл изображения
- `price` (number, required): Цена
- `user_id` (number, required): ID пользователя

**Example Request:**
```
POST /cards/
Content-Type: multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW

------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="title"

Название карточки
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="photo"; filename="photo.jpg"
Content-Type: image/jpeg

(binary data)
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="price"

100.0
------WebKitFormBoundary7MA4YWxkTrZu0gW
Content-Disposition: form-data; name="user_id"

1
------WebKitFormBoundary7MA4YWxkTrZu0gW--
```

**Response (201 Created):**
```json
{
  "id": 1,
  "title": "Название карточки",
  "description": "Описание карточки",
  "photo_path": "/path/to/photo.jpg",
  "price": 100.0,
  "user_id": 1,
  "created_at": "2023-01-01T00:00:00",
  "updated_at": "2023-01-01T00:00:00"
}
```

#### Получение карточки
**Endpoint:** `GET /cards/{card_id}`

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Название карточки",
  ...
}
```

**Response (404 Not Found):**
```json
{
  "detail": "Card not found"
}
```

#### Получение карточек пользователя
**Endpoint:** `GET /cards/user/{user_id}`

**Response (200 OK):**
```json
[
  {
    "id": 1,
    "title": "Карточка 1",
    ...
  },
  {
    "id": 2,
    "title": "Карточка 2",
    ...
  }
]
```

#### Обновление карточки
**Endpoint:** `PUT /cards/{card_id}`

**Request Body:**
```json
{
  "title": "Новое название",
  "price": 150.0
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "title": "Новое название",
  "price": 150.0,
  ...
}
```

#### Удаление карточки
**Endpoint:** `DELETE /cards/{card_id}`

**Response (200 OK):**
```json
{
  "message": "Card deleted successfully"
}
```

## Использование

1. Импортируйте роутер в ваше FastAPI приложение:
```python
from cards.handlers import router as cards_router

app = FastAPI()
app.include_router(cards_router)
```

2. Используйте сервис в коде:
```python
from cards.service import CardService
from core.service_factory import ServiceFactory

async def some_operation():
    service = await ServiceFactory.create(CardService)
    cards = await service.get_user_cards(user_id=1)
```

## Зависимости
- SQLAlchemy (асинхронный режим)
- Pydantic v2
- FastAPI