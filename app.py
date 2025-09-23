from flask import Flask, request, jsonify
from bot import get_bot_response

app = Flask(__name__)


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    user_message = data["message"]
    bot_reply = get_bot_response(user_message)
    return jsonify({"response": bot_reply})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)