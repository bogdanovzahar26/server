# server/app.py
from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

KEYS_FILE = "keys.json"
USED_FILE = "used_keys.json"

def load(path):
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except Exception:
            return []

def save(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

@app.route("/")
def home():
    return "Ultimate Optimization Key Server — ONLINE"

@app.route("/add_key", methods=["POST"])
def add_key():
    data = request.json or {}
    key = (data.get("key") or "").strip()
    if not key:
        return jsonify({"status":"error","reason":"empty_key"}), 400

    keys = load(KEYS_FILE)
    if key in keys:
        # already present
        return jsonify({"status":"already"}), 200

    keys.append(key)
    save(KEYS_FILE, keys)
    return jsonify({"status":"added"}), 200

@app.route("/validate", methods=["POST"])
def validate():
    data = request.json or {}
    key = (data.get("key") or "").strip()
    if not key:
        return jsonify({"status":"invalid","reason":"empty_key"}), 400

    keys = load(KEYS_FILE)
    used = load(USED_FILE)

    if key in used:
        return jsonify({"status":"used"}), 200

    if key not in keys:
        return jsonify({"status":"invalid"}), 200

    # determine plan by prefix
    up = key.upper()
    if up.startswith("ULT1-"):
        plan = "ULT1"
    elif up.startswith("ULT2-"):
        plan = "ULT2"
    elif up.startswith("ULT3-"):
        plan = "ULT3"
    else:
        return jsonify({"status":"invalid"}), 200

    # mark used
    used.append(key)
    save(USED_FILE, used)
    return jsonify({"status":"ok","plan":plan}), 200

if __name__ == "__main__":
    # local debug
    app.run(host="0.0.0.0", port=5000, debug=True)
