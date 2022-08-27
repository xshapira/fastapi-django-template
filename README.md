# fastapi-django

FastAPI with Django ORM.

## Directory hierarchy

```bash
$ tree -L 3 -I '__pycache__|venv|staticfiles' -P '*.py'
.
├── api
│   ├── __init__.py
│   └── api_v1
│       ├── __init__.py
│       └── api.py
├── cities
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   ├── 0001_initial.py
│   │   └── __init__.py
│   ├── models.py
│   ├── routers
│   │   ├── __init__.py
│   │   └── cities.py
│   └── schemas.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── static
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── tests
    ├── __init__.py
    └── test_api.py

7 directories, 18 files
```

- `models.py`: Django ORMs
- `schemas.py`: Pydantic models
- `routers`: FastAPI routers

## Installation

```bash
poetry install
```

## Before the first run

### Migration

```bash
./manage.py migrate
```

## Run

```bash
$ uvicorn config.asgi:application --reload

./manage.py collectstatic --noinput  # generate static files for django admin
```

## Tools

### FastAPI docs

```plaintext
http://localhost:8000/api/v1/docs
```

### Django admin

```plaintext
http://localhost:8000/admin
```

### Pre-commit hook

```bash
pre-commit install
pre-commit run --all-files
```

### Running tests

```python
python3 manage.py test
```
