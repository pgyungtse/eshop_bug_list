#!/usr/bin/env python3
"""
Migration script: SQLite to Supabase PostgreSQL
This script helps migrate data from SQLite to PostgreSQL
"""

import sqlite3
from db_supabase import get_db_connection
import sys

def migrate_data():
    """Migrate data from SQLite to PostgreSQL"""
    
    print("Starting migration from SQLite to Supabase PostgreSQL...")
    print("-" * 60)
    
    try:
        # Connect to SQLite
        print("\n1. Connecting to SQLite database...")
        sqlite_conn = sqlite3.connect('bug_tracker.db')
        sqlite_conn.row_factory = sqlite3.Row
        sqlite_cursor = sqlite_conn.cursor()
        print("   ✓ Connected to SQLite")
        
        # Connect to PostgreSQL
        print("\n2. Connecting to Supabase PostgreSQL...")
        pg_conn = get_db_connection()
        print("   ✓ Connected to PostgreSQL")
        
        # Get data from SQLite
        print("\n3. Reading data from SQLite...")
        sqlite_cursor.execute('SELECT COUNT(*) as count FROM users')
        user_count = sqlite_cursor.fetchone()['count']
        users = sqlite_conn.execute('SELECT * FROM users').fetchall()
        print(f"   ✓ Found {user_count} users")
        
        sqlite_cursor.execute('SELECT COUNT(*) as count FROM bugs')
        bug_count = sqlite_cursor.fetchone()['count']
        bugs = sqlite_conn.execute('SELECT * FROM bugs').fetchall()
        print(f"   ✓ Found {bug_count} bugs")
        
        # Migrate users
        print("\n4. Migrating users...")
        pg_cursor = pg_conn.cursor()
        
        for user in users:
            try:
                pg_cursor.execute('''
                    INSERT INTO users (id, username, password_hash, is_admin)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        username = EXCLUDED.username,
                        password_hash = EXCLUDED.password_hash,
                        is_admin = EXCLUDED.is_admin
                ''', (
                    user['id'],
                    user['username'],
                    user['password_hash'],
                    bool(user['is_admin'])
                ))
            except Exception as e:
                print(f"   ⚠ Error migrating user {user['username']}: {e}")
        
        pg_conn.commit()
        print(f"   ✓ Migrated {user_count} users")
        
        # Migrate bugs
        print("\n5. Migrating bugs...")
        
        for bug in bugs:
            try:
                pg_cursor.execute('''
                    INSERT INTO bugs (
                        id, report_date, system, bug_details, reported_by,
                        status, priority, severity, assigned_to,
                        resolution_date, notes, reported_by_user_id
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (id) DO UPDATE SET
                        report_date = EXCLUDED.report_date,
                        system = EXCLUDED.system,
                        bug_details = EXCLUDED.bug_details,
                        reported_by = EXCLUDED.reported_by,
                        status = EXCLUDED.status,
                        priority = EXCLUDED.priority,
                        severity = EXCLUDED.severity,
                        assigned_to = EXCLUDED.assigned_to,
                        resolution_date = EXCLUDED.resolution_date,
                        notes = EXCLUDED.notes,
                        reported_by_user_id = EXCLUDED.reported_by_user_id
                ''', (
                    bug['id'],
                    bug['report_date'],
                    bug['system'],
                    bug['bug_details'],
                    bug['reported_by'],
                    bug['status'],
                    bug['priority'],
                    bug['severity'],
                    bug['assigned_to'] or None,
                    bug['resolution_date'] or None,
                    bug['notes'] or None,
                    bug['reported_by_user_id'] or None
                ))
            except Exception as e:
                print(f"   ⚠ Error migrating bug {bug['id']}: {e}")
        
        pg_conn.commit()
        print(f"   ✓ Migrated {bug_count} bugs")
        
        # Verify migration
        print("\n6. Verifying migration...")
        pg_cursor.execute('SELECT COUNT(*) as count FROM users')
        pg_user_count = pg_cursor.fetchone()['count']
        
        pg_cursor.execute('SELECT COUNT(*) as count FROM bugs')
        pg_bug_count = pg_cursor.fetchone()['count']
        
        print(f"   ✓ PostgreSQL now has {pg_user_count} users and {pg_bug_count} bugs")
        
        # Close connections
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()
        
        print("\n" + "=" * 60)
        print("✓ Migration completed successfully!")
        print("=" * 60)
        
        if pg_user_count == user_count and pg_bug_count == bug_count:
            print("\n✓ All data migrated successfully!")
            return True
        else:
            print("\n⚠ Warning: Data count mismatch!")
            print(f"  Users: SQLite={user_count}, PostgreSQL={pg_user_count}")
            print(f"  Bugs: SQLite={bug_count}, PostgreSQL={pg_bug_count}")
            return False
            
    except FileNotFoundError:
        print("\n✗ Error: bug_tracker.db not found!")
        print("  Make sure you're running this script from the project directory")
        return False
    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = migrate_data()
    sys.exit(0 if success else 1)
