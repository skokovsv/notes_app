# Notes API — Этап 1 (приложение)

Простой CRUD-сервис заметок. Задача этого этапа — не сложность приложения,
а рабочая база (код + тесты) для следующих этапов: CI, сканирование на
уязвимости, деплой, мониторинг.

## Запуск приложения

```bash
docker compose up --build
```

Открыть: http://localhost:8000/docs — там же можно потыкать все эндпоинты руками.

## Эндпоинты

- `GET /health` — проверка живости
- `POST /notes` — создать заметку (`{"title": "...", "content": "..."}`)
- `GET /notes` — список всех заметок
- `GET /notes/{id}` — одна заметка
- `DELETE /notes/{id}` — удалить

## Запуск тестов (важно сделать это первым делом!)

Тесты НЕ требуют Docker/PostgreSQL — используют SQLite в памяти,
поэтому запускаются мгновенно:

```bash
python -m venv venv
source venv/bin/activate   # на Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
pytest -v
```

Ожидаемый результат — 6 тестов, все зелёные:

```
tests/test_notes.py::test_health PASSED
tests/test_notes.py::test_create_note PASSED
tests/test_notes.py::test_list_notes PASSED
tests/test_notes.py::test_get_note_not_found PASSED
tests/test_notes.py::test_delete_note PASSED
tests/test_notes.py::test_create_note_validation_error PASSED
```

Если что-то падает — не идём дальше, разбираемся здесь. На этом коде будет
строиться CI на следующем этапе, поэтому важно, чтобы он реально работал
у вас на машине, а не только "выглядел правильно".

## Структура проекта

```
app/
  main.py        — эндпоинты FastAPI
  database.py    — подключение к PostgreSQL (async SQLAlchemy)
  models.py      — модель Note
  schemas.py     — Pydantic-схемы запросов/ответов
tests/
  conftest.py    — фикстура: подменяет PostgreSQL на SQLite для тестов
  test_notes.py  — сами тесты
```

## Почему тесты на SQLite, а не на реальном PostgreSQL

Для скорости и простоты на старте. На этапе CI (следующий шаг) обсудим
альтернативу — поднимать настоящий PostgreSQL как сервис прямо в
GitHub Actions, это более честная проверка. Но для локальной разработки
и первого знакомства с тестированием — SQLite в памяти достаточно и
не требует Docker вообще.
