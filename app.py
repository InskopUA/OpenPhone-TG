from flask import Flask, request
import requests
import os
import re

app = Flask(__name__)

# Получаем переменные окружения и очищаем номер
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
ALLOWED_PHONE = re.sub(r'\D', '', os.environ.get("ALLOWED_PHONE") or '')

@app.route('/')
def index():
    return '✅ Webhook сервис работает.'

@app.route('/webhook', methods=['POST'])
def webhook():
    print("🔥 Webhook triggered")

    try:
        data = request.get_json(force=True)
    except Exception as e:
        print(f"❌ Ошибка чтения JSON: {e}")
        return 'Bad JSON', 200

    print("📦 FULL JSON:", data)

    try:
        message_data = data['data']['object']
        sender = message_data.get('from')
        message = message_data.get('body')
    except Exception as e:
        print(f"❌ Ошибка разбора JSON: {e}")
        return 'Invalid payload', 200

    if not sender or not message:
        print("⚠️ Нет номера отправителя или текста")
        return 'Missing data', 200

    normalized_sender = re.sub(r'\D', '', sender)
    print(f"🔍 Сравнение номеров: {normalized_sender} vs {ALLOWED_PHONE}")
    print(f"💬 Текст сообщения: {message}")

    if normalized_sender == ALLOWED_PHONE:
        print("✅ Совпадение! Отправляем в Telegram...")
        send_to_telegram(f"📩 SMS от {sender}:\n{message}")
    else:
        print("⛔️ Номер не совпал. Не отправляем в Telegram.")

    return 'OK', 200

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': text
    }
    try:
        response = requests.post(url, json=payload)
        print(f"📤 Telegram status: {response.status_code}")
        print(f"📤 Telegram response: {response.text}")
    except Exception as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")

if __name__ == '__main__':
    app.run()
