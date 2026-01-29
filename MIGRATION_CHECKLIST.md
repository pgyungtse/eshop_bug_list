# Migration Checklist - SQLite to Supabase PostgreSQL

## Pre-Migration ✓
- [x] Code updated to use PostgreSQL syntax
- [x] Dependencies added to requirements.txt
- [x] Database module created (db_supabase.py)
- [x] Environment configuration template created

## Setup Phase

### Phase 1: Supabase Account & Project Setup
- [ ] Create Supabase account at https://supabase.com
- [ ] Create new Supabase project
- [ ] Copy project credentials (host, user, password)
- [ ] Note project URL

### Phase 2: Local Configuration
- [ ] Copy `.env.example` to `.env`
  ```bash
  cp .env.example .env
  ```
- [ ] Edit `.env` with Supabase credentials:
  ```
  SUPABASE_URL=postgresql://...
  SECRET_KEY=your_secret_key
  ```
- [ ] Save `.env` file (don't commit to git!)

### Phase 3: Install Dependencies
- [ ] Run: `pip install -r requirements.txt`
- [ ] Verify installation: `python -c "import psycopg2; print('OK')"`

### Phase 4: Database Schema Setup
- [ ] Open Supabase SQL Editor
- [ ] Create new query
- [ ] Copy entire contents of `supabase_migration.sql`
- [ ] Paste into SQL Editor
- [ ] Execute query
- [ ] Verify tables created:
  - [ ] `users` table exists
  - [ ] `bugs` table exists

### Phase 5: Data Migration (if applicable)
- [ ] Back up current SQLite database (optional)
  ```bash
  cp bug_tracker.db bug_tracker.db.backup
  ```
- [ ] Run migration script:
  ```bash
  python migrate_to_postgresql.py
  ```
- [ ] Verify data transferred:
  - [ ] User count matches
  - [ ] Bug count matches

### Phase 6: Validation
- [ ] Run setup validation:
  ```bash
  python setup_validation.py
  ```
- [ ] All checks should pass ✓
  - [ ] .env file configured
  - [ ] Dependencies installed
  - [ ] Database connection successful
  - [ ] Database schema exists

## Testing Phase

### Basic Connectivity
- [ ] Test database connection:
  ```bash
  python db_supabase.py
  ```
  Expected: "Successfully connected to Supabase PostgreSQL!"

### Application Startup
- [ ] Start application:
  ```bash
  python app.py
  ```
- [ ] Application starts without errors
- [ ] No database connection errors in console

### Web Interface Testing
- [ ] Open http://localhost:5000 in browser
- [ ] Page loads successfully
- [ ] No error messages displayed

### Login Testing
- [ ] Attempt login with test user
- [ ] Login functionality works
- [ ] Session management works

### Bug Tracker Testing
- [ ] View bug list (should be empty or show migrated data)
- [ ] Add new bug entry
- [ ] Edit existing bug
- [ ] Delete bug entry
- [ ] Search functionality works
- [ ] Export to Excel works

### User Management
- [ ] Register new user
- [ ] Change password
- [ ] Admin functions work (if admin user)

## Deployment Phase

### Pre-Production
- [ ] Review MIGRATION_GUIDE.md
- [ ] Review MIGRATION_SUMMARY.md
- [ ] All tests pass
- [ ] No console errors
- [ ] Database queries optimized

### Production Deployment
- [ ] Configure Supabase backups
- [ ] Enable SSL for connections
- [ ] Set up monitoring
- [ ] Configure Row Level Security (RLS) if needed
- [ ] Update deployment documentation
- [ ] Update team on new database

### Post-Deployment
- [ ] Monitor application performance
- [ ] Check Supabase dashboard for metrics
- [ ] Verify regular backups
- [ ] Archive old SQLite database

## Troubleshooting Checklist

### Connection Issues
- [ ] Verify `.env` file exists and has correct values
- [ ] Check Supabase project is running
- [ ] Verify credentials are correct
- [ ] Check internet connection
- [ ] Look for firewall blocking connection
- [ ] Run: `python setup_validation.py` for diagnostics

### Data Issues
- [ ] Check migrated data count
- [ ] Verify data integrity
- [ ] Check for missing records
- [ ] Verify timestamps are correct
- [ ] Run: `python migrate_to_postgresql.py` with verbose output

### Application Issues
- [ ] Clear Python cache: `find . -type d -name __pycache__ -exec rm -r {} +`
- [ ] Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`
- [ ] Check for SQL syntax errors in app.py
- [ ] Verify all placeholders use `%s` instead of `?`
- [ ] Check error logs in console

## Rollback Plan (if needed)

### If Something Goes Wrong
- [ ] Stop application
- [ ] Restore from `.db.backup` if exists
- [ ] Revert to original db.py (git checkout db.py)
- [ ] Revert app.py changes if needed
- [ ] Remove psycopg2 from requirements.txt
- [ ] Restart with sqlite3

## Documentation

### Files to Review
- [ ] MIGRATION_GUIDE.md - Comprehensive guide
- [ ] DATABASE_MIGRATION_README.md - Quick start
- [ ] MIGRATION_SUMMARY.md - Overview
- [ ] db_supabase.py - Code documentation
- [ ] supabase_migration.sql - Schema definition

### Files to Keep
- [ ] .env (add to .gitignore!)
- [ ] supabase_migration.sql
- [ ] migrate_to_postgresql.py
- [ ] db_supabase.py
- [ ] setup_validation.py

### Files to Archive/Remove
- [ ] bug_tracker.db (original SQLite, keep as backup)
- [ ] db.py (old SQLite module, keep for reference)

## Sign-Off

- [ ] All phases completed
- [ ] All tests passed
- [ ] Application running smoothly
- [ ] Team notified of changes
- [ ] Documentation updated
- [ ] Ready for production use

---

## Quick Command Reference

```bash
# Validate setup
python setup_validation.py

# Test connection
python db_supabase.py

# Migrate data from SQLite
python migrate_to_postgresql.py

# Start application
python app.py

# Install dependencies
pip install -r requirements.txt

# Check for Python errors
python -m py_compile app.py db_supabase.py
```

---

**Last Updated**: January 28, 2026  
**Status**: Ready for Migration  
**Migration Type**: SQLite → Supabase PostgreSQL
