from psycopg2 import connect

def db_connection():
    try:
            conn = connect(
                host="localhost",
                database="Restaurant",
                user="postgres",
                password="Youssef2003@",
                port="5432",
            )
            return conn
    except Exception as e:
            print("DB connection error:", e)
            return None