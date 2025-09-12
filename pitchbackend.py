from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(_name_)

# Database setup (SQLite for simplicity)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pitches.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Pitch model (table)
class Pitch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)

# Create the table (only first time)
with app.app_context():
    db.create_all()

# Routes
@app.route('/')
def home():
    return render_template('upload.html')

@app.route('/submit_pitch', methods=['POST'])
def submit_pitch():
    data = request.get_json()
    title = data.get('pitchTitle')
    description = data.get('pitchDescription')

    if not title or not description:
        return jsonify({"status": "error", "message": "All fields required"}), 400

    new_pitch = Pitch(title=title, description=description)
    db.session.add(new_pitch)
    db.session.commit()

    return jsonify({"status": "success", "message": "Pitch submitted successfully!"})

@app.route('/pitches', methods=['GET'])
def get_pitches():
    pitches = Pitch.query.all()
    return jsonify([
        {"id": p.id, "title": p.title, "description": p.description}
        for p in pitches
    ])

if _name_ == "_main_":
    app.run(debug=True)
