def check_winner(board, symbol):
    size = len(board)  # Lấy kích thước bảng từ dữ liệu thực tế
    win_length = 5  # Số ký tự liên tiếp cần có để thắng
    
    # Kiểm tra nếu kích thước bảng nhỏ hơn win_length
    if size < win_length:
        return False, []

    # Kiểm tra theo hàng ngang
    for row in range(size):
        for col in range(size - win_length + 1):  # Giới hạn để không vượt cột
            if all(0 <= col + i < size and board[row][col + i] == symbol for i in range(win_length)):
                return True, [(row, col + i) for i in range(win_length)]

    # Kiểm tra theo hàng dọc
    for col in range(size):
        for row in range(size - win_length + 1):  # Giới hạn để không vượt hàng
            if all(0 <= row + i < size and board[row + i][col] == symbol for i in range(win_length)):
                return True, [(row + i, col) for i in range(win_length)]

    # Kiểm tra đường chéo chính (trái trên xuống phải dưới)
    for row in range(size - win_length + 1):
        for col in range(size - win_length + 1):
            if all(0 <= row + i < size and 0 <= col + i < size and board[row + i][col + i] == symbol for i in range(win_length)):
                return True, [(row + i, col + i) for i in range(win_length)]

    # Kiểm tra đường chéo phụ (phải trên xuống trái dưới)
    for row in range(win_length - 1, size):  # Hàng bắt đầu từ win_length-1
        for col in range(size - win_length + 1):
            if all(0 <= row - i < size and 0 <= col + i < size and board[row - i][col + i] == symbol for i in range(win_length)):
                return True, [(row - i, col + i) for i in range(win_length)]

    return False, []  # Không tìm thấy người thắng
