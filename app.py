from flask import Flask, request, jsonify
from flask_cors import CORS       # enable this if front end is on a different domain
from bot_logic import get_bot_response

app = Flask(__name__)
CORS(app)  # remove if front end and backend are served from same origin

@app.route("/chat", methods=["POST"])
def chat():
    """
    Receive a message from the front end and return the bot's response.
    """
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' in request"}), 400

    user_message = data["message"]
    bot_reply = get_bot_response(user_message)
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)  # default: http://127.0.0.1:5000
