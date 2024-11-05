from constants import N

def create_board():
    return [['' for _ in range(N)] for _ in range(N)]

def is_full(board):
    return all(board[row][col] != '' for row in range(N) for col in range(N))

def check_winner(board):
    from constants import WIN_CONDITION
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
