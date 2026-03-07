# FitFlow API

> A robust, secure RESTful API for fitness tracking, activity analytics, and user management.

FitFlow is a Django-based backend service designed to help users track physical activities, monitor caloric burn, and visualize progress through automated summaries. Built with a strict focus on **data isolation**, **secure authentication**, and **RESTful best practices**.

---

## Features

- **Secure Authentication** – User registration and login via Django REST Framework (DRF) Token Authentication.
- **Activity Management** – Full CRUD functionality for fitness logs.
- **Data Isolation** – Server-side filtering ensures users can only access their own data, protecting against IDOR (Insecure Direct Object Reference) attacks.
- **Dynamic Analytics** – A dedicated `/api/summary/` endpoint uses database-level aggregation to calculate total duration and calories burned via SQL.
- **Production Security** – Environment variable protection via `.env` and hardened security headers.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.x |
| API Toolkit | Django REST Framework (DRF) |
| Database | SQLite (Development) / PostgreSQL (Production) |
| Security | `python-dotenv`, Token-based Authentication |
| Deployment | PythonAnywhere / Gunicorn / uWSGI |

---

## Data Model

The API architecture revolves around a strict relationship to the authenticated `User`, ensuring absolute data integrity.

### User *(Django Auth)*
Handles authentication, token generation, and account management.

### Activity
Stores individual fitness events.

| Field | Type | Description |
|---|---|---|
| `user` | `ForeignKey` | Links to the authenticated user. |
| `activity_type` | `CharField` | e.g., Running, Weightlifting, Cycling. |
| `duration` | `PositiveIntegerField` | Duration in minutes. |
| `calories_burned` | `DecimalField` | Calories burned per session. |
| `date` | `DateField` | Date of the activity. |

---

## Design Patterns

### Safe Query Pattern

To ensure privacy, the API overrides `get_queryset` in its views. This guarantees that authenticated users can never query or modify data belonging to another user.
```python
def get_queryset(self):
    return Activity.objects.filter(user=self.request.user)
```

### Automated Summary Logic

The `/api/summary/` endpoint uses Django's `aggregate` function to offload calculations to the database via SQL `SUM`, providing high performance as activity history grows.

---

## API Endpoints

| Endpoint | Method | Description | Auth Required |
|---|---|---|---|
| `/api/register/` | `POST` | Create a new user account. | No |
| `/api/login/` | `POST` | Exchange credentials for an auth token. | No |
| `/api/logout/` | `POST`| Deletes existing token | Yes
| `/api/activities/` | `GET` / `POST` | List all activities or log a new one. | Yes |
| `/api/activities/<id>/` | `GET` / `PUT` / `DELETE` | View, update, or delete a specific activity. | Yes |
| `/api/summary/` | `GET` | Retrieve aggregated totals for calories and duration. | Yes |

---

## Installation & Setup

### 1. Clone & Install
```bash
git clone https://github.com/saybube/FitFlow.git
cd FitFlow

python -m venv venv
source venv/Scripts/activate  # Gitbash 

pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create a `.env` file in the root directory.
```env
SECRET_KEY=private_secret_key_here
DEBUG=True
```

### 3. Initialize the Database & Run
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

> **Note:** A `404` at `http://127.0.0.1:8000/` is expected — all valid routes live under `/api/` or `/admin/`.

---

## Security Configuration

| Feature | Details |
|---|---|
| Environment Separation | Sensitive keys and debug status managed via `.env`. |
| XSS Protection | `SECURE_BROWSER_XSS_FILTER` and `SECURE_CONTENT_TYPE_NOSNIFF` active. |
| Clickjacking Protection | `X_FRAME_OPTIONS = 'DENY'` enforced. |
| SSL Enforcement | `SECURE_SSL_REDIRECT` auto-activates when `DEBUG=False` in production. |

### PythonAnywhere Deployment

1. Push code to GitHub and clone into the PythonAnywhere console.
2. Create a `.env` file on the server with `DEBUG=False` and a secure `SECRET_KEY`.
3. Update the Web Tab WSGI file to point to `fitflow_project.settings`.
4. Run `python manage.py collectstatic` from the server console.
5. Map the `/static/` URL to project's static directory in the Web Tab.
6. Deployed at `https://ebube.pythonanywhere.com/`

---

## Troubleshooting

**`401 Unauthorized`**
Ensures the `Authorization` header is formatted as `Token <token_string>`.

**`500 Internal Server Error` (Production)**
Checks the host's error logs — commonly caused by a missing entry in `requirements.txt`.

**Missing CSS in Admin Panel**
Confirms `STATIC_ROOT` is configured and `collectstatic` has been run on the live server.

---
