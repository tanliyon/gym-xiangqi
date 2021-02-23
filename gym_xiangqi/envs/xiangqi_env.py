import gym
from gym import spaces
import numpy as np

from gym_xiangqi.xiangqi_game import XiangQiGame
from gym_xiangqi.piece import Piece, General, Advisor, Elephant
from gym_xiangqi.piece import Horse, Chariot, Cannon, Soldier


"""
POINT SYSTEM
invalid_move = 
valid_move = 
empty = 0.0
general = float('inf')
advisor = 2.0
elephant = 2.0
horse = 4.0
chariot = 9.0
cannon = 4.5
soldier = 1     # after crossing the river 2
"""
piece_points = [
    0., float('inf'), 2., 2., 2., 2., 4., 4.,
    9., 9., 4.5, 4.5, 1., 1., 1., 1., 1.,
]


class XiangQiEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    shape = (10, 9)
    piece_cnt = 16

    """
    ID MAPPING
    0: empty space
    1: general
    2-3: advisor
    4-5: elephant
    6-7: horse
    8-9: chariot
    10-11: cannon
    12-16: soldier
    """
    id_to_class = [
        None, General, Advisor, Advisor, Elephant, Elephant,
        Horse, Horse, Chariot, Chariot, Cannon, Cannon,
        Soldier, Soldier, Soldier, Soldier, Soldier
    ]

    initial_board = [
        [-9, -7, -5, -3, -1, -2, -4, -6, -8],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, -11, 0, 0, 0, 0, 0, -10, 0],
        [-16, 0, -15, 0, -14, 0, -13, 0, -12],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [12, 0, 13, 0, 14, 0, 15, 0, 16],
        [0, 10, 0, 0, 0, 0, 0, 11, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [8, 6, 4, 2, 1, 3, 5, 7, 9]
    ]

    def __init__(self, agent_color=Piece.red):
        self.agent_color = agent_color
        if agent_color == Piece.red:
            self.enemy_color = Piece.black
        else:
            self.enemy_color = Piece.red

        # observation space: 10 x 9 board that has pieces encoded as integers
        self.observation_space = spaces.Box(
            low=-self.piece_cnt,
            high=self.piece_cnt,
            shape=self.shape,
            dtype=int
        )

        # action space: encodes start and target position and specific piece
        n = pow(self.shape[0] * self.shape[1], 2) * self.piece_cnt
        self.action_space = spaces.Discrete(n)

        # initial board state
        self.state = np.array(self.initial_board)

        # instantiate piece objects
        self.agent_piece = [None for _ in range(self.piece_cnt + 1)]
        self.enemy_piece = [None for _ in range(self.piece_cnt + 1)]
        self.init_pieces()

        # possible moves: binary list with same shape as action space
        #                 valid action will be represented as 1 else 0
        self.possible_actions = np.zeros((n, ))
        self.get_possible_actions()

        # initialize PyGame module
        self.game = XiangQiGame()
        self.game.on_init()

    def step(self, action):
        return 0, 0, 0, 0

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def init_pieces(self):
        # initialize agent and enemy pieces
        for r in range(self.shape[0]):
            for c in range(self.shape[1]):
                piece_id = self.initial_board[r][c]
                init = self.id_to_class[abs(piece_id)]
                if piece_id < 0:
                    self.enemy_piece[-piece_id] = init(self.enemy_color, r, c)
                elif piece_id > 0:
                    self.agent_piece[piece_id] = init(self.agent_color, r, c)

    def get_possible_actions(self):
        pass
