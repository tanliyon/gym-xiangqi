import os
from gym_xiangqi.constants import BOARD_WIDTH, BOARD_HEIGHT, PATH_TO_BOARD
import pygame


class Board:
    """
    A class for Xianqi Board
    """
    def __init__(self):
        self.boardWidth = BOARD_WIDTH
        self.boardHeight = BOARD_HEIGHT
        self.board_background = None
        self.load_board_image()

    def load_board_image(self):
        filename = "BOARD.png"
        self.board_background = pygame.image.load( PATH_TO_BOARD + filename).convert_alpha()
