import os

import pkg_resources
import numpy as np
import pygame

from gym_xiangqi.utils import move_to_action_space, is_ally
from gym_xiangqi.constants import (
    ORTHOGONAL, DIAGONAL, ELEPHANT_MOVE, HORSE_MOVE,    # piece moves
    BOARD_ROWS, BOARD_COLS,                             # board specs
    PALACE_ALLY_ROW, PALACE_ENEMY_ROW, PALACE_COL,      # palace bound
    RIVER_LOW, RIVER_HIGH,                              # river bound
    MAX_REP,                                            # repetition bound
    BLACK, ALIVE, ALLY, ENEMY,                          # piece states
    COOR_DELTA, COOR_OFFSET,                            # board coordinate
    PIECE_WIDTH, PIECE_HEIGHT,                          # piece sizes
    MINI_PIECE_WIDTH, MINI_PIECE_HEIGHT,                # mini piece sizes
    PATH_TO_BLACK, PATH_TO_RED,                         # file paths to pieces
    EMPTY, GENERAL,                                     # piece IDs
    BOARD_Y_OFFSET                                      # board y offset
)


class Piece:
    """
    A base class for all Xiangqi pieces

    All pieces have the following:

        Attributes:
        - color: red or black
        - position: (row, column) coordinate
        - state: alive or dead (in game or out of game)
        - image: PyGame image object used when rendering

        Methods:
        - move(self): make allowed movements
    """

    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.state = ALIVE
        self.legal_moves = None
        self.piece_width = PIECE_WIDTH
        self.piece_height = PIECE_HEIGHT
        self.mini_piece_width = MINI_PIECE_WIDTH
        self.mini_piece_height = MINI_PIECE_HEIGHT
        self.basic_image = None
        self.select_image = None
        self.mini_image = None
        self.move_sound = None

    def move(self, new_row, new_col):
        """
        Take one move among given piece's allowed moves
        Update piece's coordinates internally
        """
        if self.move_sound is not None:
            self.move_sound.play()
        self.row = new_row
        self.col = new_col

    def get_pygame_coor(self):
        x = self.col*COOR_DELTA + COOR_OFFSET
        y = self.row*COOR_DELTA + COOR_OFFSET + BOARD_Y_OFFSET
        return (x, y)

    def load_image(self, filename: str, piece_width, piece_height):
        if self.color == BLACK:
            file_path = PATH_TO_BLACK
        else:
            file_path = PATH_TO_RED

        target_file = os.path.join(file_path, filename)
        target_file = pkg_resources.resource_filename(__name__, target_file)
        image = pygame.image.load(target_file).convert_alpha()
        image = pygame.transform.scale(
            image, (piece_width, piece_height)
        )
        return image

    def set_basic_image(self):
        filename = self.name + ".png"
        self.basic_image = (self.load_image(filename,
                            self.piece_width, self.piece_height))

    def set_select_image(self):
        filename = self.name + "_S.png"
        self.select_image = (self.load_image(filename,
                             self.piece_width, self.piece_height))

    def set_mini_image(self):
        filename = self.name + ".png"
        self.mini_image = (self.load_image(filename,
                           self.mini_piece_width, self.mini_piece_height))

    def is_alive(self):
        return self.state

    # getters
    @property
    def coor(self):
        return (self.col, self.row)


def check_action(piece_id, orig_pos, cur_pos,
                 repeat, offset, i, state, actions):
    """
    This is general searching procedure. Given the following parameters,
    repeatedly search in the same direction until either end of the board
    or another piece is blocking.

    Parameters:
        piece_id (int): piece ID
        orig_pos (tuple(int)): original coordinate of the piece
        cur_pos (tuple(int)): current position in evaluation
        repeat (int): number of repetitions to perform this procedure
        offset (tuple(int)): coordinate offset towards current direction
        i (int): current iteration number
        state (numpy.ndarray): current environment state
        actions (numpy.ndarray): pool of possible actions
    return:
        Number of times repeated; This is used to find out the farthest
        possible position used for other conditional check.
    """
    r = cur_pos[0]
    c = cur_pos[1]

    if not is_ally(piece_id):
        sign = ENEMY
        piece_id *= ENEMY
    else:
        sign = ALLY

    for i in range(repeat):
        rb = 0 <= r < BOARD_ROWS
        cb = 0 <= c < BOARD_COLS

        if not rb or not cb:
            return i

        # if ally piece is located, can't go further
        if state[r][c] * sign > 0:
            break

        if check_flying_general(state, sign, piece_id, orig_pos, (r, c)):
            return 0

        action_idx = move_to_action_space(piece_id, orig_pos, (r, c))
        actions[action_idx] = 1

        if state[r][c] != 0:
            break

        r += offset[0]
        c += offset[1]

    return i + 1


