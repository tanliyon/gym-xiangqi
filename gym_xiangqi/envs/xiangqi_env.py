import gym
from gym import spaces
from gym.utils import seeding
import numpy as np

from gym_xiangqi.xiangqi_game import XiangQiGame
from gym_xiangqi.utils import (
    action_space_to_move,
    move_to_action_space,
    is_ally
)
from gym_xiangqi.piece import (
    General, Advisor, Elephant, Horse, Chariot, Cannon, Soldier
)
from gym_xiangqi.constants import (
    INITIAL_BOARD,
    BOARD_ROWS, BOARD_COLS,
    TOTAL_POS, PIECE_CNT,
    RED, BLACK, ALIVE, DEAD,
    ILLEGAL_MOVE, PIECE_POINTS, LOSE,
    ALLY, ENEMY, EMPTY, GENERAL,
    MAX_PERPETUAL_JIANG,
)


class XiangQiEnv(gym.Env):
    """
    This is Xiangqi (Chinese chess) game implemented as reinforcement
    learning environment using OpenAI Gym framework. Xiangqi is played
    on a board of 10 rows and 9 columns with 16 pieces on each side (7
    unique pieces called General, Advisor, Elephant, Horse, Chariot,
    Cannon and Soldier.

    Starting State:
    The initial board state with pieces laid out in correct position.
    Reference the README for initial board illustration.

    Episode Termination:
    Either the red or black runs out of moves or also known as the
    general is captured. Reference the README for more details.

    Attributes:
        observation_space (gym.spaces.Box(10, 9)):
            The observation space is the state of the board and pieces.
            Each item in the space corresponds to a single coordinate on
            the board with the value range from -16 to 16. Each piece is
            encoded as an integer in that range. Negative integers are enemy
            pieces and positive integers are ally pieces.

        action_space (gym.spaces.Discrete(16 * 10 * 9 * 10 * 9)):
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

        ally_color (int):
            Current environment's ally color
            RED = 0 and BLACK = 1

        enemy_color (int):
            Current environment's enemy color
            RED = 0 and BLACK = 1

        turn (int):
            Current player that is playing
            ALLY = 0 and ENEMY = 1

        done (bool):
            flag to indicate current game termination

        state (np.array):
            2 dimensional numpy array representing current board state

        ally_actions (np.array):
            1 dimensional numpy array indicating legal and illegal actions
            among all ally's action space
            Possible values of the array are 0 and 1 indicating legal and
            illegal actions respectively

        enemy_actions (np.array):
            1 dimensional numpy array indicating legal and illegal actions
            among all enemy's action space
            Possible values of the array are 0 and 1 indicating legal and
            illegal actions respectively

        ally_piece (list):
            List of all ally piece objects

        enemy_piece (list):
            List of all enemy piece objects
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

    def __init__(self, ally_color=RED):
        self._ally_color = ally_color
        if ally_color == RED:
            self._enemy_color = BLACK
            self._turn = ALLY
        else:
            self._enemy_color = RED
            self._turn = ENEMY

        # epoch termination flag
        self._done = False
        self._done_warn = False

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
        self._state = None
        self._state_hash = None

        # instantiate piece objects
        self._ally_piece = [None for _ in range(PIECE_CNT + 1)]
        self._enemy_piece = [None for _ in range(PIECE_CNT + 1)]

        # possible moves: binary list with same shape of action space
        #                 valid action will be represented as 1 else 0
        self._ally_actions = np.zeros((n, ))
        self._enemy_actions = np.zeros((n, ))

        # history of consecutive jiangs (will be used to ban perpetual check)
        self._ally_jiang_history = None
        self._enemy_jiang_history = None

        # initialize PyGame module
        self._game = XiangQiGame()

        # user movement information during user vs agent game mode
        self.user_move_info = None

        # reset all environment components to initial state
        self.reset()

    def step(self, action):
        """
        Run one turn of Xiangqi game (ally or enemy side plays a move)
        by processing given action based on current game turn owner

        Parameters:
            action (int): a valid action in Xiangqi action space

        Return:
            tuple: observation, reward, done, info

            observation (object): current game state of the environment

            reward (float): amount of reward returned after given action

            We apply points to every type of pieces following the most widely
            used standard.

            General: infinity

            Advisor: 2.0

            Elephant: 2.0

            Horse: 4.0

            Chariot: 9.0

            Cannon: 4.5

            Soldier: 1.0 (2.0 if it has crossed the river)

            done (bool): whether the episode has ended, in which case further
            step() calls will return undefined results

            info (dict): contains auxiliary diagnostic information (helpful for
            debugging, and sometimes learning)
        """
        # Validate action input
        error_msg = "%r (%s) invalid action" % (action, type(action))
        assert self.action_space.contains(action), error_msg

        # Validate that the environment wasn't changed between steps
        assert hash(str(self._state)) == self._state_hash, \
            "Error! Game state changed illegally!"

        # Warn the user for calling step() when current game has finished
        if self._done:
            if not self._done_warn:
                self._done_warn = True
                print(gym.utils.colorize(
                    "WARN: Environment should be reset with call to reset() "
                    "when the episode has terminated (i.e 'done == True')",
                    "yellow"
                ))
            return np.array(self._state), 0, self._done, {}

        # Prepare game state variables
        reward = 0.0

        if self._turn == ALLY:
            pieces = self._ally_piece
            possible_actions = self._ally_actions
            jiang_history = self._ally_jiang_history
        else:
            pieces = self._enemy_piece
            possible_actions = self.enemy_actions
            jiang_history = self._enemy_jiang_history

        # Check for illegal move, flying general, etc. and penalize the agent
        if possible_actions[action] == 0:
            return np.array(self._state), ILLEGAL_MOVE, False, {}

        # Check if opponent is in Jiang condition before processing given move
        pre_jiang_actions = self.check_jiang()

        # Move the piece if legal move is given
        piece, start, end = action_space_to_move(action)
        pieces[piece].move(*end)

        # Update observation space
        self._state[start[0]][start[1]] = EMPTY
        rm_piece_id = self._state[end[0]][end[1]]
        self._state[end[0]][end[1]] = piece * self._turn

        if rm_piece_id < 0:
            self._enemy_piece[-rm_piece_id].state = DEAD
        elif rm_piece_id > 0:
            self._ally_piece[rm_piece_id].state = DEAD

        # Reward based on removed piece
        reward += PIECE_POINTS[abs(rm_piece_id)]

        # End game if the General on either side has been attacked
        if abs(rm_piece_id) == GENERAL:
            self._done = True

        # Check for perpetual check/jiang
        post_jiang_actions = self.check_jiang()

        if post_jiang_actions:
            for jiang_action in post_jiang_actions:
                if jiang_action in pre_jiang_actions:
                    continue

                if jiang_action not in jiang_history:
                    jiang_history[jiang_action] = 0
                jiang_history[jiang_action] += 1

                if jiang_history[jiang_action] == MAX_PERPETUAL_JIANG:
                    self._done = True
                    return np.array(self._state), LOSE, self._done, {}
        else:       # reset history if jiang spree has stopped
            if self._turn == ALLY:
                self._ally_jiang_history = {}
            else:
                self._enemy_jiang_history = {}

        # self-play: agent switches turn between ally and enemy side
        self._turn *= -1     # ALLY (1) to ENEMY (-1) and vice versa
        self.get_possible_actions(self._turn)

        # Update state hash.
        self._state_hash = hash(str(self._state))

        return np.array(self._state), reward, self._done, {}

    def reset(self):
        """
        Reset all environment components to initial state

        Return:
            observation (object): the initial observation.
        """
        self._done = False
        self._state = np.array(INITIAL_BOARD)
        self.init_pieces()

        self._ally_jiang_history = {}
        self._enemy_jiang_history = {}

        if self._ally_color == RED:
            self._turn = ALLY
        else:
            self._turn = ENEMY

        self.get_possible_actions(self._turn)
        self._game.set_pieces(self._ally_piece, self._enemy_piece)
        self._state_hash = hash(str(self._state))

        return np.array(self._state)

    def render(self, mode='human'):
        """
        Render current game state with PyGame

        For more information refer to gym.Env.render() in OpenAI Gym
        repository.

        Parameters:
            mode (str): string to indicate render mode
        """
        if self._game.display_surf is None:
            self._game.on_init()
        if self._ally_piece[GENERAL].basic_image is None:
            self._game.on_init_pieces()
        self._game.render()

    def close(self):
        """
        Free up resources and gracefully exit the Xiangqi environment
        """
        if self._game:
            self._game.cleanup()

    def seed(self, seed=None):
        """
        Generate random seed value used to reproduce the current game

        Parameters:
            seed:
                User defined input seed. If this is `None`, then it is
                generated by this method
        """
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def step_user(self):
        """
        This method functions like the environment's step() method, but
        it is specifically for users when they are player of a Xiangqi
        game. The method first renders game GUI and listens to user inputs.
        Then, the user input, the piece movement, is converted into action
        space and passed to environment's step() method. The environment then
        is able to handle the input action just like it handles any actions
        from RL agents.

        Return:
            tuple:
            The return values are the same with step() method.
        """
        error_msg = "gym_xiangqi error: calling step_user with " \
                    "incorrect game turn (must be ally's turn)"
        assert self._turn == ALLY, error_msg

        for piece_id in range(1, PIECE_CNT+1):
            self.get_possible_actions_by_piece(piece_id)

        self._game.run()

        # Game terminated by window close button
        if self._game.quit:
            return self._state, 0, True, {"exit": True}

        # Retrieve user piece movement info
        piece_id = self._game.cur_selected_pid
        start = (self._ally_piece[piece_id].row,
                 self._ally_piece[piece_id].col)
        end = self._game.end_pos

        # Reset the variables
        self._game.cur_selected_pid = None
        self._game.end_pos = None

        # Save as instance variables for debugging
        self.user_move_info = (piece_id, start, end)

        # Process the piece movement in env
        player_action = move_to_action_space(piece_id, start, end)
        return self.step(player_action)

    def init_pieces(self):
        """
        Initialize and store all ally and enemy pieces
        """
        for r in range(BOARD_ROWS):
            for c in range(BOARD_COLS):
                piece_id = INITIAL_BOARD[r][c]
                init = self.id_to_class[abs(piece_id)]
                if piece_id < 0:
                    self._enemy_piece[-piece_id] = init(self._enemy_color,
                                                        r, c)
                elif piece_id > 0:
                    self._ally_piece[piece_id] = init(self._ally_color, r, c)

    def get_possible_actions(self, player):
        """
        Searches all valid actions each piece can perform

        Parameters:
            player (int): -1 for ENEMY 1 for ALLY
        """
        # Current piece set changes depending on whose turn it is
        if player == ALLY:
            piece_set = self._ally_piece
            possible_actions = self._ally_actions
        else:
            piece_set = self._enemy_piece
            possible_actions = self._enemy_actions

        # Clear previous turn's possible actions
        # TODO: Don't clear the entire list, but only the relevant actions.
        possible_actions.fill(0)

        # Get possible moves for every piece in the piece set
        for pid, piece_obj in enumerate(piece_set[1:], 1):
            if piece_obj.state == ALIVE:
                piece_obj.get_actions(pid * self._turn,
                                      self._state,
                                      possible_actions)

    def get_possible_actions_by_piece(self, piece_id):
        """
        Given a piece_id, returns only the possible actions that
        can be taken by the piece.

        Parameters:
            piece_id (int): Piece ID to filter possible actions.
        Return:
            actions that are can be taken by the piece.
        """
        if is_ally(piece_id):
            pieces = self._ally_piece
            possible_actions = self._ally_actions
        else:
            pieces = self._enemy_piece
            possible_actions = self._enemy_actions

        piece_id = abs(piece_id)

        # Calculate the starting and ending action index of the piece
        piece_action_id_start = (piece_id - 1) * pow(TOTAL_POS, 2)
        piece_action_id_end = piece_action_id_start + pow(TOTAL_POS, 2)

        # First, filter to obtain only legal actions
        legal_actions = np.where(possible_actions == 1)[0]

        # Second, filter the legal actions using the start and end action index
        legal_actions = legal_actions[legal_actions >= piece_action_id_start]
        legal_actions = legal_actions[legal_actions < piece_action_id_end]

        # Save the start and end coordinates in each piece object's legal_moves
        pieces[piece_id].legal_moves = [
            action_space_to_move(action)[1:] for action in legal_actions
        ]

    def check_jiang(self):
        """
        Check if the general is in threat (i.e. it is check or "jiang")
        by any of current player's pieces
        """
        # Get OPPONENT General
        if self._turn == ALLY:
            general = self._enemy_piece[GENERAL]
            actions = self._ally_actions
        else:
            general = self._ally_piece[GENERAL]
            actions = self._enemy_actions

        # Update current player's moves
        self.get_possible_actions(self._turn)

        # Iterate through possible moves of current player's pieces
        actions = np.where(actions == 1)[0]
        jiang_actions = []
        for action in actions:
            _, _, (target_r, target_c) = action_space_to_move(action)
            if target_r == general.row and target_c == general.col:
                jiang_actions.append(action)
        return jiang_actions

    @property
    def ally_color(self):
        return self._ally_color

    @property
    def enemy_color(self):
        return self._enemy_color

    @property
    def turn(self):
        return self._turn

    @property
    def state(self):
        return self._state

    @property
    def ally_piece(self):
        return self._ally_piece

    @property
    def enemy_piece(self):
        return self._enemy_piece

    @property
    def ally_actions(self):
        return self._ally_actions

    @property
    def enemy_actions(self):
        return self._enemy_actions

    @property
    def game(self):
        return self._game
