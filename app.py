import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from openai import OpenAI

# Получаем API ключ из переменных окружения
OPENAI_KEY = os.environ.get("OPENAI_API_KEY")

# Инициализируем OpenAI клиент
client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None

# Создаем Flask приложение
app = Flask(__name__, static_folder='static', static_url_path='')

# Настройка CORS для production
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})

# Системный промпт для AI
SYSTEM_PROMPT = """Ты AI-навигатор по образованию и карьере для школьников из Казахстана. 
Твоя задача - помогать выбирать профессию, вузы, планировать карьеру и образовательный путь.
Отвечай чётко, дружелюбно и по-существу. Давай конкретные советы и рекомендации.
Поддерживай и мотивируй школьников в их выборе."""

@app.route('/')
def index():
    """Главная страница"""
    return app.send_static_file('index.html')

@app.route('/health')
def health():
    """Проверка состояния сервиса"""
    return jsonify({
        "status": "ok", 
        "api_configured": client is not None,
        "openai_key_present": bool(OPENAI_KEY)
    })

@app.route('/api/chat', methods=['POST', 'OPTIONS'])
def chat():
    """Основной endpoint для чата с AI"""
    
    # Обработка preflight запроса
    if request.method == 'OPTIONS':
        return '', 204
    
    # Проверка наличия OpenAI API
    if not client:
        print("❌ ERROR: OpenAI API не настроен!")
        return jsonify({
            "error": "OpenAI API не настроен. Добавьте OPENAI_API_KEY в Environment Variables на Render."
        }), 503
    
    try:
        # Получаем данные из запроса
        data = request.get_json()
        
        if not data or "message" not in data:
            return jsonify({"error": "Неверный запрос"}), 400
        
        # Извлекаем и валидируем сообщение
        user_message = data["message"].strip()
        
        if not user_message:
            return jsonify({"error": "Пустое сообщение"}), 400
        
        # Ограничиваем длину сообщения
        user_message = user_message[:2000]
        
        # Получаем историю чата из запроса
        chat_history = data.get("history", [])
        
        # Ограничиваем историю последними 15 сообщениями для экономии токенов
        if len(chat_history) > 15:
            chat_history = chat_history[-15:]
        
        # Формируем список сообщений для OpenAI API
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        
        # Добавляем историю переписки
        for msg in chat_history:
            if msg.get("role") in ["user", "assistant"] and msg.get("content"):
                messages.append({
                    "role": msg["role"],
                    "content": msg["content"]
                })
        
        # Добавляем текущее сообщение пользователя (если его еще нет в истории)
        if not chat_history or chat_history[-1].get("content") != user_message:
            messages.append({"role": "user", "content": user_message})
        
        print(f"📤 Отправка запроса в OpenAI (история: {len(messages)} сообщений)")
        
        # Отправляем запрос к OpenAI API
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=1500,
            timeout=30
        )
        
        # Извлекаем ответ
        bot_reply = response.choices[0].message.content
        
        print(f"📥 Получен ответ от OpenAI ({len(bot_reply)} символов)")
        print(f"📝 Первые 100 символов ответа: {bot_reply[:100]}")
        
        return jsonify({"reply": bot_reply}), 200
    
    except Exception as e:
        error_msg = str(e)
        print(f"❌ ОШИБКА: {error_msg}")
        
        # Определяем тип ошибки и возвращаем понятное сообщение
        if "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            return jsonify({"error": "Неверный API ключ OpenAI. Проверьте настройки."}), 401
        elif "timeout" in error_msg.lower():
            return jsonify({"error": "Превышено время ожидания ответа от OpenAI."}), 504
        elif "rate_limit" in error_msg.lower():
            return jsonify({"error": "Превышен лимит запросов. Попробуйте позже."}), 429
        else:
            return jsonify({"error": f"Ошибка связи с AI: {error_msg}"}), 502

@app.errorhandler(404)
def not_found(e):
    """Обработка 404 ошибок - возвращаем index.html для SPA"""
    return app.send_static_file('index.html')

@app.errorhandler(500)
def internal_error(e):
    """Обработка внутренних ошибок сервера"""
    print(f"❌ Внутренняя ошибка сервера: {e}")
    return jsonify({"error": "Внутренняя ошибка сервера"}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
    print("=" * 50)
    print(f"🚀 AI Navigator запущен на порту {port}")
    print(f"🔑 OpenAI API Key: {'✅ Настроен' if OPENAI_KEY else '❌ НЕ НАСТРОЕН'}")
    print("=" * 50)
    
    # Запускаем сервер
    app.run(
        host="0.0.0.0", 
        port=port, 
        debug=False  # В production всегда False
    )
