from flask import Flask, jsonify, request
import sqlite3, os

app = Flask(__name__)
DB = "/tmp/users.db"

def get_conn():
    conn = sqlite3.connect(DB, timeout=10)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )""")
    conn.commit()
    conn.close()

init_db()

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_conn()
    users = conn.execute("SELECT * FROM users").fetchall()
    conn.close()
    return jsonify([{"id": u["id"], "name": u["name"], "email": u["email"]} for u in users])

@app.route("/users/<int:uid>", methods=["GET"])
def get_user(uid):
    conn = get_conn()
    u = conn.execute("SELECT * FROM users WHERE id=?", (uid,)).fetchone()
    conn.close()
    if u:
        return jsonify({"id": u["id"], "name": u["name"], "email": u["email"]})
    return jsonify({"error": "User not found"}), 404

@app.route("/users", methods=["POST"])
def create_user():
    data = request.json
    try:
        conn = get_conn()
        conn.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                     (data["name"], data["email"]))
        conn.commit()
        conn.close()
        return jsonify({"message": "User created"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Email déjà utilisé"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)