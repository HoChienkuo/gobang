from constants import BOARD_SIZE

import numpy as np

MAX_DEPTH = 3  # 搜索深度

# 评估函数权重
SCORES = {
    5: 100000,
    4: 10000,
    3: 1000,
    2: 100,
    1: 10
}

DIRECTIONS = [(1, 0), (0, 1), (1, 1), (1, -1)]  # 横、竖、两斜


def is_within(x, y):
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def count_sequence(board, x, y, dx, dy, player):
    for i in range(5):
        nx = x + i * dx
        ny = y + i * dy
        if not is_within(nx, ny) or board[nx][ny] != player:
            return 0
    return 1


class AI:
    def __init__(self):
        self.board = np.zeros((19, 19), dtype=int)

    def move(self, row, col):
        self.board[row][col] = 1
        _, move = self.minimax(MAX_DEPTH, -float('inf'), float('inf'), True)
        (x, y) = move
        self.board[x][y] = -1
        return x, y

    def evaluate(self):
        score = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] == 0:
                    continue
                player = self.board[x][y]
                for dx, dy in DIRECTIONS:
                    count = 0
                    for i in range(5):
                        nx = x + i * dx
                        ny = y + i * dy
                        if is_within(nx, ny) and self.board[nx][ny] == player:
                            count += 1
                        else:
                            break
                    if count > 0:
                        score += SCORES.get(count, 0) * player
        return score

    def get_candidates(self):
        candidates = set()
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] != 0:
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            nx, ny = x + dx, y + dy
                            if is_within(nx, ny) and self.board[nx][ny] == 0:
                                candidates.add((nx, ny))
        return list(candidates)

    def minimax(self, depth, alpha, beta, maximizing_player):
        score = self.evaluate()
        if depth == 0 or abs(score) >= SCORES[5]:
            return score, None

        best_move = None
        candidates = self.get_candidates()

        if maximizing_player:
            max_eval = -float('inf')
            for x, y in candidates:
                self.board[x][y] = -1
                eval, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board[x][y] = 0
                if eval > max_eval:
                    max_eval = eval
                    best_move = (x, y)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            for x, y in candidates:
                self.board[x][y] = 1
                eval, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board[x][y] = 0
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
