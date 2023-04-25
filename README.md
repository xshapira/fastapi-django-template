# fastapi-django-template

Use Django with FastAPI swimmingly.

## Directory hierarchy

```bash
.
├── api
│   ├── __init__.py
│   ├── api_v1
│   │   ├── __init__.py
│   │   └── api.py
│   ├── main.py
│   └── tests
│       ├── __init__.py
│       └── test_api.py
├── config
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
├── posts
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── migrations
│   │   └── __init__.py
│   ├── models.py
│   ├── router.py
│   ├── schemas.py
│   └── views.py
├── templates
└── users
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── schemas.py
    ├── tests.py
    └── views.py

10 directories, 28 files
```

- `models.py` -  Django ORMs
- `schemas.py` - Pydantic models
- `router.py` - is a core of each module with all the endpoints

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
