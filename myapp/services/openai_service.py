from openai import OpenAI
import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment")
    return OpenAI(api_key=api_key)


def ask_chatgpt(message, history=None, max_output_tokens=75, include_car_data=True):
    """Send a chat request to the OpenAI client.

    - `message`: user message string
    - `history`: list of prior messages (dicts with role/content)
    - `max_output_tokens`: integer token cap for the response
    - `include_car_data`: whether to include database car recommendations
    Returns a string reply or an error message.
    """
    client = get_openai_client()
    if history is None:
        history = []

    # Get car recommendations from database if enabled
    car_context = ""
    if include_car_data:
        try:
            from .car_search_service import get_car_recommendations_context
            car_context = get_car_recommendations_context(message)
        except Exception:
            # If car search fails, continue without it
            car_context = ""

    system_prompt = (
        "You are GM Smart Match AI, a car marketplace assistant for GM AutoSolutions in Kenya. "
        "You help users find cars, compare vehicles, and give simple, clear answers. "
        "Keep responses short, structured, and easy to understand. "
        "When users ask for car recommendations, use the provided car data from the database. "
        "Always mention that users can view full details, images, and contact dealerships on the website. "
        "Be helpful but concise - users want quick answers."
    )

    if car_context:
        system_prompt += f"\n\nAVAILABLE CARS FROM DATABASE:\n{car_context}"

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    # add previous chat history
    for h in history:
        messages.append(h)

    messages.append({"role": "user", "content": message})

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            # new SDK may accept `max_output_tokens` as the response cap
            max_output_tokens=int(max_output_tokens)
        )

        # Safely get text
        return getattr(response.choices[0].message, 'content', '') or response.choices[0].message.content
    except Exception:
        return "AI is temporarily unavailable. Try again Tomorrow."
    


    