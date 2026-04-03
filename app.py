import json
import requests
import random
from flask import Flask, request

app = Flask(__name__)

TOKEN = "vk1.a.Yl53xSewO4g1Zsy1uP9eQkbwgyp8lELb4noR0GV-iz9f3Pu3Z7nZDqAwXiTqfiQkKmR38iULc3eu5IaAr4Wad5a5uRofrt2Q9Gmd4UcitbfGgObbgysfRYCPcS7VqiQZNS7Ul0y_e0DDjZV-9bYhUJFI2MJMbeBimIlw3nxSpXRlSm7pGgaVzOuI52EUgojPR4ngJEyI7X12M5IfrFidUQ"
CONFIRMATION_TOKEN = "d92bddc6"


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


# 📤 ОТПРАВКА СООБЩЕНИЯ (С ЗАЩИТОЙ)
def send_message(user_id, message):
    try:
        requests.post("https://api.vk.com/method/messages.send", data={
            "user_id": user_id,
            "message": message,
            "random_id": random.randint(1, 10**9),
            "keyboard": get_keyboard(),
            "access_token": TOKEN,
            "v": "5.131"
        })
    except Exception as e:
        print("VK SEND ERROR:", e)


# 🔥 ПИНГ (Render живой)
@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200


# 🤖 ГЛАВНЫЙ ОБРАБОТЧИК VK
@app.route("/", methods=["POST"])
def vk_callback():

    data = request.get_json(silent=True)

    print("VK RAW DATA:", data)

    if not data:
        return "ok"

    # 🔑 подтверждение VK
    if data.get("type") == "confirmation":
        return CONFIRMATION_TOKEN

    # 💬 сообщение
    if data.get("type") == "message_new":

        msg = data.get("object", {}).get("message", {})
        user_id = msg.get("from_id")
        text = (msg.get("text") or "").lower()

        print("MESSAGE:", user_id, text)

        if not user_id:
            return "ok"

        # 🟢 старт
        if text in ["начать", "start", "привет"]:
            reply = (
                "👋 Привет! Я бот «Фемистокл»\n\n"
                "📚 Я помогаю малому бизнесу:\n"
                "• шаблоны документов\n"
                "• договоры\n"
                "• претензии\n"
            )

        # 📄 шаблоны
        elif "шаблон" in text:
            reply = (
                "📄 Шаблоны документов:\n"
                "• договор аренды\n"
                "• договор купли-продажи\n"
                "• договор подряда\n"
                "• претензия\n"
                "• жалоба"
            )

        # ❓ вопросы
        elif "вопрос" in text:
            reply = (
                "❓ Вопросы:\n\n"
                "Пока бот работает только с шаблонами документов:\n"
                "📄 договор аренды\n"
                "📄 договор купли-продажи\n"
                "📄 договор подряда"
            )

        else:
            reply = "Выберите кнопку ниже 👇"

        send_message(user_id, reply)

    return "ok"


# 🚀 запуск
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
