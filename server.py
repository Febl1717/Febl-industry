from flask import Flask, request, jsonify
from flask_cors import CORS
# Importiert die unzensierte Funktion aus deiner ki.py
from ki import generate_response 

app = Flask(__name__)
CORS(app)

@app.get("/")
def home():
    return jsonify({
        "status": "online",
        "name": "febl ki",
        "message": "febl ki läuft unzensiert über server.py!"
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

        # Holt die Antwort direkt aus der ki.py
        reply = generate_response(messages)

        return jsonify({"reply": reply})

    except Exception as e:
        print("Fehler in server.py:", e)
        return jsonify({"error": "Server-Fehler.", "details": str(e)}), 500

if __name__ == "__main__":
    # Wichtig für den 1GB Server: host="0.0.0.0" macht ihn im Internet erreichbar
    app.run(host="0.0.0.0", port=3000, debug=False)
