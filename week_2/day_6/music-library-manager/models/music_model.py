import psycopg2
from psycopg2.extras import RealDictCursor
from database.index import get_db_connection

class MusicModel:
    def __init__(self):
        pass

    def get_albums_paginated(self, page=1, per_page=6):
        offset = (page - 1) * per_page

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("SELECT COUNT(*) FROM albums")
            total = cur.fetchone()['count']

            query = """
            SELECT a.id, a.title, a.release_year, a.genre, a.created_at,
                   STRING_AGG(ar.name, ', ' ORDER BY ar.name) as artists
            FROM albums a
            LEFT JOIN album_artists aa ON a.id = aa.album_id
            LEFT JOIN artists ar ON aa.artist_id = ar.id
            GROUP BY a.id, a.title, a.release_year, a.genre, a.created_at
            ORDER BY a.created_at DESC
            LIMIT %s OFFSET %s
            """

            cur.execute(query, (per_page, offset))
            albums = cur.fetchall()

            return albums, total

        finally:
            cur.close()
            conn.close()

    def search_albums(self, search_term, page=1, per_page=6):
        offset = (page - 1) * per_page
        search_pattern = f'%{search_term}%'

        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            count_query = """
            SELECT COUNT(DISTINCT a.id) 
            FROM albums a
            LEFT JOIN album_artists aa ON a.id = aa.album_id
            LEFT JOIN artists ar ON aa.artist_id = ar.id
            WHERE LOWER(a.title) LIKE LOWER(%s) 
               OR LOWER(ar.name) LIKE LOWER(%s)
               OR LOWER(a.genre) LIKE LOWER(%s)
            """

            cur.execute(count_query, (search_pattern, search_pattern, search_pattern))
            total = cur.fetchone()['count']

            search_query = """
            SELECT DISTINCT a.id, a.title, a.release_year, a.genre, a.created_at,
                   STRING_AGG(ar.name, ', ' ORDER BY ar.name) as artists
            FROM albums a
            LEFT JOIN album_artists aa ON a.id = aa.album_id
            LEFT JOIN artists ar ON aa.artist_id = ar.id
            WHERE LOWER(a.title) LIKE LOWER(%s) 
               OR LOWER(ar.name) LIKE LOWER(%s)
               OR LOWER(a.genre) LIKE LOWER(%s)
            GROUP BY a.id, a.title, a.release_year, a.genre, a.created_at
            ORDER BY a.created_at DESC
            LIMIT %s OFFSET %s
            """

            cur.execute(search_query, (search_pattern, search_pattern, search_pattern, per_page, offset))
            albums = cur.fetchall()

            return albums, total

        finally:
            cur.close()
            conn.close()

    def get_album_by_id(self, album_id):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            query = """
            SELECT a.id, a.title, a.release_year, a.genre, a.created_at,
                   ARRAY_AGG(ar.name ORDER BY ar.name) as artists,
                   ARRAY_AGG(ar.id ORDER BY ar.name) as artist_ids
            FROM albums a
            LEFT JOIN album_artists aa ON a.id = aa.album_id
            LEFT JOIN artists ar ON aa.artist_id = ar.id
            WHERE a.id = %s
            GROUP BY a.id, a.title, a.release_year, a.genre, a.created_at
            """

            cur.execute(query, (album_id,))
            album = cur.fetchone()

            return dict(album) if album else None

        finally:
            cur.close()
            conn.close()

    def create_album(self, title, release_year, genre, artist_ids):
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO albums (title, release_year, genre) VALUES (%s, %s, %s) RETURNING id",
                (title, release_year, genre)
            )
            album_id = cur.fetchone()[0]

            for artist_id in artist_ids:
                cur.execute(
                    "INSERT INTO album_artists (album_id, artist_id) VALUES (%s, %s)",
                    (album_id, artist_id)
                )

            conn.commit()
            return album_id

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def update_album(self, album_id, title, release_year, genre, artist_ids):
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "UPDATE albums SET title = %s, release_year = %s, genre = %s WHERE id = %s",
                (title, release_year, genre, album_id)
            )

            cur.execute("DELETE FROM album_artists WHERE album_id = %s", (album_id,))

            for artist_id in artist_ids:
                cur.execute(
                    "INSERT INTO album_artists (album_id, artist_id) VALUES (%s, %s)",
                    (album_id, artist_id)
                )

            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def delete_album(self, album_id):
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute("DELETE FROM albums WHERE id = %s", (album_id,))
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def get_all_artists(self):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("SELECT * FROM artists ORDER BY name")
            return cur.fetchall()

        finally:
            cur.close()
            conn.close()

    def create_artist(self, name, country, formed_year=None):
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            cur.execute(
                "INSERT INTO artists (name, country, formed_year) VALUES (%s, %s, %s)",
                (name, country, formed_year)
            )
            conn.commit()

        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cur.close()
            conn.close()

    def get_statistics(self):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            stats = {}

            cur.execute("SELECT COUNT(*) as count FROM albums")
            stats['total_albums'] = cur.fetchone()['count']

            cur.execute("SELECT COUNT(*) as count FROM artists")
            stats['total_artists'] = cur.fetchone()['count']

            cur.execute("SELECT COUNT(DISTINCT genre) as count FROM albums")
            stats['total_genres'] = cur.fetchone()['count']

            cur.execute("""
                SELECT ROUND(AVG(album_count), 2) as avg_albums
                FROM (
                    SELECT COUNT(*) as album_count
                    FROM album_artists
                    GROUP BY artist_id
                ) as artist_albums
            """)
            result = cur.fetchone()
            stats['avg_albums_per_artist'] = result['avg_albums'] if result['avg_albums'] else 0

            cur.execute("""
                SELECT title, release_year 
                FROM albums 
                ORDER BY created_at DESC 
                LIMIT 1
            """)
            recent = cur.fetchone()
            stats['most_recent_album'] = dict(recent) if recent else None

            cur.execute("""
                SELECT title, release_year 
                FROM albums 
                ORDER BY release_year ASC 
                LIMIT 1
            """)
            oldest = cur.fetchone()
            stats['oldest_album'] = dict(oldest) if oldest else None

            return stats

        finally:
            cur.close()
            conn.close()

    def get_genre_statistics(self):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("""
                SELECT genre, COUNT(*) as count
                FROM albums
                GROUP BY genre
                ORDER BY count DESC
            """)

            return [dict(row) for row in cur.fetchall()]

        finally:
            cur.close()
            conn.close()

    def get_year_statistics(self):
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cur.execute("""
                SELECT release_year, COUNT(*) as count
                FROM albums
                GROUP BY release_year
                ORDER BY release_year
            """)

            return [dict(row) for row in cur.fetchall()]

        finally:
            cur.close()
            conn.close()
