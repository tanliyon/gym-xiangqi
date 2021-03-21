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
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.init()
        pygame.mixer.init()

        # load sound effet for piece movements
        self.load_piece_move()

    # load background music
    def play_bgm(self):
        filename = "bgm.mp3"
        pygame.mixer.music.load(PATH_TO_SOUNDS + filename)
        pygame.mixer.music.play(-1)

    # load the sound effect for piece movements
    def load_piece_move(self):
        filename = "piece_move.mp3"
        target_file = PATH_TO_SOUNDS + filename
        self.piece_move = pygame.mixer.Sound(target_file)
