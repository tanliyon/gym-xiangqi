import pygame
from gym_xiangqi.constants import PATH_TO_SOUNDS


class Sound:
    """
    A class for sounds
    """
    def __init__(self, piece_move, bgm):
        # declare variables
        self.piece_move = None

        # init pygame mixer
        pygame.init()
        pygame.mixer.init()

        # load sounds on init
        self.load_bgm(bgm)
        self.load_piece_move(piece_move)

    # load background music
    def load_bgm(self, _bgm):
        target_file = PATH_TO_SOUNDS + _bgm
        pygame.mixer.music.load(target_file)

    # load the sound effect for piece movements
    def load_piece_move(self, _piece_move):
        target_file = PATH_TO_SOUNDS + _piece_move
        self.piece_move = pygame.mixer.Sound(target_file)
