from flask import Flask, render_template_string, request, session, redirect, url_for
import random

app = Flask(__name__)
app.secret_key = "somethingsecret"

html_template = """
<!DOCTYPE html>
<html>
<head>
    <title>Ahem... a question</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding-top: 50px; }
        button { font-size: 24px; padding: 10px 20px; margin: 20px; }
        img { max-width: 300px; margin-top: 20px; }
        #bonus { margin-top: 40px; }
    </style>
</head>
<body>
    {% if not session.get('name') %}
        <form method="post">
            <h2>What's your name, babe?</h2>
            <input type="text" name="name" required>
            <br><br>
            <button type="submit" name="step" value="name">Submit</button>
        </form>
    {% elif answer %}
        <h1>{{ answer }}</h1>
        {% if gif %}
            <img src="{{ gif }}">
        {% endif %}
        {% if bonus %}
            <div id="bonus">
                <h2>🎁 Bonus Round 🎁</h2>
                <img src="/static/bonus.gif">
                <br><br>
                <form method="post">
                    <button name="truth_dare" value="truth">Truth</button>
                    <button name="truth_dare" value="dare">Dare</button>
                </form>
                {% if truth_dare %}
                    <p><strong>Your {{ truth_dare }}:</strong> {{ challenge }}</p>
                {% endif %}
            </div>
        {% endif %}
        <br>
        <a href="/">↩️ Start Over</a>
    {% else %}
        <h1>Hey {{ session.get('name') }}... wanna bang? 😏</h1>
        <form method="post">
            <button type="submit" name="response" value="yes" onclick="playSound('yes')">Yes 😍</button>
            <button type="submit" name="response" value="no" onclick="playSound('no')">No 🙃</button>
        </form>
        <audio id="yesSound" src="/static/yes.mp3"></audio>
        <audio id="noSound" src="/static/no.mp3"></audio>

        <script>
            function playSound(type) {
                const sound = type === 'yes' ? document.getElementById('yesSound') : document.getElementById('noSound');
                setTimeout(() => sound.play(), 100);  // slight delay
            }
        </script>
    {% endif %}
</body>
</html>
"""

truths = [
    "What was your first dirty thought today?",
    "What's something you wish I'd do more often?",
    "Have you ever faked it? 😲",
]

dares = [
    "Text me a sexy photo right now 📸",
    "Whisper something dirty in my ear later 👂😉",
    "Send a risky emoji 😈 and nothing else.",
]

@app.route("/", methods=["GET", "POST"])
def ask():
    answer = gif = bonus = challenge = truth_dare = None

    if request.method == "POST":
        if request.form.get("step") == "name":
            session["name"] = request.form.get("name")
            session["no_count"] = 0
            return redirect(url_for('ask'))

        if "response" in request.form:
            choice = request.form.get("response")
            if choice == "yes":
                answer = "Hell yeah! 💃🕺 Light some candles!"
                gif = "/static/yes.gif"
                bonus = True
            else:
                session["no_count"] = session.get("no_count", 0) + 1
                if session["no_count"] >= 3:
                    answer = "Okay okay 😅 I get it. I'm backing off... for now 🥺"
                else:
                    answer = "Aww, maybe later? 🥺"
                gif = "/static/no.gif"

        if "truth_dare" in request.form:
            truth_dare = request.form["truth_dare"]
            challenge = random.choice(truths if truth_dare == "truth" else dares)
            answer = "Hell yeah! 💃🕺 Light some candles!"
            gif = "/static/yes.gif"
            bonus = True

    return render_template_string(html_template,
        answer=answer,
        gif=gif,
        bonus=bonus,
        truth_dare=truth_dare,
        challenge=challenge
    )

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    
