from flask import render_template, request, session, redirect, url_for
import random
from typing import Tuple
from modules.highscores import is_new_highscore  # Import necessário para verificar recorde

class PenaltyGame:
    def __init__(self, random_generator=None):
        if random_generator is None:
            self.random_generator = random
        else:
            self.random_generator = random_generator
    
    def play_round(self, player_direction: str) -> Tuple[str, str, str]:
        directions = ["left", "center", "right"]
        goalkeeper_direction = self.random_generator.choice(directions)
        if player_direction == goalkeeper_direction:
            result = "SAVED"
        else:
            result = "GOAL"
        return player_direction, goalkeeper_direction, result

def handle_penalty():
    game = PenaltyGame()
    
    if request.method == "POST":
        if "direction" in request.form:
            player_direction = request.form["direction"]
            player_direction, goalkeeper_direction, result = game.play_round(player_direction)
            
            consecutive_goals = session.get("penalty_consecutive_goals", 0)
            
            if result == "GOAL":
                consecutive_goals += 1
                session["penalty_consecutive_goals"] = consecutive_goals
                
                new_highscore = is_new_highscore("penalty", consecutive_goals)
                
                return render_template(
                    "penalty_result.html",
                    player_direction=player_direction,
                    goalkeeper_direction=goalkeeper_direction,
                    result=result,
                    consecutive_goals=consecutive_goals,
                    new_highscore=new_highscore
                )
            else:
                score_to_submit = consecutive_goals
                session["penalty_consecutive_goals"] = 0
                return redirect(url_for('submit_score', game_slug='penalty', score=score_to_submit))
    
    consecutive_goals = session.get("penalty_consecutive_goals", 0)
    return render_template("penalty.html", consecutive_goals=consecutive_goals)
