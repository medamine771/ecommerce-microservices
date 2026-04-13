from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)
DB = "users.db"

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )""")
    conn.commit()
    conn.close()

@app.route("/users", methods=["GET"])
def get_users():
    conn = sqlite3.connect(DB)
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([{"id": u[0], "name": u[1], "email": u[2]} for u in users])

@app.route("/users/<int:uid>", methods=["GET"])
def get_user(uid):
    conn = sqlite3.connect(DB)
    u = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    if u:
        return jsonify({"id": u[0], "name": u[1], "email": u[2]})
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    conn = sqlite3.connect(DB)
    conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (data["name"], data["email"]))
    conn.commit()
    conn.close()
    return jsonify({"message": "User created"}), 201

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)