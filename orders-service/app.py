from flask import Flask, jsonify, request
import sqlite3, requests

app = Flask(__name__)
DB = "orders.db"
USERS_URL = "ecommerce-microservices-production.up.railway.app"
PRODUCTS_URL = "clever-appreciation-production-a91f.up.railway.app"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,
        quantity INTEGER NOT NULL
    )""")
    conn.commit()
    conn.close()

@app.route("/orders", methods=["GET"])
def get_orders():
    conn = sqlite3.connect(DB)
    orders = conn.execute("SELECT * FROM orders").fetchall()
    conn.close()
    return jsonify([{"id": o[0], "user_id": o[1], "product_id": o[2], "quantity": o[3]} for o in orders])

@app.route("/orders", methods=["POST"])
def create_order():
    data = request.json
    # Vérification que l'utilisateur existe
    user_resp = requests.get(f"{USERS_URL}/users/{data['user_id']}")
    if user_resp.status_code != 200:
        return jsonify({"error": "User not found"}), 404
    # Vérification que le produit existe
    prod_resp = requests.get(f"{PRODUCTS_URL}/products/{data['product_id']}")
    if prod_resp.status_code != 200:
        return jsonify({"error": "Product not found"}), 404

    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO orders (user_id, product_id, quantity) VALUES (?, ?, ?)",
                 (data["user_id"], data["product_id"], data["quantity"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Order created"}), 201

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5003)