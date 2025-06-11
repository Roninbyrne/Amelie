from flask import Flask, request, jsonify
from Amelie import app
from Amelie.core.mongo import video_channels_collection
from pyrogram.errors import PeerIdInvalid

app_webhook = Flask(__name__)

@app_webhook.route("/", methods=["GET"])
def home():
    return "Webhook running."

@app_webhook.route("/paypal-webhook", methods=["POST"])
def paypal_webhook():
    data = request.json
    event_type = data.get("event_type")

    # Get resource and custom field
    resource = data.get("resource", {})
    custom = resource.get("custom", "")

    if "_" not in custom:
        return jsonify({"status": "ignored"}), 200

    user_id_str, video_id = custom.split("_", 1)
    try:
        user_id = int(user_id_str)
    except ValueError:
        return jsonify({"status": "invalid user_id"}), 400

    if event_type == "PAYMENT.SALE.COMPLETED":
        # Payment successful, send video
        video_data = video_channels_collection.find_one({"video_id": video_id})
        if video_data:
            video_file_id = video_data.get("file_id")
            if video_file_id:
                try:
                    app.send_video(chat_id=user_id, video=video_file_id)
                except PeerIdInvalid:
                    app.send_message(chat_id=user_id, text="✅ Payment received, but I couldn't deliver the video. Please start me in DM and try again.")
                except Exception as e:
                    print("Error sending video:", e)
        return jsonify({"status": "video sent"}), 200

    elif event_type in ["PAYMENT.SALE.DENIED", "PAYMENT.SALE.REFUNDED", "PAYMENT.SALE.REVERSED"]:
        # Payment failed or refunded, notify user
        try:
            app.send_message(chat_id=user_id, text="❌ Your payment for the video has failed or was refunded. If you believe this is an error, please contact support.")
        except Exception as e:
            print("Error sending failure message:", e)
        return jsonify({"status": "failure notified"}), 200

    # Ignore other events
    return jsonify({"status": "ignored"}), 200
