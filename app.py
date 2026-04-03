import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "vk1.a.Yl53xSewO4g1Zsy1u9eQkbwgyp8lELb4noR0GV-iz9f3Pu3Z7nZDqAwXiTqfiQkKmR38iULc3eu5IaAr4Wad5a5uRofrt2Q9Gmd4UcitbfGgObbgysfRYCPcS7VqiQZNS7Ul0y_e0DDjZV-9bYhUJFI2MJMbeBimIlw3nxSpXRlSm7pGgaVzOuI52EUgojPR4ngJEyI7X12M5IfrFidUQ"
CONFIRMATION_TOKEN = "d92bddc6"
SECRET_KEY = "mysecret123"


# 📌 КНОПКИ
def get_keyboard():
    keyboard = {
        "one_time": False,
        "buttons": [
            [
                {"action": {"type": "text", "label": "📄 Шаблоны документов"}, "color": "primary"},
                {"action": {"type": "text", "label": "❓ Вопросы"}, "color": "secondary"}
            ]
        ]
    }
    return json.dumps(keyboard, ensure_ascii=False)


# 📤 ОТПРАВКА СООБЩЕНИЯ
def send_message(user_id, message):
    requests.post("https://api.vk.com/method/messages.send", {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "keyboard": get_keyboard(),
        "access_token": TOKEN,
        "v": "5.131"
    })


# 🌐 ПИНГ ДЛЯ UPTIMEROBOT
@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200


# 🤖 ВК CALLBACK
@app.route("/", methods=["POST"])
def vk_callback():
    data = request.json or {}

    # 🔑 подтверждение сервера VK
    if data.get("type") == "confirmation":
        return CONFIRMATION_TOKEN

    # 💬 новое сообщение
    if data.get("type") == "message_new":
        message = data["object"]["message"]
        user_id = message.get("from_id")
        text = message.get("text", "").lower()

        # 🟢 старт
        if text in ["начать", "start", ""]:
            reply = (
                "👋 Привет! Я бот «Фемистокл»\n\n"
                "📚 Я помогаю малому бизнесу:\n"
                "• находить шаблоны документов\n\n"
                "👇 Выбери нужный раздел:"
            )

        # 📄 шаблоны
        elif "шаблон" in text:
            reply = (
                "📄 Шаблоны документов:\n"
                "• договор аренды\n"
                "• договор оказания услуг\n"
                "• договор подряда\n"
                "• претензия\n"
                "• жалоба\n"
            )

        # ❓ раздел (пока без реальных ответов)
        elif "вопрос" in text:
            reply = (
                "❓ Сейчас доступны только шаблоны документов.\n"
                "Выберите раздел 📄"
            )

        else:
            reply = "Выберите кнопку ниже 👇"

        send_message(user_id, reply)

    return "ok"
