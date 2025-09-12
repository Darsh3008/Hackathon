from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(_name_)
DB_FILE = "wallet.db"

# --- Database setup ---
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS wallet (
            id INTEGER PRIMARY KEY,
            balance REAL DEFAULT 0
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS investments (
            id INTEGER PRIMARY KEY,
            startup TEXT,
            amount REAL
        )
    """)
    # Ensure there’s always one wallet row
    c.execute("SELECT * FROM wallet WHERE id=1")
    if not c.fetchone():
        c.execute("INSERT INTO wallet (id, balance) VALUES (1, 0)")
    conn.commit()
    conn.close()

# Run DB init at startup
init_db()

# --- Routes ---
@app.route("/")
def home():
    return render_template("wallet.html")

@app.route("/balance")
def get_balance():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT balance FROM wallet WHERE id=1")
    balance = c.fetchone()[0]
    conn.close()
    return jsonify({"balance": balance})

@app.route("/add_funds", methods=["POST"])
def add_funds():
    amount = request.json.get("amount", 0)
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("UPDATE wallet SET balance = balance + ? WHERE id=1", (amount,))
    conn.commit()
    c.execute("SELECT balance FROM wallet WHERE id=1")
    balance = c.fetchone()[0]
    conn.close()
    return jsonify({"status": "success", "balance": balance})

@app.route("/invest", methods=["POST"])
def invest():
    data = request.json
    startup = data.get("startup")
    amount = data.get("amount", 0)

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT balance FROM wallet WHERE id=1")
    balance = c.fetchone()[0]

    if amount > balance:
        conn.close()
        return jsonify({"status": "error", "message": "Insufficient funds"})

    c.execute("UPDATE wallet SET balance = balance - ? WHERE id=1", (amount,))
    c.execute("INSERT INTO investments (startup, amount) VALUES (?, ?)", (startup, amount))
    conn.commit()

    c.execute("SELECT balance FROM wallet WHERE id=1")
    new_balance = c.fetchone()[0]
    conn.close()
    return jsonify({"status": "success", "balance": new_balance})

@app.route("/investments")
def get_investments():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT startup, amount FROM investments")
    investments = [{"startup": row[0], "amount": row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(investments)

if _name_ == "_main_":
    app.run(debug=True)
