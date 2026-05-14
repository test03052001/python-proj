# Enterprise Platform Python API

FastAPI + SQLAlchemy demo project generated from `mysql-schema.sql`.

The project uses a controller, service, and repository layout:

- `app/controllers/`: HTTP routes.
- `app/services/`: business rules and transactions.
- `app/repositories/`: database access.
- `app/models.py`: SQLAlchemy models mapped to the MySQL schema.
- `app/schemas/`: request and response DTOs.

## Setup

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

The default local database URL uses:

- username: `root`
- password: `root`
- database: `enterprise_platform`

## Start MySQL

With Docker:

```powershell
docker compose up -d mysql
```

Or run `mysql-schema.sql` manually against your local MySQL server.

## Run the API

```powershell
uvicorn app.main:app --reload
```

Open:

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/v1/health`

## Main Endpoints

- `POST /api/v1/users`
- `GET /api/v1/users`
- `POST /api/v1/categories`
- `POST /api/v1/products`
- `PUT /api/v1/stock`
- `POST /api/v1/stock/adjust`
- `POST /api/v1/orders`
- `PATCH /api/v1/orders/{order_id}/status`

## Security Checks

This repo includes security scanning tools:

```powershell
bandit -r app
pip-audit
```

I did not add a known vulnerable dependency to the default app install because that would make the project unsafe by default.
