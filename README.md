# NovaCorp — Company Management Platform

**NovaCorp Platform** is an internal web application for managing companies and their associated comments. It supports three roles (`admin`, `owner`, `user`) with different access levels.

---

## Installation

```bash
pip install -r requirements.txt
pip install flask-wtf
python main.py
```

Visit: `http://127.0.0.1:5000`

The database is automatically initialized on first run.

---

## Default Users

| Username | Password   | Role   | Notes                      |
|----------|------------|--------|----------------------------|
| `alice`  | password1  | user   | Standard employee          |
| `bob`    | password2  | owner  | Owns "Insegura Corp"       |
| `admin`  | admin123   | admin  | Full access                |

---

## Project Structure

```
.
├── main.py                 # Entry point
├── server.py               # Flask app configuration
├── db/
│   └── __init__.py         # Database initialization and helpers
├── routes/
│   ├── auth.py             # Login/logout
│   ├── companies.py        # Company views, dashboard, search
│   ├── companies_admin.py  # Admin company management
│   ├── users_admin.py      # Admin user management
│   └── profile.py          # User profiles
├── templates/
│   ├── base.html           # Shared layout
│   ├── dashboard.html      # Main dashboard
│   ├── auth/               # Login page
│   ├── companies/          # Company pages
│   ├── admin/              # Admin panels
│   ├── profile/            # User profile pages
│   └── errors/             # 404, 403 pages
├── static/
│   └── css/style.css       # Custom styles
└── requirements.txt
```

---

## Technologies

- Python 3 + Flask
- SQLite
- Bootstrap 5.3
- Jinja2 + Bootstrap Icons


---

## Security Improvements

This project includes a full security audit and remediation process based on SAST and manual analysis.

The following vulnerabilities were identified and fixed:

- SQL Injection (CWE-89)
- Stored Cross-Site Scripting (XSS) (CWE-79)
- Cross-Site Request Forgery (CSRF) (CWE-352)
- Session Fixation (CWE-384)
- Insecure password hashing (MD5 → Werkzeug secure hashing)
- Open Redirect
- Weak access control

---

## Static Analysis (SAST)

Static analysis was performed using SonarQube Community Edition.

- Integrated with GitHub Actions
- Automatic scan on each push
- Quality Gate: Sonar Way

---

## Remediation Process

The remediation process followed these steps:

1. Identification of vulnerabilities (SAST + manual analysis)
2. Validation of findings through functional testing
3. Code correction using secure coding practices
4. Re-testing to ensure vulnerabilities were properly mitigated
5. Documentation of each fix in the audit report

---

## Commit Signing

All commits in this repository are digitally signed using SSH keys (ed25519).

This guarantees:
- Author authenticity
- Integrity of the changes
- Traceability of the remediation process

---

## Project Context

This project was developed as part of a security audit scenario for NovaCorp Solutions.

The objective was to:
- Perform a full SAST analysis
- Identify security vulnerabilities
- Remediate insecure code
- Deliver a professional security audit report

---

## Validation

All vulnerabilities were validated before and after remediation:

- SQL Injection payloads no longer affect queries
- XSS payloads are rendered as plain text
- CSRF protection implemented via Flask-WTF
- Session handling hardened

The application remains fully functional after all fixes.

