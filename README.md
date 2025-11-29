# Django CRM (mobile-friendly)

This repository contains a minimal, runnable Django CRM with a REST API and a mobile-friendly frontend.

Quick start (Windows PowerShell):

```powershell
python -m venv .venv; 
.\.venv\Scripts\Activate.ps1; 
python -m pip install --upgrade pip; 
python -m pip install -r requirements.txt; 
python manage.py migrate; 
python manage.py createsuperuser; 
python manage.py runserver 0.0.0.0:8000
```

Open http://127.0.0.1:8000/ to use the mobile-friendly frontend.

API endpoints (examples):
- `GET /api/customers/` - list customers
- `POST /api/customers/` - create customer
- `GET /api/interactions/` - list interactions

Notes:
- This is intentionally minimal to stay easy to run locally.
- For production, turn off `DEBUG`, secure `SECRET_KEY`, and configure allowed hosts, static files and a proper DB.