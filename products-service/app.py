from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB = "products.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price REAL NOT NULL,
        stock INTEGER NOT NULL
    )""")
    conn.commit()
    conn.close()

@app.route("/products", methods=["GET"])
def get_products():
    conn = sqlite3.connect(DB)
    products = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([{"id": p[0], "name": p[1], "price": p[2], "stock": p[3]} for p in products])

@app.route("/products/<int:pid>", methods=["GET"])
def get_product(pid):
    conn = sqlite3.connect(DB)
    p = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    conn.close()
    if p:
        return jsonify({"id": p[0], "name": p[1], "price": p[2], "stock": p[3]})
    return jsonify({"error": "Product not found"}), 404

@app.route("/products", methods=["POST"])
def create_product():
    data = request.json
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)",
                 (data["name"], data["price"], data["stock"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "Product created"}), 201

if __name__ == "__main__":
    init_db()
    import os
    port = int(os.environ.get("PORT", 5002))
    app.run(host="0.0.0.0", port=port)