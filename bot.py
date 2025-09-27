from cleaner import clean_corpus
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer

CORPUS_FILE = "chat.txt"

# Create ChatBot instance
chatbot = ChatBot("Chatpot")

# Train the bot
trainer = ListTrainer(chatbot)
cleaned_corpus = clean_corpus(CORPUS_FILE)
trainer.train(cleaned_corpus)

def get_bot_response(message: str, settings: dict = None) -> str:
    """
    Return the chatbot response for a given message.
    Settings can control logic adapters or similarity threshold.
    """
    if not settings:
        settings = {}

    # Example: override default maximum similarity
    max_sim = settings.get("max_similarity", 0.9)
    chatbot.logic_adapters[0].maximum_similarity_threshold = max_sim

    return str(chatbot.get_response(message))