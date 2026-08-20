import express from "express";
import fetch from "node-fetch";
import cors from "cors";

const app = express();
app.use(cors());
app.use(express.json());

const GROQ_API_KEY = "DEIN_GROQ_KEY_HIER";

app.post("/api/groq", async (req, res) => {
    const userMessage = req.body.message;

    const response = await fetch("https://api.groq.com/openai/v1/chat/completions", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "Authorization": `Bearer ${GROQ_API_KEY}`
        },
        body: JSON.stringify({
            model: "llama-3.1-70b-versatile",
            messages: [
                { role: "system", content: "Du bist eine hilfreiche KI für Felix." },
                { role: "user", content: userMessage }
            ]
        })
    });

    const data = await response.json();
    res.json(data);
});

app.listen(3000, () => console.log("Groq Proxy läuft auf http://localhost:3000"));
