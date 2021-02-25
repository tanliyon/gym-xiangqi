import gym
from gym import spaces
import numpy as np

from gym_xiangqi.xiangqi_game import XiangQiGame
from gym_xiangqi.piece import Piece, General, Advisor, Elephant
from gym_xiangqi.piece import Horse, Chariot, Cannon, Soldier


PIECE_POINTS = [
    0.,                     # EMPTY: No point for empty grid
    float('inf'),           # GENERAL: Priceless for the general
    2., 2.,                 # ADVISOR: 2.0 points
    2., 2.,                 # ELEPHANT: 2.0 points
    4., 4.,                 # HORSE: 4.0 points
    9., 9.,                 # CHARIOT: 9.0 points
    4.5, 4.5,               # CANNON: 4.5 points
    1., 1., 1., 1., 1.,     # SOLDIER: 1.0 point (2.0 after crossing river)
]

# Piece IDs
EMPTY = 0
GENERAL = 1
ADVISOR_1 = 2
ADVISOR_2 = 3
ELEPHANT_1 = 4
ELEPHANT_2 = 5
HORSE_1 = 6
HORSE_2 = 7
CHARIOT_1 = 8
CHARIOT_2 = 9
CANNON_1 = 10
CANNON_2 = 11
SOLDIER_1 = 12
SOLDIER_2 = 13
SOLDIER_3 = 14
SOLDIER_4 = 15
SOLDIER_5 = 16

# Piece Movement Offsets
ORTHOGONAL = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIAGONAL = [(-1, 1), (1, 1), (-1, 1), (-1, -1)]
ELEPHANT_MOVE = [(-2, 2), (2, 2), (-2, 2), (-2, -2)]
HORSE_MOVE = [
    [(-1, 0), (-1, -1)], [(-1, 0), (-1, 1)],
    [(0, 1), (-1, 1)], [(0, 1), (1, 1)],
    [(1, 0), (1, 1)], [(1, 0), (1, -1)],
    [(0, -1), (1, -1)], [(0, -1), (-1, -1)]
]

