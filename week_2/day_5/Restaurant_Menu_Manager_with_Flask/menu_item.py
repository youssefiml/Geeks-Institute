import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="restaurant",
        user="postgres",
        password="12345678",
        host="localhost",
        port="5432"
    )

class MenuItem:
    def __init__(self, item_id=None, name=None, price=None):
        self.item_id = item_id
        self.name = name
        self.price = price

    def save(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO Menu_Items (item_name, item_price) VALUES (%s, %s) RETURNING item_id;",
            (self.name, self.price)
        )
        self.item_id = cur.fetchone()[0]  # store generated id
        conn.commit()
        cur.close()
        conn.close()

    def delete(self):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Menu_Items WHERE item_id = %s;", (self.item_id,))
        conn.commit()
        cur.close()
        conn.close()

    def update(self, new_name=None, new_price=None):
        conn = get_connection()
        cur = conn.cursor()
        if new_name:
            self.name = new_name
        if new_price is not None:
            self.price = new_price
        cur.execute(
            "UPDATE Menu_Items SET item_name = %s, item_price = %s WHERE item_id = %s;",
            (self.name, self.price, self.item_id)
        )
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_all():
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT item_id, item_name, item_price FROM Menu_Items ORDER BY item_id;")
        items = cur.fetchall()
        cur.close()
        conn.close()
        return [MenuItem(item_id=row[0], name=row[1], price=row[2]) for row in items]

    @staticmethod
    def get_by_id(item_id):
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT item_id, item_name, item_price FROM Menu_Items WHERE item_id = %s;", (item_id,))
        row = cur.fetchone()
        cur.close()
        conn.close()
        return MenuItem(item_id=row[0], name=row[1], price=row[2]) if row else None
