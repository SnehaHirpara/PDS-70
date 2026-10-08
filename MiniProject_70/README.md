# ⚡ TalentTracker Pro — Full-Stack Recruitment Portal

A modern, full-stack recruitment and talent tracking application built with a **Python Flask** REST API backend and a persistent **SQLite (`.db`)** relational database.

---

## 📁 Project Structure

```text
ssasit/
│
├── frontend/
│   └── talent_tracker.html       # Client interface (HTML5, Vanilla CSS, JS Fetch API)
│
├── backend/
│   ├── app.py                   # Flask REST API server with CORS & SQLite integration
│   ├── init_db.py               # Database schema generator & seed script
│   └── requirements.txt         # Python dependencies (Flask, Flask-Cors)
│
├── database/
│   └── talent_tracker.db        # Physical SQLite 3 database file
│
├── talent_tracker.html          # Root redirect pointer to frontend/talent_tracker.html
└── README.md                    # Setup documentation & API reference
```

---

## 🛠️ Technology Stack

- **Frontend:** HTML5, Modern Vanilla CSS (Glassmorphism, Dark Mode, Animations), JavaScript (Fetch API, ES6 Modules)
- **Backend:** Python 3, Flask, Flask-CORS
- **Database:** SQLite 3 (`database/talent_tracker.db`) via Python `sqlite3` driver
- **Authentication:** Token / Session-based verification with role validation against SQLite

---

## 🗃️ Database Schema Design

The SQLite database is located at `database/talent_tracker.db`.

### 1. `users` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique user identifier |
| `name` | TEXT | NOT NULL | Full name of the user |
| `email` | TEXT | UNIQUE, NOT NULL | Login email address |
| `password` | TEXT | NOT NULL | User password |
| `role` | TEXT | NOT NULL, CHECK(`seeker`, `employer`, `admin`) | User role |
| `title` | TEXT | | Professional headline / title |
| `phone` | TEXT | | Phone / WhatsApp number |
| `bio` | TEXT | | Profile summary |
| `skills` | TEXT | | Comma-separated skills |
| `portfolio` | TEXT | | Portfolio / GitHub URL |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Registration timestamp |

### 2. `jobs` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique job identifier |
| `title` | TEXT | NOT NULL | Job title |
| `company` | TEXT | NOT NULL | Company / Organization name |
| `location` | TEXT | | Work location (e.g. Remote, City) |
| `type` | TEXT | | Employment type (Full-time, Part-time, etc.) |
| `category` | TEXT | | Job category / industry |
| `salary` | TEXT | | Compensation package / CTC |
| `description` | TEXT | NOT NULL | Role description and duties |
| `requirements` | TEXT | | Required skills & experience |
| `owner_id` | INTEGER | FOREIGN KEY REFERENCES `users(id)` | Employer account ID |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Posting timestamp |

### 3. `applications` Table
| Column | Type | Constraints | Description |
|---|---|---|---|
| `id` | INTEGER | PRIMARY KEY AUTOINCREMENT | Unique application identifier |
| `job_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES `jobs(id)` | Applied job ID |
| `seeker_id` | INTEGER | NOT NULL, FOREIGN KEY REFERENCES `users(id)` | Seeker user ID |
| `cover_letter` | TEXT | | Candidate pitch / cover letter |
| `expected_salary` | TEXT | | Candidate expected CTC |
| `phone` | TEXT | | Contact number |
| `skills` | TEXT | | Relevant candidate skills |
| `portfolio_url`| TEXT | | Candidate portfolio link |
| `status` | TEXT | DEFAULT 'Pending', CHECK(`Pending`, `Shortlisted`, `Rejected`, `Hired`) | Current ATS status |
| `applied_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Application timestamp |

---

## 🔑 Demo Accounts & Credentials

| Role | Name | Email | Password |
|---|---|---|---|
| **Admin** | System Administrator | `admin@talenttrack.com` | `admin123` |
| **Seeker** | Meet Patel | `meet@example.com` | `meet123` |
| **Seeker** | Aarav Patel | `aarav@gmail.com` | `seeker123` |
| **Employer** | TechCorp Solutions | `employer@example.com` | `employer123` |
| **Employer** | Creative Labs | `sarah@techcorp.io` | `emp123` |

---

## 🚀 Step-by-Step Running Instructions

### 1. Open Terminal in Project Root
Navigate to the root directory `ssasit/`:
```bash
cd d:\ssasit
```

### 2. (Optional) Create and Activate Virtual Environment
```bash
python -m venv venv
# On Windows PowerShell:
.\venv\Scripts\Activate.ps1
```

### 3. Install Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### 4. Initialize SQLite Database & Demo Seed Data
```bash
python backend/init_db.py
```
> This will automatically create `database/talent_tracker.db` and insert initial demo users, jobs, and applications.

### 5. Start the Flask Backend Server
```bash
python backend/app.py
```
> The API server will start on `http://127.0.0.1:5000`.

### 6. Launch the Frontend
You can open `frontend/talent_tracker.html` directly in any web browser, via VS Code Live Server (`http://localhost:5500`), or via Flask (`http://127.0.0.1:5000/frontend/talent_tracker.html`).

---

## 📡 REST API Reference

| Method | Endpoint | Access | Description |
|---|---|---|---|
| `POST` | `/api/register` | Public | Register a new user (`seeker`, `employer`) |
| `POST` | `/api/login` | Public | Authenticate user & return token |
| `GET` | `/api/me` | Authenticated | Retrieve currently logged in user profile |
| `PUT` | `/api/profile` | Authenticated | Update user profile details |
| `GET` | `/api/jobs` | Public | Get all jobs (supports `?q=...`, `?type=...`, `?category=...`, `?sort=...`) |
| `GET` | `/api/jobs/<id>` | Public | Get single job details & applicant count |
| `POST` | `/api/jobs` | Employer/Admin | Create a new job posting |
| `DELETE` | `/api/jobs/<id>` | Employer/Admin | Delete job posting |
| `POST` | `/api/applications` | Seeker | Apply for an open job |
| `GET` | `/api/applications/my` | Seeker | Get applications submitted by logged-in seeker |
| `GET` | `/api/employer/applications` | Employer/Admin | Get all applicants for jobs posted by employer |
| `PUT` | `/api/applications/<id>/status` | Employer/Admin | Update candidate status (`Shortlisted`, `Rejected`, `Hired`, `Pending`) |
| `GET` | `/api/admin/stats` | Public | Aggregate counts of users, jobs, and applications |
| `GET` | `/api/admin/users` | Admin | Get list of all registered users |
| `GET` | `/api/admin/jobs` | Admin | Get list of all jobs across all employers |
| `GET` | `/api/admin/applications` | Admin | Get all applications across platform |
| `DELETE` | `/api/admin/users/<id>` | Admin | Delete user account from database |
| `POST` | `/api/query` | Public/Studio | Execute raw SQL query for `.db Studio` console |
| `GET` | `/api/db/export` | Public | Direct binary download of `talent_tracker.db` |
