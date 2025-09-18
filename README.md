

````markdown
# MindCare – AI-powered Mental Wellness Chatbot

MindCare is a **Python + React-based AI chatbot** designed to help users monitor and improve their mental wellbeing. Using AI/NLP (Gemini API or fallback sentiment analysis), it **detects users' moods, provides personalized interventions, and offers guidance to promote healthier digital habits**.

---

## **Project Overview**

MindCare focuses on creating a **safe and interactive environment** for users to:

- **Identify emotional state** in real-time using conversational AI.
- **Provide instant interventions** (like breathing exercises or motivational prompts) when negative moods are detected.
- **Maintain a chat history** to analyze overall mood when the conversation ends.
- **Give personalized feedback** and suggestions to improve mood and mental health.

The frontend is a **modern React UI** with a scrollable chat box, **dark/light mode toggle**, and responsive design. The backend is powered by **Flask**, handling AI interactions, sentiment analysis, and chat storage.

---

## **Key Features**

1. **Real-time mood detection**
   - Gemini API (Google’s AI) or fallback sentiment analysis.
   - Detects moods: very negative, negative, neutral, positive, very positive.

2. **Instant interventions**
   - Friendly pop-ups and suggestions when the user is sad or stressed.

3. **End chat summary**
   - Analyzes the overall conversation.
   - Shows dominant mood and average sentiment score.
   - Provides a personalized goodbye message.

4. **Interactive UI**
   - Chat messages scroll automatically.
   - Input can be sent with Enter key.
   - Modern chat bubbles for user and bot.
   - Fixed-width container (80–90% of screen), responsive height.
   - Dark/light mode toggle for user preference.

5. **Privacy & security**
   - Local database (`SQLite`) for chat storage.
   - API keys (Gemini) stored in `.env` files, not pushed to GitHub.

---

## **Tech Stack**

| Layer | Technology |
|-------|------------|
| Frontend | React.js, CSS3 |
| Backend | Python, Flask |
| AI/NLP | Gemini API (Google) or fallback sentiment analysis |
| Database | SQLite |
| Tools | Git, Node.js, npm |

---

## **Setup Instructions**

### **Backend**

1. Navigate to `backend` folder:

```bash
cd backend
````

2. Create virtual environment:

```bash
python -m venv venv
```

3. Activate virtual environment:

* Windows:

```bash
venv\Scripts\activate
```


4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set your Gemini API key (optional, for AI mood detection):

```bash
set GEMINI_API_KEY="YOUR_GEMINI_KEY"     # Windows
```

6. Run backend server:

```bash
python app.py
```

Server runs on: `http://localhost:5000`

---

### **Frontend**

1. Navigate to `frontend` folder:

```bash
cd frontend
```

2. Install Node.js dependencies:

```bash
npm install
```

3. Start React app:

```bash
npm start
```

Frontend runs on: `http://localhost:3000`

> Ensure backend is running before starting frontend for full functionality.

---

## **How to Use**

1. Open the frontend in your browser.
2. Type messages in the chat box.
3. **Instant interventions** pop up if negative emotions are detected.
4. Chat normally with the bot; it responds empathetically.
5. Click **“End Chat”** to see **overall mood summary** and a personalized goodbye.

---

## **Folder Structure**

```
mindcare-chatbot/
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│   ├── .gitignore
│   └── (SQLite DB will be created automatically)
│
├── frontend/
│   ├── package.json
│   ├── src/
│   │   ├── App.js
│   │   ├── App.css
│   │   └── ...
│   ├── public/
│   │   └── index.html
│   └── .gitignore
│
└── README.md
```

---



