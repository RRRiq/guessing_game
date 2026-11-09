
import os
import random
from flask import Flask, request, session, redirect, url_for, render_template_string

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "local-development-only")

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Guess the Number</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f3f4f6;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
        }
        .game {
            background: white;
            padding: 40px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 15px #0002;
            width: 320px;
        }
        input, button {
            padding: 12px;
            margin: 8px 0;
            border-radius: 6px;
            font-size: 16px;
        }
        input { width: 85%; border: 1px solid #ccc; }
        button {
            background: #2563eb;
            color: white;
            border: none;
            cursor: pointer;
        }
        button:hover { background: #1d4ed8; }
    </style>
</head>
<body>
    <div class="game">
        <h1>Guess the Number</h1>
        <p>I'm thinking of a number between 1 and 100.</p>
        <h2>{{ message }}</h2>
        <p>Attempts: {{ attempts }}</p>

        {% if not won %}
        <form method="POST" action="/guess">
            <input type="number" name="guess" min="1" max="100"
                   placeholder="Enter a number" required>
            <button type="submit">Guess</button>
        </form>
        {% endif %}

        <form method="POST" action="/reset">
            <button type="submit">New Game</button>
        </form>
    </div>
</body>
</html>
"""

@app.route("/")
def home():
    if "number" not in session:
        session["number"] = random.randint(1, 100)
        session["attempts"] = 0
        session["message"] = "Make your first guess!"
        session["won"] = False

    return render_template_string(
        HTML,
        message=session["message"],
        attempts=session["attempts"],
        won=session["won"]
    )

@app.route("/guess", methods=["POST"])
def guess():
    if "number" not in session:
        return redirect(url_for("home"))

    if session.get("won"):
        return redirect(url_for("home"))

    try:
        number = int(request.form["guess"])
    except (ValueError, KeyError):
        session["message"] = "Please enter a valid number."
        return redirect(url_for("home"))

    if not 1 <= number <= 100:
        session["message"] = "Choose a number between 1 and 100."
        return redirect(url_for("home"))

    session["attempts"] += 1

    if number < session["number"]:
        session["message"] = "Too low!"
    elif number > session["number"]:
        session["message"] = "Too high!"
    else:
        session["message"] = "Correct! You won!"
        session["won"] = True

    return redirect(url_for("home"))

@app.route("/reset", methods=["POST"])
def reset():
    session.clear()
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
