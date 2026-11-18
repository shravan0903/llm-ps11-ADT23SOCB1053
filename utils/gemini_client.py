import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")


def get_gemini_client():
    if not API_KEY:
        raise ValueError(
            "GEMINI_API_KEY is missing. Check your .env file."
        )

    return genai.Client(api_key=API_KEY)


def generate_response_stream(prompt):

    try:
        client = get_gemini_client()

        response_stream = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=1500,
                temperature=0.2
            )
        )

        finish_reason = None

        for chunk in response_stream:
            if chunk.text:
                yield chunk.text

            if chunk.candidates:
                finish_reason = chunk.candidates[0].finish_reason

        print("\nGemini finish reason:", finish_reason)

    except Exception as e:

        error_message = str(e)
        print("\nGemini API Error:", error_message)

        if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
            if "quota" in error_message.lower():
                yield (
                    "The chatbot has temporarily reached its "
                    "free API usage limit. Please try again later."
                )
            else:
                yield (
                    "Too many requests were made. "
                    "Please wait a little and try again."
                )

        elif "503" in error_message or "UNAVAILABLE" in error_message:
            yield (
                "Gemini is temporarily overloaded. "
                "Please try again after some time."
            )

        elif "403" in error_message or "PERMISSION_DENIED" in error_message:
            yield (
                "Gemini API access was denied. "
                "Please check your API key and permissions."
            )

        elif "400" in error_message or "INVALID_ARGUMENT" in error_message:
            yield (
                "The request could not be processed. "
                "Please check the chatbot configuration."
            )

        else:
            yield (
                "Sorry! Something went wrong while generating "
                "the answer. Please try again later."
            )
