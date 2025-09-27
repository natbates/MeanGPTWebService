from flask import Flask, request, jsonify
import subprocess
import json

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400

    user_message = data["message"]
    settings = data.get("settings", {})  # fetch settings, default to empty dict

    try:
        # Serialize settings as JSON string to pass to generate.py
        settings_str = json.dumps(settings)

        # Call generate.py and capture output
        result = subprocess.run(
            ["python3", "generate.py", user_message, settings_str],
            capture_output=True,
            text=True,
            check=True
        )
        reply = result.stdout.strip()
        return jsonify({"reply": reply})
    except subprocess.CalledProcessError as e:
        return jsonify({"error": e.stderr}), 500

if __name__ == "__main__":
    app.run(debug=False)
