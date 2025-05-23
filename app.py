@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # 🔍 Показываем весь полученный JSON
    print("FULL JSON:")
    print(data)

    sender = data.get('from', {}).get('phoneNumber')
    message = data.get('text')

    print(f"DEBUG: Raw sender: {sender}")

    if not sender or not message:
        return '', 200

    normalized_sender = re.sub(r'\D', '', sender)
    print(f"DEBUG: Normalized: {normalized_sender} vs ALLOWED: {ALLOWED_PHONE}")
    print(f"DEBUG: Message: {message}")

    if normalized_sender == ALLOWED_PHONE:
        send_to_telegram(f"📩 SMS от {sender}:\n{message}")

    return '', 200

