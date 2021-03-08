"""
This file contains all the constants used throughout
the Xiangqi environment.
"""


""" POINTS """
ILLEGAL_MOVE = -10

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

""" PIECE """
AGENT = 1
ENEMY = -1

PIECE_CNT = 16              # Total number of pieces in each side

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
DIAGONAL = [(-1, 1), (1, 1), (1, -1), (-1, -1)]
ELEPHANT_MOVE = [(-2, 2), (2, 2), (2, -2), (-2, -2)]
HORSE_MOVE = [
    [(-1, 0), (-1, -1)], [(-1, 0), (-1, 1)],
    [(0, 1), (-1, 1)], [(0, 1), (1, 1)],
    [(1, 0), (1, 1)], [(1, 0), (1, -1)],
    [(0, -1), (1, -1)], [(0, -1), (-1, -1)]
]

# Piece States
RED = 0
BLACK = 1
DEAD = 0
ALIVE = 1

""" BOARD """
# Board Dimension
BOARD_ROWS = 10
BOARD_COLS = 9

# Palace coordinates
PALACE_ENEMY_ROW = (0, 2)
PALACE_AGENT_ROW = (7, 9)
PALACE_COL = (3, 5)

# River line
RIVER_LOW = 4
RIVER_HIGH = 5

""" OTHER """
MAX_REP = 9
TOTAL_POS = BOARD_ROWS * BOARD_COLS


""" Coordinate Conversion """
COOR_DELTA = 57
COOR_OFFSET = 5
