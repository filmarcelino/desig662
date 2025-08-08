from flask import render_template, request, session
import random
from typing import Tuple
from modules.highscores import load_high_scores, is_new_highscore

class OddsOrEvensGame:
    def __init__(self, random_generator=None):
        if random_generator is None:
            self.random_generator = random
        else:
            self.random_generator = random_generator

    def determine_winner(self, user_choice: str, total: int) -> str:
        is_even_total = total % 2 == 0
        if (is_even_total and user_choice == "Par") or (not is_even_total and user_choice == "Impar"):
            return "Voce Venceu!"
        else:
            return "Voce Perdeu!"

    def play_round(self, user_choice: str, user_number: int) -> Tuple[str, int, int, str]:
        computer_choice = "Par" if user_choice == "Impar" else "Impar"
        computer_number = self.random_generator.randint(1, 5)
        total = user_number + computer_number
        result = self.determine_winner(user_choice, total)
        return computer_choice, computer_number, total, result

    def calculate_score(self, user_number: int, computer_number: int, result: str) -> int:
        if result == "Voce Venceu!":
            return 5 * user_number + 5 * (10 - computer_number)
        return 0

def handle_odds_or_evens():
    game = OddsOrEvensGame()
    game_slug = "odds-or-evens"

    if request.method == "POST":
        if "choice" in request.form:
            user_choice = request.form["choice"]
            computer_choice = "Par" if user_choice == "Impar" else "Impar"
            session["ooe_user_choice"] = user_choice
            session["ooe_computer_choice"] = computer_choice

            return render_template(
                "odds_or_evens_numbers.html",
                user_choice=user_choice,
                computer_choice=computer_choice,
                streak=session.get("ooe_streak", 0)
            )

        elif "number" in request.form:
            user_choice = session.get("ooe_user_choice")
            user_number = int(request.form["number"])

            computer_choice, computer_number, total, result = game.play_round(user_choice, user_number)

            streak = session.get("ooe_streak", 0)
            if result == "Voce Venceu!":
                streak += 1
                session["ooe_streak"] = streak
                current_streak = streak

                return render_template(
                    "odds_or_evens_result.html",
                    user_choice=user_choice,
                    computer_choice=computer_choice,
                    user_number=user_number,
                    computer_number=computer_number,
                    total=total,
                    result=result,
                    score=current_streak,
                    streak=current_streak,
                    show_continue_options=True
                )
            else:
                current_streak = streak
                session["ooe_streak"] = 0
                session.pop("ooe_user_choice", None)
                session.pop("ooe_computer_choice", None)

                if is_new_highscore(game_slug, current_streak):
                    return render_template(
                        "new_highscore.html",
                        game_slug=game_slug,
                        user_choice=user_choice,
                        computer_choice=computer_choice,
                        user_number=user_number,
                        computer_number=computer_number,
                        total=total,
                        result=result,
                        score=current_streak,
                        streak=current_streak,
                        show_continue_options=True
                    )
                else:
                    return render_template(
                        "odds_or_evens_result.html",
                        user_choice=user_choice,
                        computer_choice=computer_choice,
                        user_number=user_number,
                        computer_number=computer_number,
                        total=total,
                        result=result,
                        score=current_streak,
                        streak=current_streak,
                        show_continue_options=True
                    )

    return render_template("odds_or_evens.html")
