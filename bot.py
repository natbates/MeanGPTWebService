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

def get_bot_response(message: str) -> str:
    """Return the chatbot response for a given message."""
    return str(chatbot.get_response(message))
