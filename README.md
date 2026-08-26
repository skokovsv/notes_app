# Notes API

Асинхронный REST API для заметок на FastAPI с полным DevOps-окружением вокруг:
контейнеризация, reverse proxy с TLS и rate limiting, мониторинг, CI/CD с
автотестами и сканированием на уязвимости.

Проект создавался как учебный.


## Возможности

- CRUD для заметок (создание, чтение, список с пагинацией, удаление)
- Авторизация по API-ключу для операций записи (`POST`, `DELETE`)
- Асинхронная работа с PostgreSQL через SQLAlchemy 2.0
- Метрики Prometheus из коробки (`/metrics`)
- Полностью типизированные Pydantic-схемы запросов/ответов

## Стек

| Категория      | Технологии                                      |
|----------------|--------------------------------------------------|
| Backend        | Python 3.13, FastAPI, SQLAlchemy (async), Pydantic v2 |
| База данных    | PostgreSQL 16                                    |
| Инфраструктура | Docker, Docker Compose, nginx (reverse proxy + TLS + rate limiting) |
| Мониторинг     | Prometheus, Grafana                              |
| CI/CD          | GitHub Actions: pytest, Trivy (сканирование образа), Bandit (статический анализ) |
| Тестирование   | pytest, pytest-asyncio, httpx, SQLite (in-memory для тестов) |


## Тестирование

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements-dev.txt
pytest -v
```


## Быстрый старт

```bash
git clone https://github.com/skokovsv/notes_app.git
cd notes_app
cp .env.example .env   # впишите свой API_KEY
docker compose up --build
```