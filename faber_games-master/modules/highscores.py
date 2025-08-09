import os
import json
from typing import List, Dict, Optional
from flask import redirect, url_for

SCORES_DIR = "scores"  

def is_new_highscore(game_slug: str, score: int) -> bool:
    scores = load_high_scores(game_slug)
    max_score = max((entry["score"] for entry in scores), default=0)
    return score > max_score


def ensure_scores_dir() -> None:
    if not os.path.exists(SCORES_DIR):
        os.makedirs(SCORES_DIR)

def get_scores_file(game_slug: str) -> str:
    ensure_scores_dir()
    return os.path.join(SCORES_DIR, f"{game_slug}.json")

def load_high_scores(game_slug: str) -> List[Dict[str, Optional[int]]]:
    file_path = get_scores_file(game_slug)
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            f.write("[]")
        return []
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_high_scores(game_slug: str, scores: List[Dict[str, Optional[int]]]) -> None:
    ensure_scores_dir()
    file_path = get_scores_file(game_slug)
    with open(file_path, "w") as f:
        json.dump(scores, f, indent=4)

def add_score(game_slug: str, name: str, score: int) -> None:
    if not name or not isinstance(score, int):
        return
    scores = load_high_scores(game_slug)
    scores.append({"name": name, "score": score})
    scores = sorted(scores, key=lambda x: x["score"], reverse=True)
    save_high_scores(game_slug, scores)

def redirect_to_submit_score(game_slug: str, score: int):
    # Redirect helper to the submit_score route with score as query param
    return redirect(url_for('submit_score', game_slug=game_slug) + f'?score={score}')
