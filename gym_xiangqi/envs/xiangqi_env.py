import gym
from gym import spaces
from gym.utils import seeding
import numpy as np

from gym_xiangqi.xiangqi_game import XiangQiGame
from gym_xiangqi.utils import action_space_to_move, is_agent
from gym_xiangqi.piece import (
    General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier
)
from gym_xiangqi.constants import (
    BOARD_ROWS, BOARD_COLS,
    TOTAL_POS, PIECE_CNT,
    RED, BLACK, ALIVE, DEAD,
    ILLEGAL_MOVE, PIECE_POINTS, JIANG_POINT, LOSE,
    AGENT, ENEMY, EMPTY, GENERAL,
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

        # epoch termination flag
        self._done = False
        self.done_warn = False

        # observation space: 10 x 9 space with pieces encoded as integers
        self.observation_space = spaces.Box(
            low=-PIECE_CNT,
            high=PIECE_CNT,
            shape=(BOARD_ROWS, BOARD_COLS),
            dtype=int
        )

        # action space: encodes start and target position and specific piece
        n = pow(TOTAL_POS, 2) * PIECE_CNT
        # TODO: Figure out if action_space is still needed.
        self.action_space = spaces.Discrete(n)

        # initial board state
        self.state = None

        # instantiate piece objects
        self.agent_piece = [None for _ in range(PIECE_CNT + 1)]
        self.enemy_piece = [None for _ in range(PIECE_CNT + 1)]

        # possible moves: binary list with same shape of action space
        #                 valid action will be represented as 1 else 0
        self.agent_actions = np.zeros((n, ))
        self.enemy_actions = np.zeros((n, ))

        # history of consecutive jiangs (will be used to ban perpetual check)
        self.agent_jiang_history = None
        self.enemy_jiang_history = None

        # initialize PyGame module
        self.game = None

        # reset all environment components to initial state
        self.reset()

    def step(self, action):
        """
        Run one time step of Xiangqi game: agent and enemy each plays a move

        Parameter:
            action (int): a valid action in Xiangqi action space
        Return:
            observation (object): current game state of the environment
            reward (float) : amount of reward returned after given action
            done (bool): whether the episode has ended, in which case further
                         step() calls will return undefined results
            info (dict): contains auxiliary diagnostic information (helpful for
                         debugging, and sometimes learning)
        """
        error_msg = "%r (%s) invalid action" % (action, type(action))
        assert self.action_space.contains(action), error_msg

        if self._done:
            if not self.done_warn:
                self.done_warn = True
                print(gym.utils.colorize(
                    "WARN: Environment should be reset with call to reset() "
                    "when the episode has terminated (i.e 'done == True')",
                    "yellow"
                ))
            return np.array(self.state), 0, self._done, {}

        reward = 0.0

        if self.turn == AGENT:
            pieces = self.agent_piece
            possible_actions = self.agent_actions
            jiang_history = self.agent_jiang_history
        else:
            pieces = self.enemy_piece
            possible_actions = self.enemy_actions
            jiang_history = self.enemy_jiang_history

        # check for illegal move, flying general, etc. and penalize the agent
        if possible_actions[action] == 0:
            return np.array(self.state), ILLEGAL_MOVE, False, {}
        if self.check_flying_general(action):
            return np.array(self.state), ILLEGAL_MOVE, False, {}

        # if legal move is given, move the piece
        piece, start, end = action_space_to_move(action)
        pieces[piece].move(*end)

        # update observation space
        self.state[start[0]][start[1]] = EMPTY
        rm_piece_id = self.state[end[0]][end[1]]
        self.state[end[0]][end[1]] = piece * self.turn

        if rm_piece_id < 0:
            self.enemy_piece[-rm_piece_id].state = DEAD
        elif rm_piece_id > 0:
            self.agent_piece[rm_piece_id].state = DEAD

        # reward based on removed piece
        reward += PIECE_POINTS[abs(rm_piece_id)]

        # if the General on either side has been attacked, end game
        if abs(rm_piece_id) == GENERAL:
            self._done = True

        # check for perpetual check (check in Xiangqi is called jiang)
        is_jiang, jiang_action = self.check_jiang()

        # check if the player is making consecutive jiang's
        if is_jiang:
            if jiang_action not in jiang_history:
                jiang_history[jiang_action] = 0
            jiang_history[jiang_action] += 1
            if jiang_history[jiang_action] == 4:
                self._done = True
                return np.array(self.state), LOSE, self._done, {}
            reward += JIANG_POINT
        else:   # reset history if jiang spree has stopped
            if self.turn == AGENT:
                self.agent_jiang_history = {}
            else:
                self.enemy_jiang_history = {}

        # self-play: agent switches turn between agent and enemy side
        self.turn *= -1     # AGENT (1) -> ENEMY (-1) and vice versa
        self.get_possible_actions(self.turn)

        return np.array(self.state), reward, self._done, {}

    def reset(self):
        """
        Reset all environment components to initial state
        """
        self.state = np.array(self.initial_board)
        self.init_pieces()

        self.agent_jiang_history = {}
        self.enemy_jiang_history = {}

        if self.agent_color == RED:
            self.turn = AGENT
        else:
            self.turn = ENEMY

        self.get_possible_actions(self.turn)

    def render(self, mode='human'):
        """
        Render current game state with PyGame
        """
        if self.game is None:
            self.game = XiangQiGame()
            self.game.on_init(self.agent_piece, self.enemy_piece)
        self.game.render()

    def close(self):
        """
        Free up resources and gracefully exit
        """
        if self.game:
            self.game.cleanup()

    def seed(self, seed=None):
        """
        Generate random seed value used to reproduce the current game
        """
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def init_pieces(self):
        """
        Method initializes and stores all ally and enemy pieces
        """
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                piece_id = self.initial_board[r][c]
                init = self.id_to_class[abs(piece_id)]
                if piece_id < 0:
                    self.enemy_piece[-piece_id] = init(self.enemy_color, r, c)
                elif piece_id > 0:
                    self.agent_piece[piece_id] = init(self.agent_color, r, c)

    def get_possible_actions(self, player):
        """
        Searches all valid actions each piece can perform

        Parameter:
            player (int): -1 for enemy 1 for agent
        """
        # current piece set changes depending on whose turn it is
        if player == AGENT:
            piece_set = self.agent_piece
            possible_actions = self.agent_actions
        else:
            piece_set = self.enemy_piece
            possible_actions = self.enemy_actions

        # Clear all possible actions to remove possible actions from
        # previous turn.
        # TODO: Don't clear the entire list, but only the relevant actions.
        possible_actions.fill(0)

        # get possible moves for every piece in the piece set
        for pid, piece_obj in enumerate(piece_set[1:], 1):
            if piece_obj.state == ALIVE:
                piece_obj.get_actions(pid * self.turn,
                                      self.state,
                                      possible_actions)

    def get_possible_actions_by_piece(self, piece_id):
        """
        Given a piece_id, returns only the possible actions that
        can be taken by the piece.

        Parameters:
            piece_id (int): Piece ID to filter possible actions.
        return:
            actions that are can be taken by the piece.
        """
        if is_agent(piece_id):
            self.get_possible_actions(AGENT)
            possible_actions = self.agent_actions
        else:
            self.get_possible_actions(ENEMY)
            possible_actions = self.enemy_actions

        piece_id = abs(piece_id)

        # Calculate the starting and ending index of a piece
        # based on its piece id.
        piece_action_id_start = (piece_id - 1) * pow(TOTAL_POS, 2)
        piece_action_id_end = piece_action_id_start + pow(TOTAL_POS, 2)

        # First filter to obtain only legal actions.
        all_possible_actions = np.where(possible_actions == 1)[0]
        # Second filter to limit the actions to only a piece done via
        # limiting the index.
        all_possible_actions = all_possible_actions[
            all_possible_actions >= piece_action_id_start]
        return all_possible_actions[
            all_possible_actions < piece_action_id_end]

    def check_flying_general(self, action):
        """
        Check if given input action results in flying general

        Parameters:
            action (int): action value in the range of env's action space
        """
        piece_id, (r1, c1), (r2, c2) = action_space_to_move(action)

        # simulate input action without altering current game state
        new_state = np.array(self.state)
        new_state[r1][c1] = EMPTY
        new_state[r2][c2] = piece_id * self.turn

        enemy_gen = self.enemy_piece[GENERAL]
        agent_gen = self.agent_piece[GENERAL]

        # check if they are in the same column
        if enemy_gen.col != agent_gen.col:
            return False

        # check if anything is in between the two generals
        c = enemy_gen.col
        for r in range(enemy_gen.row+1, agent_gen.row):
            if new_state[r][c] != EMPTY:
                return False
        return True

    def check_jiang(self):
        """
        Check if the general is in threat (i.e it is check or "jiang")
        by any of current player's pieces
        """
        # This is OPPONENT General
        if self.turn == AGENT:
            general = self.enemy_piece[GENERAL]
            actions = self.agent_actions
        else:
            general = self.agent_piece[GENERAL]
            actions = self.enemy_actions

        # update current player's moves
        self.get_possible_actions(self.turn)

        # iterate through possible moves of current player's pieces
        actions = np.where(actions == 1)[0]
        for action in actions:
            _, _, (target_r, target_c) = action_space_to_move(action)
            if target_r == general.row and target_c == general.col:
                return True, action
        return False, -1
