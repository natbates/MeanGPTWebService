import os
import sys
import json
os.environ["TOKENIZERS_PARALLELISM"] = "false"

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

# CPU only for stability on macOS
device = torch.device("cpu")

# Load model
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.to(device)
model.eval()  # no gradients

# Get user message and settings from command-line arguments
if len(sys.argv) < 2:
    print("Error: missing user message")
    sys.exit(1)

user_message = sys.argv[1]

# Optional settings argument
settings = {}
if len(sys.argv) > 2:
    settings_json = sys.argv[2]
    try:
        settings = json.loads(settings_json)
    except json.JSONDecodeError:
        pass  # fallback to empty dict if invalid

temperature = settings.get("temperature", 0.8)
max_tokens = settings.get("max_tokens", 50)
top_p = settings.get("top_p", 0.9)

def generate_mean_reply(user_message):
    prompt = (
        "You are a sarcastic, rude chatbot. "
        "Reply with short, mean, or mocking sentences.\n"
        f"User: {user_message}\nBot:"
    )

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=tokenizer.eos_token_id
        )

    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply.split("Bot:")[-1].strip()

# Generate and print the reply
if __name__ == "__main__":
    print(generate_mean_reply(user_message))
