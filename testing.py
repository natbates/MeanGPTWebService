import requests

BASE_URL = "http://127.0.0.1:8000"

print("Console chat test. Type 'exit' to quit.")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    try:
        response = requests.post(
            f"{BASE_URL}/chat",
            json={"message": user_input, "settings": {"max_similarity": 0.8}}
        )
        if response.ok:
            data = response.json()
            print("Bot:", data.get("response"))
        else:
            print("Error:", response.text)
    except Exception as e:
        print("Failed to connect to server:", e)
