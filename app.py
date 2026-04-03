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


# 📤 ОТПРАВКА СООБЩЕНИЯ
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
        print("SEND ERROR:", e)


# 🌐 ПИНГ (для Render / UptimeRobot)
@app.route("/ping", methods=["GET"])
def ping():
    return "OK", 200


# 🤖 VK CALLBACK
@app.route("/", methods=["POST"])
def vk_callback():
    data = request.get_json(silent=True) or {}

    print("VK DATA:", data)

    # 🔑 подтверждение сервера VK
    if data.get("type") == "confirmation":
        return CONFIRMATION_TOKEN

    # 💬 новое сообщение
    if data.get("type") == "message_new":

        msg = data.get("object", {}).get("message", {})
        user_id = msg.get("from_id")
        text = (msg.get("text") or "").lower()

        if not user_id:
            return "ok"

        # 🟢 старт
        if text in ["начать", "start", ""]:
            reply = (
                "👋 Привет! Я бот «Фемистокл»\n\n"
                "📚 Я помогаю малому бизнесу:\n"
                "• шаблоны документов\n"
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

        # ❓ вопросы (заглушка)
        elif "вопрос" in text:
            reply = "❓ Сейчас доступны только шаблоны документов."

        else:
            reply = "Выберите кнопку ниже 👇"

        send_message(user_id, reply)

    return "ok"


# 🔥 ВАЖНО ДЛЯ RENDER
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
