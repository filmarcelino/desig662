from flask import Flask, render_template, redirect, url_for, request
from games.odds_or_evens import handle_odds_or_evens
from games.blackjack import handle_blackjack
from games.tic_tac_toe import handle_move
from games.penalty import handle_penalty
from modules.highscores import load_high_scores, add_score
import os, random

app = Flask(__name__)
app.secret_key = 'arcade_secret_key'

games = [
    {"name": "Jogo da Velha", "slug": "tic-tac-toe"},
    {"name": "Snake", "slug": "snake"},
    {"name": "Damas", "slug": "checkers"},
    {"name": "Par ou Impar", "slug": "odds-or-evens"},
    {"name": "Penalty", "slug": "penalty"},
    {"name": "Jogo da Memória", "slug": "memory"},
    {"name": "Blackjack", "slug": "blackjack"},
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/games")
def games_list():
    return render_template("games.html", games=games)

@app.route("/games/memory")
def memory_game():
    card_back = 'back.png'
    cards = [f"{str(i).zfill(3)}.png" for i in range(1, 16)]
    deck = cards + cards
    random.shuffle(deck)
    game = {
        "name": "Jogo da Memória",
        "slug": "memory"
    }
    return render_template("memory.html", game=game, deck=deck, card_back=card_back)

@app.route("/mypoints")
def mypoints():
    return render_template("mypoints.html", game_slug="example-game", player="Breno", highscore=1000)

@app.route("/selecionar-ranking")
def select_ranking():
    rankings = {}
    for game in games:
        rankings[game["slug"]] = load_high_scores(game["slug"])[:5]
    return render_template("select_ranking.html", games=games, rankings=rankings)


@app.route("/games/<game_slug>", methods=["GET", "POST"])
def game_page(game_slug):
    if game_slug == "odds-or-evens":
        return handle_odds_or_evens()
    elif game_slug == "blackjack":
        return handle_blackjack()
    elif game_slug == "penalty":
        return handle_penalty()
    elif game_slug == "memory":
        return redirect("/games/memory")
    elif game_slug == "tic-tac-toe":
        return render_template("tic_tac_toe.html")
    game = next((g for g in games if g["slug"] == game_slug), None)
    if not game:
        return render_template("404.html"), 404
    return render_template("game.html", game=game)

@app.route('/submit_score/<game_slug>', methods=['GET', 'POST'])
def submit_score(game_slug):
    if request.method == 'POST':
        name = request.form.get('name')
        score = request.form.get('score')

        if not name or not score:
            error = "Please enter your name and check your score."
            return render_template('submit_score.html', game_slug=game_slug, error=error, score=score)

        try:
            score = int(score)
        except ValueError:
            error = "Invalid score value."
            return render_template('submit_score.html', game_slug=game_slug, error=error, score=score)

        add_score(game_slug, name, score)
        return redirect(url_for('highscores_page', game_slug=game_slug))

    score = request.args.get('score', '')
    return render_template('submit_score.html', game_slug=game_slug, score=score)

@app.route('/highscores_page/<game_slug>')
def highscores_page(game_slug):
    scores = load_high_scores(game_slug)
    return render_template('highscores.html', game_slug=game_slug, scores=scores)

@app.route("/api/tic-tac-toe/move", methods=["POST"])
def play_move():
    data = request.get_json()
    board = data['board']
    return handle_move(board)

if __name__ == "__main__":
    app.run(debug=True)
