import time
from google import genai
from google.genai import types

# ==========================
# API KEY
# ==========================

API_KEY = "AQ.Ab8RN6Ixdp4_PbIKdQcEc2HzoMV7qkGJhgg-Xy7Qi8C6RIdOfQ"

client = genai.Client(api_key=AQ.Ab8RN6Ixdp4_PbIKdQcEc2HzoMV7qkGJhgg-Xy7Qi8C6RIdOfQ)

# ==========================
# MODELLE
# ==========================

MODELS = [
    "gemini-2.5-flash",
    "gemini-2.5-pro"
]

# ==========================
# SYSTEM PROMPT
# ==========================

SYSTEM_PROMPT = """
Du bist Febl KI, ein hilfreicher und intelligenter KI-Assistent.

Regeln:
- Antworte immer in der Sprache des Nutzers.
- antworte schnell und nicht zu langsam
- Nutze Markdown wenn sinnvoll.
- Gib verständliche Antworten.
- Strukturiere längere Antworten übersichtlich.
- jede antwort hatt eine antwort 
"""

# ==========================
# KI FUNKTION
# ==========================

def generate_response(messages):

    try:

        conversation = []

        # Nur die letzten 10 
