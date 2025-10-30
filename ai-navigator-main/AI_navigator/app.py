import os
from flask import Flask, render_template, request, jsonify, session
from openai import OpenAI
from markupsafe import escape

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY")

if not OPENAI_KEY:
    raise RuntimeError("OPENAI_API_KEY не задан.")
if not SECRET_KEY:
    SECRET_KEY = "dev-secret"
    print("⚠️ Warning: SECRET_KEY не задан — используется dev-secret.")

client = OpenAI(api_key=OPENAI_KEY)
app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = SECRET_KEY

MAX_MESSAGE_LENGTH = 2000
MAX_HISTORY_MESSAGES = 10
SYSTEM_PROMPT = (
    "Ты AI-навигатор по образованию и карьере. "
    "Отвечай чётко и по существу, используй списки и примеры."
)

def get_history():
    return session.get("chat_history", [])

def save_history(history):
    session["chat_history"] = history[-MAX_HISTORY_MESSAGES:]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/policy")
def policy():
    return render_template("policy.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True)
    if not data or "message" not in data:
        return jsonify({"error": "Неверный запрос"}), 400

    user_message = escape(data["message"].strip())
    if not user_message:
        return jsonify({"error": "Пустое сообщение"}), 400
    if len(user_message) > MAX_MESSAGE_LENGTH:
        user_message = user_message[:MAX_MESSAGE_LENGTH]

    history = get_history()
    history.append({"role": "user", "content": user_message})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history[-MAX_HISTORY_MESSAGES:]

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
        )
        bot_reply = response.choices[0].message.content
    except Exception as e:
        print("OpenAI error:", e)
        return jsonify({"error": "Ошибка связи с AI"}), 502

    history.append({"role": "assistant", "content": bot_reply})
    save_history(history)
    return jsonify({"reply": bot_reply})

@app.route("/clear", methods=["POST"])
def clear():
    session.pop("chat_history", None)
    return jsonify({"ok": True})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
