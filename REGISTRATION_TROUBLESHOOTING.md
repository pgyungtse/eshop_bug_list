# Registration Error Troubleshooting Guide

## Symptoms & Solutions

### Error: "Internal Server Error" on Registration

**Step 1: Check Database Connection**
```bash
python diagnose_db.py
```

Expected output should show:
- ✓ SUPABASE_HOST: aws-1*** (masked)
- ✓ SUPABASE_USER: postg*** (masked)
- ✓ Connected to PostgreSQL
- ✓ users table: EXISTS
- ✓ bugs table: EXISTS

**Step 2: Check Environment Variables**
Verify your `.env` file has all required variables:
```
SUPABASE_HOST=db.supabase.co
SUPABASE_PORT=5432
SUPABASE_DB=postgres
SUPABASE_USER=postgres
SUPABASE_PASSWORD=your_password
SECRET_KEY=your_secret_key
```

**Step 3: Check Python Dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Test Registration Programmatically**
```bash
python test_register.py
```

---

## Common Issues & Solutions

### Issue 1: "ModuleNotFoundError: No module named 'psycopg2'"
**Solution:**
```bash
pip install psycopg2==2.9.11
```

### Issue 2: "Database connection error"
**Check:**
- Is Supabase running?
- Are credentials correct in `.env`?
- Is network connectivity working?

**Test:**
```python
python diagnose_db.py
```

### Issue 3: "Username already exists" but it shouldn't
**Reason:** This is normal behavior - usernames must be unique
**Solution:** Try a different username

### Issue 4: "Password length must be at least 6 characters"
**Solution:** Use a longer password (minimum 6 characters)

### Issue 5: "Passwords do not match"
**Solution:** Make sure both password fields have the same value

---

## Form Field Validation

The registration form validates:
- ✓ Username is required and not empty
- ✓ Password is required and not empty  
- ✓ Passwords match
- ✓ Password length >= 6 characters
- ✓ Username is unique (not already registered)

---

## Server-Side Logging

For debugging, check the Flask server output for detailed error messages. The app logs:
- Connection attempts
- Database errors
- Registration attempts
- User authentication attempts

---

## Debug Mode

To enable detailed error reporting, you can modify the Flask app:
```python
app.config['DEBUG'] = True  # Shows detailed error pages
```

**Note**: Only use DEBUG mode for development, not production!

---

## Contact Support

If issues persist:
1. Run `python diagnose_db.py` and share the output
2. Check Flask server logs
3. Verify environment configuration
4. Ensure database tables exist with proper schema
