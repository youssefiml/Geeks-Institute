from flask import Flask, render_template, request, redirect, url_for
import psycopg2

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(
        dbname="restaurant",
        user="postgres",
        password="12345678",
        host="localhost",
        port="5432"
    )

@app.route("/")
def menu():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT item_id, item_name, item_price FROM Menu_Items ORDER BY item_id;")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("menu.html", items=items)

@app.route("/add", methods=["POST"])
def add_item():
    if request.method == "POST":
        name = request.form["name"]
        price = request.form["price"]

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Menu_Items (item_name, item_price) VALUES (%s, %s);", (name, price))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for("menu"))

    return render_template("add_item.html")

@app.route("/update/<int:item_id>", methods=["POST"])
def update_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        new_name = request.form["name"]
        new_price = request.form["price"]
        cursor.execute("UPDATE Menu_Items SET item_name=%s, item_price=%s WHERE item_id=%s;",
                    (new_name, new_price, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for("menu"))

    cursor.execute("SELECT item_name, item_price FROM Menu_Items WHERE item_id=%s;", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("update_item.html", item=item, item_id=item_id)

@app.route("/delete/<int:item_id>", methods = ["DELETE"])
def delete_item(item_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Menu_Items WHERE item_id=%s;", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for("menu"))

if __name__ == "__main__":
    app.run(debug=True)
