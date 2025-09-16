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
    conn = get_db_connection()
    cur = conn.cursor()
    
    try:
        sql_file_path = 'database/seed/index.sql'
        
        encodings_to_try = ['utf-8', 'latin1', 'cp1252', 'iso-8859-1']
        
        sql_commands = None
        for encoding in encodings_to_try:
            try:
                with open(sql_file_path, 'r', encoding=encoding) as f:
                    sql_commands = f.read()
                print(f"Successfully read SQL file with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if sql_commands is None:
            print("Could not read SQL file, creating tables programmatically...")
            create_tables_programmatically(cur)
        else:
            cur.execute(sql_commands)
        
        conn.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        conn.rollback()
        print(f"Error initializing database: {e}")
        try:
            print("Attempting programmatic table creation...")
            create_tables_programmatically(cur)
            conn.commit()
            print("Database initialized successfully using programmatic creation!")
        except Exception as e2:
            print(f"Programmatic creation also failed: {e2}")
            raise e
    finally:
        cur.close()
        conn.close()

def create_tables_programmatically(cur):
    """Create tables and insert data programmatically (fallback method)"""
    
    cur.execute("DROP TABLE IF EXISTS album_artists CASCADE;")
    cur.execute("DROP TABLE IF EXISTS albums CASCADE;")
    cur.execute("DROP TABLE IF EXISTS artists CASCADE;")
    
    cur.execute("""
        CREATE TABLE artists (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL UNIQUE,
            country VARCHAR(100) NOT NULL,
            formed_year INTEGER CHECK (formed_year >= 1900 AND formed_year <= 2024),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    cur.execute("""
        CREATE TABLE albums (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            release_year INTEGER NOT NULL CHECK (release_year >= 1900 AND release_year <= 2024),
            genre VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    
    cur.execute("""
        CREATE TABLE album_artists (
            id SERIAL PRIMARY KEY,
            album_id INTEGER REFERENCES albums(id) ON DELETE CASCADE,
            artist_id INTEGER REFERENCES artists(id) ON DELETE CASCADE,
            UNIQUE(album_id, artist_id)
        );
    """)
    
    cur.execute("CREATE INDEX idx_albums_title ON albums(title);")
    cur.execute("CREATE INDEX idx_albums_genre ON albums(genre);")
    cur.execute("CREATE INDEX idx_albums_year ON albums(release_year);")
    cur.execute("CREATE INDEX idx_artists_name ON artists(name);")
    cur.execute("CREATE INDEX idx_album_artists_album ON album_artists(album_id);")
    cur.execute("CREATE INDEX idx_album_artists_artist ON album_artists(artist_id);")
    
    artists_data = [
        ('The Beatles', 'United Kingdom', 1960),
        ('Pink Floyd', 'United Kingdom', 1965),
        ('Led Zeppelin', 'United Kingdom', 1968),
        ('Queen', 'United Kingdom', 1970),
        ('The Rolling Stones', 'United Kingdom', 1962),
        ('Bob Dylan', 'United States', 1961),
        ('David Bowie', 'United Kingdom', 1962),
        ('Radiohead', 'United Kingdom', 1985),
        ('Nirvana', 'United States', 1987),
        ('The Doors', 'United States', 1965),
        ('Jimi Hendrix', 'United States', 1966),
        ('AC/DC', 'Australia', 1973),
        ('Black Sabbath', 'United Kingdom', 1968),
        ('Deep Purple', 'United Kingdom', 1968),
        ('The Who', 'United Kingdom', 1964)
    ]
    
    for artist in artists_data:
        cur.execute(
            "INSERT INTO artists (name, country, formed_year) VALUES (%s, %s, %s)",
            artist
        )
    
    albums_data = [
        ('Abbey Road', 1969, 'Rock'),
        ('The Dark Side of the Moon', 1973, 'Progressive Rock'),
        ('Led Zeppelin IV', 1971, 'Hard Rock'),
        ('Bohemian Rhapsody', 1975, 'Rock'),
        ('Sticky Fingers', 1971, 'Rock'),
        ('Highway 61 Revisited', 1965, 'Folk Rock'),
        ('The Rise and Fall of Ziggy Stardust', 1972, 'Glam Rock'),
        ('OK Computer', 1997, 'Alternative Rock'),
        ('Nevermind', 1991, 'Grunge'),
        ('The Doors', 1967, 'Psychedelic Rock'),
        ('Are You Experienced', 1967, 'Psychedelic Rock'),
        ('Back in Black', 1980, 'Hard Rock'),
        ('Paranoid', 1970, 'Heavy Metal'),
        ('Machine Head', 1972, 'Hard Rock'),
        ('Who\'s Next', 1971, 'Rock'),
        ('Sgt. Pepper\'s Lonely Hearts Club Band', 1967, 'Psychedelic Rock'),
        ('Wish You Were Here', 1975, 'Progressive Rock'),
        ('Physical Graffiti', 1975, 'Hard Rock'),
        ('A Night at the Opera', 1975, 'Rock'),
        ('Let It Bleed', 1969, 'Rock')
    ]
    
    for album in albums_data:
        cur.execute(
            "INSERT INTO albums (title, release_year, genre) VALUES (%s, %s, %s)",
            album
        )
    
    relationships = [
        (1, 1), (16, 1), (2, 2), (17, 2), (3, 3), (18, 3), (4, 4), (19, 4),
        (5, 5), (20, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11),
        (12, 12), (13, 13), (14, 14), (15, 15)
    ]
    
    for album_id, artist_id in relationships:
        cur.execute(
            "INSERT INTO album_artists (album_id, artist_id) VALUES (%s, %s)",
            (album_id, artist_id)
        )

if __name__ == '__main__':
    init_database()