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
        self.state = Piece.alive

    # constants
    red = 0
    black = 1
    dead = 0
    alive = 1

    # Must set this attributes in subclasses
    color = 0
    row = 0
    col = 0
    state = 0
    image = None

    def move(self, new_row, new_col):
        """
        Take one move among given piece's allowed moves
        Update piece's coordinates internally
        """
        self.row = new_row
        self.col = new_col


class King(Piece):
    """
    This piece is equivalent to King. It is called "Jiang" or "Shuai"
    meaning Governor (red) and General (black) respectively.
    - Only one piece exists in each side
    - Can only move 1 unit of space orthogonally within the special square area
    """

    def __init__(self, color, row, col):
        super(King, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


class Queen(Piece):
    """
    This piece is not quite equivalent to Queen
    but for the sake of simplicity we will name this class as so.
    It is called "Shi" meaning counselor/scholar.
    - 2 pieces exist in each side
    - Can only move 1 unit of space diagonally within the special square area
    """

    def __init__(self, color, row, col):
        super(Queen, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


class Bishop(Piece):
    """
    This piece is similar to Bishop.
    It is called "Shiang" meaning minister (red) and elephant (black)
    - 2 pieces exist in each side
    - This piece cannot cross the river
    - Moves 2 unit of space diagonally
    """

    def __init__(self, color, row, col):
        super(Bishop, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


class Knight(Piece):
    """
    This piece is almost identical to knight.
    It is called "Ma" meaning horse.
    - 2 Pieces in each side.
    - Moves just like knights in chess. (The "L" shape move)
    - Cannot jump over pieces unlike Knights in Chess
    """

    def __init__(self, color, row, col):
        super(Knight, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


class Rook(Piece):
    """
    This piece is identical to Rook.
    It is called "Chuh" meaning chariot
    2 pieces in each side.
    Moves just like a Rook in chess
    - As many as you want horizontally or vertically.
    """

    def __init__(self, color, row, col):
        super(Rook, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


class Cannon(Piece):
    """
    This piece has no equivalent in chess.
    It is called "Pao" meaning cannon or catapult.
    2 pieces in each side.
    It moves similar to a Rook. The difference is, it has to jump over
    ONE piece (enemy or foe) to capture enemy piece.
    """

    def __init__(self, color, row, col):
        super(Cannon, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


class Pawn(Piece):
    """
    This is equivalent to Pawn in chess.
    It is called "Ping" (red) and "Tsuh" (black) meaning a foot soldier.
    5 pieces in each side.
    Moves 1 unit of space forward
    When it crosses the river, it gets options to move left or right as well.
    """

    def __init__(self, color, row, col):
        super(Pawn, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =
