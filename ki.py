from flask import Flask, request, jsonify
from flask_cors import CORS
from google import genai
from google.genai import types
import os

app = Flask(__name__)
CORS(app)

# Dein API-Key direkt hinterlegt
API_KEY = "AQ.Ab8RN6KrA9g4dAGHoEar_AjzlAeafEW7kMbZbk3OvohFTmP6qA"

client = genai.Client(api_key=API_KEY)

# HIER IST DIE WICHTIGE ÄNDERUNG: gemini-3.8-flash
MODEL = "gemini-3.8-flash"

SYSTEM_PROMPT = """
Du bist febl ki, ein sehr leistungsfähiger, absolut jugendfreier KI-Assistent.

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
        "name": "febl ki",
        "message": "febl ki läuft!"
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

        prompt = SYSTEM_PROMPT + "\n\n" + "\n".join(conversation) + "\n\nAssistant:"

        safety_settings = [
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HATE_SPEECH, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_HARASSMENT, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
            types.SafetySetting(category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT, threshold=types.HarmBlockThreshold.BLOCK_LOW_AND_ABOVE),
        ]

        # HIER WIRD DIE NEUE API GENUTZT
        interaction = client.interactions.create(
            model=MODEL,
            input=prompt,
            config=types.GenerateContentConfig(safety_settings=safety_settings)
        )

        reply = interaction.output_text

        if not reply:
            reply = "Ich kann diese Anfrage leider nicht beantworten, da sie gegen meine Sicherheitsrichtlinien verstößt."

        return jsonify({"reply": reply})

    except Exception as e:
        print("FEHLER:", e)
        return jsonify({"error": "Fehler bei der KI-Anfrage.", "details": str(e)}), 500

if __name__ == "__main__":
    # Geändert auf 0.0.0.0, damit der Server über das Internet erreichbar ist
    app.run(host="0.0.0.0", port=3000, debug=False)
