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
        target_file = PATH_TO_BOARD + filename
        self.board_background = pygame.image.load(target_file).convert_alpha()