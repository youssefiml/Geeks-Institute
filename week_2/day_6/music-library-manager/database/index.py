import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
        'host': os.getenv('DB_HOST', 'localhost'),
        'database': os.getenv('DB_NAME', 'music_library'),
        'user': os.getenv('DB_USER', 'postgres'),
        'password': os.getenv('DB_PASSWORD', 'password'),
        'port': os.getenv('DB_PORT', '5432')
    }

print("DB_CONFIG:", DB_CONFIG)

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def init_database():
    """Initialize database with schema and seed data"""
    try:
        # Read the SQL file
        sql_file_path = os.path.join('database', 'seed', 'index.sql')
        if not os.path.exists(sql_file_path):
            print(f"SQL file not found at: {sql_file_path}")
            print("Make sure you have created the database/seed/index.sql file")
            return False
            
        with open(sql_file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        conn = get_db_connection()
        conn.autocommit = True  # Important for CREATE/DROP statements
        cur = conn.cursor()
        
        # Split SQL content by semicolon and execute each statement
        statements = sql_content.split(';')
        for statement in statements:
            statement = statement.strip()
            if statement:  # Skip empty statements
                try:
                    cur.execute(statement)
                    print(f"✅ Executed: {statement[:50]}...")
                except psycopg2.Error as e:
                    print(f"❌ Error executing statement: {e}")
                    print(f"Statement was: {statement[:100]}...")
        
        cur.close()
        conn.close()
        
        print("\n🎉 Database initialized successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        return False

def test_connection():
    """Test database connection"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        print(f"✅ Connected to: {version[0]}")
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        return False

def verify_tables():
    """Verify that all tables were created"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Check if tables exist
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        
        tables = cur.fetchall()
        expected_tables = ['organizers', 'attendees', 'events', 'tickets']
        
        print("\n📋 Tables in database:")
        existing_tables = []
        for table in tables:
            table_name = table[0]
            existing_tables.append(table_name)
            print(f"  ✅ {table_name}")
        
        # Check for missing tables
        missing_tables = [t for t in expected_tables if t not in existing_tables]
        if missing_tables:
            print(f"\n❌ Missing tables: {missing_tables}")
            return False
        
        # Count records in each table
        print("\n📊 Record counts:")
        for table in expected_tables:
            cur.execute(f"SELECT COUNT(*) FROM {table}")
            count = cur.fetchone()[0]
            print(f"  {table}: {count} records")
        
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verifying tables: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Testing database connection...")
    if test_connection():
        print("✅ Connection successful!")
        
        print("\n🏗️  Initializing database...")
        if init_database():
            print("\n🔍 Verifying tables...")
            verify_tables()
        else:
            print("❌ Database initialization failed!")
    else:
        print("❌ Please check your database configuration in the .env file.")
        print("\nMake sure:")
        print("1. PostgreSQL is running")
        print("2. Database 'event_management' exists")
        print("3. Your .env file has correct credentials")