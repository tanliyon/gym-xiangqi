import pygame
from gym_xiangqi.constants import PATH_TO_SOUNDS


class Sound:

    """
    A class for sounds
    """
    def __init__(self):

        # declare variables
        self.bgm = None
        self.piece_move = None

        # init pygame mixer
        pygame.init()
        pygame.mixer.init()

    # load background music
    def play_bgm(self):
        filename = "bgm.mp3"
        pygame.mixer.music.load(PATH_TO_SOUNDS + filename)
        pygame.mixer.music.play(-1)