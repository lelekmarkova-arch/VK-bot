import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "vk1.a.Yl53xSewO4g1Zsy1uP9eQkbwgyp8lELb4noR0GV-iz9f3Pu3Z7nZDqAwXiTqfiQkKmR38iULc3eu5IaAr4Wad5a5uRofrt2Q9Gmd4UcitbfGgObbgysfRYCPcS7VqiQZNS7Ul0y_e0DDjZV-9bYhUJFI2MJMbeBimIlw3nxSpXRlSm7pGgaVzOuI52EUgojPR4ngJEyI7X12M5IfrFidUQ"
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


@app.route("/", methods=["POST"])
def vk_callback():
    data = request.json

    # 🔑 подтверждение сервера
    if data["type"] == "confirmation":
        return CONFIRMATION_TOKEN

    # 💬 новое сообщение
    if data["type"] == "message_new":
        user_id = data["object"]["message"]["from_id"]
        text = data["object"]["message"]["text"].lower()

        # 🟢 старт
        if text in ["начать", "start", ""]:
            reply = (
                "👋 Привет! Я бот «Фемистокл»\n\n"
                "📚 Я помогаю малому бизнесу:\n"
                "• находить шаблоны документов\n"
                "• отвечать на юридические вопросы\n\n"
                "👇 Выбери, что тебе нужно:"
            )

        # 📄 шаблоны
        elif "шаблон" in text:
            reply = (
                "📄 Шаблоны документов:\n"
                "• договор аренды\n"
                "• договор оказания услуг\n"
                "• NDA\n\n"
                "Напиши, какой нужен 👍"
            )

        # ❓ вопросы
        elif "вопрос" in text:
            reply = (
                "❓ Задай юридический вопрос\n\n"
                "Например:\n"
                "• налоги ИП\n"
                "• регистрация бизнеса\n"
                "• штрафы"
            )

        else:
            reply = "Выбери кнопку ниже 👇"

        send_message(user_id, reply)

    return "ok"
