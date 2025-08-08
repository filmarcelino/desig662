# Faber Games Arcade - Highscore Ranking System

This is the highscore ranking system integrated into Faber Games Arcade. It allows players to submit and view their scores for each game, providing a simple leaderboard experience.

## Features

- Save and load highscores for each game identified by a unique slug.
- Players submit their name and score via a friendly form after finishing a game.
- View game-specific leaderboards with sorted scores.
- Built with Flask Blueprints for modularity.
- Data stored in a JSON file (`high_scores.json`).

## How It Works

1. After finishing a game with a score, the player is redirected to a submission form.
2. Player name and score are saved under the corresponding game slug.
3. Leaderboards display scores in descending order.

## Integration Guide

To add this ranking system to a new game:

1. Import the redirect helper in your game module:

   ```python
   from modules.highscores import redirect_to_submit_score
When a player finishes with a score, redirect them to the submission page:

python
Copy
return redirect_to_submit_score("your-game-slug", score)
Players can view leaderboards at:

bash
Copy
/highscores_page/your-game-slug
Example Usage in Odds or Evens Game
python
Copy
from modules.highscores import redirect_to_submit_score

# Game logic ...

if player_won:
    return redirect_to_submit_score("odds-or-evens", player_score)
Running the Application
Run your Flask app normally:

bash
Copy
python app.py
Navigate the site and enjoy the ranking system integrated seamlessly with your games.

Feel free to customize and extend the system as needed!