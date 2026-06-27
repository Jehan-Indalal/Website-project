from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "chocolate_world_secret"

ADMIN_PASSWORD = "admin123"

DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "",
    "database": "chocolate_world"
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def login_required(role=None):
    if "role" not in session:
        return redirect(url_for("login"))
    if role and session["role"] != role:
        return redirect(url_for("home"))
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        if role == "user":
            session["role"] = "user"
            return redirect(url_for("home"))
        elif role == "admin":
            password = request.form.get("password", "")
            if password == ADMIN_PASSWORD:
                session["role"] = "admin"
                return redirect(url_for("admin"))
            else:
                return render_template("login.html", error="Wrong password. Try again.")
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
def home():
    guard = login_required()
    if guard:
        return guard
    return render_template("index.html")


@app.route("/menu")
def menu():
    guard = login_required()
    if guard:
        return guard
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()
    db.close()
    return render_template("menu.html", items=items)


@app.route("/order")
def order():
    guard = login_required()
    if guard:
        return guard
    return render_template("order.html")


@app.route("/payment")
def payment():
    guard = login_required()
    if guard:
        return guard
    return render_template("payment.html")


@app.route("/confirm_order", methods=["POST"])
def confirm_order():
    data = request.get_json()
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO orders (full_name, address, phone, payment_method, total) VALUES (%s, %s, %s, %s, %s)",
        (data["full_name"], data["address"], data["phone"], data["payment_method"], data["total"])
    )
    db.commit()
    db.close()
    return jsonify({"success": True})


@app.route("/admin")
def admin():
    guard = login_required(role="admin")
    if guard:
        return guard
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM menu_items")
    items = cursor.fetchall()
    cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
    orders = cursor.fetchall()
    db.close()
    return render_template("admin.html", items=items, orders=orders)


@app.route("/admin/add", methods=["POST"])
def add_item():
    guard = login_required(role="admin")
    if guard:
        return guard
    name = request.form["name"]
    description = request.form["description"]
    price = int(request.form["price"])
    image = request.form["image"]
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO menu_items (name, description, price, image) VALUES (%s, %s, %s, %s)",
        (name, description, price, image)
    )
    db.commit()
    db.close()
    return redirect(url_for("admin"))


@app.route("/admin/delete/<int:item_id>")
def delete_item(item_id):
    guard = login_required(role="admin")
    if guard:
        return guard
    db = get_db()
    cursor = db.cursor()
    cursor.execute("DELETE FROM menu_items WHERE id = %s", (item_id,))
    db.commit()
    db.close()
    return redirect(url_for("admin"))


if __name__ == "__main__":
    app.run(debug=True)
