import os
from gym_xiangqi.constants import B_WIDTH, B_HEIGHT
import pygame


class Board:
    """
    A class for Xianqi Board
    """

    def __init__(self):
        self.boardWidth = B_WIDTH
        self.boardHeight = B_HEIGHT
        self.board_background = None
        self.load_board_image()

    def load_board_image(self):
        file_path = os.path.split(os.path.abspath(__file__))[0]
        target_file = file_path + "/images/board/BOARD.png"
        self.board_background = pygame.image.load(target_file).convert_alpha()
