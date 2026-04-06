# MHD Platform

Modular Django platform for MHD, a company that sells magnetohydrodynamic devices for water and gas boiler systems.

## Stack

- Python
- Django
- Django templates
- Tailwind CSS
- PostgreSQL

## Included apps

- `core`: marketing pages and internal staff dashboard
- `products`: B2B catalog for MHD Agua and MHD Gas
- `distributors`: registration, approval flow, dashboard, installer locator
- `orders`: session cart, order creation, order history
- `invoices`: invoice generation and PDF download
- `blog`: SEO-ready articles
- `support`: FAQ and lightweight assistant endpoint

## Environment

Copy `.env.example` into `.env` or set these variables in your shell:

```env
DJANGO_SECRET_KEY=change-me
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
POSTGRES_DB=mhd_platform
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
DEFAULT_FROM_EMAIL=no-reply@mhd-platform.com
```

## Install

```powershell
.venv\Scripts\python.exe -m pip install -r requirements.txt
```

## Run

Start PostgreSQL first, then run:

```powershell
.venv\Scripts\python.exe manage.py migrate
.venv\Scripts\python.exe manage.py seed_mhd_data
.venv\Scripts\python.exe manage.py createsuperuser
.venv\Scripts\python.exe manage.py runserver
```

## Notes

- Distributor registrations are created with `pending` status.
- Approving a distributor in Django admin sends an approval email.
- Orders generate invoices automatically.
- Invoice PDFs are generated from Django templates.
- The assistant widget uses a lightweight keyword-based FAQ responder.