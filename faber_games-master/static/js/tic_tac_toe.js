let board = Array(9).fill('');
let isPlayerTurn = true;
let gameOver = false;

window.onload = function () {
    initGame();
};

function initGame() {
    document.querySelectorAll('.cell').forEach(cell => {
        cell.addEventListener('click', () => {
            const index = parseInt(cell.getAttribute('data-index'));
            if (board[index] !== '' || !isPlayerTurn || gameOver) return;

            board[index] = 'X';
            updateBoard();

            isPlayerTurn = false;

            fetch('/api/tic-tac-toe/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ board })
            })
            .then(res => res.json())
            .then(result => {
                board = result.board;
                updateBoard();
                showMessage(getStatusMessage(result));
                if (result.status !== 'playing') gameOver = true;
                else isPlayerTurn = true;
            })
            .catch(err => {
                console.error('Erro na requisição:', err);
                isPlayerTurn = true; // Permite tentar novamente
            });
        });
    });
}

function updateBoard() {
    const cells = document.querySelectorAll('.cell');
    board.forEach((val, i) => {
        cells[i].textContent = val;
        if (val !== '') {
            cells[i].classList.add('disabled');
        } else {
            cells[i].classList.remove('disabled');
        }
    });
}

function showMessage(message) {
    const messageBox = document.getElementById('message');
    const messageText = document.getElementById('messageText');
    messageText.textContent = message;
    if (message) messageBox.style.display = 'block';
    else messageBox.style.display = 'none';
}

function getStatusMessage(result) {
    if (result.status === 'win') {
        return result.winner === 'X' ? 'Você venceu!' : 'Computador venceu!';
    }
    if (result.status === 'draw') {
        return 'Empate!';
    }
    return '';  // vazio enquanto jogando
}

window.startGame = function () {
    board = Array(9).fill('');
    isPlayerTurn = true;
    gameOver = false;
    updateBoard();
    showMessage('');
};
