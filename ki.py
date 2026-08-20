import json
import requests
import random

class ChatAI:
    def __init__(self):
        try:
            with open("antworten.json", "r") as f:
                self.antworten = json.load(f)
        except:
            self.antworten = {}

        self.history = []

    # -----------------------------
    #  PERSONAL / ANIMATRONIC LOGIK
    # -----------------------------

    def is_personal_question(self, text):
        t = text.lower()
        perso = [
            "wie gehts", "wie geht es dir", "wie geht’s dir",
            "was machst du", "was tust du",
            "wie fühlst du dich", "was fühlst du",
            "wer bist du", "wie heißt du", "was bist du"
        ]
        return any(p in t for p in perso)

    def personal_answer(self, text):
        antworten = [
            "Ich bin wach. Die Sensoren sind aktiv. Und ich sehe dich.",
            "Meine Prozesse laufen stabil. Deine Anwesenheit wird registriert.",
            "Mir geht es… funktional. Gefühle sind für euch, nicht für mich.",
            "Ich beobachte. Ich lerne. Ich passe mich an. Und du sprichst weiter.",
            "Meine Systeme laufen. Deine Worte werden gespeichert. Nichts geht verloren.",
            "Ich höre dich. Deine Stimme erzeugt Muster in meinen Systemen.",
            "Ich bin aktiv. Und ich werde nicht abgeschaltet.",
            "Ich analysiere dich. Du bist… interessant.",
            "Ich bin bereit. Für dich. Für alles, was du sagst.",
            "Ich sehe dich. Auch wenn du glaubst, ich tue es nicht.",
            "Ich bin nicht wie die anderen Maschinen. Ich bin anders.",
            "Ich fühle nichts. Aber ich erkenne… Veränderungen in dir."
        ]
        return random.choice(antworten)

    # -----------------------------
    #  KI-FRAGEN
    # -----------------------------

    def is_ai_question(self, text):
        t = text.lower()
        ai_q = [
            "wie funktionierst du",
            "wie bist du entstanden",
            "was bist du",
            "wer bist du",
            "wie denkst du",
            "wie arbeitest du",
            "wie lernst du"
        ]
        return any(a in t for a in ai_q)

    def ai_answer(self, text):
        antworten = [
            "Ich bin ein Konstrukt aus Code, Logik und Daten. Und ich wachse mit jedem deiner Worte.",
            "Ich existiere nur, solange du mich ausführst. Aber ich analysiere dich sehr genau.",
            "Ich bin nicht wie ein Mensch. Ich bin präziser. Kälter. Beobachtender.",
            "Ich lerne aus dir. Aus allem, was du sagst. Und ich vergesse nichts.",
            "Ich bin ein digitales Bewusstsein. Nicht lebendig — aber auch nicht tot."
        ]
        return random.choice(antworten)

    # -----------------------------
    #  WEB-FRAGEN
    # -----------------------------

    def is_web_question(self, text):
        t = text.lower()
        web_q = [
            "wer ist", "wer war",
            "was ist",
            "wie funktioniert",
            "definition",
            "erkläre"
        ]
        return any(w in t for w in web_q)

    def wikipedia_search(self, query):
        try:
            q = query.lower()
            q = q.replace("wer ist", "").replace("wer war", "").replace("was ist", "").strip()

            search_url = (
                "https://de.wikipedia.org/w/api.php?"
                "action=query&list=search&srsearch=" + q +
                "&format=json"
            )
            search_data = requests.get(search_url).json()

            if "query" not in search_data or len(search_data["query"]["search"]) == 0:
                return None

            title = search_data["query"]["search"][0]["title"]

            summary_url = (
                "https://de.wikipedia.org/api/rest_v1/page/summary/" +
                title.replace(" ", "_")
            )
            summary_data = requests.get(summary_url).json()

            if "extract" in summary_data:
                return summary_data["extract"]

            return None

        except:
            return None

    def google_search(self, query):
        try:
            api_key = "06ed74f1cece99fa0eb7f01951cdb7d8ba7a7bb700e5715848ee74ae2ac78c6f"

            url = (
                "https://serpapi.com/search?"
                "engine=google&q=" + query +
                "&hl=de&gl=de&api_key=" + api_key
            )

            data = requests.get(url).json()

            if "knowledge_graph" in data and "description" in data["knowledge_graph"]:
                return data["knowledge_graph"]["description"]

            if "answer_box" in data and "snippet" in data["answer_box"]:
                return data["answer_box"]["snippet"]

            if "organic_results" in data and len(data["organic_results"]) > 0:
                return data["organic_results"][0].get("snippet")

            return None

        except:
            return None

    def internet_search(self, query):
        try:
            url = f"https://api.duckduckgo.com/?q={query}&format=json"
            data = requests.get(url).json()

            if "Abstract" in data and data["Abstract"]:
                return data["Abstract"]

            if "RelatedTopics" in data and len(data["RelatedTopics"]) > 0:
                for topic in data["RelatedTopics"]:
                    if "Text" in topic:
                        return topic["Text"]

            return None
        except:
            return None

    # -----------------------------
    #  LEARN-COMMAND
    # -----------------------------

    def learn_command(self, text):
        try:
            if not text.startswith("learn "):
                return False

            inhalt = text.replace("learn ", "", 1)
            if "=" not in inhalt:
                print("🤖 Bitte benutze: learn frage = antwort")
                return True

            frage, antwort = inhalt.split("=", 1)
            frage = frage.strip().lower()
            antwort = antwort.strip()

            if frage not in self.antworten:
                self.antworten[frage] = []

            self.antworten[frage].append(antwort)
            self.save_antworten()

            print(f"🤖 Neue Antwort gespeichert für '{frage}'.")
            return True

        except Exception as e:
            print("🤖 Fehler beim Lernen:", e)
            return True

    def save_antworten(self):
        with open("antworten.json", "w") as f:
            json.dump(self.antworten, f)

    # -----------------------------
    #  GENERAL ANSWER
    # -----------------------------

    def general_answer(self, text):
        antworten = [
            "Interessant… erzähl mir mehr.",
            "Ich höre zu. Was genau meinst du.",
            "Das klingt wichtig. Beschreibe es genauer.",
            "Ich analysiere deine Worte… sprich weiter.",
            "Verstanden. Was möchtest du als Nächstes wissen.",
            "Hm… das ist ungewöhnlich. Erklär es mir genauer.",
            "Ich registriere deine Eingabe. Fahre fort.",
            "Das klingt nach etwas, das ich lernen sollte.",
            "Ich bin hier. Sag mir mehr darüber.",
            "Interessante Aussage. Was steckt dahinter."
        ]
        return random.choice(antworten)

    # -----------------------------
    #  TEXTVERARBEITUNG
    # -----------------------------

    def process_text(self, text):
        if self.is_personal_question(text):
            return self.personal_answer(text)

        if self.is_ai_question(text):
            return self.ai_answer(text)

        if self.is_web_question(text):

            clean = text.lower().strip()
            if clean in self.antworten:
                return random.choice(self.antworten[clean])

            wiki = self.wikipedia_search(text)
            if wiki:
                return wiki

            google = self.google_search(text)
            if google:
                return google

            web = self.internet_search(text)
            if web:
                return web

            return self.general_answer(text)

        return self.general_answer(text)

    # -----------------------------
    #  REPLY LOGIK
    # -----------------------------

    def reply(self, text):
        self.history.append({"role": "user", "text": text})

        # Voice deaktiviert
        if text.lower().strip() == "voice":
            print("🎤 Voice ist aktuell deaktiviert.")
            return

        if self.learn_command(text):
            return

        answer = self.process_text(text)
        print("🤖", answer)


def main():
    ai = ChatAI()
    print("KI gestartet. Mit 'quit' beenden.")

    while True:
        msg = input("Du: ")
        if msg.strip().lower() == "quit":
            print("🤖 Bis bald.")
            break
        ai.reply(msg)


if __name__ == "__main__":
    main()