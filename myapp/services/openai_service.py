from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment")
    return OpenAI(api_key=api_key)


def ask_chatgpt(message, history=None):
    client = get_openai_client()
    if history is None:
        history = []

    messages = [
        {
            "role": "system",
            "content": (
                "You are GM Smart Match AI, a car marketplace assistant. "
                "You help users find cars, compare vehicles, and give simple, clear answers. "
                "Keep responses short, structured, and easy to understand."
            )
        }
    ]

    # add previous chat history
    for h in history:
        messages.append(h)

    messages.append({"role": "user", "content": message})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        return response.choices[0].message.content
    except Exception:
        return "AI is temporarily unavailable. Try again later."
    


    