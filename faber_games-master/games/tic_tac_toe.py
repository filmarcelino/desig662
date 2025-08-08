from flask import jsonify

def check_winner(board, mark):
    win_conditions = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [2, 4, 6]
    ]
    return any(all(board[i] == mark for i in combo) for combo in win_conditions)

def is_draw(board):
    return all(cell != '' for cell in board)

def best_move(board):
    for i in range(9):
        if board[i] == '':
            board[i] = 'O'
            if check_winner(board, 'O'):
                return i
            board[i] = ''
    for i in range(9):
        if board[i] == '':
            board[i] = 'X'
            if check_winner(board, 'X'):
                board[i] = ''
                return i
            board[i] = ''
    for i in range(9):
        if board[i] == '':
            return i
    return -1

def handle_move(board):
    if not check_winner(board, 'X') and not is_draw(board):
        ai_move = best_move(board)
        if ai_move != -1:
            board[ai_move] = 'O'

    if check_winner(board, 'X'):
        return jsonify({
            'board': board,
            'status': 'win',
            'winner': 'X'
        })
    elif check_winner(board, 'O'):
        return jsonify({
            'board': board,
            'status': 'win',
            'winner': 'O'
        })
    elif is_draw(board):
        return jsonify({
            'board': board,
            'status': 'draw'
        })
    else:
        return jsonify({
            'board': board,
            'status': 'playing'
        })
