# backend/app.py
import os
import json
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime
import re

# ---------- CONFIG ----------
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyA0GNNmHqHQL2nh1o4UDieseWqmBjlsYeU")  # set env var or replace string
USE_GEMINI = GEMINI_KEY != "YOUR_GEMINI_API_KEY"
INTERVENTION_THRESHOLD = -0.35
# ----------------------------

app = Flask(__name__)
CORS(app)

if USE_GEMINI:
    genai.configure(api_key=GEMINI_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

DB = "conversations.db"

# --------- DB helpers ----------
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            message TEXT,
            mood_label TEXT,
            mood_score REAL,
            created_at TEXT
        )
    ''')
    conn.commit()
    conn.close()

def save_chat(sender, message, mood_label=None, mood_score=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('INSERT INTO chats (sender,message,mood_label,mood_score,created_at) VALUES (?,?,?,?,?)',
              (sender, message, mood_label, mood_score, datetime.utcnow().isoformat()))
    conn.commit()
    conn.close()

init_db()

# ---------- Lightweight fallback sentiment ----------
positive_words = {"good","great","happy","well","fine","awesome","love","enjoy","relaxed","calm","productive"}
negative_words = {"sad","anxious","anxiety","stress","stressed","bad","upset","hate","depressed","angry","worried","suicidal"}

def fallback_analyze(text):
    tokens = re.findall(r"\w+", text.lower())
    pos = sum(1 for t in tokens if t in positive_words)
    neg = sum(1 for t in tokens if t in negative_words)
    score = (pos - neg) / max(1, len(tokens))
    if score > 0.1:
        label = "positive"
    elif score < -0.1:
        label = "negative"
    else:
        label = "neutral"
    return {"label": label, "score": round(score, 3)}

# ---------- Gemini API call ----------
def call_gemini_for_mood_and_reply(user_message):
    prompt = f"""
You are an empathetic mental wellness assistant. Analyze the user's short message and:
1) Detect mood label (one of: very_negative, negative, neutral, positive, very_positive).
2) Provide a numeric sentiment score between -1 and +1.
3) Decide whether an immediate friendly intervention is recommended (true/false).
4) Provide one short intervention_text.
5) Provide a short empathetic reply to the user (1-2 sentences).

Return ONLY valid JSON with keys: "mood", "score", "intervention_recommended", "intervention_text", "reply".

User message: \"\"\"{user_message}\"\"\"
"""
    response = model.generate_content(prompt)
    txt = response.text.strip()
    try:
        json_str = txt[txt.find("{"): txt.rfind("}")+1]
        return json.loads(json_str)
    except Exception:
        return {"mood": "neutral", "score": 0.0, "intervention_recommended": False,
                "intervention_text": "", "reply": txt}

# ---------- Chat endpoint ----------
@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error":"no message"}), 400

    if USE_GEMINI:
        try:
            gem_res = call_gemini_for_mood_and_reply(user_message)
            mood = gem_res.get("mood")
            score = gem_res.get("score")
            intervention = bool(gem_res.get("intervention_recommended", False))
            intervention_text = gem_res.get("intervention_text", "")
            reply = gem_res.get("reply", "Thanks for sharing.")
        except Exception:
            fb = fallback_analyze(user_message)
            mood = fb["label"]
            score = fb["score"]
            intervention = score < INTERVENTION_THRESHOLD
            intervention_text = "Try a 2-min breathing exercise: inhale 4s, hold 4s, exhale 6s."
            reply = "Thanks for sharing — I'm here to listen."
    else:
        fb = fallback_analyze(user_message)
        mood = fb["label"]
        score = fb["score"]
        intervention = score < INTERVENTION_THRESHOLD
        intervention_text = "Try a 2-min breathing exercise: inhale 4s, hold 4s, exhale 6s."
        if mood == "negative":
            reply = "I’m sorry you’re feeling this way. Would you like a short breathing exercise or a grounding activity?"
        else:
            reply = "Thanks for sharing. Want a short tip to reset attention?"

    save_chat("user", user_message, mood, score)
    save_chat("bot", reply, mood, score)

    return jsonify({
        "reply": reply,
        "mood": mood,
        "score": score,
        "intervention": intervention,
        "intervention_text": intervention_text
    })

# ---------- Summary endpoint ----------
@app.route("/api/summary", methods=["GET"])
def summary():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    # ✅ Use correct column name
    c.execute("SELECT mood_label, mood_score, message, sender, created_at FROM chats ORDER BY id DESC LIMIT 100")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return jsonify({"summary": "No conversations yet.", "dominant_mood":"neutral", "entries": []})

    counts = {}
    scores = []
    entries = []

    for mood_label, score, message, sender, created_at in rows:
        if mood_label:
            counts[mood_label] = counts.get(mood_label, 0) + 1
        if score is not None:
            scores.append(score)
        entries.append({"sender": sender, "message": message, "mood": mood_label, "score": score, "when": created_at})

    dominant_mood = max(counts.items(), key=lambda x: x[1])[0] if counts else "neutral"
    avg_score = round(sum(scores)/len(scores), 3) if scores else 0.0
    human = f"Dominant mood in recent chat: {dominant_mood}. Average sentiment score: {avg_score}."

    return jsonify({"summary": human, "dominant_mood": dominant_mood, "avg_score": avg_score, "entries": entries})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
