import json
import requests
from flask import Flask, request

app = Flask(__name__)

TOKEN = "vk1.a.Yl53xSewO4g1Zsy1uP9eQkbwgyp8lELb4noR0GV-iz9f3Pu3Z7nZDqAwXiTqfiQkKmR38iULc3eu5IaAr4Wad5a5uRofrt2Q9Gmd4UcitbfGgObbgysfRYCPcS7VqiQZNS7Ul0y_e0DDjZV-9bYhUJFI2MJMbeBimIlw3nxSpXRlSm7pGgaVzOuI52EUgojPR4ngJEyI7X12M5IfrFidUQ"
CONFIRMATION_TOKEN = "14eaaf7c"
SECRET_KEY = "mysecret123"

def send_message(user_id, message):
    requests.post("https://api.vk.com/method/messages.send", {
        "user_id": user_id,
        "message": message,
        "random_id": 0,
        "access_token": TOKEN,
        "v": "5.131"
    })

@app.route("/", methods=["POST"])
def vk_callback():
    data = request.json

    # проверка сервера
    if data["type"] == "confirmation":
        return CONFIRMATION_TOKEN

    # проверка секретного ключа
    if data.get("secret") != SECRET_KEY:
        return "ok"

    # новое сообщение
    if data["type"] == "message_new":
        user_id = data["object"]["message"]["from_id"]
        text = data["object"]["message"]["text"]

        if "привет" in text.lower():
            reply = "Привет 👋"
        else:
            reply = f"Ты написал: {text}"

        send_message(user_id, reply)

    return "ok"
