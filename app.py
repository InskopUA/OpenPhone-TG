from flask import Flask, request
import requests
import os
import re

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
ALLOWED_PHONE = re.sub(r'\D', '', os.environ.get("ALLOWED_PHONE"))

@app.route('/')
def index():
    return '✅ Webhook сервис работает.'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # Показываем весь JSON
    print("FULL JSON:")
    print(data)

    # Новый путь к номеру отправителя и сообщению
    try:
        message_data = data['data']['object']
        sender = message_data.get('from')
        message = message_data.get('body')
    except Exception as e:
        print(f"DEBUG: Parsing error: {e}")
        return 'Invalid payload', 200

    print(f"DEBUG: Raw sender: {sender}")

    if not sender or not message:
        return 'Missing data', 200

    normalized_sender = re.sub(r'\D', '', sender)
    print(f"DEBUG: Normalized: {normalized_sender} vs ALLOWED: {ALLOWED_PHONE}")
    print(f"DEBUG: Message: {message}")

    if normalized_sender == ALLOWED_PHONE:
        send_to_telegram(f"📩 SMS от {sender}:\n{message}")

    return 'OK', 200

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': text})
        print(f"DEBUG: Telegram response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"DEBUG: Telegram error: {e}")

if __name__ == '__main__':
    app.run()
