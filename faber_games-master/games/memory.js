let flippedCards = [];
let lockBoard = false;
let matches = 0;
let attempts = 0;
let timeLeft = 60;
let timerInterval;

document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".card img");
    const timerDisplay = document.getElementById("timer");
    const restartBtn = document.getElementById("restart-btn");

    function startTimer() {
        timerInterval = setInterval(() => {
            timeLeft--;
            timerDisplay.textContent = timeLeft;
            if (timeLeft <= 0) {
                clearInterval(timerInterval);
                lockBoard = true;
                endGame();
            }
        }, 1000);
    }

    function flipCard(card, unflip = false) {
        if (unflip) {
            card.src = card.dataset.back;
        } else {
            card.src = card.dataset.front;
        }
    }

    function endGame() {
        saveScore(matches, attempts);
        displayHistory();
        alert(`Tempo esgotado! Acertos: ${matches} | Tentativas: ${attempts}`);
    }

    function saveScore(matches, attempts) {
        const scores = JSON.parse(localStorage.getItem("memoryScores")) || [];
        scores.unshift({ matches, attempts });
        localStorage.setItem("memoryScores", JSON.stringify(scores.slice(0, 3)));
    }

    function displayHistory() {
        const scores = JSON.parse(localStorage.getItem("memoryScores")) || [];
        const historyDiv = document.getElementById("history");
        historyDiv.innerHTML = "<h3>Últimos placares</h3><ul>" +
            scores.map(s => `<li>Acertos: ${s.matches} | Tentativas: ${s.attempts}</li>`).join("") +
            "</ul>";
    }

    cards.forEach(card => {
        card.addEventListener("click", () => {
            if (lockBoard || flippedCards.includes(card)) return;

            flipCard(card);
            flippedCards.push(card);

            if (flippedCards.length === 2) {
                lockBoard = true;
                attempts++;
                document.getElementById("attempts").textContent = attempts;

                const [first, second] = flippedCards;
                if (first.dataset.front === second.dataset.front) {
                    matches++;
                    document.getElementById("matches").textContent = matches;
                    flippedCards = [];
                    lockBoard = false;
                } else {
                    setTimeout(() => {
                        flipCard(first, true);
                        flipCard(second, true);
                        flippedCards = [];
                        lockBoard = false;
                    }, 800);
                }
            }
        });
    });

    restartBtn.addEventListener("click", () => {
        location.reload();
    });

    startTimer();
    displayHistory();
});