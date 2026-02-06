import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

# Supabase PostgreSQL connection parameters
# Prefer an actual Postgres connection URL in `DATABASE_URL` or `SUPABASE_DB_URL`.
# If the project SUPABASE_URL (https://...) was provided by mistake, fall back to
# using separate host/user/password/env vars.
SUPABASE_DB_URL = os.getenv('DATABASE_URL') or os.getenv('SUPABASE_DB_URL')
SUPABASE_URL = os.getenv('SUPABASE_URL')  # project URL (https://...) - not a DB dsn
SUPABASE_HOST = os.getenv('SUPABASE_HOST')
SUPABASE_PORT = os.getenv('SUPABASE_PORT', '5432')
SUPABASE_DB = os.getenv('SUPABASE_DB', 'postgres')
SUPABASE_USER = os.getenv('SUPABASE_USER')
SUPABASE_PASSWORD = os.getenv('SUPABASE_PASSWORD')

def get_db_connection():
    """Create and return a PostgreSQL database connection"""
    try:
        # If a real Postgres URL is provided prefer it
        if SUPABASE_DB_URL:
            return psycopg2.connect(SUPABASE_DB_URL)

        # If SUPABASE_URL was set to a project HTTP URL (starts with http),
        # it is not a valid DSN. Fall back to individual env vars.
        if SUPABASE_URL and SUPABASE_URL.startswith('http'):
            if not all([SUPABASE_HOST, SUPABASE_USER, SUPABASE_PASSWORD]):
                raise psycopg2.OperationalError(
                    'SUPABASE_URL appears to be a project URL (https://...).\n'
                    'Set `DATABASE_URL` (postgres://...) or provide SUPABASE_HOST, SUPABASE_USER, and SUPABASE_PASSWORD in your .env'
                )

        # Use individual parameters
        conn = psycopg2.connect(
            host=SUPABASE_HOST,
            port=SUPABASE_PORT,
            database=SUPABASE_DB,
            user=SUPABASE_USER,
            password=SUPABASE_PASSWORD
        )
        return conn
    except psycopg2.Error as e:
        print(f"Database connection error: {e}")
        raise

def dict_factory(cursor, row):
    """Convert database row to dictionary"""
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class Row:
    """Mimic sqlite3.Row behavior for PostgreSQL"""
    def __init__(self, cursor, data):
        self.cursor = cursor
        self.data = data
        self._keys = [col[0] for col in cursor.description] if cursor.description else []
    
    def __getitem__(self, key):
        if isinstance(key, int):
            return self.data[key]
        if isinstance(self.data, dict):
            return self.data[key]
        return self.data[self._keys.index(key)]
    
    def __setitem__(self, key, value):
        if isinstance(key, int):
            self.data[key] = value
        else:
            if isinstance(self.data, dict):
                self.data[key] = value
            else:
                self.data[self._keys.index(key)] = value
    
    def __iter__(self):
        return iter(self.data)
    
    def keys(self):
        return self._keys

class Connection:
    """Wrapper around psycopg2 connection to provide sqlite3-like interface"""
    def __init__(self, pg_conn):
        self.conn = pg_conn
        self.cursor = None
    
    def execute(self, query, params=None):
        """Execute a query and return self for method chaining"""
        try:
            self.cursor = self.conn.cursor(cursor_factory=RealDictCursor)
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
        except psycopg2.Error as e:
            print(f"Database execution error: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            raise
        return self
    
    def fetchone(self):
        """Fetch one row as dictionary"""
        if self.cursor:
            return self.cursor.fetchone()
        return None
    
    def fetchall(self):
        """Fetch all rows as list of dictionaries"""
        if self.cursor:
            return self.cursor.fetchall()
        return []
    
    def commit(self):
        """Commit the transaction"""
        try:
            self.conn.commit()
        except psycopg2.Error as e:
            print(f"Database commit error: {e}")
            self.conn.rollback()
            raise
    
    def close(self):
        """Close the connection"""
        try:
            if self.cursor:
                self.cursor.close()
            self.conn.close()
        except psycopg2.Error as e:
            print(f"Error closing connection: {e}")
    
    @property
    def row_factory(self):
        """Placeholder for sqlite3 compatibility"""
        return None
    
    @row_factory.setter
    def row_factory(self, value):
        """Placeholder for sqlite3 compatibility"""
        pass

def get_db_connection_wrapper():
    """Get a connection wrapper that mimics sqlite3 interface"""
    pg_conn = get_db_connection()
    return Connection(pg_conn)

# Initialize database schema if needed
def init_db():
    """Initialize database schema"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    try:
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id SERIAL PRIMARY KEY,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                is_admin BOOLEAN DEFAULT FALSE,
                active BOOLEAN DEFAULT TRUE,
                m18 BOOLEAN DEFAULT FALSE,
                eshop BOOLEAN DEFAULT FALSE,
                jetplus BOOLEAN DEFAULT FALSE,
                sugarcrm BOOLEAN DEFAULT FALSE,
                shopline BOOLEAN DEFAULT FALSE
            )
        ''')
        
        # Create bugs table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS bugs (
                id SERIAL PRIMARY KEY,
                report_date TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
                system TEXT NOT NULL,
                bug_details TEXT NOT NULL,
                reported_by TEXT NOT NULL,
                status TEXT DEFAULT '開放中',
                priority TEXT DEFAULT '中',
                severity TEXT DEFAULT '中',
                assigned_to TEXT,
                resolution_date TIMESTAMPTZ,
                notes TEXT,
                reported_by_user_id INTEGER REFERENCES users(id),
                file_path TEXT
            )
        ''')
        
        conn.commit()
        print("Database schema initialized successfully!")
    except Exception as e:
        print(f"Error initializing database: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    # Test connection
    try:
        conn = get_db_connection_wrapper()
        print("Successfully connected to Supabase PostgreSQL!")
        conn.close()
    except Exception as e:
        print(f"Connection failed: {e}")