def check_flying_general(state, side, piece_id, start, end):
    """
    Check if given input action results in flying general

    Parameters:
        state (np.array): 2D array representing current state
        side (int): -1 or 1 representing enemy or ally side
        piece_id (int): piece ID
        start (tuple(int)): current coordinate of given piece
        end (tuple(int)): destination coordinate of given piece
    Return (bool):
        indicates whether the action results in flying general or not
    """

    # simulate input action without altering current game state
    new_state = np.array(state)
    new_state[start[0]][start[1]] = EMPTY
    new_state[end[0]][end[1]] = piece_id * side

    enemy_gen_row = -1
    enemy_gen_col = -1
    ally_gen_row = -1
    ally_gen_col = -1

    for r in range(PALACE_ENEMY_ROW[0], PALACE_ENEMY_ROW[1]+1):
        for c in range(PALACE_COL[0], PALACE_COL[1]+1):
            if new_state[r][c] == GENERAL * ENEMY:
                enemy_gen_row = r
                enemy_gen_col = c

    for r in range(PALACE_ALLY_ROW[0], PALACE_ALLY_ROW[1] + 1):
        for c in range(PALACE_COL[0], PALACE_COL[1] + 1):
            if new_state[r][c] == GENERAL * ALLY:
                ally_gen_row = r
                ally_gen_col = c

    # check if they are in the same column
    if enemy_gen_col != ally_gen_col:
        return False

    # check if anything is in between the two generals
    for r in range(enemy_gen_row+1, ally_gen_row):
        if new_state[r][ally_gen_col] != EMPTY:
            return False
    return True


class General(Piece):
    """
    This piece is equivalent to King. It is called "Jiang" or "Shuai"
    meaning Governor (red) and General (black) respectively.
    - Only one piece exists in each side
    - Can only move 1 unit of space orthogonally within the special square area
    """

    def __init__(self, color, row, col):
        super(General, self).__init__(color, row, col)
        self.name = "GEN"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the General
        """
        if not is_ally(piece_id):
            low = PALACE_ENEMY_ROW[0]
            high = PALACE_ENEMY_ROW[1]
        else:
            low = PALACE_ALLY_ROW[0]
            high = PALACE_ALLY_ROW[1]

        for offset in ORTHOGONAL:
            next_pos = (self.row + offset[0], self.col + offset[1])

            # general must stay in the palace: row and column bound check
            rb = low <= next_pos[0] <= high
            cb = PALACE_COL[0] <= next_pos[1] <= PALACE_COL[1]
            if rb and cb:
                check_action(piece_id, (self.row, self.col), next_pos,
                             1, offset, 0, state, actions)


class Advisor(Piece):
    """
    This piece is called "Shi" meaning advisor/scholar.
    - 2 pieces exist in each side
    - Can only move 1 unit of space diagonally within the special square area
    """

    def __init__(self, color, row, col):
        super(Advisor, self).__init__(color, row, col)
        self.name = "ADV"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Advisors
        """
        if not is_ally(piece_id):
            low = PALACE_ENEMY_ROW[0]
            high = PALACE_ENEMY_ROW[1]
        else:
            low = PALACE_ALLY_ROW[0]
            high = PALACE_ALLY_ROW[1]

        for offset in DIAGONAL:
            next_pos = (self.row + offset[0], self.col + offset[1])

            # advisor must stay in the palace: row and column bound check
            rb = low <= next_pos[0] <= high
            cb = PALACE_COL[0] <= next_pos[1] <= PALACE_COL[1]
            if rb and cb:
                check_action(piece_id, (self.row, self.col), next_pos,
                             1, offset, 0, state, actions)


