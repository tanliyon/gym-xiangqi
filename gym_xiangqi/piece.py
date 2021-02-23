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
    red = 0
    black = 1
    dead = 0
    alive = 1

    def __init__(self, color, row, col):
        self.color = color
        self.row = row
        self.col = col
        self.state = Piece.alive
        self.image = None

    def move(self, new_row, new_col):
        """
        Take one move among given piece's allowed moves
        Update piece's coordinates internally
        """
        self.row = new_row
        self.col = new_col


class General(Piece):
    """
    This piece is equivalent to King. It is called "Jiang" or "Shuai"
    meaning Governor (red) and General (black) respectively.
    - Only one piece exists in each side
    - Can only move 1 unit of space orthogonally within the special square area
    """

    def __init__(self, color, row, col):
        super(General, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


class Advisor(Piece):
    """
    This piece is called "Shi" meaning advisor/scholar.
    - 2 pieces exist in each side
    - Can only move 1 unit of space diagonally within the special square area
    """

    def __init__(self, color, row, col):
        super(Advisor, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


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
        # TODO: add image for pygame rendering
        #  self.image =


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
        # TODO: add image for pygame rendering
        #  self.image =


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
        # TODO: add image for pygame rendering
        #  self.image =


class Cannon(Piece):
    """
    It is called "Pao" meaning cannon or catapult.
    2 pieces in each side.
    It moves similar to a Rook. The difference is, it has to jump over
    ONE piece (enemy or foe) to capture enemy piece.
    """

    def __init__(self, color, row, col):
        super(Cannon, self).__init__(color, row, col)
        # TODO: add image for pygame rendering
        #  self.image =


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
        # TODO: add image for pygame rendering
        #  self.image =
