from flask import Flask, render_template, request
import random

app = Flask(__name__)

rejections = 0
names = []

@app.route("/", methods=["GET", "POST"])
def ask():
    global rejections
    global names

    if request.method == "POST":
        name = request.form.get("name") or "babe"
        choice = request.form.get("response")

        if name not in names:
            names.append(name)

        if choice == "yes":
            answer = f"Hell yeah, {name}! 💃🕺 Light some candles!"
            bonus = random.choice([
                "Truth: What's the naughtiest thought you've had today?",
                "Dare: Send a spicy emoji 👀",
                "Truth: Have you ever thought about me today… like that?",
                "Dare: Kiss me for 10 seconds, no breaks!"
            ])
            return render_template("response.html", answer=answer, bonus=bonus)

        elif choice == "no":
            rejections += 1
            if rejections >= 3:
                answer = f"Aww c'mon {name}, now you're just teasing 😏"
            else:
                answer = f"Aww, maybe later, {name}? 🥺"
            return render_template("response.html", answer=answer)

    return render_template("form.html")

