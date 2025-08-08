import os
import json

# Current scores data for odds-or-evens game
odds_or_evens_scores = [
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000},
    {"player": "Breno", "score": 1000}
]

game_slugs = ["odds-or-evens", "memory", "tic-tac-toe", "snake", "checkers"]

if not os.path.exists("scores"):
    os.makedirs("scores")
    print("Created folder 'scores'")

# Create odds-or-evens.json file
path_odds = "scores/odds-or-evens.json"
if not os.path.exists(path_odds):
    with open(path_odds, "w") as f:
        json.dump(odds_or_evens_scores, f, indent=4)
    print(f"Created {path_odds}")
else:
    print(f"{path_odds} already exists")

# Create empty json files for other games
for slug in game_slugs:
    if slug == "odds-or-evens":
        continue
    path = f"scores/{slug}.json"
    if not os.path.exists(path):
        with open(path, "w") as f:
            f.write("[]")
        print(f"Created empty {path}")
    else:
        print(f"{path} already exists")
