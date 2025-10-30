import os
from flask import Flask, request, jsonify, session
from flask_cors import CORS
from openai import OpenAI
from datetime import timedelta
import secrets

OPENAI_KEY = os.environ.get("OPENAI_API_KEY")
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))

client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

app = Flask(__name__, static_folder='static', static_url_path='')
app.secret_key = SECRET_KEY
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
CORS(app, supports_credentials=True, origins=["*"])

SYSTEM_PROMPT = """Ты AI-навигатор по образованию и карьере для школьников из Казахстана. Помогай выбирать профессию, вузы, планировать карьеру. Отвечай чётко, дружелюбно."""

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/health')
def health():
    return jsonify({"status": "ok", "api_configured": client is not None})

@app.route('/api/chat', methods=['POST'])
def chat():
    if not client:
        return jsonify({"error": "OpenAI API не настроен"}), 503
    data = request.get_json()
    if not data or "message" not in data:
        return jsonify({"error": "Неверный запрос"}), 400
    user_message = data["message"].strip()[:2000]
    if not user_message:
        return jsonify({"error": "Пустое сообщение"}), 400
    chat_id = str(data.get("chatId", "default"))
    if 'chat_history' not in session:
        session['chat_history'] = {}
        session.permanent = True
    if chat_id not in session['chat_history']:
        session['chat_history'][chat_id] = []
    chat_history = session['chat_history'][chat_id]
    chat_history.append({"role": "user", "content": user_message})
    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + chat_history[-20:]
    try:
        response = client.chat.completions.create(model="gpt-4o-mini", messages=messages, temperature=0.7, max_tokens=1500)
        bot_reply = response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {e}")
        return jsonify({"error": "Ошибка связи с AI"}), 502
    chat_history.append({"role": "assistant", "content": bot_reply})
    session['chat_history'][chat_id] = chat_history
    session.modified = True
    return jsonify({"reply": bot_reply})

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"🚀 AI Navigator запущен на http://localhost:{port}")
    app.run(host="0.0.0.0", port=port, debug=os.environ.get("FLASK_ENV") == "development")
