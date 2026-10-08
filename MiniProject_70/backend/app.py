import os
import re
import sqlite3
import time
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS
from init_db import get_db_path, init_db

app = Flask(__name__, static_folder=None)
CORS(app, resources={r"/*": {"origins": "*"}})

# Ensure database exists
DB_PATH = get_db_path()
if not os.path.exists(DB_PATH):
    init_db()

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def dict_from_row(row):
    return dict(row) if row else None

def get_current_user():
    """Verify and retrieve current user from SQLite based on headers."""
    auth_header = request.headers.get("Authorization", "")
    user_id = request.headers.get("X-User-Id")
    user_email = request.headers.get("X-User-Email")

    token_val = None
    if auth_header.startswith("Bearer "):
        token_val = auth_header.split(" ", 1)[1].strip()

    target_id = user_id or token_val
    conn = get_db()
    cursor = conn.cursor()

    user = None
    if target_id:
        # Check if target_id is integer ID or email
        if str(target_id).isdigit():
            cursor.execute("SELECT * FROM users WHERE id = ?", (int(target_id),))
        else:
            cursor.execute("SELECT * FROM users WHERE email = ?", (str(target_id),))
        row = cursor.fetchone()
        if row:
            user = dict_from_row(row)

    if not user and user_email:
        cursor.execute("SELECT * FROM users WHERE email = ?", (user_email,))
        row = cursor.fetchone()
        if row:
            user = dict_from_row(row)

    conn.close()
    return user

def sanitize_user(user):
    if not user:
        return None
    u = dict(user)
    u.pop("password", None)
    return u

def is_valid_email(email):
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(pattern, email))

# ═════════════════════════════════════════════════════════════
# 1. AUTHENTICATION & USER PROFILE APIS
# ═════════════════════════════════════════════════════════════

