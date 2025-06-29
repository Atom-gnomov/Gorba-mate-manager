# Gorba-mate-manager

A lightweight task-and-staff management system built with **Django 5.2** and **SQLite**.  
It lets you create workers, assign tasks, track their status & priority, and view statistics—all from a clean Bootstrap-based UI.
https://gorba-mate-manager.onrender.com/
test user
login:user1
password:password
---

## 📑 Table of Contents
1. [Key Features](#key-features)  
2. [Tech Stack](#tech-stack)  
3. [Quick Start](#quick-start)  


---

## Key Features
- **Workers & Positions** – create, edit, delete workers; assign job positions.  
- **Tasks** – CRUD for tasks with title, description, deadline, priority, status.  
- **Search & Filters** – filter tasks by worker, priority or completion state.  
- **Auth** – Django’s built-in login/logout plus registration form (`WorkerCreationForm`).  
- **Admin panel** – fully-registered models for quick data inspection.  
- **Seed script** – one-shot command to populate the DB with realistic demo data.  
- **Responsive templates** – minimal CSS (Bootstrap 5) for desktop & mobile parity.

---

## Tech Stack
| Layer            | Choice                      | Notes                                   |
| ---------------- | --------------------------- | --------------------------------------- |
| Language         | Python 3.12                 | `cp312` byte-codes already in repo      |
| Framework        | Django 5.2.1                | ASGI-ready; uses function-based views   |
| Database (dev)   | SQLite 3                    | File: `db.sqlite3`                      |
| Templates        | Django templates + Bootstrap| Located in `manager/templates/`         |
| Auth             | Django auth                 | Username = email by default             |
| Task Queue (opt) | None                        | Add Celery if you need async workers    |

---

## Quick Start

```bash
# 1️⃣ Clone repository
git clone https://github.com/YourUser/Gorba-mate-manager.git
cd Gorba-mate-manager

# 2️⃣ Create & activate virtualenv (recommended)
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
.\.venv\Scripts\activate         # Windows

# 3️⃣ Install Python dependencies
pip install -r requirements.txt  # file supplied in repo

# 4️⃣ Set environment variables
export DJANGO_SECRET_KEY='YOUR-32-CHAR-RANDOM-STRING'
export DJANGO_DEBUG=1            # 0 in production
# (Windows PowerShell)  setx DJANGO_SECRET_KEY "YOUR-32-CHAR-RANDOM-STRING"

# 5️⃣ Apply migrations & create admin user
python manage.py migrate
python manage.py createsuperuser

# 6️⃣ (Optional) Seed demo data
python manage.py seed_db

# 7️⃣ Fire up the dev server
python manage.py runserver 8000
