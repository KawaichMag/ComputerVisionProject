.PHONY: up down build rebuild logs clean

# Запуск контейнеров в фоновом режиме
up:
	docker-compose up -d

# Остановка контейнеров
down:
	docker-compose down

# Пересборка и запуск контейнеров
rebuild:
	docker-compose up -d --build

# Просмотр логов бэкенда
logs:
	docker-compose logs -f backend

# Просмотр логов базы данных
logs-db:
	docker-compose logs -f postgres

# Остановка и удаление контейнеров, volumes
clean:
	docker-compose down -v

# Запуск в интерактивном режиме
dev:
	docker-compose up

# Перезапуск бэкенда
restart-backend:
	docker-compose restart backend

# Выполнение команд в контейнере бэкенда
exec-backend:
	docker-compose exec backend bash

# Создание .env файла из примера
setup-env:
	cp .env.example .env
	@echo "Файл .env создан. Пожалуйста, отредактируйте настройки."

# Миграции базы данных
migrate:
	alembic upgrade head

migrate-revision:
	alembic revision --autogenerate -m "$(message)"

migrate-downgrade:
	alembic downgrade -1

migrate-history:
	alembic history