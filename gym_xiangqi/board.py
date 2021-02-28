import gym_xiangqi.piece
import pygame
import os
#import envs.xianqi_env


class Board:
    """
    A class for Xianqi Board
    """
    
    def __init__(self):
        self.board_background = self.load_board_image()

    def load_board_image(self):
        file_path = os.path.split(os.path.abspath(__file__))[0]
        target_file = file_path + "/images/board/BOARD.GIF"
        try:
            image = pygame.image.load(target_file).convert()
        except pygame.error:
            raise SystemExit('Board Image Load Failure: "%s" %s' %(target_file, pygame.get_error()))
        return image