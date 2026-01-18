from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

KEYS_FILE = "keys.json"

def load_keys():
    if not os.path.exists(KEYS_FILE):
        return {"valid": {}, "used": {}}
    with open(KEYS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_keys(data):
    with open(KEYS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return "Ultimate Optimization Key Server — ONLINE"

@app.route("/add_key", methods=["POST"])
def add_key():
    data = request.json
    key = data.get("key")

    if not key:
        return jsonify({"error": "no key"}), 400

    db = load_keys()

    if key in db["valid"] or key in db["used"]:
        return jsonify({"status": "already"})

    plan = "ULT1" if key.startswith("ULT1") else \
           "ULT2" if key.startswith("ULT2") else \
           "ULT3" if key.startswith("ULT3") else "UNKNOWN"

    db["valid"][key] = plan
    save_keys(db)

    return jsonify({"status": "added", "plan": plan})

@app.route("/validate", methods=["POST"])
def validate():
    data = request.json
    key = data.get("key")

    db = load_keys()

    if key in db["used"]:
        return jsonify({"status": "used"})

    if key not in db["valid"]:
        return jsonify({"status": "invalid"})

    plan = db["valid"].pop(key)
    db["used"][key] = plan
    save_keys(db)

    return jsonify({"status": "ok", "plan": plan})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
