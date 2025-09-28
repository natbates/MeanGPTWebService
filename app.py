from flask import Flask, request, jsonify
from bot import get_bot_response
from flask_cors import CORS
import os
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000",
                   "https://meangpt.netlify.app",
                   "http://localhost:3000/chat",
                   "https://meangpt.netlify.app"])

@app.route("/ping", methods=["GET"])
def ping():
    return jsonify({"status": "ok", "message": "Service is online"}), 200

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400

        user_message = data["message"]
        settings = data.get("settings", {})

        print(f"[CHAT LOG] User message: {user_message}")
        print(f"[CHAT LOG] Settings: {settings}")

        bot_reply = get_bot_response(user_message, settings)
        return jsonify({"response": bot_reply})
    except Exception as e:
        print("Error in /chat route:", e)
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # default to 8000 locally
    app.run(host="0.0.0.0", port=port, debug=True)
