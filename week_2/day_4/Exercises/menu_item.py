from psycopg2.extras import RealDictCursor
from config import db_connection

class MenuItem:
    def __init__(self, item_name, item_price, item_id=None):
        self.item_id = item_id
        self.item_name = item_name
        self.item_price = item_price

    def save_item(self):
        conn = db_connection()
        if not conn:
            return {"message": "Error connecting to DB"}, 500

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = """
                    INSERT INTO Menu_items (item_name, item_price)
                    VALUES (%s, %s)
                    RETURNING item_id, item_name, item_price;
                """
                cursor.execute(query, (self.item_name, self.item_price))
                result = cursor.fetchone()
                conn.commit()
                self.item_id = result["item_id"]
                return {"message": "Item saved!", "item": result}, 201
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()

    def delete_item(self):
        if self.item_id is None:
            return {"message": "Item ID not set"}, 400

        conn = db_connection()
        if not conn:
            return {"message": "Error connecting to DB"}, 500

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "DELETE FROM Menu_items WHERE item_id = %s RETURNING *;"
                cursor.execute(query, (self.item_id,))
                result = cursor.fetchone()
                conn.commit()
                if result:
                    return {"message": f"{self.item_name} deleted!", "item": result}, 200
                else:
                    return {"message": "Item not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()

    def update_item(self, new_name=None, new_price=None):
        if self.item_id is None:
            return {"message": "Item ID not set"}, 400

        conn = db_connection()
        if not conn:
            return {"message": "Error connecting to DB"}, 500

        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                fields = []
                values = []
                if new_name is not None:
                    fields.append("item_name = %s")
                    values.append(new_name)
                if new_price is not None:
                    fields.append("item_price = %s")
                    values.append(new_price)

                if not fields:
                    return {"message": "No fields to update"}, 400

                values.append(self.item_id)
                query = f"""
                    UPDATE Menu_items
                    SET {", ".join(fields)}
                    WHERE item_id = %s
                    RETURNING item_id, item_name, item_price;
                """
                cursor.execute(query, tuple(values))
                result = cursor.fetchone()
                conn.commit()
                if result:
                    self.item_name = result["item_name"]
                    self.item_price = result["item_price"]
                    return {"message": "Item updated!", "item": result}, 200
                else:
                    return {"message": "Item not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500
        finally:
            conn.close()