class Elephant(Piece):
    """
    It is called "Shiang" meaning minister (red) and elephant (black)
    This piece is similar to Bishop.
    - 2 pieces exist in each side
    - This piece cannot cross the river
    - Moves 2 unit of space diagonally
    """

    def __init__(self, color, row, col):
        super(Elephant, self).__init__(color, row, col)
        self.name = "ELE"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Elephants
        """
        if not is_ally(piece_id):
            low = 0
            high = RIVER_LOW
        else:
            low = RIVER_HIGH
            high = BOARD_ROWS - 1

        for offset in ELEPHANT_MOVE:
            next_pos = (self.row + offset[0], self.col + offset[1])

            # bound check: must not cross the river
            rb = low <= next_pos[0] <= high
            cb = 0 <= next_pos[1] < BOARD_COLS
            if not rb or not cb:
                continue

            # must be not blocked
            block_r = self.row + offset[0] // 2
            block_c = self.col + offset[1] // 2
            if state[block_r][block_c] != 0:
                continue

            check_action(piece_id, (self.row, self.col), next_pos,
                         1, offset, 0, state, actions)


class Horse(Piece):
    """
    This piece is almost identical to knight in Chess.
    It is called "Ma" meaning horse.
    - 2 Pieces in each side.
    - Moves just like knights in chess. (The "L" shape move)
    - Cannot jump over pieces unlike Knights in Chess
    """

    def __init__(self, color, row, col):
        super(Horse, self).__init__(color, row, col)
        self.name = "HRS"

    def get_actions(self, piece_id, state, actions):
        """
        Finds legal moves for the Horses
        """
        # horse moves consist of 2 separate moves:
        # 1. along the line up or down or left or right
        # 2. diagonally left or right along the same direction
        for first_move, second_move in HORSE_MOVE:
            next_r = self.row + first_move[0]
            next_c = self.col + first_move[1]

            # bound check
            rb = 0 <= next_r < BOARD_ROWS
            cb = 0 <= next_c < BOARD_COLS

            if not rb or not cb:
                continue

            # check for any blocking piece
            if state[next_r][next_c] != 0:
                continue

            next_pos = (next_r + second_move[0], next_c + second_move[1])

            # no need to recurse on next moves; (0, 0) just a placeholder
            check_action(piece_id, (self.row, self.col), next_pos,
                         1, (0, 0), 0, state, actions)


class Chariot(Piece):
    """
    It is called "Chuh" meaning chariot
    2 pieces in each side.
    This piece is identical to Rook in Chess.
    Moves just like a Rook in chess
    - As many as you want horizontally or vertically.
    """

    def __init__(self, color, row, col):
        super(Chariot, self).__init__(color, row, col)
        self.name = "CHR"

    def get_actions(self, piece_id, state, actions):
        """
        Find legal moves for the Chariots
        """
        for offset in ORTHOGONAL:
            next_pos = (self.row + offset[0], self.col + offset[1])
            # No need to check for repetition; check as far as possible
            check_action(piece_id, (self.row, self.col), next_pos,
                         MAX_REP, offset, 0, state, actions)


class Cannon(Piece):
    """
    It is called "Pao" meaning cannon or catapult.
    2 pieces in each side.
    It moves similar to a Rook. The difference is, it has to jump over
    ONE piece (enemy or foe) to capture enemy piece.
    """

    def __init__(self, color, row, col):
        super(Cannon, self).__init__(color, row, col)
        self.name = "CAN"

    def get_actions(self, piece_id, state, actions):
        """
        Find legal moves for the Cannons
        """
        if not is_ally(piece_id):
            sign = ENEMY
        else:
            sign = ALLY

        for offset in ORTHOGONAL:
            # moving positions
            next_pos = (self.row + offset[0], self.col + offset[1])
            reps = check_action(piece_id, (self.row, self.col), next_pos,
                                MAX_REP, offset, 0, state, actions)

            # mark the farthest position invalid if it is an enemy
            last_r = self.row + offset[0] * reps
            last_c = self.col + offset[1] * reps

            if state[last_r][last_c] * sign < 0:
                action_idx = move_to_action_space(piece_id * sign,
                                                  (self.row, self.col),
                                                  (last_r, last_c))
                actions[action_idx] = 0

            # attacking positions
            next_r = self.row + offset[0] * (reps + 1)
            next_c = self.col + offset[1] * (reps + 1)

            while True:
                rb = 0 <= next_r < BOARD_ROWS
                cb = 0 <= next_c < BOARD_COLS

                if not rb or not cb:
                    break

                if state[next_r][next_c] * sign > 0:
                    break
                elif state[next_r][next_c] * sign < 0:
                    if check_flying_general(state, sign, piece_id,
                                            (self.row, self.col),
                                            (next_r, next_c)):
                        break

                    action_idx = move_to_action_space(
                        piece_id * sign, (self.row, self.col), (next_r, next_c)
                    )
                    actions[action_idx] = 1
                    break

                next_r += offset[0]
                next_c += offset[1]


class Soldier(Piece):
    """
    It is called "Ping" (red) and "Tsuh" (black) meaning a foot soldier.
    5 pieces in each side.
    This is equivalent to Pawn in chess.
    Moves 1 unit of space forward
    When it crosses the river, it gets options to move left or right as well.
    """

    def __init__(self, color, row, col):
        super(Soldier, self).__init__(color, row, col)
        self.name = "SOL"

    def get_actions(self, piece_id, state, actions):
        """
        Find legal moves for the soldiers
        """
        # ORTHOGONAL contains 4 moves in clock-wise [UP, RIGHT, DOWN, LEFT]
        if not is_ally(piece_id):   # enemy side is always at the top half
            low = RIVER_HIGH
            high = BOARD_ROWS - 1
            moves = [2]             # therefore enemy soldiers move downwards
        else:                       # ally side is always at the bottom half
            low = 0
            high = RIVER_LOW
            moves = [0]             # therefore ally soldiers move upwards

        # low and high are set to be after-river row ranges
        if low <= self.row <= high:     # After crossing the river,
            moves.append(1)             # can move right
            moves.append(3)             # can move left

        for i in moves:
            offset = ORTHOGONAL[i]
            next_pos = (self.row + offset[0], self.col + offset[1])
            check_action(piece_id, (self.row, self.col), next_pos,
                         1, offset, 0, state, actions)
