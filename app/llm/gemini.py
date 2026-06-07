from google import genai

from app.config.settings import GEMINI_API_KEY


_client = None


def get_client():
    global _client

    if _client is None:
        _client = genai.Client(
            api_key=GEMINI_API_KEY
        )

    return _client


def generate_response(prompt: str) -> str:

    client = get_client()

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text