import gym
from gym import spaces
import numpy as np

from gym_xiangqi.xiangqi_game import XiangQiGame
from gym_xiangqi.piece import (
    General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier
)
from gym_xiangqi.constants import (
    BOARD_ROWS, BOARD_COLS,
    TOTAL_POS, PIECE_CNT,
    RED, BLACK,
)


class XiangQiEnv(gym.Env):
    """
    This is Xiangqi (Chinese chess) game implemented as reinforcement
    learning environment using OpenAI Gym framework. Xiangqi is played
    on a board of 10 rows and 9 columns with 16 pieces on each side (7
    unique pieces called General, Advisor, Elephant, Horse, Chariot,
    Cannon and Soldier.

    Observation:
        Type: Box(10, 9)
        The observation space is the state of the board and pieces.
        Each item in the space corresponds to a single coordinate on
        the board with the value range from -16 to 16. Each piece is
        encoded as an integer in that range. Negative integers are enemy
        pieces and positive integers are ally pieces.

    Actions:
        Type: Discrete(16 * 10 * 9 * 10 * 9)
        The action space is an aggregation of all possible moves even
        including illegal moves. Each space encodes 3 information: which
        piece, from where, and to where. From 16 * 10 * 9 * 10 * 9, 16 is
        the number of pieces and 10 * 9 is all possible grid positions on
        the board. The first 10 * 9 represents the start position and the
        second half represents the end position which is the position the
        piece wants to move to.

        In addition to this, the environment will calculate legal and
        illegal moves within the action space to penalize an agent trying
        to perform illegal moves and to correctly implement Xiangqi rules.

    Reward:
        We apply points to every type of pieces following the most widely
        used standard.
        General: infinity
        Advisor: 2.0
        Elephant: 2.0
        Horse: 4.0
        Chariot: 9.0
        Cannon: 4.5
        Soldier: 1.0 (2.0 if it has crossed the river)

    Starting State:
        The initial board state with pieces laid out in correct position.
        Reference the README for initial board illustration.

    Episode Termination:
        Either the red or black runs out of moves or also known as the
        general is captured. Reference the README for more details.
    """
    metadata = {'render.modes': ['human']}

    id_to_class = [
        None,
        General,
        Advisor, Advisor,
        Elephant, Elephant,
        Horse, Horse,
        Chariot, Chariot,
        Cannon, Cannon,
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

    def __init__(self, agent_color=RED):
        self.agent_color = agent_color
        if agent_color == RED:
            self.enemy_color = BLACK
        else:
            self.enemy_color = RED

        # observation space: 10 x 9 space with pieces encoded as integers
        self.observation_space = spaces.Box(
            low=-PIECE_CNT,
            high=PIECE_CNT,
            shape=(BOARD_ROWS, BOARD_COLS),
            dtype=int
        )

        # action space: encodes start and target position and specific piece
        n = pow(TOTAL_POS, 2) * PIECE_CNT
        self.action_space = spaces.Discrete(n)

        # initial board state
        self.state = np.array(self.initial_board)

        # instantiate piece objects
        self.agent_piece = [None for _ in range(PIECE_CNT + 1)]
        self.enemy_piece = [None for _ in range(PIECE_CNT + 1)]
        self.init_pieces()

        # possible moves: binary list with same shape as action space
        #                 valid action will be represented as 1 else 0
        self.possible_actions = np.zeros((n, ))
        self.get_possible_actions()

        # initialize PyGame module
        self.game = XiangQiGame()

    def step(self, action):
        return 0, 0, 0, 0

    def reset(self):
        pass

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def init_pieces(self):
        """
        Method initializes and stores all ally and enemy pieces
        """
        # initialize agent and enemy pieces
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                piece_id = self.initial_board[r][c]
                init = self.id_to_class[abs(piece_id)]
                if piece_id < 0:
                    self.enemy_piece[-piece_id] = init(self.enemy_color, r, c)
                elif piece_id > 0:
                    self.agent_piece[piece_id] = init(self.agent_color, r, c)

    def get_possible_actions(self):
        """
        Searches all valid actions each piece can perform
        """
        # Clear possible actions list.
        self.possible_actions.fill(0)
        # skip first element which is piece id 0: empty space ID
        for pid, piece_obj in enumerate(self.agent_piece[1:], 1):
            piece_obj.get_actions(pid, self.state, self.possible_actions)
    
    def get_possible_actions_by_piece(self, piece_id):
        """
        Given a piece_id, returns only the possible actions that
        can be taken by the piece.
        
        Parameters:
            piece_id (int): Piece ID to filter possible actions.
        return:
            actions that are can be taken by the piece.
        """
        self.get_possible_actions()

        # Calculate the starting and ending index of a piece
        # based on its piece id.
        piece_action_id_start = (piece_id - 1) * pow(TOTAL_POS, 2)
        piece_action_id_end = piece_action_id_start + pow(TOTAL_POS, 2)

        # First filter to obtain only legal actions.
        all_possible_actions = np.where(self.possible_actions == 1)[0]
        # Second filter to limit the actions to only a piece done via
        # limiting the index.
        all_possible_actions = all_possible_actions[
            all_possible_actions >= piece_action_id_start]
        return all_possible_actions[
            all_possible_actions < piece_action_id_end]
