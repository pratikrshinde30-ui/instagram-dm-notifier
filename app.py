from flask import Flask, request, jsonify
from twilio.rest import Client
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("VERIFY_TOKEN")
TWILIO_SID = os.environ.get("TWILIO_SID")
TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN")
MY_WHATSAPP = os.environ.get("MY_WHATSAPP")

@app.route("/webhook", methods=["GET"])
def verify():
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")
    if mode == "subscribe" and token == VERIFY_TOKEN:
        return challenge, 200
    return "Forbidden", 403

@app.route("/webhook", methods=["POST"])
def receive_dm():
    data = request.get_json()
    try:
        messages = data["entry"][0]["changes"][0]["value"].get("messages", [])
        if messages:
            msg = messages[0]
            sender = msg.get("from", "Unknown")
            text = msg.get("text", {}).get("body", "[media message]")
            notify(f"New Instagram DM!\nFrom: {sender}\nMessage: {text}")
    except Exception as e:
        print(f"Error: {e}")
    return jsonify({"status": "ok"}), 200

def notify(message):
    client = Client(TWILIO_SID, TWILIO_TOKEN)
    client.messages.create(
        from_="whatsapp:+14155238886",
        to=f"whatsapp:{MY_WHATSAPP}",
        body=message
    )

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
