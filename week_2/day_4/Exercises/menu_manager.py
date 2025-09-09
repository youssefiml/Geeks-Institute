from psycopg2.extras import RealDictCursor
from config import db_connection
from menu_item import MenuItem

class MenuManager:

    @classmethod
    def get_by_name(cls, name):
        conn = db_connection()
        if not conn:
            return None
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM Menu_items WHERE item_name = %s;"
                cursor.execute(query, (name,))
                result = cursor.fetchone()
                if result:
                    return MenuItem(result["item_name"], result["item_price"], result["item_id"])
                return None
        except Exception as e:
            print("Error in get_by_name:", e)
            return None
        finally:
            conn.close()

    @classmethod
    def all_items(cls):
        conn = db_connection()
        if not conn:
            return []
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM Menu_items;"
                cursor.execute(query)
                results = cursor.fetchall()
                return [MenuItem(item["item_name"], item["item_price"], item["item_id"]) for item in results]
        except Exception as e:
            print("Error in all_items:", e)
            return []
        finally:
            conn.close()
