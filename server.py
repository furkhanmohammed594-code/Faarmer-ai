from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

@app.route("/")
def home():
    return "Farmer AI is running 🌱"

@app.route("/weather")
def weather():
    city = request.args.get("city")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    data = requests.get(url).json()

    if data.get("cod") != 200:
        return jsonify({"error": "City not found"})

    return jsonify({
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "desc": data["weather"][0]["description"]
    })

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message")

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are an agriculture expert helping farmers."},
            {"role": "user", "content": user_msg}
        ]
    )

    return jsonify({
        "reply": response["choices"][0]["message"]["content"]
    })

if __name__ == "__main__":
    app.run()
