from flask import Flask, request, jsonify, send_from_directory
import requests
import os

app = Flask(__name__, static_folder='public')

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🛠️ GROUP RITE SOLUTIONS - CONFIGURATION
TELEGRAM_TOKEN = "8595813958:AAFpKSuq9j_qny2DlIgP2rJwHe1Mu_xTsDU"
CHAT_ID = "8187670531"
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/lead', methods=['POST'])
def handle_lead():
    try:
        name = request.form.get('name')
        phone = request.form.get('phone')
        address = request.form.get('address')
        service = request.form.get('service')
        is_subscription = request.form.get('is_subscription')
        details = request.form.get('details')

        # High-Impact Telegram Formatting
        priority_tag = "💳 SUBSCRIPTION" if is_subscription == 'true' else "🚨 EMERGENCY SERVICE"
        
        caption = (
            f"{priority_tag}: GROUP RITE\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"👤 Client: {name}\n"
            f"📞 Phone: {phone}\n"
            f"📍 Address: {address}\n"
            f"🛠 Service: {service}\n\n"
            f"📝 Notes: {details}\n"
            f"━━━━━━━━━━━━━━━━━━"
        )

        image = request.files.get('image')
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/"
        
        if image:
            requests.post(url + "sendPhoto", data={'chat_id': CHAT_ID, 'caption': caption}, files={'photo': (image.filename, image.read(), image.content_type)})
        else:
            requests.post(url + "sendMessage", data={'chat_id': CHAT_ID, 'text': caption})

        return jsonify({"success": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    app.run(host='0.0.0.0', port=port)