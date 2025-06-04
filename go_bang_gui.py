import sys

import pygame
import tkinter as tk
from tkinter import messagebox
from constants import *

from ai_aigorithm import AI


class GoBang:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption("五子棋")
        icon = pygame.image.load("assets//logo.png")
        pygame.display.set_icon(icon)

        self.board = [[FREE_POS for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK_STONE
        self.running = True
        # 引入messagebox，并隐藏tkinter窗体
        self.root = tk.Tk()
        self.root.withdraw()

        self.ai = AI()

    def draw_board(self):
        """绘制棋盘"""
        self.screen.fill(YELLOW)  # 修改为浅灰色的棋盘背景
        board_size = BOARD_SIZE - 1
        for i in range(BOARD_SIZE):
            pygame.draw.line(self.screen, BLACK, (i * CELL_SIZE + ml, mt),
                             (i * CELL_SIZE + ml, CELL_SIZE * board_size + mt))
            pygame.draw.line(self.screen, BLACK, (ml, i * CELL_SIZE + mt),
                             (CELL_SIZE * board_size + ml, i * CELL_SIZE + mt))
        dots = [  # 绘制棋盘上的点
            (3, 3), (3, 9), (3, 15),
            (9, 3), (9, 9), (9, 15),
            (15, 3), (15, 9), (15, 15)
        ]
        for dot in dots:
            pygame.draw.circle(self.screen, BLACK, (dot[0] * CELL_SIZE + ml, dot[1] * CELL_SIZE + mt), 5)

    def draw_stones(self):
        """绘制棋子"""
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == BLACK_STONE:
                    pygame.draw.circle(self.screen, BLACK, (col * CELL_SIZE + ml,
                                                            row * CELL_SIZE + mt), CELL_SIZE // 2 - 5)
                elif self.board[row][col] == WHITE_STONE:
                    pygame.draw.circle(self.screen, WHITE, (col * CELL_SIZE + ml,
                                                            row * CELL_SIZE + mt), CELL_SIZE // 2 - 5)

    def check_winner(self, player):
        """检查指定玩家是否获胜"""
        # 简单的胜利检查，这里只检查水平和垂直方向
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE - 4):
                if all(self.board[i][j + k] == player for k in range(5)):
                    return True
                if all(self.board[j + k][i] == player for k in range(5)):
                    return True
        # 对角线检查（斜线）
        for i in range(BOARD_SIZE - 4):
            for j in range(BOARD_SIZE - 4):
                if all(self.board[i + k][j + k] == player for k in range(5)):
                    return True
                if all(self.board[i + k][j + 4 - k] == player for k in range(5)):
                    return True
        return False

    def reset_game(self):
        self.board = [[FREE_POS for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = BLACK_STONE
        self.ai = AI()

    def quit(self):
        # 弹出确认对话框
        confirm = messagebox.askyesno("退出确认", "确定要退出游戏吗？")
        if confirm:
            self.running = False

    def make_a_move(self, event):
        mouse_pos = event.pos
        row, col = (mouse_pos[1] + CELL_SIZE // 2 - mt) // CELL_SIZE, \
                   (mouse_pos[0] + CELL_SIZE // 2 - ml) // CELL_SIZE
        if row < 0 or col < 0 or row >= BOARD_SIZE or col >= BOARD_SIZE:
            return
        if self.board[row][col] != FREE_POS:
            return

        self.board[row][col] = BLACK_STONE
        self.current_player = WHITE_STONE
        if self.check_winner(BLACK_STONE):
            return
        x, y = self.ai.move(row, col)
        self.board[x][y] = WHITE_STONE
        self.current_player = BLACK_STONE

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.make_a_move(event)

            self.screen.fill(YELLOW)
            self.draw_board()
            self.draw_stones()

            if self.check_winner(BLACK_STONE):
                messagebox.showinfo("winner!", "恭喜获胜!!!")
                self.reset_game()
            elif self.check_winner(WHITE_STONE):
                messagebox.showinfo("lose!", "再接再厉!!!")
                self.reset_game()
            pygame.display.flip()
        pygame.quit()
        sys.exit()
