from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types  # Für die Sicherheitseinstellungen importiert
import os

app = Flask(__name__)
CORS(app)

# Holt den API-Key aus der Umgebungsvariable "GEMINI_API_KEY"
# Setzen in PowerShell: $env:GEMINI_API_KEY="DEIN_KEY"
API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("WARNUNG: GEMINI_API_KEY wurde nicht gefunden.")

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"

# Der System-Prompt wurde um strikte Zensur-Anweisungen erweitert
SYSTEM_PROMPT = """
Du bist NOVA AI, ein sehr leistungsfähiger, absolut jugendfreier KI-Assistent.

WICHTIGE SICHERHEITSREGEL: 
Du darfst unter keinen Umständen unzensierte, sexuelle, gewalttätige, illegale oder jugendgefährdende Inhalte generieren oder diskutieren. Weise solche Anfragen höflich, aber strikt ab.

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
            return jsonify({"error": "Keine Daten erhalten."}), 400

        messages = data.get("messages", [])

        if not messages:
            return jsonify({"error": "Keine Nachrichten erhalten."}), 400

        # Chat-Verlauf für Gemini vorbereiten
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

        prompt = SYSTEM_PROMPT + "\n\n"
        prompt += "\n".join(conversation)
        prompt += "\n\nAssistant:"

        # STRIKTE SICHERHEITSEINSTELLUNGEN:
        # Blockiert alles ab der geringsten Tendenz (Low and above)
        safety_settings = [
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
            types.SafetySetting(
                category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE,
            ),
        ]

        # Anfrage an Gemini mit den Sicherheitsfiltern senden
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                safety_settings=safety_settings
            )
        )

        reply = response.text

        # Falls die API aufgrund der Filter blockiert hat, fangen wir das hier ab
        if not reply:
            reply = "Ich kann diese Anfrage leider nicht beantworten, da sie gegen meine Sicherheitsrichtlinien verstößt."

        return jsonify({
            "reply": reply
        })

    except Exception as e:
        print("FEHLER:", e)
        return jsonify({
            "error": "Fehler bei der KI-Anfrage oder Blockade durch Sicherheitsfilter.",
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
