from flask import Flask, render_template, jsonify, request
import sqlite3
import re

app = Flask(__name__)


@app.route("/")
def home():
    connection = sqlite3.connect("pixelvault.db")
    connection.row_factory = sqlite3.Row

    products = connection.execute(
        "SELECT * FROM products"
    ).fetchall()

    connection.close()

    return render_template("index.html", products=products)


@app.route("/api/products/<int:product_id>")
def get_product(product_id):
    connection = sqlite3.connect("pixelvault.db")
    connection.row_factory = sqlite3.Row

    product = connection.execute(
        "SELECT * FROM products WHERE id = ?",
        (product_id,)
    ).fetchone()

    connection.close()

    if product is None:
        return jsonify({"error": "Product not found"}), 404

    return jsonify({
        "id": product["id"],
        "title": product["title"],
        "desc": product["description"],
        "cost": product["cost_price"],
        "sell": product["sell_price"],
        "image": product["image"]
    })

@app.route("/api/checkout", methods=["POST"])
def checkout():
    data = request.get_json()

    email = data.get("email", "").strip()
    phone = data.get("phone", "").strip()
    suburb = data.get("suburb", "").strip()
    cart = data.get("cart", [])

    email_pattern = r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
    phone_pattern = r"^04\d{8}$"

    if not re.match(email_pattern, email):
        return jsonify({"error": "Invalid email address"}), 400

    if not re.match(phone_pattern, phone):
        return jsonify({"error": "Invalid phone number"}), 400

    if not suburb:
        return jsonify({"error": "Suburb is required"}), 400

    if not cart:
        return jsonify({"error": "Cart is empty"}), 400

    connection = sqlite3.connect("pixelvault.db")
    connection.row_factory = sqlite3.Row
    cursor = connection.cursor()

    try:
        total_cost = 0
        total_sale = 0

        verified_items = []

        for item in cart:
            product = cursor.execute(
                "SELECT * FROM products WHERE id = ?",
                (item["id"],)
            ).fetchone()

            if product is None:
                return jsonify({"error": "Product not found"}), 404

            quantity = int(item["qty"])

            if quantity < 1:
                return jsonify({"error": "Invalid quantity"}), 400

            item_cost = product["cost_price"] * quantity
            item_sale = product["sell_price"] * quantity

            total_cost += item_cost
            total_sale += item_sale

            verified_items.append({
                "product": product,
                "quantity": quantity
            })

        profit = total_sale - total_cost

        import random
        order_number = f"ORD-{random.randint(100000, 999999)}"

        cursor.execute("""
            INSERT INTO orders
            (order_number, email, phone, suburb, total_cost, total_sale, profit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            order_number,
            email,
            phone,
            suburb,
            total_cost,
            total_sale,
            profit
        ))

        order_id = cursor.lastrowid

        for item in verified_items:
            product = item["product"]
            quantity = item["quantity"]

            cursor.execute("""
                INSERT INTO order_items
                (order_id, product_id, product_title, quantity, cost_price, sell_price)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                order_id,
                product["id"],
                product["title"],
                quantity,
                product["cost_price"],
                product["sell_price"]
            ))

        connection.commit()

        return jsonify({
            "success": True,
            "order_number": order_number
        })

    except Exception:
        connection.rollback()
        return jsonify({"error": "Unable to complete sale"}), 500

    finally:
        connection.close()

@app.route("/api/admin/sales")
def admin_sales():
    connection = sqlite3.connect("pixelvault.db")
    connection.row_factory = sqlite3.Row

    orders = connection.execute("""
        SELECT *
        FROM orders
        ORDER BY created_at DESC
    """).fetchall()

    sales = []

    for order in orders:
        items = connection.execute("""
            SELECT *
            FROM order_items
            WHERE order_id = ?
        """, (order["id"],)).fetchall()

        sales.append({
            "orderId": order["order_number"],
            "email": order["email"],
            "phone": order["phone"],
            "suburb": order["suburb"],
            "totalCost": order["total_cost"],
            "totalSell": order["total_sale"],
            "profit": order["profit"],
            "items": [
                {
                    "title": item["product_title"],
                    "qty": item["quantity"]
                }
                for item in items
            ]
        })

    connection.close()

    return jsonify(sales)

if __name__ == "__main__":
    app.run(debug=True)