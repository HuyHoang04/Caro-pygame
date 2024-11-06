# leaderboard.py
import csv
from constants import *

LEADERBOARD_FILE = "leaderboard.csv"

# Hàm lưu kết quả vào bảng xếp hạng
def save_score(player_name, status):
    with open(LEADERBOARD_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([player_name, status])

# Hàm đọc bảng xếp hạng từ file
def load_leaderboard():
    leaderboard = []
    try:
        with open(LEADERBOARD_FILE, mode="r") as file:
            reader = csv.reader(file)
            leaderboard = list(reader)
    except FileNotFoundError:
        # File chưa tồn tại, không cần làm gì thêm
        pass
    return leaderboard
