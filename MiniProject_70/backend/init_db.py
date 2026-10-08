import os
import sqlite3

def get_db_path():
    # Resolve project root regardless of whether script is run from backend/ or project root
    base_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(base_dir) if os.path.basename(base_dir) == 'backend' else base_dir
    db_dir = os.path.join(project_root, 'database')
    os.makedirs(db_dir, exist_ok=True)
    return os.path.join(db_dir, 'talent_tracker.db')

def init_db():
    db_path = get_db_path()
    print(f"Initializing database at: {db_path}")

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('seeker', 'employer', 'admin')),
        title TEXT,
        phone TEXT,
        bio TEXT,
        skills TEXT,
        portfolio TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Create jobs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT NOT NULL,
        location TEXT,
        type TEXT,
        category TEXT,
        salary TEXT,
        description TEXT,
        requirements TEXT,
        owner_id INTEGER,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE SET NULL
    );
    """)

    # Create applications table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS applications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        job_id INTEGER NOT NULL,
        seeker_id INTEGER NOT NULL,
        cover_letter TEXT,
        expected_salary TEXT,
        phone TEXT,
        skills TEXT,
        portfolio_url TEXT,
        status TEXT DEFAULT 'Pending' CHECK(status IN ('Pending', 'Shortlisted', 'Rejected', 'Hired')),
        applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
        FOREIGN KEY (seeker_id) REFERENCES users(id) ON DELETE CASCADE,
        UNIQUE(job_id, seeker_id)
    );
    """)

    # Create saved_jobs table (optional helper)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_jobs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        job_id INTEGER NOT NULL,
        saved_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
        FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
        UNIQUE(user_id, job_id)
    );
    """)

    conn.commit()

    # Seed data if users table is empty
    cursor.execute("SELECT COUNT(*) FROM users")
    user_count = cursor.fetchone()[0]

    if user_count == 0:
        print("Seeding initial demo data into talent_tracker.db...")
        demo_users = [
            (
                "System Administrator",
                "admin@talenttrack.com",
                "admin123",
                "admin",
                "System Supervisor",
                "+91 99000 11000",
                "TalentTracker Platform Supervisor & DB Administrator",
                "SQLite, System Admin, Security, Python",
                "https://talenttracker.io"
            ),
            (
                "Meet Patel",
                "meet@example.com",
                "meet123",
                "seeker",
                "Full Stack Python Developer",
                "+91 98765 43210",
                "Passionate software engineer experienced with Python, Flask, SQLite and modern web apps.",
                "Python, Flask, SQLite, JavaScript, HTML, CSS, REST APIs",
                "https://github.com/meetpatel"
            ),
            (
                "TechCorp Solutions",
                "employer@example.com",
                "employer123",
                "employer",
                "Talent Acquisition & Hiring Lead",
                "+91 98222 33445",
                "Hiring stellar engineering and analytical talent across India and global remote roles.",
                "Technical Recruitment, Team Scaling",
                "https://techcorp.io"
            ),
            (
                "Aarav Patel",
                "aarav@gmail.com",
                "seeker123",
                "seeker",
                "Senior Software Engineer",
                "+91 98765 00112",
                "Full-stack developer with 4+ years experience in Python, SQLite, and Frontend architecture.",
                "Python, React, TypeScript, SQLite, Docker",
                "https://github.com/aarav-dev"
            ),
            (
                "Creative Labs",
                "sarah@techcorp.io",
                "emp123",
                "employer",
                "VP of Engineering",
                "+91 97111 22334",
                "Building next-generation design and web tools.",
                "Engineering Leadership, Web Architecture",
                "https://creativelabs.design"
            )
        ]

        cursor.executemany("""
        INSERT INTO users (name, email, password, role, title, phone, bio, skills, portfolio)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_users)
        conn.commit()

        # Retrieve user IDs for associations
        cursor.execute("SELECT id, email FROM users")
        user_map = {email: uid for uid, email in cursor.fetchall()}

        emp_id = user_map.get("employer@example.com", 3)
        creative_emp_id = user_map.get("sarah@techcorp.io", emp_id)
        meet_id = user_map.get("meet@example.com", 2)
        aarav_id = user_map.get("aarav@gmail.com", 4)

        demo_jobs = [
            (
                "Python Developer",
                "TechCorp Solutions",
                "Remote",
                "Full-time",
                "Software Development",
                "₹6–10 LPA",
                "Build and maintain Python web applications and REST APIs.",
                "Python, Flask, SQL, REST APIs",
                emp_id
            ),
            (
                "Frontend Developer",
                "Creative Labs",
                "Ahmedabad, Gujarat",
                "Full-time",
                "Web Development",
                "₹5–8 LPA",
                "Create responsive and accessible web interfaces.",
                "HTML, CSS, JavaScript, Bootstrap",
                creative_emp_id
            ),
            (
                "Data Analyst",
                "Insight Analytics",
                "Surat, Gujarat",
                "Part-time",
                "Data & Analytics",
                "₹3–6 LPA",
                "Analyze datasets and prepare business dashboards.",
                "Python, SQL, Excel, Data Visualization",
                emp_id
            ),
            (
                "Senior Cloud & DevOps Engineer",
                "TechCorp Solutions",
                "Bangalore / Remote",
                "Full-time",
                "Software Development",
                "₹12–18 LPA",
                "Lead infrastructure automation, CI/CD pipelines, and high availability systems.",
                "Linux, Docker, Python, AWS, SQLite",
                emp_id
            ),
            (
                "UI/UX Product Designer",
                "Creative Labs",
                "Ahmedabad, Gujarat",
                "Full-time",
                "Design & UX",
                "₹6–9 LPA",
                "Design high fidelity prototypes and intuitive user interfaces for modern web applications.",
                "Figma, UI Design, Wireframing, CSS",
                creative_emp_id
            )
        ]

        cursor.executemany("""
        INSERT INTO jobs (title, company, location, type, category, salary, description, requirements, owner_id)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, demo_jobs)
        conn.commit()

        # Seed sample application
        cursor.execute("""
        INSERT INTO applications (job_id, seeker_id, cover_letter, expected_salary, phone, skills, portfolio_url, status)
        VALUES (1, ?, 'I have extensive experience building Python Flask and SQLite REST APIs. I would love to contribute to TechCorp!', '₹8 LPA', '+91 98765 43210', 'Python, Flask, SQLite, REST APIs', 'https://github.com/meetpatel', 'Shortlisted')
        """, (meet_id,))

        cursor.execute("""
        INSERT INTO applications (job_id, seeker_id, cover_letter, expected_salary, phone, skills, portfolio_url, status)
        VALUES (2, ?, 'Hi! I specialize in semantic HTML5, modern CSS, and vanilla JS responsive layouts.', '₹6 LPA', '+91 98765 00112', 'HTML, CSS, JavaScript', 'https://github.com/aarav-dev', 'Pending')
        """, (aarav_id,))

        conn.commit()
        print("Demo seed data successfully inserted.")
    else:
        print("Database already contains data, skipping seed.")

    conn.close()
    print("Database initialization complete.")

if __name__ == '__main__':
    init_db()
