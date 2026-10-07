import time
from google import genai
from google.genai import types

API_KEY = "AQ.Ab8RN6Ixdp4_PbIKdQcEc2HzoMV7qkGJhgg-Xy7Qi8C6RIdOfQ"

client = genai.Client(api_key=API_KEY)

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro"
]

SYSTEM_PROMPT = """
Du bist febl ki, ein leistungsfähiger KI-Assistent.

Antworte hilfreich, präzise und verständlich.
Passe deine Sprache an die Sprache des Benutzers an.
Verwende Markdown, wenn es die Antwort übersichtlicher macht.
"""

def generate_response(messages):
    try:

        conversation = []

        # Weniger Verlauf = schneller + weniger Fehler
        for message in messages[-10:]:

   
