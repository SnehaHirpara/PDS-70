import os
import random
import sqlite3
from init_db import get_db_path

def seed_100_data():
    db_path = get_db_path()
    print(f"Connecting to database: {db_path}")
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    # Clear old data cleanly
    cursor.execute("DELETE FROM saved_jobs;")
    cursor.execute("DELETE FROM applications;")
    cursor.execute("DELETE FROM jobs;")
    cursor.execute("DELETE FROM users;")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('users', 'jobs', 'applications', 'saved_jobs');")
    conn.commit()

    print("Cleared existing records. Generating ~100+ comprehensive sample dataset...")

    # 1. CORE DEMO USERS
    core_users = [
        (
            "System Administrator",
            "admin@talenttrack.com",
            "admin123",
            "admin",
            "Principal System Administrator",
            "+91 99000 11000",
            "TalentTracker Platform Supervisor & DB Administrator. Overseeing enterprise infrastructure and audit systems.",
            "SQLite, Python, Flask, Security Auditing, DevOps, Linux",
            "https://talenttracker.io"
        ),
        (
            "Meet Patel",
            "meet@example.com",
            "meet123",
            "seeker",
            "Senior Full Stack Python Developer",
            "+91 98765 43210",
            "Passionate software engineer experienced with Python, Flask, SQLite, Vue, and modern enterprise web apps.",
            "Python, Flask, SQLite, JavaScript, HTML5, CSS3, REST APIs, Docker, Git",
            "https://github.com/meetpatel"
        ),
        (
            "TechCorp Solutions",
            "employer@example.com",
            "employer123",
            "employer",
            "Head of Global Talent Acquisition",
            "+91 98222 33445",
            "TechCorp is a leading enterprise software provider delivering mission-critical SaaS solutions worldwide.",
            "Technical Recruitment, High-Growth Scaling, Leadership Hiring",
            "https://techcorp.io"
        ),
        (
            "Aarav Patel",
            "aarav@gmail.com",
            "seeker123",
            "seeker",
            "Senior React & Frontend Architect",
            "+91 98765 00112",
            "Full-stack frontend specialist focusing on design systems, performance optimization, and clean micro-frontends.",
            "JavaScript, TypeScript, React, Next.js, HTML5, CSS3, TailwindCSS, Figma",
            "https://github.com/aarav-dev"
        ),
        (
            "Creative Labs Studio",
            "sarah@techcorp.io",
            "emp123",
            "employer",
            "VP of Engineering & Design",
            "+91 97111 22334",
            "Creative Labs builds cutting-edge web design tools, creative suites, and collaborative cloud software.",
            "Design Engineering, Product Strategy, Cloud Systems",
            "https://creativelabs.design"
        )
    ]

    # Additional Employers
    company_names = [
        ("CloudScale Systems", "talent@cloudscale.net", "Cloud & DevOps Infrastructure Lead", "Building enterprise cloud orchestration."),
        ("Apex FinTech Technologies", "careers@apexfintech.com", "Chief Technology Officer", "Next-generation algorithmic banking & payments."),
        ("DataMinds AI Labs", "hr@dataminds.ai", "Director of AI Research", "Pioneering LLMs, machine learning, and computer vision."),
        ("PixelCraft Interactive", "jobs@pixelcraft.studio", "Design Director", "Award-winning UI/UX digital agency and web products."),
        ("HyperScale Logistics", "hiring@hyperscale.co", "Engineering VP", "Supply chain intelligence and real-time fleet analytics."),
        ("CyberShield Defense", "recruiting@cybershield.sec", "Head of InfoSec", "Zero-trust cybersecurity platforms and threat hunting."),
        ("HealthPulse MedTech", "people@healthpulse.org", "Lead Architect", "Digital health platforms and AI diagnostics."),
        ("Nexus Robotics", "careers@nexusrobotics.io", "Robotics Software Director", "Autonomous warehouse automation and IoT robotics."),
        ("Velocity eCommerce", "jobs@velocityshop.com", "Staff Platform Engineer", "Ultra-fast distributed shopping engines.")
    ]

    employer_users = []
    for cname, cemail, ctitle, cbio in company_names:
        employer_users.append((
            cname,
            cemail,
            "emp123",
            "employer",
            ctitle,
            f"+91 98{random.randint(100,999)} {random.randint(10000,99999)}",
            cbio,
            "Talent Management, Technical Hiring, Agile Scaling",
            f"https://{cname.lower().replace(' ', '')}.com"
        ))

    # Additional Job Seekers
    seeker_first_names = [
        "Rohan", "Ananya", "Vikram", "Pooja", "Siddharth", "Neha", "Rahul", "Priya",
        "Arjun", "Sneha", "Karan", "Tanvi", "Aditya", "Ishita", "Varun", "Riya",
        "Dev", "Kavya", "Manish", "Divya", "Suresh", "Meera", "Chirag", "Simran",
        "Harsh", "Anjali", "Gaurav", "Swati", "Nikhil", "Deepika"
    ]
    seeker_last_names = [
        "Sharma", "Verma", "Mehta", "Shah", "Gupta", "Deshmukh", "Nair", "Iyer",
        "Reddy", "Chopra", "Joshi", "Bose", "Kapoor", "Malhotra", "Singhania", "Trivedi"
    ]
    seeker_titles_skills = [
        ("Full Stack Developer", "Python, Django, React, PostgreSQL, REST APIs"),
        ("Backend Python Engineer", "Python, Flask, FastAPI, SQLite, Docker, Redis"),
        ("Frontend UI Engineer", "JavaScript, Vue.js, CSS3, HTML5, Webpack"),
        ("Data Scientist & ML Engineer", "Python, Pandas, NumPy, Scikit-Learn, PyTorch, SQL"),
        ("DevOps & Site Reliability Engineer", "Linux, Docker, Kubernetes, AWS, Terraform, CI/CD"),
        ("Mobile App Developer (Flutter/React Native)", "Dart, Flutter, React Native, Firebase, REST APIs"),
        ("UI/UX Product Designer", "Figma, Adobe XD, Wireframing, User Research, CSS3"),
        ("QA Automation Engineer", "Selenium, Cypress, Python, pytest, Postman, Jenkins"),
        ("Cloud Solutions Architect", "AWS, Azure, Microservices, Python, SQL, System Design"),
        ("Database Administrator", "PostgreSQL, MySQL, SQLite, Query Optimization, Backup & Recovery")
    ]

    seeker_users = []
    for i in range(35):
        fn = seeker_first_names[i % len(seeker_first_names)]
        ln = seeker_last_names[(i * 3 + 2) % len(seeker_last_names)]
        full_name = f"{fn} {ln}"
        email = f"{fn.lower()}.{ln.lower()}{random.randint(10, 99)}@gmail.com"
        title, skills = seeker_titles_skills[i % len(seeker_titles_skills)]
        bio = f"Experienced {title.lower()} passionate about building scalable, maintainable, and high-performance software systems."
        phone = f"+91 9{random.randint(700, 999)} {random.randint(10000, 99999)}"
        portfolio = f"https://github.com/{fn.lower()}-{ln.lower()}"
        seeker_users.append((
            full_name,
            email,
            "seeker123",
            "seeker",
            title,
            phone,
            bio,
            skills,
            portfolio
        ))

    all_users = core_users + employer_users + seeker_users
    cursor.executemany("""
    INSERT INTO users (name, email, password, role, title, phone, bio, skills, portfolio)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, all_users)
    conn.commit()

    # Get user mappings
    cursor.execute("SELECT id, role, email FROM users")
    user_rows = cursor.fetchall()
    all_employer_ids = [row[0] for row in user_rows if row[1] == 'employer']
    all_seeker_ids = [row[0] for row in user_rows if row[1] == 'seeker']

    # 2. GENERATE ~100 REALISTIC JOB LISTINGS
    job_templates = [
        # Software & Web Development
        ("Senior Python Backend Engineer", "Python, Flask, FastAPI, SQLite, Redis", "₹12–18 LPA", "Full-time", "Software Development", "Architect robust backend services, microservices, and database models."),
        ("Full Stack JavaScript Developer", "React, Node.js, Express, MongoDB, TailwindCSS", "₹8–14 LPA", "Full-time", "Web Development", "Develop responsive end-to-end web applications with modern frontend frameworks."),
        ("Lead Frontend Architect", "TypeScript, React, Next.js, Webpack, Design Systems", "₹18–26 LPA", "Full-time", "Web Development", "Define frontend architecture, establish design system standards, and mentor frontend engineers."),
        ("Junior Python Developer", "Python, Django, HTML, CSS, SQL basics", "₹4–7 LPA", "Full-time", "Software Development", "Collaborate on backend business logic, write unit tests, and maintain database integrity."),
        ("Senior Java / Spring Boot Engineer", "Java 17, Spring Boot, Microservices, Kafka, PostgreSQL", "₹14–22 LPA", "Full-time", "Software Development", "Design distributed transactional architectures with Spring Cloud and high-throughput messaging."),
        ("Golang High Performance Systems Engineer", "Go, gRPC, Docker, Kubernetes, Distributed Systems", "₹16–25 LPA", "Full-time", "Software Development", "Develop ultra-low-latency backend services and distributed networking primitives."),
        ("React.js Frontend Specialist", "React, Redux Toolkit, CSS3, REST APIs, Jest", "₹6–11 LPA", "Full-time", "Web Development", "Build sleek, responsive dashboards and interactive client-facing portals."),
        ("Vue.js / Nuxt Fullstack Developer", "Vue 3, Nuxt, Node.js, SQLite, CSS Grid", "₹7–12 LPA", "Full-time", "Web Development", "Create modular web user experiences with lightning-fast page speed metrics."),
        ("PHP / Laravel Web Developer", "Laravel 10, MySQL, REST APIs, Alpine.js, Blade", "₹5–9 LPA", "Full-time", "Web Development", "Maintain and expand enterprise CRM and eCommerce custom modules."),
        ("C# / .NET Core Backend Developer", ".NET Core 8, C#, SQL Server, Azure, Microservices", "₹10–16 LPA", "Full-time", "Software Development", "Build mission-critical enterprise APIs and business management microservices."),
        
        # Data & AI
        ("Senior Data Scientist", "Python, PyTorch, Scikit-learn, SQL, MLOps", "₹16–24 LPA", "Full-time", "Data & Analytics", "Develop predictive models, feature engineering pipelines, and statistical clustering algorithms."),
        ("Data Engineer (ETL / Pipelines)", "Python, Apache Spark, Airflow, Snowflake, SQL", "₹12–19 LPA", "Full-time", "Data & Analytics", "Build real-time data pipelines and scalable warehousing architectures."),
        ("Machine Learning Research Engineer", "Python, TensorFlow, NLP, Transformers, CUDA", "₹20–30 LPA", "Full-time", "Data & Analytics", "Train and fine-tune large foundation models and computer vision pipelines."),
        ("BI & Data Analyst", "SQL, Tableau, Power BI, Python, Excel", "₹6–10 LPA", "Full-time", "Data & Analytics", "Create executive business dashboards, KPI scorecards, and operational forecasting."),
        ("Junior Data Analyst", "SQL, Python, Pandas, Matplotlib, Excel", "₹4–6 LPA", "Full-time", "Data & Analytics", "Extract, clean, and validate daily operational datasets for stakeholders."),
        ("Big Data Architect", "Hadoop, Kafka, Spark, Scala, AWS EMR", "₹22–32 LPA", "Full-time", "Data & Analytics", "Design petabyte-scale data streaming lakes and enterprise data lakes."),
        
        # DevOps & Cloud
        ("DevOps / Cloud Infrastructure Engineer", "AWS, Terraform, Docker, Kubernetes, CI/CD", "₹12–18 LPA", "Full-time", "DevOps & Cloud", "Automate immutable cloud infrastructure, manage container orchestration, and optimize cost."),
        ("Site Reliability Engineer (SRE)", "Linux, Prometheus, Grafana, Python, Ansible", "₹14–22 LPA", "Full-time", "DevOps & Cloud", "Ensure 99.99% system uptime, incident response automation, and SLA monitoring."),
        ("Cloud Security Architect", "AWS Security, IAM, SIEM, Compliance, DevSecOps", "₹18–28 LPA", "Full-time", "DevOps & Cloud", "Implement zero-trust security postures, cloud threat vulnerability scans, and guardrails."),
        ("Kubernetes Platform Engineer", "K8s, Helm, Istio, Golang, Linux Kernel", "₹16–25 LPA", "Full-time", "DevOps & Cloud", "Maintain self-healing multi-tenant Kubernetes clusters in multi-region environments."),
        
        # Design & UX
        ("Principal UI/UX Product Designer", "Figma, Design Systems, UX Research, Prototyping", "₹12–18 LPA", "Full-time", "Design & UX", "Lead end-to-end design strategy from discovery workshops to production design tokens."),
        ("Senior Product Designer (Mobile & Web)", "Figma, Wireframing, Micro-interactions, User Journey", "₹9–15 LPA", "Full-time", "Design & UX", "Craft delighting user journeys and clean SaaS dashboard interfaces."),
        ("Visual & Brand Designer", "Adobe Illustrator, Photoshop, 3D Design, Typography", "₹6–10 LPA", "Full-time", "Design & UX", "Develop brand guidelines, iconography sets, and high-impact marketing visuals."),
        ("UI/UX Designer & Researcher", "Figma, User Testing, Prototyping, Usability Audits", "₹5–9 LPA", "Full-time", "Design & UX", "Conduct customer usability interviews, analyze funnel drop-offs, and refine flows."),
        
        # Product & QA & Management
        ("Technical Product Manager (SaaS)", "Product Strategy, Roadmap, Agile, SQL, PRDs", "₹18–26 LPA", "Full-time", "Product & Marketing", "Own the product vision, coordinate engineering sprints, and drive revenue KPIs."),
        ("Associate Product Manager", "Agile/Scrum, User Stories, Jira, Analytics, UX", "₹8–13 LPA", "Full-time", "Product & Marketing", "Bridge customer needs with sprint backlogs, release notes, and feature prioritization."),
        ("Senior QA Automation Engineer", "Selenium, Cypress, TypeScript, Python, Jenkins", "₹8–14 LPA", "Full-time", "Software Development", "Build robust end-to-end automated testing suites and CI regression pipelines."),
        ("Performance & Security QA Specialist", "JMeter, Postman, OWASP ZAP, load testing, SQL", "₹9–15 LPA", "Full-time", "Software Development", "Execute load, stress, and vulnerability scans on API endpoints and web microservices."),
        ("Product Marketing Manager", "Go-To-Market Strategy, SEO, Content, Positioning", "₹10–16 LPA", "Full-time", "Product & Marketing", "Drive developer adoption, produce product launch campaigns, and optimize funnels.")
    ]

    locations = [
        "Remote / Work From Home",
        "Bengaluru, Karnataka",
        "Ahmedabad, Gujarat",
        "Pune, Maharashtra",
        "Hyderabad, Telangana",
        "Mumbai, Maharashtra",
        "Gurugram, Haryana",
        "Noida, Uttar Pradesh",
        "Chennai, Tamil Nadu",
        "Kolkata, West Bengal",
        "Surat, Gujarat",
        "Vadodara, Gujarat",
        "Jaipur, Rajasthan",
        "Kochi, Kerala",
        "Chandigarh, Punjab"
    ]

    employment_types = ["Full-time", "Full-time", "Full-time", "Remote", "Contract", "Part-time", "Internship"]

    companies_pool = [
        "TechCorp Solutions", "Creative Labs Studio", "CloudScale Systems", "Apex FinTech Technologies",
        "DataMinds AI Labs", "PixelCraft Interactive", "HyperScale Logistics", "CyberShield Defense",
        "HealthPulse MedTech", "Nexus Robotics", "Velocity eCommerce", "Zeta Enterprise Cloud",
        "InfoTech Global", "Cognitive Systems", "QuantumByte Labs", "BlueWave Digital"
    ]

    jobs_to_insert = []
    
    # We will generate 105 rich job records
    for i in range(105):
        tmpl = job_templates[i % len(job_templates)]
        company = companies_pool[i % len(companies_pool)]
        loc = locations[(i * 2 + 1) % len(locations)]
        emp_type = employment_types[i % len(employment_types)]
        owner_id = all_employer_ids[i % len(all_employer_ids)]
        
        # Add slight variation to titles
        title = tmpl[0]
        if i >= len(job_templates):
            variants = ["Enterprise", "Specialist", "Staff", "Principal", "Core", "Global"]
            title = f"{variants[i % len(variants)]} {tmpl[0]}"

        reqs = tmpl[1]
        salary = tmpl[2]
        cat = tmpl[4]
        desc = (
            f"We are looking for an exceptional {title} to join {company}. "
            f"In this role, you will {tmpl[5].lower()} "
            f"You will work closely with cross-functional teams, contribute to high-impact product releases, and help scale our technology foundations."
        )

        jobs_to_insert.append((
            title,
            company,
            loc,
            emp_type,
            cat,
            salary,
            desc,
            reqs,
            owner_id
        ))

    cursor.executemany("""
    INSERT INTO jobs (title, company, location, type, category, salary, description, requirements, owner_id)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, jobs_to_insert)
    conn.commit()

    # 3. GENERATE ~100+ REALISTIC JOB APPLICATIONS
    cursor.execute("SELECT id FROM jobs")
    all_job_ids = [row[0] for row in cursor.fetchall()]

    statuses = ["Pending", "Shortlisted", "Shortlisted", "Hired", "Pending", "Rejected", "Pending", "Hired"]
    sample_cover_letters = [
        "I am highly enthusiastic about this role. With strong hands-on experience in backend and frontend system engineering, I have delivered scalable solutions that reduced system latency by over 35%. I am confident I can add immediate value to your team.",
        "Having worked across high-velocity product teams, I specialize in clean architecture, database indexing, and automated CI pipelines. My technical background aligns directly with your stack and mission.",
        "I have spent the past 3+ years building high-performance modern web apps and REST APIs. I love solving difficult technical hurdles and would love the opportunity to contribute to this position.",
        "Your company's culture and engineering standards truly resonate with me. With deep skills in system design, responsive UI, and reliable SQL architectures, I am eager to discuss how I can contribute.",
        "I am an active open-source contributor and technical builder. I have built and maintained several high-traffic services, ensuring 99.9% uptime and great developer experience.",
        "Enclosed is my application for this position. I possess hands-on proficiency in full-stack web applications, automated testing, and agile sprints, and I am ready to hit the ground running."
    ]

    applications_to_insert = []
    used_pairs = set()

    # Create 110 unique (job_id, seeker_id) applications
    for i in range(110):
        # Pick job and seeker
        job_id = all_job_ids[i % len(all_job_ids)]
        seeker_id = all_seeker_ids[(i * 3 + 1) % len(all_seeker_ids)]
        
        if (job_id, seeker_id) in used_pairs:
            # Shift seeker
            for s in all_seeker_ids:
                if (job_id, s) not in used_pairs:
                    seeker_id = s
                    break

        used_pairs.add((job_id, seeker_id))

        status = statuses[i % len(statuses)]
        cover = sample_cover_letters[i % len(sample_cover_letters)]
        expected_sal = f"₹{random.randint(6, 22)} LPA"
        phone = f"+91 98{random.randint(100, 999)} {random.randint(10000, 99999)}"
        skills = "Python, SQL, JavaScript, REST APIs, HTML5, CSS3"
        portfolio = f"https://github.com/developer-{seeker_id}"

        applications_to_insert.append((
            job_id,
            seeker_id,
            cover,
            expected_sal,
            phone,
            skills,
            portfolio,
            status
        ))

    cursor.executemany("""
    INSERT INTO applications (job_id, seeker_id, cover_letter, expected_salary, phone, skills, portfolio_url, status)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, applications_to_insert)
    conn.commit()

    # 4. GENERATE ~50 SAVED JOBS (BOOKMARKS)
    saved_jobs_to_insert = []
    saved_pairs = set()
    for i in range(50):
        seeker_id = all_seeker_ids[i % len(all_seeker_ids)]
        job_id = all_job_ids[(i * 2 + 5) % len(all_job_ids)]
        if (seeker_id, job_id) not in saved_pairs:
            saved_pairs.add((seeker_id, job_id))
            saved_jobs_to_insert.append((seeker_id, job_id))

    cursor.executemany("""
    INSERT INTO saved_jobs (user_id, job_id)
    VALUES (?, ?)
    """, saved_jobs_to_insert)
    conn.commit()

    # Verification counts
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM jobs")
    total_jobs = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM applications")
    total_apps = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM saved_jobs")
    total_saved = cursor.fetchone()[0]

    print("=" * 60)
    print(f" DATABASE POPULATION COMPLETE:")
    print(f" - Total Users:        {total_users} (Seekers, Employers, Admin)")
    print(f" - Total Jobs:         {total_jobs} (across tech domains & locations)")
    print(f" - Total Applications: {total_apps} (Pending, Shortlisted, Hired, Rejected)")
    print(f" - Total Saved Jobs:   {total_saved}")
    print("=" * 60)

    conn.close()

if __name__ == '__main__':
    seed_100_data()
