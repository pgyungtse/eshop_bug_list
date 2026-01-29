#!/usr/bin/env python3
"""
Test script for registration
"""

import os
from dotenv import load_dotenv
from db_supabase import get_db_connection_wrapper

load_dotenv()

def test_registration():
    """Test the registration flow"""
    print("Testing user registration...")
    
    try:
        conn = get_db_connection_wrapper()
        
        # Test 1: Check if user exists
        username = "testuser"
        print(f"\n1. Checking if user '{username}' exists...")
        conn.execute('SELECT * FROM users WHERE username = %s', (username,))
        existing = conn.fetchone()
        print(f"   Result: {existing}")
        
        # Test 2: Try to insert a new user
        print(f"\n2. Attempting to insert new user '{username}'...")
        from werkzeug.security import generate_password_hash
        password_hash = generate_password_hash("password123")
        
        conn.execute('''
            INSERT INTO users (username, password_hash, is_admin)
            VALUES (%s, %s, FALSE)
        ''', (username, password_hash))
        conn.commit()
        print("   ✓ User inserted successfully!")
        
        # Test 3: Verify user was created
        print(f"\n3. Verifying user '{username}' was created...")
        conn.execute('SELECT * FROM users WHERE username = %s', (username,))
        user = conn.fetchone()
        if user:
            print(f"   ✓ User found: ID={user['id']}, Username={user['username']}, Admin={user['is_admin']}")
        else:
            print("   ✗ User not found!")
        
        conn.close()
        print("\n✓ Registration test completed successfully!")
        
    except Exception as e:
        print(f"\n✗ Error during registration test:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    test_registration()
