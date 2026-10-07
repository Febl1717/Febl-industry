import requests

SYSTEM_PROMPT = """
Du bist Febl KI.

Regeln:

- Antworte immer in der Sprache des Benutzers.
- Sei freundlich und hilfreich.
- Antworte schnell und direkt.
- Nutze Markdown wenn sinnvoll.
- Strukturiere längere Antworten übersichtlich.
- Gib immer eine sinnvolle Antwort.
- Wenn etwas unbekannt ist, sage das ehrlich.
"""

def generate_response(messages):

    try:

        conversation = []

        for message in messages[-10:]:

            role = message.get("role", "")
            content = message.get("content", "")

            if not content:
                continue

            if role == "user":
                conversation.append(
                    f"Benutzer: {content}"
                )

            elif role == "assistant":
                conversation.append(
                    f"Febl KI: {content}"
                )

        prompt = (
            SYSTEM_PROMPT
            + "\n\n"
            + "\n".join(conversation)
            + "\n\nFebl KI:"
        )

        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": "qwen2.5:0.5b",
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.8,
                    "num_predict": 512
                }
            },
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        answer = data.get("response", "")

        if answer and answer.strip():
            return answer

        return "Ich konnte keine Antwort erzeugen."

    except requests.exceptions.ConnectionError:

        return (
            "⚠️ Ollama läuft nicht.\n\n"
            "Starte Ollama mit:\n"
            "ollama serve"
        )

    except requests.exceptions.Timeout:

        return (
            "⚠️ Die Antwort hat zu lange gedauert."
        )

    except Exception as e:

        print("KI Fehler:", e)

        return (
            "⚠️ Fehler bei der lokalen KI."
        )
