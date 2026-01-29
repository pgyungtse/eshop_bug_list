# Migration Guide: SQLite to Supabase PostgreSQL

## Overview
This guide explains how to migrate your eshop_bug_list application from SQLite to Supabase PostgreSQL.

## Changes Made

### 1. Dependencies Updated (`requirements.txt`)
- Added `psycopg2-binary==2.9.9` - PostgreSQL driver for Python
- Added `SQLAlchemy==2.0.23` - Optional, for future ORM support

### 2. New Database Module (`db_supabase.py`)
- Replaces `db.py` with PostgreSQL-specific implementation
- Provides `get_db_connection_wrapper()` that mimics sqlite3 interface
- Handles both connection string and individual parameter configurations
- Includes connection pooling and error handling

### 3. Updated `app.py`
- Changed import from `sqlite3` to `db_supabase`
- Updated all SQL queries to use PostgreSQL syntax:
  - `?` placeholders → `%s` placeholders
  - `LIKE` → `ILIKE` (case-insensitive search)
  - Boolean handling: `== 1` → `is True`

### 4. Database Schema Changes
The schema is now in PostgreSQL format (already provided in `supabase_migration.sql`):
- Uses `SERIAL PRIMARY KEY` instead of `INTEGER PRIMARY KEY AUTOINCREMENT`
- Uses `TIMESTAMP DEFAULT CURRENT_TIMESTAMP` instead of `DATETIME`
- Uses `BOOLEAN` for boolean fields instead of `0/1`

## Setup Instructions

### Step 1: Create Supabase Project
1. Go to https://supabase.com and sign up/login
2. Create a new project
3. Note your project ID and password

### Step 2: Get Database Credentials
1. In Supabase dashboard, go to Settings → Database
2. Copy the connection string or individual parameters:
   - Host: `db.YOUR_PROJECT_ID.supabase.co`
   - Port: `5432`
   - Database: `postgres`
   - User: `postgres`
   - Password: (your project password)

### Step 3: Create `.env` File
```bash
# Copy from .env.example
cp .env.example .env

# Edit .env with your Supabase credentials:
# Option A: Using connection string (recommended)
SUPABASE_URL=postgresql://postgres.YOUR_PROJECT_ID:YOUR_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres
SECRET_KEY=your_secret_key_here

# Option B: Using individual parameters
SUPABASE_HOST=db.YOUR_PROJECT_ID.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_password_here
SECRET_KEY=your_secret_key_here
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Initialize Database Schema
Go to Supabase SQL Editor and run the contents of `supabase_migration.sql`:
```sql
-- Run the entire migration script in Supabase SQL Editor
```

Alternatively, use Python to initialize:
```python
from db_supabase import init_db
init_db()
```

### Step 6: Migrate Data (if you have existing SQLite data)

#### Option A: Using Supabase SQL Editor
1. Export data from SQLite
2. Convert to PostgreSQL format
3. Import via Supabase SQL Editor

#### Option B: Using Python Script
```python
import sqlite3
from db_supabase import get_db_connection

# Read from SQLite
sqlite_conn = sqlite3.connect('bug_tracker.db')
sqlite_conn.row_factory = sqlite3.Row
sqlite_cursor = sqlite_conn.cursor()

# Get users
users = sqlite_cursor.execute('SELECT * FROM users').fetchall()
bugs = sqlite_cursor.execute('SELECT * FROM bugs').fetchall()

# Write to PostgreSQL
pg_conn = get_db_connection()
pg_cursor = pg_conn.cursor()

for user in users:
    pg_cursor.execute('''
        INSERT INTO users (username, password_hash, is_admin)
        VALUES (%s, %s, %s)
    ''', (user['username'], user['password_hash'], bool(user['is_admin'])))

for bug in bugs:
    pg_cursor.execute('''
        INSERT INTO bugs (
            report_date, system, bug_details, reported_by, status, priority, 
            severity, assigned_to, resolution_date, notes, reported_by_user_id
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ''', (
        bug['report_date'], bug['system'], bug['bug_details'],
        bug['reported_by'], bug['status'], bug['priority'],
        bug['severity'], bug['assigned_to'], bug['resolution_date'],
        bug['notes'], bug['reported_by_user_id']
    ))

pg_conn.commit()
pg_conn.close()
sqlite_conn.close()

print("Data migration complete!")
```

### Step 7: Test Connection
```bash
python db_supabase.py
```
You should see: "Successfully connected to Supabase PostgreSQL!"

### Step 8: Run Application
```bash
python app.py
```

## Key Differences Between SQLite and PostgreSQL

| Aspect | SQLite | PostgreSQL |
|--------|--------|-----------|
| Parameter Placeholder | `?` | `%s` |
| Boolean | `0/1` (INTEGER) | `BOOLEAN` |
| Auto-increment | `INTEGER PRIMARY KEY AUTOINCREMENT` | `SERIAL PRIMARY KEY` |
| Timestamps | `DATETIME` | `TIMESTAMP` |
| Case-insensitive Search | `LIKE` | `ILIKE` |
| Connection | File-based | Network-based |
| Concurrency | Limited | Excellent |

## Connection Methods

### Method 1: Connection String (Recommended)
```python
SUPABASE_URL=postgresql://postgres.YOUR_PROJECT_ID:YOUR_PASSWORD@db.YOUR_PROJECT_ID.supabase.co:5432/postgres
```

### Method 2: Individual Parameters
```python
SUPABASE_HOST=db.YOUR_PROJECT_ID.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_password_here
```

## Troubleshooting

### Connection Refused
- Check your Supabase project is running
- Verify correct host, port, and credentials
- Ensure your IP is whitelisted (if applicable)

### Table Does Not Exist
- Run the migration script in Supabase SQL Editor
- Or call `init_db()` from Python

### Parameter Mismatch
- Ensure all SQL queries use `%s` instead of `?`
- Check parameter order matches the placeholders

### Import Error: psycopg2
```bash
pip install psycopg2-binary
```

## Rollback to SQLite (if needed)
1. Restore the original `db.py`
2. Update imports in `app.py` back to `import sqlite3`
3. Revert SQL queries to use `?` placeholders
4. Ensure `bug_tracker.db` SQLite file exists

## Next Steps
- Consider adding connection pooling for better performance
- Implement automated backups in Supabase
- Set up Row Level Security (RLS) policies in Supabase for better security
- Monitor database performance in Supabase dashboard
