"""Flask backend for the Slot Machine web UI.

This file contains NO game logic of its own. Every rule of the game
(how the reels spin, how winnings are checked, the symbol weights and
payouts) still lives in main.py - the code written for this project.

Flask's only job here is to expose that logic over HTTP so a browser
can talk to it. Think of it as a thin translator sitting between your
Python functions and the web page.
"""

from flask import Flask, render_template, request, jsonify, session

# This is YOUR file. Importing it gives us access to get_slot_machine_spin,
# check_winnings, and the constants/dictionaries you defined.
import main as engine

app = Flask(__name__)

# A secret key is required for Flask to store the balance in a signed
# session cookie. Any random string works; change it to your own.
app.secret_key = "replace-this-with-any-random-string"


@app.route("/")
def index():
    # Serves the single web page (templates/index.html).
    return render_template("index.html")


@app.route("/state")
def state():
    """Send the browser the current balance and the game's fixed config.

    The frontend uses this on page load to size the controls and build
    the paytable - all of it derived from the constants in main.py, so
    there is a single source of truth.
    """
    return jsonify({
        "balance": session.get("balance", 0),
        "config": {
            "maxLines": engine.MAX_LINES,
            "minBet": engine.MIN_BET,
            "maxBet": engine.MAX_BET,
            "rows": engine.ROWS,
            "cols": engine.COLS,
            "values": engine.symbol_value,
        },
    })


@app.route("/deposit", methods=["POST"])
def deposit():
    """Add money to the balance. Mirrors the validation in deposit()."""
    data = request.get_json(silent=True) or {}
    amount = data.get("amount")

    if not isinstance(amount, int) or amount <= 0:
        return jsonify({"error": "The deposit must be a positive whole number."}), 400

    session["balance"] = session.get("balance", 0) + amount
    return jsonify({"balance": session["balance"]})


@app.route("/spin", methods=["POST"])
def spin():
    """Play one round.

    Validation here mirrors get_number_of_lines() and get_bet(). The two
    lines that actually run the game are your functions, untouched.
    """
    balance = session.get("balance", 0)
    if balance <= 0:
        return jsonify({"error": "Deposit some money before you spin."}), 400

    data = request.get_json(silent=True) or {}
    lines = data.get("lines")
    bet = data.get("bet")

    if not isinstance(lines, int) or not (1 <= lines <= engine.MAX_LINES):
        return jsonify({"error": f"Lines must be between 1 and {engine.MAX_LINES}."}), 400
    if not isinstance(bet, int) or not (engine.MIN_BET <= bet <= engine.MAX_BET):
        return jsonify({"error": f"The bet must be between {engine.MIN_BET} and {engine.MAX_BET}."}), 400

    total_bet = bet * lines
    if total_bet > balance:
        return jsonify({"error": f"You don't have enough to bet \u20ac{total_bet}."}), 400

    # --- Your code does all the real work below ---
    slots = engine.get_slot_machine_spin(engine.ROWS, engine.COLS, engine.symbol_count)
    winnings, winning_lines = engine.check_winnings(slots, lines, bet, engine.symbol_value)
    # ----------------------------------------------

    net = winnings - total_bet
    session["balance"] = balance + net

    return jsonify({
        "slots": slots,            # list of columns, each a list of symbols
        "winnings": winnings,      # gross amount won this spin
        "winningLines": winning_lines,
        "totalBet": total_bet,
        "net": net,                # winnings minus what was staked
        "balance": session["balance"],
    })


if __name__ == "__main__":
    # debug=True auto-reloads when you save and prints errors in the browser.
    app.run(debug=True, port=5000)
