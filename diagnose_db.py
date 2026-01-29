#!/usr/bin/env python3
"""
Database diagnostic script for Supabase PostgreSQL setup
"""

import os
from dotenv import load_dotenv
from db_supabase import get_db_connection_wrapper, init_db

load_dotenv()

def check_env_vars():
    """Check if all required environment variables are set"""
    print("=" * 60)
    print("Checking Environment Variables...")
    print("=" * 60)
    
    required_vars = ['SUPABASE_HOST', 'SUPABASE_USER', 'SUPABASE_PASSWORD', 'SUPABASE_DB']
    
    for var in required_vars:
        value = os.getenv(var)
        if value:
            masked_value = value[:5] + "***" if len(value) > 5 else "***"
            print(f"✓ {var}: {masked_value}")
        else:
            print(f"✗ {var}: NOT SET")
    
    print()

def check_db_connection():
    """Check database connection"""
    print("=" * 60)
    print("Checking Database Connection...")
    print("=" * 60)
    
    try:
        conn = get_db_connection_wrapper()
        conn.execute("SELECT version();")
        result = conn.fetchone()
        print(f"✓ Connected to PostgreSQL")
        print(f"  Version: {result['version'] if result else 'Unknown'}")
        conn.close()
        return True
    except Exception as e:
        print(f"✗ Connection failed: {str(e)}")
        return False

def check_tables():
    """Check if tables exist"""
    print("\n" + "=" * 60)
    print("Checking Database Tables...")
    print("=" * 60)
    
    try:
        conn = get_db_connection_wrapper()
        
        # Check users table
        conn.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'users'
            )
        """)
        users_exist = conn.fetchone()['exists']
        print(f"{'✓' if users_exist else '✗'} users table: {'EXISTS' if users_exist else 'MISSING'}")
        
        # Check bugs table
        conn.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'bugs'
            )
        """)
        bugs_exist = conn.fetchone()['exists']
        print(f"{'✓' if bugs_exist else '✗'} bugs table: {'EXISTS' if bugs_exist else 'MISSING'}")
        
        conn.close()
        
        if not users_exist or not bugs_exist:
            print("\n⚠ Missing tables! Running init_db()...")
            init_db()
            print("✓ Database schema initialized")
            
    except Exception as e:
        print(f"✗ Error checking tables: {str(e)}")

def check_users():
    """Check existing users"""
    print("\n" + "=" * 60)
    print("Checking Existing Users...")
    print("=" * 60)
    
    try:
        conn = get_db_connection_wrapper()
        conn.execute("SELECT id, username, is_admin FROM users")
        users = conn.fetchall()
        
        if users:
            print(f"Found {len(users)} user(s):")
            for user in users:
                print(f"  - ID: {user['id']}, Username: {user['username']}, Admin: {user['is_admin']}")
        else:
            print("No users found")
        
        conn.close()
    except Exception as e:
        print(f"✗ Error checking users: {str(e)}")

def main():
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 15 + "DATABASE DIAGNOSTIC REPORT" + " " * 17 + "║")
    print("╚" + "=" * 58 + "╝")
    print()
    
    check_env_vars()
    
    if check_db_connection():
        check_tables()
        check_users()
        print("\n" + "=" * 60)
        print("✓ Database setup looks good!")
        print("=" * 60 + "\n")
    else:
        print("\n" + "=" * 60)
        print("✗ Database connection failed!")
        print("Please check your .env file configuration.")
        print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
