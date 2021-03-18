import pygame
import os

class Sound:

    """
    A class for sounds
    """
    def __init__(self):

        # declare variables
        self.bgm = None
        self.piece_move = None

        # init pygame mixer
        pygame.mixer.init()

        #load sound effet for piece movements
        self.load_piece_move()
    
    # load background music
    def play_bgm(self):
        file_path = os.path.split(os.path.abspath(__file__))[0]
        target_file = file_path + "/sounds/bgm.mp3"
        pygame.mixer.music.load(target_file)
        pygame.mixer.music.play(-1)

    # load the sound effect for piece movements
    def load_piece_move(self):
        file_path = os.path.split(os.path.abspath(__file__))[0]
        target_file = file_path + "/sounds/piece_move.mp3"
        self.piece_move = pygame.mixer.Sound(target_file)
