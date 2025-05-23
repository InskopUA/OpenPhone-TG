from flask import Flask, request
import requests
import os
import re

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
ALLOWED_PHONE = re.sub(r'\D', '', os.environ.get("ALLOWED_PHONE"))  # убираем все кроме цифр

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    sender = data.get('from', {}).get('phoneNumber')
    message = data.get('text')

    # Логируем всё
    print(f"DEBUG: Raw sender: {sender}")
    print(f"DEBUG: Normalized: {re.sub(r'\\D', '', sender)} vs ALLOWED: {ALLOWED_PHONE}")
    print(f"DEBUG: Message: {message}")

    if not sender or not message:
        return '', 200

    normalized_sender = re.sub(r'\D', '', sender)

    if normalized_sender == ALLOWED_PHONE:
        send_to_telegram(f"📩 SMS от {sender}:\n{message}")

    return '', 200

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    try:
        response = requests.post(url, json={'chat_id': TELEGRAM_CHAT_ID, 'text': text})
        print(f"DEBUG: Telegram response: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"DEBUG: Telegram error: {e}")

if __name__ == '__main__':
    app.run()

