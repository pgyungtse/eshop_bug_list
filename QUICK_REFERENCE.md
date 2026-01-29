# Quick Reference - Registration & Database

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Verify database connection
python diagnose_db.py

# 3. Start the application
python app.py

# 4. Open browser
# Navigate to http://localhost:5000/register
```

## 📝 Registration Flow

```
User enters form data
        ↓
App validates input
        ↓
Check if username exists in Supabase PostgreSQL
        ↓
Hash password with werkzeug
        ↓
Insert into users table
        ↓
Commit transaction
        ↓
Show success message
        ↓
Redirect to login page
```

## 🔍 Database Schema

### Users Table
```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
)
```

### Bugs Table
```sql
CREATE TABLE bugs (
    id SERIAL PRIMARY KEY,
    report_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    system TEXT NOT NULL,
    bug_details TEXT NOT NULL,
    reported_by TEXT NOT NULL,
    status TEXT DEFAULT '開放中',
    priority TEXT DEFAULT '中',
    severity TEXT DEFAULT '中',
    assigned_to TEXT,
    resolution_date TIMESTAMP,
    notes TEXT,
    reported_by_user_id INTEGER REFERENCES users(id)
)
```

## ⚙️ Configuration

### `.env` File
```
# Supabase PostgreSQL Connection
SUPABASE_HOST=your-project.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_database_password

# Flask Configuration
SECRET_KEY=your_secret_key_here
FLASK_ENV=production
```

## 🛠️ Useful Commands

```bash
# Check database connection
python diagnose_db.py

# Test registration process
python test_register.py

# Run Flask in debug mode
FLASK_DEBUG=1 python app.py

# Show existing users
python -c "
from db_supabase import get_db_connection_wrapper
conn = get_db_connection_wrapper()
conn.execute('SELECT id, username, is_admin FROM users')
for user in conn.fetchall():
    print(f\"ID: {user['id']}, User: {user['username']}, Admin: {user['is_admin']}\")
conn.close()
"
```

## 📊 Validation Rules

| Field | Min | Max | Rules |
|-------|-----|-----|-------|
| Username | 1 | - | Alphanumeric, unique |
| Password | 6 | - | Must match confirmation |
| Admin | - | - | Boolean (set by admin) |

## 🔐 Password Security

- Passwords are hashed using Werkzeug's `generate_password_hash()`
- Passwords are never stored in plaintext
- Hashing uses PBKDF2 with 200 iterations by default
- Salt is automatically generated and stored in hash

## 📊 HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Form submission successful |
| 302 | Redirect | After successful registration → login |
| 400 | Bad Request | Missing form fields |
| 500 | Server Error | Database connection error |

## 🚨 Error Handling

```python
# Each operation is wrapped in try-catch
try:
    # Database operation
    conn.execute(query, params)
    conn.commit()
except psycopg2.Error as e:
    # Handle database error
    logger.error(f"DB Error: {e}")
    flash("錯誤信息", 'error')
finally:
    # Always close connection
    conn.close()
```

## 📁 File Structure

```
eshop_bug_list/
├── app.py                              # Main Flask app
├── db_supabase.py                      # Database connection wrapper
├── diagnose_db.py                      # Database diagnostic tool
├── test_register.py                    # Registration test script
├── requirements.txt                    # Python dependencies
├── .env                                # Environment variables (not in git)
├── docker-compose.yml                  # Docker configuration
├── Dockerfile                          # Container definition
├── templates/
│   ├── base.html                      # Base template
│   ├── register.html                  # Registration form
│   ├── login.html                     # Login form
│   ├── index.html                     # Bug list
│   ├── add.html                       # Add bug form
│   ├── edit.html                      # Edit bug form
│   └── error.html                     # Error page
└── README.md                           # Documentation
```

## 🐛 Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Internal Server Error" | DB connection | Check `.env`, run diagnose_db.py |
| "No module psycopg2" | Missing package | `pip install -r requirements.txt` |
| "Username exists" | Duplicate username | Use different username |
| "Passwords don't match" | Form validation | Verify password fields match |
| "Password too short" | Validation rule | Use minimum 6 characters |

## 📞 Support Files

- `REGISTRATION_FIX_SUMMARY.md` - What was fixed
- `REGISTRATION_TROUBLESHOOTING.md` - How to troubleshoot
- `REGISTRATION_VERIFICATION_CHECKLIST.md` - Verification steps

## ✅ Health Check

```bash
# Quick health check
python -c "
from db_supabase import get_db_connection_wrapper
try:
    conn = get_db_connection_wrapper()
    conn.execute('SELECT 1')
    conn.close()
    print('✓ Database connection OK')
except Exception as e:
    print(f'✗ Database error: {e}')
"
```

## 🎯 Key Improvements Made

1. ✅ Fixed Python 3.14 compatibility
2. ✅ Added comprehensive error handling
3. ✅ Improved logging and debugging
4. ✅ Created diagnostic tools
5. ✅ Added error templates
6. ✅ Enhanced form validation
7. ✅ Better connection management
8. ✅ User-friendly error messages
