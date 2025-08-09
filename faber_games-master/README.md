# Faber Games Arcade Web App

A retro arcade-themed web application with classic games.

## Features
- **Games**: Browse classic games at `/games` and visit each game at `/games/<game_slug>`.

## Games Available

### Par ou Impar (Odds or Evens)
A classic Brazilian game where players choose "Par" (Even) or "Impar" (Odd) and pick a number. The computer also picks a number, and the winner is determined by whether the sum is even or odd.

### Penalty
A soccer penalty game where you play as the penalty kicker against an AI goalkeeper.

**How to Play:**
- Choose to shoot left, center, or right
- The goalkeeper randomly chooses a direction to dive
- If directions match: Shot is saved
- If directions differ: Goal scored!
- Track your consecutive goals streak

**Features:**
- Beautiful SVG graphics with animations
- Visual feedback for kicks and goalkeeper movements
- Goal counter for consecutive goals
- Responsive web-based gameplay
- Arcade-style design matching the application theme

**Play directly in your browser at:** `/games/penalty`

### Available Games
- **Par ou Impar**: Classic odds or evens game
- **Jogo da Memória**: Memory card matching game
- **Blackjack**: Classic card game where you try to get closest to 21 without busting

## Setup

1. Install [Python3](https://www.python.org/downloads/) (if not already installed):

2. If you're using Windows, install [Git Bash](https://git-scm.com/downloads).

3. Install [mise](https://mise.jdx.dev/):
   ```sh
   curl https://mise.run | sh
   mise install
   mise trust
   ```

4. Make sure mise has automatically created a .venv folder. Otherwise create it by yourself:
   ```sh
   python3 -m venv .venv
   ```

5. Source the virtual environment.
- If in Linux/Mac:
   ```sh
   source .venv/bin/activate
   ```

- If in Windows' git bash:
   ```sh
   source .venv/Scripts/activate
   ```

6. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

7. Run the app:
   ```sh
   python app.py
   ```

The app will be available at http://localhost:5000

## Testing

The project includes comprehensive unit tests for the game logic. The `OddsOrEvensGame` class has been modularized for easy testing.

### Running Tests

```sh
# Run all tests
pytest

# Run tests with coverage
pytest --cov=games

# Run specific test file
pytest tests/test_odds_or_evens.py
pytest tests/test_blackjack.py
pytest tests/

# Run tests with verbose output
pytest -v
```

## Dependencies

- **Flask**: Web framework for the application
- **pytest**: Testing framework
- **pytest-cov**: Coverage reporting for tests

## Como enviar este projeto para o GitHub

Siga estes passos para publicar este projeto no seu GitHub usando Windows (PowerShell):

1. Pré‑requisitos
   - Ter uma conta no GitHub: https://github.com/
   - Instalar o Git para Windows: https://git-scm.com/download/win
   - (Opcional) Ter o Python/venv já configurado conforme a seção de Setup acima.

2. Abra o PowerShell e navegue até a pasta do projeto
   ```powershell
   cd "C:\Users\luisf\Downloads\designhaul\faber_games-master"
   ```

3. Inicialize o repositório Git (se ainda não existir a pasta .git)
   ```powershell
   git init
   ```

4. (Somente na primeira vez) Configure seu nome e e‑mail do Git
   ```powershell
   git config --global user.name "Seu Nome"
   git config --global user.email "seu-email@exemplo.com"
   ```

5. Crie um .gitignore (recomendado)
   Crie um arquivo chamado `.gitignore` na raiz do projeto com o conteúdo abaixo para evitar subir arquivos desnecessários:
   ```
   # Python
   __pycache__/
   *.py[cod]
   *.pyo
   .pytest_cache/
   .mypy_cache/
   .coverage
   .coverage.*

   # Virtual env
   .venv/
   venv/

   # OS/IDE
   .DS_Store
   Thumbs.db
   .idea/
   .vscode/

   # Local data (ajuste conforme necessário)
   scores/*.json
   !scores/tic-tac-toe.json
   !scores/odds-or-evens.json
   !scores/snake.json
   !scores/scores.json
   !scores/checkers.json
   !scores/memory.json
   ```
   Ajuste as regras acima conforme sua necessidade (por exemplo, se quiser versionar todos os arquivos de scores, remova as linhas relativas a `scores/`).

6. Faça o primeiro commit
   ```powershell
   git add .
   git commit -m "Primeiro commit: Faber Games Arcade"
   ```

7. Crie um repositório vazio no GitHub
   - Acesse https://github.com/new
   - Dê um nome (ex.: `faber-games`), deixe como público/privado conforme desejar e clique em "Create repository" (sem adicionar README, .gitignore ou LICENSE pelo GitHub para evitar conflitos).

8. Conecte o repositório local ao remoto (escolha HTTPS ou SSH)
   - Opção A — HTTPS:
     ```powershell
     git remote add origin https://github.com/SEU_USUARIO/faber-games.git
     ```
   - Opção B — SSH (requer chave SSH configurada):
     ```powershell
     git remote add origin git@github.com:SEU_USUARIO/faber-games.git
     ```

9. Defina a branch principal como main e envie o código
   ```powershell
   git branch -M main
   git push -u origin main
   ```

10. Enviar alterações futuras
    ```powershell
    git add -A
    git commit -m "Descrição das alterações"
    git push
    ```

Dicas e solução de problemas
- Autenticação HTTPS: ao fazer `git push`, o Git pedirá login no navegador ou usuário/senha (token). Recomenda-se usar o Git Credential Manager (instalado por padrão no Git para Windows).
- Usando SSH: gere uma chave e adicione ao GitHub:
  ```powershell
  ssh-keygen -t ed25519 -C "seu-email@exemplo.com"
  # press Enter para aceitar o caminho padrão e defina uma passphrase (opcional)
  # Em seguida, copie o conteúdo de ~/.ssh/id_ed25519.pub e adicione em GitHub > Settings > SSH and GPG keys
  ```
- Trocar a URL do remoto (caso tenha errado):
  ```powershell
  git remote set-url origin NOVA_URL
  ```
- Verificar remotos configurados:
  ```powershell
  git remote -v
  ```
