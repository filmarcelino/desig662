import pytest
from app import app as flask_app
from games.tic_tac_toe import check_winner, is_draw, best_move, handle_move

@pytest.fixture
def app():
    with flask_app.app_context():
        yield flask_app

def test_print_output(app):
    board = ['X', '', '', '', '', '', '', '', '']
    response = handle_move(board.copy())
    data = response.get_json()
    print(">>> DEBUG OUTPUT:", data)
    assert data is not None

def test_check_winner_x():
    board = ['X', 'X', 'X', '', '', '', '', '', '']
    assert check_winner(board, 'X')

def test_check_winner_o():
    board = ['O', '', '', 'O', '', '', 'O', '', '']
    assert check_winner(board, 'O')

def test_check_winner_none():
    board = ['X', 'O', 'X', '', '', '', '', '', '']
    assert not check_winner(board, 'X')
    assert not check_winner(board, 'O')

def test_is_draw_true():
    board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
    assert is_draw(board)

def test_is_draw_false():
    board = ['X', 'O', 'X', '', 'O', '', '', '', '']
    assert not is_draw(board)

def test_best_move_blocks_opponent():
    board = ['X', 'X', '', '', 'O', '', '', '', '']
    move = best_move(board)
    assert move == 2

def test_best_move_wins_if_possible():
    board = ['O', 'O', '', '', 'X', '', '', '', '']
    move = best_move(board)
    assert move == 2

def test_best_move_picks_first_empty():
    board = ['X', 'O', 'X', 'O', 'X', 'O', 'O', 'X', '']
    move = best_move(board)
    assert move == 8

def test_handle_move_playing(app):
    board = ['X', '', '', '', '', '', '', '', '']
    response = handle_move(board.copy())
    data = response.get_json()
    print(f"Teste playing: {data}")
    assert data['status'] == 'playing'
    assert data['board'].count('O') == 1

def test_handle_move_win_x(app):
    board = ['X', 'X', 'X', '', '', '', '', '', '']
    response = handle_move(board.copy())
    data = response.get_json()
    print(f"Teste vitória X: {data}")
    assert data['status'] == 'win'
    assert data['winner'] == 'X'

def test_handle_move_win_o(app):
    board = ['O', 'O', 'O', '', '', '', '', '', '']
    response = handle_move(board.copy())
    data = response.get_json()
    print(f"Teste vitória O: {data}")
    assert data['status'] == 'win'
    assert data['winner'] == 'O'

def test_handle_move_draw(app):
    board = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
    response = handle_move(board.copy())
    data = response.get_json()
    print(f"Teste empate: {data}")
    assert data['status'] == 'draw'
