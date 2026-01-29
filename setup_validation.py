#!/usr/bin/env python3
"""
Quick setup script for Supabase PostgreSQL migration
Run this to validate your setup and initialize the database
"""

import os
import sys
from pathlib import Path

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("\n1. Checking .env file...")
    if not Path('.env').exists():
        print("   ✗ .env file not found")
        print("   Copy .env.example to .env and fill in your Supabase credentials")
        return False
    
    # Load .env
    from dotenv import load_dotenv
    load_dotenv()
    
    # Check for required variables
    secret_key = os.getenv('SECRET_KEY')
    supabase_url = os.getenv('SUPABASE_URL')
    
    if not secret_key:
        print("   ✗ SECRET_KEY not found in .env")
        return False
    
    if not supabase_url:
        # Check individual parameters
        host = os.getenv('SUPABASE_HOST')
        user = os.getenv('SUPABASE_USER')
        password = os.getenv('SUPABASE_PASSWORD')
        
        if not (host and user and password):
            print("   ✗ Missing Supabase credentials (neither SUPABASE_URL nor individual parameters found)")
            return False
    
    print("   ✓ .env file configured")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n2. Checking dependencies...")
    required = ['flask', 'psycopg2', 'dotenv', 'openpyxl']
    missing = []
    
    for package in required:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"   ✗ Missing packages: {', '.join(missing)}")
        print(f"   Run: pip install -r requirements.txt")
        return False
    
    print("   ✓ All dependencies installed")
    return True

def test_database_connection():
    """Test connection to Supabase PostgreSQL"""
    print("\n3. Testing database connection...")
    
    try:
        from db_supabase import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT version()')
        version = cursor.fetchone()
        print(f"   ✓ Connected to {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"   ✗ Connection failed: {e}")
        print("   Check your .env file and Supabase project status")
        return False

def check_database_schema():
    """Check if database tables exist"""
    print("\n4. Checking database schema...")
    
    try:
        from db_supabase import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check users table
        cursor.execute('''
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'users'
            )
        ''')
        users_exist = cursor.fetchone()[0]
        
        # Check bugs table
        cursor.execute('''
            SELECT EXISTS (
                SELECT 1 FROM information_schema.tables 
                WHERE table_name = 'bugs'
            )
        ''')
        bugs_exist = cursor.fetchone()[0]
        
        cursor.close()
        conn.close()
        
        if users_exist and bugs_exist:
            print("   ✓ Database schema found")
            return True
        else:
            print("   ✗ Database tables not found")
            print("   Run the migration script in Supabase SQL Editor:")
            print("   - Open supabase_migration.sql")
            print("   - Copy all contents")
            print("   - Paste into Supabase SQL Editor and run")
            return False
            
    except Exception as e:
        print(f"   ✗ Schema check failed: {e}")
        return False

def main():
    """Run all checks"""
    print("=" * 60)
    print("Supabase PostgreSQL Setup Validation")
    print("=" * 60)
    
    checks = [
        check_env_file(),
        check_dependencies(),
        test_database_connection(),
        check_database_schema()
    ]
    
    print("\n" + "=" * 60)
    
    if all(checks):
        print("✓ Setup validation passed!")
        print("=" * 60)
        print("\nYou can now run: python app.py")
        return 0
    else:
        print("✗ Setup validation failed")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Check your .env file configuration")
        print("2. Verify Supabase project is running")
        print("3. Run database migration script")
        print("\nFor detailed help, see MIGRATION_GUIDE.md")
        return 1

if __name__ == '__main__':
    sys.exit(main())
