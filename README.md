# CV Project API Documentation

## Текущее состояние API

### Аутентификация (`/api/auth`)

#### POST /login
- **Метод:** POST
- **Content-Type:** `application/x-www-form-urlencoded`
- **Параметры:** username, password (стандартный OAuth2 flow)
- **Ответ:** TokenResponse с access_token
- **Код ответа:** 200 при успехе

#### POST /register  
- **Метод:** POST
- **Content-Type:** `application/json`
- **Тело:** UserCreate (email, full_name, password)
- **Ответ:** {message, user_id, email}
- **Код ответа:** 201 при успехе

#### GET /test-auth
- **Метод:** GET
- **Аутентификация:** Требуется
- **Ответ:** {message: "Authenticated successfully"}
- **Код ответа:** 200

### Пользователи (`/api/users`)

#### GET /me
- **Метод:** GET  
- **Аутентификация:** Требуется
- **Ответ:** UserOut (без поля password)
- **Код ответа:** 200

### Карточки (`/api/cards`)

#### POST /
- **Метод:** POST
- **Content-Type:** `multipart/form-data`
- **Параметры:** title (str), description (str), price (float), file (UploadFile)
- **Аутентификация:** Требуется
- **Ответ:** CardInDB
- **Код ответа:** 200

## Конфигурация

Из `src/core/config.py`:
- `DATABASE_URL`: "postgresql+asyncpg://user:password@localhost:5432/cv_project"
- `SECRET_KEY`: "secret-key" 
- `ALGORITHM`: "HS256"
- `ACCESS_TOKEN_EXPIRE_MINUTES`: 30
- `PHOTO_FOLDER_FULL_NAME`: "~/Python_projects/cv_project/photos"

## Примеры запросов

### Аутентификация
```bash
# Логин
curl -X POST "http://localhost:8000/api/auth/login" \
  -d "username=user@example.com" -d "password=password123"

# Регистрация  
curl -X POST "http://localhost:8000/api/auth/register" \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","full_name":"John Doe","password":"password123"}'
```

### Работа с карточками
```bash
# Создание карточки
curl -X POST "http://localhost:8000/api/cards" \
  -H "Authorization: Bearer {token}" \
  -F "title=Test" -F "description=Test" -F "price=100" -F "file=@test.jpg"
```

### Получение профиля
```bash
curl -X GET "http://localhost:8000/api/users/me" \
  -H "Authorization: Bearer {token}"
```