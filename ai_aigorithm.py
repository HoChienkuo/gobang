from constants import BOARD_SIZE, BLACK_STONE, WHITE_STONE, FREE_POS

import numpy as np

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
        self.board[row][col] = BLACK_STONE
        best_x, best_y = None, None
        ai_level, ai_best_pos = self.get_max_kill_level(WHITE_STONE)
        player_level, player_best_pos = self.get_max_kill_level(BLACK_STONE)
        if ai_level >= 100:
            best_x, best_y = ai_best_pos
        elif player_level >= 100:
            best_x, best_y = player_best_pos
        elif ai_level >= 90 and ai_level >= player_level:
            best_x, best_y = ai_best_pos
        elif player_level >= 90:
            best_x, best_y = player_best_pos
        elif ai_level >= 60 and ai_level >= player_level + 10:
            best_x, best_y = ai_best_pos
        else:
            _, move = self.minimax(MAX_DEPTH, -float('inf'), float('inf'), False)
            best_x, best_y = move
        self.board[best_x][best_y] = WHITE_STONE
        return best_x, best_y

    def get_line(self, x, y, dx, dy):
        line = ''
        for i in range(-4, 5):
            nx, ny = x + i * dx, y + i * dy
            if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                cell = self.board[nx][ny]
                if cell == WHITE_STONE:
                    line += '1'  # AI
                elif cell == BLACK_STONE:
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
                if self.board[x][y] == FREE_POS:
                    continue
                for dx, dy in DIRECTIONS:
                    line = self.get_line(x, y, dx, dy)
                    for pattern, value in patterns.items():
                        score += line.count(pattern) * (value if self.board[x][y] == WHITE_STONE else -value)
        return score

    def get_max_kill_level(self, player):
        patterns = {
            '11111': 100,  # 五连
            '011110': 90,  # 活四
            '01111': 80, '11110': 80, '10111': 80, '11011': 80,  # 冲四
            '01110': 60, '010110': 60,  # 活三
            '001112': 50, '010112': 50,  # 冲三
        }
        max_level = 0
        best_pos = None

        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] != FREE_POS:
                    continue
                for dx, dy in DIRECTIONS:
                    line = ''
                    for i in range(-4, 5):
                        nx, ny = x + i * dx, y + i * dy
                        if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE:
                            if nx == x and ny == y:
                                line += '1'  # 假设当前位置是当前玩家下子
                            elif self.board[nx][ny] == player:
                                line += '1'
                            elif self.board[nx][ny] == -player:
                                line += '2'
                            else:
                                line += '0'
                        else:
                            line += '2'
                    for pattern, level in patterns.items():
                        if pattern in line and level > max_level:
                            max_level = max(max_level, level)
                            best_pos = (x, y)
        return max_level, best_pos

    def get_candidates(self):
        candidates = set()
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                if self.board[x][y] != FREE_POS:
                    for dx in range(-2, 3):
                        for dy in range(-2, 3):
                            nx, ny = x + dx, y + dy
                            if is_within(nx, ny) and self.board[nx][ny] == FREE_POS:
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
                self.board[x][y] = WHITE_STONE
                eval, _ = self.minimax(depth - 1, alpha, beta, False)
                self.board[x][y] = FREE_POS
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
                self.board[x][y] = BLACK_STONE
                eval, _ = self.minimax(depth - 1, alpha, beta, True)
                self.board[x][y] = FREE_POS
                if eval < min_eval:
                    min_eval = eval
                    best_move = (x, y)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval, best_move
