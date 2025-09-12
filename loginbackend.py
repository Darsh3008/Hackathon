from flask import Flask, request, jsonify, render_template, redirect, url_for
import sqlite3
import os

app = Flask(_name_)

DB_NAME = "users.db"

# Initialize database
def init_db():
    if not os.path.exists(DB_NAME):
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

init_db()

# Serve HTML
@app.route("/")
def index():
    return render_template("index.html")

# Signup route
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        conn.close()
        return jsonify({"error": "Username already taken"}), 400

    conn.close()
    return jsonify({"message": "Sign up successful!"})

# Login route
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return jsonify({"error": "User does not exist"}), 400
    if row[0] != password:
        return jsonify({"error": "Incorrect password"}), 400

    return jsonify({"message": "Login successful!"})

if _name_ == "_main_":
    app.run(debug=True, host="127.0.0.1", port=5000)
