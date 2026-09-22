from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
import os

app = Flask(__name__)
CORS(app)

# Deinen Gemini API-Key als Umgebungsvariable setzen:
# Windows PowerShell:
# $env:GEMINI_API_KEY="DEIN_KEY"

API_KEY = os.getenv("AQ.Ab8RN6Jvd-e66MRhvNqxyZrrLsUw3uPBVqS5bbqTh7DZ6b1MuQ")

if not API_KEY:
    print("WARNUNG: GEMINI_API_KEY wurde nicht gefunden.")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"

SYSTEM_PROMPT = """
Du bist NOVA AI, ein sehr leistungsfähiger KI-Assistent.

Antworte hilfreich, präzise und verständlich.
Passe deine Sprache an die Sprache des Benutzers an.
Wenn der Benutzer nach Code fragt, liefere funktionierenden Code.
Wenn du etwas nicht sicher weißt, erfinde keine Fakten.
Verwende Markdown, wenn es die Antwort übersichtlicher macht.
"""


@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "name": "NOVA AI",
        "message": "NOVA AI läuft!"
    })


@app.get("/health")
def health():
    return jsonify({
        "status": "ok",
        "api_configured": bool(API_KEY)
    })


@app.post("/api/chat")
def chat():

    try:
        data = request.get_json()

        if not data:
            return jsonify({
                "error": "Keine Daten erhalten."
            }), 400

        messages = data.get("messages", [])

        if not messages:
            return jsonify({
                "error": "Keine Nachrichten erhalten."
            }), 400

        # Chat-Verlauf für Gemini vorbereiten
        conversation = []

        for message in messages[-30:]:

            role = message.get("role")
            content = message.get("content")

            if not content:
                continue

            if role == "user":
                conversation.append(
                    f"User: {content}"
                )

            elif role == "assistant":
                conversation.append(
                    f"Assistant: {content}"
                )

        prompt = SYSTEM_PROMPT + "\n\n"

        prompt += "\n".join(conversation)

        prompt += "\n\nAssistant:"

        # Anfrage an Gemini
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        reply = response.text

        return jsonify({
            "reply": reply
        })

    except Exception as e:

        print("FEHLER:", e)

        return jsonify({
            "error": "Fehler bei der KI-Anfrage.",
            "details": str(e)
        }), 500


if __name__ == "__main__":

    print("")
    print("=" * 50)
    print("             NOVA AI")
    print("=" * 50)
    print("Server läuft auf:")
    print("http://localhost:3000")
    print("")
    print("Chat API:")
    print("http://localhost:3000/api/chat")
    print("")

    if API_KEY:
        print("Gemini API Key: OK")
    else:
        print("Gemini API Key: FEHLT!")

    print("=" * 50)
    print("")

    app.run(
        host="127.0.0.1",
        port=3000,
        debug=False
    )
