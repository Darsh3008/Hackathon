from flask import Flask, render_template, jsonify

app = Flask(_name_)

# Fake database in memory
pitches = [
    {"id": 1, "title": "Smart Campus App", "description": "An app that helps students navigate campus, find events, and connect with peers.", "votes": 0},
    {"id": 2, "title": "Eco-Friendly Packaging", "description": "Innovative packaging solutions using biodegradable and recycled materials.", "votes": 0},
]

@app.route("/")
def home():
    # Serve your existing HTML (no edits needed inside)
    return render_template("voting.html")

@app.route("/vote/<int:pitch_id>", methods=["POST"])
def vote(pitch_id):
    for pitch in pitches:
        if pitch["id"] == pitch_id:
            pitch["votes"] += 1
            return jsonify({"status": "success", "votes": pitch["votes"]})
    return jsonify({"status": "error", "message": "Pitch not found"}), 404

if _name_ == "_main_":
    app.run(debug=True)
