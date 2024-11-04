from flask import Flask, render_template, jsonify, request
import random

app = Flask(__name__)

N = 15
WIN_CONDITION = 4
board = [['' for _ in range(N)] for _ in range(N)]
current_player = "X"

def check_winner():
    for row in range(N):
        for col in range(N - WIN_CONDITION + 1):
            if board[row][col] != '' and all(board[row][col + i] == board[row][col] for i in range(WIN_CONDITION)):
                return board[row][col]
    for col in range(N):
        for row in range(N - WIN_CONDITION + 1):
            if board[row][col] != '' and all(board[row + i][col] == board[row][col] for i in range(WIN_CONDITION)):
                return board[row][col]
    for row in range(N - WIN_CONDITION + 1):
        for col in range(N - WIN_CONDITION + 1):
            if board[row][col] != '' and all(board[row + i][col + i] == board[row][col] for i in range(WIN_CONDITION)):
                return board[row][col]
    for row in range(WIN_CONDITION - 1, N):
        for col in range(N - WIN_CONDITION + 1):
            if board[row][col] != '' and all(board[row - i][col + i] == board[row][col] for i in range(WIN_CONDITION)):
                return board[row][col]
    return None

def is_full():
    return all(board[row][col] != '' for row in range(N) for col in range(N))

def smart_move():
    for row in range(N):
        for col in range(N):
            if board[row][col] == '':
                board[row][col] = "O"
                if check_winner() == "O":
                    return
                board[row][col] = ''
    for row in range(N):
        for col in range(N):
            if board[row][col] == '':
                board[row][col] = "X"
                if check_winner() == "X":
                    board[row][col] = "O"
                    return
                board[row][col] = ''
    while True:
        row = random.randint(0, N-1)
        col = random.randint(0, N-1)
        if board[row][col] == '':
            board[row][col] = "O"
            return

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global current_player
    row, col = request.json['row'], request.json['col']
    if board[row][col] == '' and not check_winner():
        board[row][col] = current_player
        if check_winner() or is_full():
            return jsonify({'board': board, 'winner': check_winner()})
        current_player = "O" if current_player == "X" else "X"
        if current_player == "O":
            smart_move()
            current_player = "X"
    return jsonify({'board': board, 'winner': check_winner()})

if __name__ == '__main__':
    app.run(debug=True)
