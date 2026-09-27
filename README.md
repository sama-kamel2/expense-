# Expense Management System

A complete, production-ready Django project for managing personal expenses.
**Note:** The user-facing interface (all pages, labels, and messages) is in **Arabic**, with right-to-left (RTL) layout. This README and the code itself are in English.

## Features
- User registration / login / logout
- Dashboard with real-time statistics
- Add / edit / delete expenses
- Per-user expense categories
- Date + amount + description for each expense
- Total expenses and current-month total
- Category breakdown and last 6 months breakdown
- Search / filter (by category, date range, description)
- Django Admin panel
- Responsive UI (Arabic, RTL)
- Production-ready settings for real server/domain deployment

## Run locally

```bash
python3 -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # then edit the values inside .env
```

Open `.env` and set:
```
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
```

Then run:
```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open your browser at: http://127.0.0.1:8000/

## Environment variables (.env)

Copy `.env.example` to `.env` and fill in the values:

| Variable | Description |
|---|---|
| `SECRET_KEY` | A long, random secret key (change before deploying) |
| `DEBUG` | `False` in production |
| `ALLOWED_HOSTS` | Your domain(s), comma-separated |
| `CSRF_TRUSTED_ORIGINS` | Your https domain URL(s) |
| `DATABASE_URL` | Postgres connection URL (optional — uses SQLite if empty) |

## Deployment (Railway / any PaaS)

The project includes a `Procfile` and `runtime.txt`, so it works out of the box on platforms like **Railway**, **Render**, or similar Python/WSGI hosts:

1. Push the project to a GitHub repository.
2. Create a new project on the platform and connect it to that repo.
3. Add the environment variables listed above (at minimum `SECRET_KEY`, `DEBUG=False`, `ALLOWED_HOSTS`).
4. The platform runs `release: migrate` and `web: gunicorn` automatically from the `Procfile`.
5. Once deployed, connect your custom domain from the platform's domain settings.

## Project structure
```
expense_manager/
├── config/              # Project settings (settings, urls, wsgi)
├── expenses/             # Main app (models, views, forms, urls, admin)
├── templates/expenses/   # HTML templates (Arabic, RTL)
├── static/css/           # CSS files
├── requirements.txt
├── Procfile
├── runtime.txt
├── .env.example
└── manage.py
```

## Security checklist before going live
- Change `SECRET_KEY` to a new random value.
- Set `DEBUG=False` in production.
- Set `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` to your real domain only.
- Always use HTTPS in production.
