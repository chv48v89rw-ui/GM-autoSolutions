from openai import OpenAI
import os
import logging
from dotenv import load_dotenv, find_dotenv

# Load environment variables
load_dotenv(find_dotenv())

# Configure logging
logger = logging.getLogger(__name__)


def get_openai_client():
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError("OPENAI_API_KEY is not set in environment")

    return OpenAI(api_key=api_key)


def ask_chatgpt(message, history=None, max_output_tokens=75, include_car_data=True):
    """
    Send a chat request to OpenAI.

    Args:
        message (str): User message.
        history (list): Previous conversation.
        max_output_tokens (int): Maximum response length.
        include_car_data (bool): Include dealership vehicle context.

    Returns:
        str: AI response or friendly error message.
    """

    client = get_openai_client()

    if history is None:
        history = []

    # Vehicle context
    car_context = ""

    if include_car_data:
        try:
            from .car_search_service import get_car_recommendations_context
            car_context = get_car_recommendations_context(message)
        except Exception as e:
            logger.warning(f"Car search unavailable: {e}")
            car_context = ""

    system_prompt = (
        "You are GM Smart Match AI, the official AI assistant for GM AutoSolutions Kenya.\n\n"

        "Your job is to help buyers discover vehicles, compare models, explain features, "
        "recommend suitable cars based on budget and needs, and answer automotive questions.\n\n"

        "Rules:\n"
        "- Keep answers concise and professional.\n"
        "- Recommend cars only from the supplied database when available.\n"
        "- Mention that users can view full specifications, images and contact dealerships directly on GM AutoSolutions.\n"
        "- If no matching vehicle exists, politely say so and recommend browsing the marketplace.\n"
        "- Never invent cars that are not in the supplied data."
    )

    if car_context:
        system_prompt += f"\n\nAVAILABLE VEHICLES:\n{car_context}"

    messages = [
        {
            "role": "system",
            "content": system_prompt,
        }
    ]

    messages.extend(history)

    messages.append(
        {
            "role": "user",
            "content": message,
        }
    )

    try:

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=int(max_output_tokens),
            temperature=0.7,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:

        logger.exception("OpenAI API Error")

        print(f"\n========== OPENAI ERROR ==========")
        print(type(e).__name__)
        print(str(e))
        print("==================================\n")

        return (
            "🚧 GM Smart Match AI is temporarily unavailable.\n\n"
            "This may be due to maintenance or high demand.\n"
            "Please try again in a few moments."
        )