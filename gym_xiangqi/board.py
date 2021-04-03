import os

import pkg_resources
import pygame

from gym_xiangqi.constants import BOARD_WIDTH, BOARD_HEIGHT, PATH_TO_BOARD


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
        target_file = os.path.join(PATH_TO_BOARD, "BOARD.png")
        target_file = pkg_resources.resource_filename(__name__, target_file)
        self.board_background = pygame.image.load(target_file).convert_alpha()