# Other constants
MAX_REP = 9


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

    shape = (10, 9)
    piece_cnt = 16

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

    def __init__(self, agent_color=Piece.red):
        self.agent_color = agent_color
        if agent_color == Piece.red:
            self.enemy_color = Piece.black
        else:
            self.enemy_color = Piece.red

        # observation space: 10 x 9 space with pieces encoded as integers
        self.observation_space = spaces.Box(
            low=-self.piece_cnt,
            high=self.piece_cnt,
            shape=self.shape,
            dtype=int
        )

        # action space: encodes start and target position and specific piece
        self.total_pos = self.shape[0] * self.shape[1]
        n = pow(self.total_pos, 2) * self.piece_cnt
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
        for r in range(self.shape[0]):
            for c in range(self.shape[1]):
                piece_id = self.initial_board[r][c]
                init = self.id_to_class[abs(piece_id)]
                if piece_id < 0:
                    self.enemy_piece[-piece_id] = init(self.enemy_color, r, c)
                elif piece_id > 0:
                    self.agent_piece[piece_id] = init(self.agent_color, r, c)

    def move_to_action_space(self, piece_id, start, end):
        """
        The action space is a 1D flat array. We can convert piece id,
        start position and end position to a corresponding index value
        in the action space.

        Parameters:
            piece_id (int): a piece ID integer
            start (tuple(int)): (row, col) start coordinate
            end (tuple(int)): (row, col) end coordinate
        return:
            Index within the self.possible_actions
        """
        piece_id_val = (piece_id-1) * pow(self.total_pos, 2)
        start_val = (start[0] * 9 + start[1]) * self.total_pos
        end_val = end[0] * 9 + end[1]
        return piece_id_val + start_val + end_val

    def action_space_to_move(self, action):
        """
        This is exact opposite of move_to_action_space() method.
        With index value, we can convert this back to piece id,
        start position and end position values.

        Parameters:
            action (int): index value within action space
        return:
            piece ID, start coordinate, end coordinate
        """
        piece_id, r = divmod(action, pow(self.total_pos, 2))
        start_val, end_val = divmod(r, self.total_pos)
        start = [0, 0]
        end = [0, 0]
        start[0], start[1] = divmod(start_val, 9)
        end[0], end[1] = divmod(end_val, 9)
        return piece_id+1, start, end

    def get_possible_actions(self):
        """
        Searches all valid actions each piece can perform
        """
        self.get_general_actions()
        self.get_advisor_actions()
        self.get_elephant_actions()
        self.get_horse_actions()
        self.get_chariot_actions()
        self.get_cannon_actions()
        self.get_soldier_actions()

    def check_action(self, piece, orig_pos, cur_pos, repeat, offset, i):
        """
        This is general searching procedure. Given the following parameters,
        repeatedly search in the same direction until either end of the board
        or another piece is blocking.

        Parameters:
            piece (int): piece ID
            orig_pos (tuple(int)): original position coordinate
            cur_pos (tuple(int)): current position in evaluation
            repeat (int): number of repetitions
            offset (tuple(int)): direction offset
            i (int): current iteration number
        return:
            Number of times repeated; This is used to find out the farthest
            possible position.
        """
        r = cur_pos[0]
        c = cur_pos[1]

        for i in range(repeat):
            row_bound = 0 <= r < self.shape[0]
            col_bound = 0 <= c < self.shape[1]

            if not row_bound or not col_bound:
                return i

            if self.state[r][c] > 0:
                break

            action_idx = self.move_to_action_space(piece, orig_pos, (r, c))
            self.possible_actions[action_idx] = 1

            if self.state[r][c] != 0:
                break

            r += offset[0]
            c += offset[1]

        return i + 1

    def get_general_actions(self):
        """
        Finds legal moves for the General
        """
        orig_pos = (self.agent_piece[GENERAL].row,
                    self.agent_piece[GENERAL].col)
        lb = 7      # lower bound row value
        ub = 9      # upper bound row value

        for offset in ORTHOGONAL:
            next_pos = (orig_pos[0] + offset[0], orig_pos[1] + offset[1])

            # must stay in the special square
            row_bound = lb <= next_pos[0] <= ub
            col_bound = 3 <= next_pos[1] <= 5
            if row_bound and col_bound:
                self.check_action(GENERAL, orig_pos, next_pos, 1, offset, 0)

    def get_advisor_actions(self):
        """
        Finds legal moves for the Advisors
        """
        for pid in range(ADVISOR_1, ADVISOR_2+1):
            orig_pos = (self.agent_piece[pid].row,
                        self.agent_piece[pid].col)
            lb = 7  # lower bound row value
            ub = 9  # upper bound row value

            for offset in DIAGONAL:
                next_pos = (orig_pos[0] + offset[0], orig_pos[1] + offset[1])

                # must stay in the special square
                row_bound = lb <= next_pos[0] <= ub
                col_bound = 3 <= next_pos[1] <= 5
                if row_bound and col_bound:
                    self.check_action(pid, orig_pos, next_pos, 1, offset, 0)

    def get_elephant_actions(self):
        """
        Finds legal moves for the Elephants
        """
        for pid in range(ELEPHANT_1, ELEPHANT_2+1):
            orig_pos = (self.agent_piece[pid].row,
                        self.agent_piece[pid].col)
            lb = 5  # lower bound row value
            ub = 9  # upper bound row value

            for offset in ELEPHANT_MOVE:
                next_pos = (orig_pos[0] + offset[0], orig_pos[1] + offset[1])

                # bound check: must not cross the river
                row_bound = lb <= next_pos[0] <= ub
                col_bound = 0 <= next_pos[1] < self.shape[1]
                if not row_bound or not col_bound:
                    continue

                # must be not blocked
                block_r = orig_pos[0] + offset[0] // 2
                block_c = orig_pos[1] + offset[1] // 2
                if self.state[block_r][block_c] != 0:
                    continue

                self.check_action(pid, orig_pos, next_pos, 1, offset, 0)

    def get_horse_actions(self):
        """
        Finds legal moves for the Horses
        """
        for pid in range(HORSE_1, HORSE_2+1):
            orig_pos = (self.agent_piece[pid].row,
                        self.agent_piece[pid].col)

            # horse moves consist of 2 separate moves:
            # 1. along the line up or down or left or right
            # 2. diagonally left or right along the same direction
            for first_move, second_move in HORSE_MOVE:
                next_r = orig_pos[0] + first_move[0]
                next_c = orig_pos[1] + first_move[1]

                # bound check
                row_bound = 0 <= next_r < self.shape[0]
                col_bound = 0 <= next_c < self.shape[1]

                if not row_bound or not col_bound:
                    continue

                # check for any blocking piece
                if self.state[next_r][next_c] != 0:
                    continue

                next_pos = (next_r + second_move[0], next_c + second_move[1])

                # no need to recurse on next moves; (0, 0) just a placeholder
                self.check_action(pid, orig_pos, next_pos, 1, (0, 0), 0)

    def get_chariot_actions(self):
        """
        Find legal moves for the Chariots
        """
        for pid in range(CHARIOT_1, CHARIOT_2+1):
            orig_pos = (self.agent_piece[pid].row,
                        self.agent_piece[pid].col)

            for offset in ORTHOGONAL:
                next_pos = (orig_pos[0] + offset[0], orig_pos[1] + offset[1])
                # No need to check for repetition; check as far as possible
                self.check_action(pid, orig_pos, next_pos, MAX_REP, offset, 0)

    def get_cannon_actions(self):
        """
        Find legal moves for the Cannons
        """
        for pid in range(CANNON_1, CANNON_2+1):
            orig_pos = (self.agent_piece[pid].row,
                        self.agent_piece[pid].col)

            for offset in ORTHOGONAL:
                # moving positions
                next_pos = (orig_pos[0] + offset[0], orig_pos[1] + offset[1])
                reps = self.check_action(pid, orig_pos, next_pos,
                                         MAX_REP, offset, 0)

                # mark the farthest position invalid if it is an enemy
                last_r = orig_pos[0] + offset[0] * reps
                last_c = orig_pos[1] + offset[1] * reps

                if self.state[last_r][last_c] < 0:
                    action_idx = self.move_to_action_space(pid, orig_pos,
                                                           (last_r, last_c))
                    self.possible_actions[action_idx] = 0

                # attacking positions
                next_r = orig_pos[0] + offset[0] * (reps + 1)
                next_c = orig_pos[1] + offset[1] * (reps + 1)

                while True:
                    row_bound = 0 <= next_r < self.shape[0]
                    col_bound = 0 <= next_c < self.shape[1]

                    if not row_bound or not col_bound:
                        break

                    if self.state[next_r][next_c] > 0:
                        break
                    elif self.state[next_r][next_c] < 0:
                        action_idx = self.move_to_action_space(
                            pid, orig_pos, (next_r, next_c)
                        )
                        self.possible_actions[action_idx] = 1
                        break

                    next_r += offset[0]
                    next_c += offset[1]

    def get_soldier_actions(self):
        """
        Find legal moves for the soldiers
        """
        for pid in range(SOLDIER_1, SOLDIER_5+1):
            orig_pos = (self.agent_piece[pid].row,
                        self.agent_piece[pid].col)

            if orig_pos[0] > 4:
                moves = [0]
            else:
                moves = [0, 1, 3]

            for i in moves:
                offset = ORTHOGONAL[i]
                next_pos = (orig_pos[0] + offset[0], orig_pos[1] + offset[1])
                self.check_action(pid, orig_pos, next_pos, 1, offset, 0)
