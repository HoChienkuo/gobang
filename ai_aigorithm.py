from constants import BOARD_SIZE

import numpy as np
from collections import defaultdict

MAX_DEPTH = 2  # 搜索深度

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
        kill_moves = self.detect_kill_moves()
        if kill_moves:
            (x, y) = kill_moves
            self.board[x][y] = -1
            return x, y
        _, move = self.minimax(MAX_DEPTH, -float('inf'), float('inf'), False)
        (x, y) = move
        self.board[x][y] = -1
        return x, y

    def get_line(self, x, y, dx, dy):
        line = ''
        for i in range(-4, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                cell = self.board[nx][ny]
                if cell == -1:
                    line += '1'  # AI
                elif cell == 1:
                    line += '2'  # 玩家
                else:
                    line += '0'
            else:
                line += '2'  # 边界视为敌方，防止超界活型误判
        return line

    def evaluate(self):
        patterns = {
            '11111': 100000,  # 连五
            '011110': 10000,  # 活四
            '011112': 5000,
            '211110': 5000,  # 冲四
            '001110': 1000,  # 活三
            '011100': 1000,
            '011010': 800,
            '010110': 800,
            '000110': 500,  # 眠三
            '011000': 500,
            '001100': 500,
            '001010': 300,  # 活二
            '010100': 300,
            '000100': 100  # 眠二
        }
        score = 0
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] == 0:
                    continue
                for dx, dy in DIRECTIONS:
                    line = self.get_line(x, y, dx, dy)
                    for pattern, value in patterns.items():
                        score += line.count(pattern) * (value if self.board[x][y] == -1 else -value)
        return score

    def detect_kill_moves(self):
        patterns = ['011110', '01111', '11110', '10111', '11011']
        threat_score = defaultdict(int)

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] != 0:
                    continue
                for dx, dy in DIRECTIONS:
                    line = ''
                    for i in range(-4, 5):
                        nx, ny = x + i * dx, y + i * dy
                        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                            cell = self.board[nx][ny]
                            if nx == x and ny == y:
                                line += '1'
                            elif cell == 1:
                                line += '1'
                            elif cell == -1:
                                line += '2'
                            else:
                                line += '0'
                        else:
                            line += '2'
                    for pattern in patterns:
                        if pattern in line:
                            threat_score[(x, y)] += 1

        if threat_score:
            # 选择能阻挡最多威胁的点
            return max(threat_score.items(), key=lambda kv: kv[1])[0]
        return None

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
