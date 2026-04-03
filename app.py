import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "ТОКЕН"
CONFIRMATION_TOKEN = "d92bddc6"


@app.route("/", methods=["POST", "GET"])
def vk_callback():

    if request.method == "GET":
        return "OK", 200

    data = request.json

    # 🔑 подтверждение VK
    if data.get("type") == "confirmation":
        return CONFIRMATION_TOKEN

    # 💬 сообщения
    if data.get("type") == "message_new":
        message = data["object"]["message"]
        user_id = message.get("from_id")
        text = message.get("text", "").lower()

        if text in ["начать", "start", ""]:
            reply = "👋 Бот работает"
        elif "шаблон" in text:
            reply = "📄 Шаблоны документов"
        else:
            reply = "Выберите кнопку 👇"

        requests.post("https://api.vk.com/method/messages.send", data={
            "user_id": user_id,
            "message": reply,
            "random_id": 0,
            "access_token": TOKEN,
            "v": "5.131"
        })

    return "ok"
