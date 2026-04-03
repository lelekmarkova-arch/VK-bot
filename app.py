import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "ТОКЕН"
CONFIRMATION_TOKEN = "d92bddc6"


def get_keyboard():
    return json.dumps({
        "one_time": False,
        "buttons": [
            [
                {"action": {"type": "text", "label": "📄 Шаблоны документов"}, "color": "primary"},
                {"action": {"type": "text", "label": "❓ Вопросы"}, "color": "secondary"}
            ]
        ]
    }, ensure_ascii=False)


def send_message(user_id, message):
    requests.post("https://api.vk.com/method/messages.send", data={
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "keyboard": get_keyboard(),
        "access_token": TOKEN,
        "v": "5.131"
    })


@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200


@app.route("/", methods=["POST"])
def vk_callback():
    data = request.json or {}

    if data.get("type") == "confirmation":
        return CONFIRMATION_TOKEN

    if data.get("type") == "message_new":
        message = data["object"]["message"]
        user_id = message.get("from_id")
        text = message.get("text", "").lower()

        if text in ["начать", "start", ""]:
            reply = "👋 Привет! Я бот «Фемистокл»"
        elif "шаблон" in text:
            reply = "📄 Шаблоны документов"
        elif "вопрос" in text:
            reply = "❓ Сейчас только шаблоны"
        else:
            reply = "Выберите кнопку 👇"

        send_message(user_id, reply)

    return "ok"
