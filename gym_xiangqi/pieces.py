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

    # constants
    RED = 0
    BLACK = 1
    OUT = 0
    IN = 1

    # Must set this attributes in subclasses
    color = 0
    row = 0
    col = 0
    state = 0
    image = None

    def move(self):
        """
        Take one move among given piece's allowed moves
        Update piece's coordinates internally
        """
        raise NotImplementedError


class King(Piece):
    """
    This piece is equivalent to King.
    It is called "Jiang" or "Shuai" meaning Governor (red) and General (black) respectively.
    Only one piece exists in each side
    Can only move 1 unit of space orthogonally within the special square area
    """

    def __init__(self, side, row, col, imgFile):
        pass

    def move(self):
        raise NotImplementedError


class Queen(Piece):
    """
    This piece is not quite equivalent to Queen but for the sake of simplicity we will regard as so.
    It is called "Shi" meaning counselor/scholar.
    2 pieces exist in each side
    Can only move 1 unit of space diagonally within the special square area
    """

    def __init__(self, side, row, col, imgFile):
        pass

    def move(self):
        raise NotImplementedError


class Bishop(Piece):
    """
    This piece is similar to Bishop.
    It is called "Shiang" meaning minister (red) and elephant (black)
    2 pieces exist in each side
    This piece cannot cross the river
    Moves 2 unit of space diagonally
    """

    def __init__(self, side, row, col, imgFile):
        pass

    def move(self):
        raise NotImplementedError


class Knight(Piece):
    """
    This piece is almost identical to knight.
    It is called "Ma" meaning horse.
    2 Pieces in each side.
    Moves just like knights in chess. (The "L" shape move)
    The difference is that it cannot jump over pieces
    """

    def __init__(self, side, row, col, imgFile):
        pass

    def move(self):
        raise NotImplementedError


class Rook(Piece):
    """
    This piece is identical to Rook.
    It is called "Chuh" meaning chariot
    2 pieces in each side.
    Moves just like a Rook in chess; As many as you want horizontally and vertically.
    """

    def __init__(self, side, row, col, imgFile):
        pass

    def move(self):
        raise NotImplementedError


class Cannon(Piece):
    """
    This piece has no equivalent in chess.
    It is called "Pao" meaning cannon or catapult.
    2 pieces in each side.
    It moves like a Rook; However, has to jump over ONE piece (enemy or foe) to capture enemy piece.
    """

    def __init__(self, side, row, col, imgFile):
        pass

    def move(self):
        raise NotImplementedError


class Pawn(Piece):
    """
    This is equivalent to Pawn in chess.
    It is called "Ping" (red) and "Tsuh" (black) meaning a foot soldier.
    5 pieces in each side.
    Moves 1 unit of space forward
    When it crosses the river, it gets options to move left or right as well.
    """

    def __init__(self, side, row, col, imgFile):
        pass

    def move(self):
        raise NotImplementedError