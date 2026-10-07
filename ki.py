import time
from google import genai
from google.genai import types

API_KEY = "AQ.Ab8RN6Ixdp4_PbIKdQcEc2HzoMV7qkGJhgg-Xy7Qi8C6RIdOfQ"

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """
Du bist febl ki, ein leistungsfähiger KI-Assistent.

Antworte hilfreich, präzise und verständlich.
Passe deine Sprache an die Sprache des Benutzers an.
Verwende Markdown, wenn es die Antwort übersichtlicher macht.
"""

def generate_response(messages):
    try:
        conversation = []

        for message in messages[-30:]:
            role = message.get("role")
            content = message.get("content")

            if not content:
                continue

            if role == "user":
                conversation.append(f"User: {content}")
            elif role == "assistant":
                conversation.append(f"Assistant: {content}")

        prompt = (
            SYSTEM_PROMPT +
            "\n\n" +
            "\n".join(conversation) +
            "\n\nAssistant:"
        )

        safety_settings = [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_NONE
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_NONE
            ),
        
