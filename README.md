# Django Backend for Auto Journal

## Quick start

1. Create venv and install deps
```bash
cd backend
py -m venv .venv
.\\.venv\\Scripts\\pip install -r requirements.txt
```

2. Run with auto-migrations
```bash
.\\.venv\\Scripts\\python runserver.py
```

The server starts at `http://127.0.0.1:8000`.

## API endpoints
- `POST /api/auth/register/` { username, email, password }
- `POST /api/auth/login/` { username, password }
- `POST /api/auth/logout/`
- `GET /api/auth/me/`
- `GET /api/trades/` list own trades
- `POST /api/trades/` create trade (user auto-set)
- `GET /api/trades/{id}/` retrieve own trade
- `PUT/PATCH /api/trades/{id}/` update own trade
- `DELETE /api/trades/{id}/` delete own trade

Auth uses Django session cookies. Include credentials in frontend requests.

## Admin
Create superuser:
```bash
.\\.venv\\Scripts\\python manage.py createsuperuser
```
Admin at `/admin/`.