@app.route("/api/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()
    role = data.get("role", "seeker").strip().lower()

    if not name or not email or not password:
        return jsonify({"success": False, "error": "Name, email, and password are required"}), 400

    if not is_valid_email(email):
        return jsonify({"success": False, "error": "Invalid email address format"}), 400

    if len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters long"}), 400

    if role not in ("seeker", "employer", "admin"):
        return jsonify({"success": False, "error": "Role must be 'seeker', 'employer', or 'admin'"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            return jsonify({"success": False, "error": "An account with this email already exists"}), 409

        title = "Hiring Lead" if role == "employer" else "Job Seeker"
        cursor.execute("""
            INSERT INTO users (name, email, password, role, title, phone, bio, skills, portfolio)
            VALUES (?, ?, ?, ?, ?, '', '', '', '')
        """, (name, email, password, role, title))
        conn.commit()

        user_id = cursor.lastrowid
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        new_user = dict_from_row(cursor.fetchone())

        return jsonify({
            "success": True,
            "message": "User registered successfully",
            "token": str(user_id),
            "user": sanitize_user(new_user)
        }), 201
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip().lower()
    password = data.get("password", "").strip()

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "error": "Invalid email or password"}), 401

        user = dict_from_row(row)
        if user["password"] != password:
            return jsonify({"success": False, "error": "Invalid email or password"}), 401

        return jsonify({
            "success": True,
            "message": "Login successful",
            "token": str(user["id"]),
            "user": sanitize_user(user)
        })
    finally:
        conn.close()

@app.route("/api/me", methods=["GET"])
def get_me():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized / Session expired"}), 401
    return jsonify({"success": True, "user": sanitize_user(user)})

@app.route("/api/profile", methods=["PUT"])
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    name = data.get("name", user["name"]).strip()
    title = data.get("title", user.get("title", "")).strip()
    phone = data.get("phone", user.get("phone", "")).strip()
    bio = data.get("bio", user.get("bio", "")).strip()
    skills = data.get("skills", user.get("skills", "")).strip()
    portfolio = data.get("portfolio", user.get("portfolio", "")).strip()

    if not name:
        return jsonify({"success": False, "error": "Name cannot be empty"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            UPDATE users
            SET name = ?, title = ?, phone = ?, bio = ?, skills = ?, portfolio = ?
            WHERE id = ?
        """, (name, title, phone, bio, skills, portfolio, user["id"]))
        conn.commit()

        cursor.execute("SELECT * FROM users WHERE id = ?", (user["id"],))
        updated = dict_from_row(cursor.fetchone())
        return jsonify({"success": True, "message": "Profile updated successfully", "user": sanitize_user(updated)})
    finally:
        conn.close()

# ═════════════════════════════════════════════════════════════
# 2. JOBS APIS
# ═════════════════════════════════════════════════════════════

@app.route("/api/jobs", methods=["GET"])
def get_jobs():
    q = request.args.get("q", "").strip().lower()
    job_type = request.args.get("type", "").strip()
    category = request.args.get("category", "").strip()
    sort_by = request.args.get("sort", "newest").strip()

    conn = get_db()
    cursor = conn.cursor()
    try:
        sql = """
            SELECT j.*, u.name as owner_name, u.email as owner_email,
                   (SELECT COUNT(*) FROM applications a WHERE a.job_id = j.id) as applicant_count
            FROM jobs j
            LEFT JOIN users u ON j.owner_id = u.id
            WHERE 1=1
        """
        params = []

        if job_type:
            sql += " AND j.type = ?"
            params.push(job_type) if hasattr(params, 'push') else params.append(job_type)

        if category:
            sql += " AND j.category = ?"
            params.append(category)

        if q:
            sql += """ AND (
                LOWER(j.title) LIKE ? OR
                LOWER(j.company) LIKE ? OR
                LOWER(j.location) LIKE ? OR
                LOWER(j.description) LIKE ? OR
                LOWER(j.requirements) LIKE ?
            )"""
            wildcard = f"%{q}%"
            params.extend([wildcard, wildcard, wildcard, wildcard, wildcard])

        if sort_by == "title":
            sql += " ORDER BY j.title ASC"
        elif sort_by == "company":
            sql += " ORDER BY j.company ASC"
        else:
            sql += " ORDER BY j.created_at DESC"

        cursor.execute(sql, params)
        rows = cursor.fetchall()
        jobs_list = [dict_from_row(r) for r in rows]

        return jsonify({"success": True, "count": len(jobs_list), "jobs": jobs_list})
    finally:
        conn.close()

@app.route("/api/jobs/<int:job_id>", methods=["GET"])
def get_job_detail(job_id):
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT j.*, u.name as owner_name, u.email as owner_email,
                   (SELECT COUNT(*) FROM applications a WHERE a.job_id = j.id) as applicant_count
            FROM jobs j
            LEFT JOIN users u ON j.owner_id = u.id
            WHERE j.id = ?
        """, (job_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "error": "Job not found"}), 404

        job = dict_from_row(row)
        return jsonify({"success": True, "job": job})
    finally:
        conn.close()

@app.route("/api/jobs", methods=["POST"])
def create_job():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized. Please log in."}), 401

    if user["role"] not in ("employer", "admin"):
        return jsonify({"success": False, "error": "Only employers can create job postings."}), 403

    data = request.get_json() or {}
    title = data.get("title", "").strip()
    company = data.get("company", "").strip()
    location = data.get("location", "Remote").strip()
    job_type = data.get("type", "Full-time").strip()
    category = data.get("category", "Software Development").strip()
    salary = data.get("salary", "Not specified").strip()
    description = data.get("description", "").strip()
    requirements = data.get("requirements", "").strip()

    if not title or not company or not description:
        return jsonify({"success": False, "error": "Title, company, and description are required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO jobs (title, company, location, type, category, salary, description, requirements, owner_id)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (title, company, location, job_type, category, salary, description, requirements, user["id"]))
        conn.commit()

        job_id = cursor.lastrowid
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        created_job = dict_from_row(cursor.fetchone())

        return jsonify({
            "success": True,
            "message": "Job posted successfully",
            "job": created_job
        }), 201
    finally:
        conn.close()

@app.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        job_row = cursor.fetchone()
        if not job_row:
            return jsonify({"success": False, "error": "Job not found"}), 404

        job = dict_from_row(job_row)
        if user["role"] != "admin" and job["owner_id"] != user["id"]:
            return jsonify({"success": False, "error": "You do not have permission to delete this job"}), 403

        cursor.execute("DELETE FROM applications WHERE job_id = ?", (job_id,))
        cursor.execute("DELETE FROM saved_jobs WHERE job_id = ?", (job_id,))
        cursor.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        conn.commit()

        return jsonify({"success": True, "message": "Job deleted successfully"})
    finally:
        conn.close()

# ═════════════════════════════════════════════════════════════
# 3. APPLICATION & CANDIDATE MANAGEMENT APIS
# ═════════════════════════════════════════════════════════════

@app.route("/api/applications", methods=["POST"])
def apply_for_job():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized. Please log in."}), 401

    if user["role"] != "seeker":
        return jsonify({"success": False, "error": "Only job seekers can apply to positions."}), 403

    data = request.get_json() or {}
    job_id = data.get("job_id")
    cover_letter = data.get("cover_letter", "").strip()
    expected_salary = data.get("expected_salary", "").strip()
    phone = data.get("phone", user.get("phone", "")).strip()
    skills = data.get("skills", user.get("skills", "")).strip()
    portfolio_url = data.get("portfolio_url", user.get("portfolio", "")).strip()

    if not job_id:
        return jsonify({"success": False, "error": "Job ID is required"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, title FROM jobs WHERE id = ?", (job_id,))
        job = cursor.fetchone()
        if not job:
            return jsonify({"success": False, "error": "Target job does not exist"}), 404

        # Check for existing application
        cursor.execute("SELECT id FROM applications WHERE job_id = ? AND seeker_id = ?", (job_id, user["id"]))
        if cursor.fetchone():
            return jsonify({"success": False, "error": "You have already applied for this position."}), 409

        cursor.execute("""
            INSERT INTO applications (job_id, seeker_id, cover_letter, expected_salary, phone, skills, portfolio_url, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'Pending')
        """, (job_id, user["id"], cover_letter, expected_salary, phone, skills, portfolio_url))
        conn.commit()

        app_id = cursor.lastrowid
        cursor.execute("SELECT * FROM applications WHERE id = ?", (app_id,))
        created_app = dict_from_row(cursor.fetchone())

        return jsonify({
            "success": True,
            "message": "Application submitted successfully",
            "application": created_app
        }), 201
    finally:
        conn.close()

@app.route("/api/applications/my", methods=["GET"])
def get_my_applications():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.id, a.job_id, a.status, a.applied_at, a.expected_salary, a.cover_letter,
                   j.title as job_title, j.company, j.location, j.salary as salary, j.type as type
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.seeker_id = ?
            ORDER BY a.applied_at DESC
        """, (user["id"],))
        rows = cursor.fetchall()
        apps = [dict_from_row(r) for r in rows]

        return jsonify({"success": True, "count": len(apps), "applications": apps})
    finally:
        conn.close()

@app.route("/api/employer/applications", methods=["GET"])
def get_employer_applications():
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    if user["role"] not in ("employer", "admin"):
        return jsonify({"success": False, "error": "Employer access required"}), 403

    conn = get_db()
    cursor = conn.cursor()
    try:
        if user["role"] == "admin":
            cursor.execute("""
                SELECT a.id, a.job_id, a.seeker_id, a.status, a.applied_at, a.cover_letter,
                       a.expected_salary, a.phone as applicant_phone, a.skills as applicant_skills,
                       a.portfolio_url as applicant_portfolio,
                       j.title as job_title, j.company,
                       u.name as applicant_name, u.email as applicant_email
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                JOIN users u ON a.seeker_id = u.id
                ORDER BY a.applied_at DESC
            """)
        else:
            cursor.execute("""
                SELECT a.id, a.job_id, a.seeker_id, a.status, a.applied_at, a.cover_letter,
                       a.expected_salary, a.phone as applicant_phone, a.skills as applicant_skills,
                       a.portfolio_url as applicant_portfolio,
                       j.title as job_title, j.company,
                       u.name as applicant_name, u.email as applicant_email
                FROM applications a
                JOIN jobs j ON a.job_id = j.id
                JOIN users u ON a.seeker_id = u.id
                WHERE j.owner_id = ?
                ORDER BY a.applied_at DESC
            """, (user["id"],))

        rows = cursor.fetchall()
        apps = [dict_from_row(r) for r in rows]

        return jsonify({"success": True, "count": len(apps), "applications": apps})
    finally:
        conn.close()

@app.route("/api/applications/<int:app_id>/status", methods=["PUT"])
def update_application_status(app_id):
    user = get_current_user()
    if not user:
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    data = request.get_json() or {}
    new_status = data.get("status", "").strip()
    allowed_statuses = ("Pending", "Shortlisted", "Rejected", "Hired")

    if new_status not in allowed_statuses:
        return jsonify({"success": False, "error": f"Status must be one of {allowed_statuses}"}), 400

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.*, j.owner_id
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            WHERE a.id = ?
        """, (app_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "error": "Application not found"}), 404

        app_data = dict_from_row(row)
        if user["role"] != "admin" and app_data["owner_id"] != user["id"]:
            return jsonify({"success": False, "error": "Only the employer who posted this job can update application status"}), 403

        cursor.execute("UPDATE applications SET status = ? WHERE id = ?", (new_status, app_id))
        conn.commit()

        return jsonify({
            "success": True,
            "message": f"Application status changed to {new_status}",
            "application_id": app_id,
            "status": new_status
        })
    finally:
        conn.close()

# ═════════════════════════════════════════════════════════════
# 4. ADMIN APIS & SYSTEM DASHBOARD
# ═════════════════════════════════════════════════════════════

@app.route("/api/admin/stats", methods=["GET"])
def get_admin_stats():
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM jobs")
        total_jobs = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM applications")
        total_applications = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'employer'")
        total_employers = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'seeker'")
        total_seekers = cursor.fetchone()[0]

        return jsonify({
            "success": True,
            "stats": {
                "total_users": total_users,
                "total_jobs": total_jobs,
                "total_applications": total_applications,
                "total_employers": total_employers,
                "total_seekers": total_seekers
            }
        })
    finally:
        conn.close()

@app.route("/api/admin/users", methods=["GET"])
def get_admin_users():
    user = get_current_user()
    if not user or user["role"] != "admin":
        return jsonify({"success": False, "error": "Admin access required"}), 403

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM users ORDER BY created_at DESC")
        users = [sanitize_user(dict_from_row(r)) for r in cursor.fetchall()]
        return jsonify({"success": True, "count": len(users), "users": users})
    finally:
        conn.close()

@app.route("/api/admin/jobs", methods=["GET"])
def get_admin_jobs():
    user = get_current_user()
    if not user or user["role"] != "admin":
        return jsonify({"success": False, "error": "Admin access required"}), 403

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT j.*, u.name as owner_name, u.email as owner_email,
                   (SELECT COUNT(*) FROM applications a WHERE a.job_id = j.id) as applicant_count
            FROM jobs j
            LEFT JOIN users u ON j.owner_id = u.id
            ORDER BY j.created_at DESC
        """)
        jobs = [dict_from_row(r) for r in cursor.fetchall()]
        return jsonify({"success": True, "count": len(jobs), "jobs": jobs})
    finally:
        conn.close()

@app.route("/api/admin/applications", methods=["GET"])
def get_admin_applications():
    user = get_current_user()
    if not user or user["role"] != "admin":
        return jsonify({"success": False, "error": "Admin access required"}), 403

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.*, j.title as job_title, j.company,
                   u.name as applicant_name, u.email as applicant_email
            FROM applications a
            JOIN jobs j ON a.job_id = j.id
            JOIN users u ON a.seeker_id = u.id
            ORDER BY a.applied_at DESC
        """)
        apps = [dict_from_row(r) for r in cursor.fetchall()]
        return jsonify({"success": True, "count": len(apps), "applications": apps})
    finally:
        conn.close()

@app.route("/api/admin/users/<int:user_id>", methods=["DELETE"])
def admin_delete_user(user_id):
    user = get_current_user()
    if not user or user["role"] != "admin":
        return jsonify({"success": False, "error": "Admin access required"}), 403

    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        if not row:
            return jsonify({"success": False, "error": "User not found"}), 404

        if row[0] == "admin@talenttrack.com":
            return jsonify({"success": False, "error": "Primary administrator account cannot be deleted"}), 400

        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        conn.commit()
        return jsonify({"success": True, "message": "User deleted successfully"})
    finally:
        conn.close()

# ═════════════════════════════════════════════════════════════
# 5. SQL STUDIO QUERY RUNNER & DATABASE EXPORT
# ═════════════════════════════════════════════════════════════

@app.route("/api/query", methods=["POST"])
def execute_raw_query():
    data = request.get_json() or {}
    sql = data.get("query", "").strip()

    if not sql:
        return jsonify({"success": False, "error": "Query cannot be empty"}), 400

    start_time = time.time()
    conn = get_db()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        duration_ms = round((time.time() - start_time) * 1000, 2)

        if cursor.description:
            columns = [desc[0] for desc in cursor.description]
            rows = cursor.fetchall()
            values = [[item for item in row] for row in rows]
            return jsonify({
                "success": True,
                "columns": columns,
                "values": values,
                "row_count": len(values),
                "duration_ms": duration_ms
            })
        else:
            conn.commit()
            return jsonify({
                "success": True,
                "columns": [],
                "values": [],
                "rows_affected": cursor.rowcount,
                "duration_ms": duration_ms,
                "message": "Query executed successfully"
            })
    except Exception as e:
        duration_ms = round((time.time() - start_time) * 1000, 2)
        return jsonify({
            "success": False,
            "error": str(e),
            "duration_ms": duration_ms
        }), 400
    finally:
        conn.close()

@app.route("/api/db/export", methods=["GET"])
def export_db_file():
    if os.path.exists(DB_PATH):
        return send_file(DB_PATH, as_attachment=True, download_name="talent_tracker.db")
    return jsonify({"success": False, "error": "Database file not found"}), 404

# ═════════════════════════════════════════════════════════════
# 6. STATIC / FRONTEND SERVING
# ═════════════════════════════════════════════════════════════

@app.route("/", methods=["GET"])
@app.route("/index.html", methods=["GET"])
@app.route("/talent_tracker.html", methods=["GET"])
def serve_frontend():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir) if os.path.basename(base_dir) == 'backend' else base_dir
    frontend_dir = os.path.join(project_root, "frontend")
    if os.path.exists(os.path.join(frontend_dir, "talent_tracker.html")):
        return send_from_directory(frontend_dir, "talent_tracker.html")
    elif os.path.exists(os.path.join(project_root, "talent_tracker.html")):
        return send_from_directory(project_root, "talent_tracker.html")
    return "TalentTracker API Server Active", 200

if __name__ == "__main__":
    print(f"Starting TalentTracker Flask API on http://127.0.0.1:5000")
    print(f"Connected to SQLite database: {DB_PATH}")
    app.run(host="0.0.0.0", port=5000, debug=True)
