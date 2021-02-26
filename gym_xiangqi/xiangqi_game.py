from gym_xiangqi.pieces import King, Queen, Bishop, Knight, Rook, Cannon, Pawn
import random
import pygame


class XiangQiGame:
    """
    This class represents the Xiangqi game using PyGame.
    It is also a medium in which different components interact as a whole.
    For example, rendering the game graphics, taking user input from the game
    and providing information necessary for our XiangQiEnv class to function as
    reinforcement learning environment are all communicated and integrated
    through this class.
    """

    boardCols = 9
    boardRows = 10
    classMap = {                # mapping of piece name to class constructor
        "king": King,
        "queen": Queen,
        "bishop": Bishop,
        "knight": Knight,
        "rook": Rook,
        "cannon": Cannon,
        "pawn": Pawn
    }
    pieceCount = {          # mapping of piece name to piece counts
        "king": 1,
        "queen": 2,
        "bishop": 2,
        "knight": 2,
        "rook": 2,
        "cannon": 2,
        "pawn": 5
    }
    agentCoord = {          # mapping of piece name to agent initial positions
        "king": [(9, 4)],
        "queen": [(9, 3), (9, 5)],
        "bishop": [(9, 2), (9, 6)],
        "knight": [(9, 1), (9, 7)],
        "rook": [(9, 0), (9, 8)],
        "cannon": [(7, 1), (7, 7)],
        "pawn": [(6, 0), (6, 2), (6, 4), (6, 6), (6, 8)]
    }
    enemyCoord = {          # mapping of piece name to enemy initial positions
        "king": [(0, 4)],
        "queen": [(0, 3), (0, 5)],
        "bishop": [(0, 2), (0, 6)],
        "knight": [(0, 1), (0, 7)],
        "rook": [(0, 0), (0, 8)],
        "cannon": [(2, 1), (2, 7)],
        "pawn": [(3, 0), (3, 2), (3, 4), (3, 6), (3, 8)]
    }

    def __init__(self):
        # Xiangqi components
        self.board = [
          [None for _ in range(self.boardCols)] for _ in range(self.boardRows)
        ]
        self.agentColor = random.randint(0, 1)
        self.enemyColor = 0 if self.agentColor == 1 else 1
        self.initAllPieces()

        # PyGame components
        self.running = False
        self.winWidth = 900
        self.winHeight = 1000
        self.dim = (self.winWidth, self.winHeight)
        self.display_surf = None

    def initAllPieces(self):
        # initialize agent and enemy pieces and place them on the board
        for piece, pieceClass in self.classMap.items():
            for i in range(self.pieceCount[piece]):
                r = self.agentCoord[piece][i][0]
                c = self.agentCoord[piece][i][1]
                self.board[r][c] = pieceClass(self.agentColor, row=r, col=c)

                r = self.enemyCoord[piece][i][0]
                c = self.enemyCoord[piece][i][1]
                self.board[r][c] = pieceClass(self.enemyColor, row=r, col=c)

    def onInit(self):
        """
        Initialize/start the game with PyGame
        ex. pygame.init()
            (anything related to PyGame module that needs to be initialized)
        """
        pygame.init()
        self.display_surf = pygame.display.set_mode(
            self.dim,
            pygame.HWSURFACE | pygame.DOUBLEBUF
        )

        pygame.display.set_caption("AI Xiangqi(Chinese Chess) Game")

        return True

    def onEvent(self, event):
        """
        This routine is triggered when some kind of user/game event is detected
        ex. when user closes the PyGame window
            (mostly any keyboard/mouse input)
        """
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == MOUSEBUTTONDOWN:

            if self.agent_turn:
                is_left_clicked = pygame.mouse.get_pressed()[0] #clicked: 1 not_clicked: 0
                
                if is_left_clicked:
                    self.clicked_x, self.clicked_y = pygame.mouse.get_pos()
                    self.clicked_coor = (self.click_x, self.click_y)

                    if self.clicked_coor in agentCoord:
                        self.target_piece = self.clicked_coor
                        #identify the piece
                        #load the object's valid_next_moves

                    elif self.target_piece != None and self.clicked_coor in self.target_piece.valid_next_moves:
                        #change object coordinates
                        self.target_piece = None #reset target selection
                        self.agent_turn = False #turn switch

                    else:
                        pass



    def onUpdate(self):
        """
        Relfect detected changes and update game states
        """
        pass

    def render(self):
        """
        Render current game state into graphics
        """
        pass

    def cleanup(self):
        """
        Free resources and exit the game and
        """
        pygame.quit()

    def reset(self):
        """
        terminate current game and create a new game
        """
        pass

    def run(self):
        """
        Run the game until terminating condition is achieved
        """
        if self.onInit():
            self.running = True

        # TODO: this is just a high-level overview
        while self.running:
            for event in pygame.event.get():
                self.onEvent(event)
            self.onUpdate()
        self.cleanup()


if __name__ == "__main__":
    # initializing and running the game for manual testing
    myGame = XiangQiGame()
    myGame.onInit()
    myGame.run()
