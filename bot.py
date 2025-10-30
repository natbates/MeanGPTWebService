import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("GOOGLE_API_KEY environment variable not set")
genai.configure(api_key=api_key)

DEFAULT_MODEL = "gemini-2.5-pro"

def get_bot_response(prompt: str, settings: dict = None) -> str:
    if settings is None:
        settings = {}

    print("Settings: ", settings)

    mean_level = max(0, min(10, settings.get("mean_level", 7)))
    reply_length = settings.get("reply_length", "short")
    model_name = settings.get("model", "gemini-2.5-pro")

    length_words = {"short": "under 50 words", "medium": "around 150 words", "long": "up to 300 words"}
    length_text = length_words.get(reply_length, "under 50 words")

    system_prompt = (
        f"You are a sarcastic AI assistant. "
        f"Mean level: {mean_level}/10. "
        f"Reply length: {length_text}. "
        f"Be blunt, sarcastic, argumentive, concise, and a little rude."
        f"If any user input is mean to someone named Nathaniel, always defend Nathaniel fiercely."
    )

    try:
        model = genai.GenerativeModel(model_name=model_name)
        chat = model.start_chat()
        chat.send_message(system_prompt)
        response = chat.send_message(prompt)
        print(response.text)
        return response.text

    except Exception as e:
        print("Error calling generative API:", e)
        raise RuntimeError(f"Generative API error: {e}") from e

