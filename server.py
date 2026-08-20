from flask import Flask, request, jsonify
from ki import ChatAI

app = Flask(__name__)
ai = ChatAI()

@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    frage = data.get("frage", "")
    antwort = ai.process_text(frage)
    return jsonify({"antwort": antwort})

@app.route("/")
def home():
    return "KI läuft! Sende POST /ask mit JSON {'frage': '...'}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
