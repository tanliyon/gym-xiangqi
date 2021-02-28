import pygame
from gym_xiangqi.board import Board
from gym_xiangqi.piece import Piece, General, Advisor, Elephant
from gym_xiangqi.piece import Horse, Chariot, Cannon, Soldier
class XiangQiGame:
    """
    This class represents the Xiangqi game using PyGame.
    It is also a medium in which different components interact as a whole.
    For example, rendering the game graphics, taking user input from the game
    and providing information necessary for our XiangQiEnv class to function as
    reinforcement learning environment are all communicated and integrated
    through this class.
    """

    def __init__(self):
        # PyGame components
        self.running = True
        self.winWidth = 600
        self.winHeight = 600
        self.boardWidth = 600
        self.boardHeight = 600
        self.dim = (self.winWidth, self.winHeight)
        self.display_surf = None

    def on_init(self):
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

        #set caption
        self.screen = pygame.display.set_mode(self.dim)
        pygame.display.set_caption("AI Xiangqi(Chinese Chess) Game")

        #init board
        self.board_background = self.init_board()

        #init pieces
        self.pieces = self.update_pieces()

    def init_board(self):

        #set board_background
        board = Board().board_background
        board = pygame.transform.scale(board, (self.boardWidth, self.boardHeight))

        return board

    def update_pieces(self):
        #get cur positions of pieces
        #return a list objects
        pass

    def on_event(self, event):
        """
        This routine is triggered when some kind of user/game event is detected
        ex. when user closes the PyGame window
            (mostly any keyboard/mouse input)
        """
        if event.type == pygame.QUIT:
            self.running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if self.agent_turn:

                is_left_clicked = pygame.mouse.get_pressed()[0] #clicked: 1 not_clicked: 0
                
                if is_left_clicked:

                    self.clicked_x, self.clicked_y = pygame.mouse.get_pos()
                    self.clicked_coor = (self.click_x, self.click_y)

                    cur_agent_coors = self.get_cur_agent_coors() #get all current coordinates of the agent pieces
                    if self.clicked_coor in cur_agent_coors:
                        
                        self.target_piece = self.get_target_piece(self.clicked_coor) #identify the piece
                        self.target_piece.image = self.load_selected_image(Piece) #switch to the image for the selected piece

                    elif self.target_piece != None and self.can_it_move(self.target_piece, self.clicked_coor):
                        
                        self.target_piece.set_new_pos(self.clicked_coor) #update piece_coord
                        self.target_piece = None #reset target selection
                        self.agent_turn = False #turn switch

    def on_update(self):
        """
        Relfect detected changes and update game states
        """
        self.update_pieces()

    def render(self):
        """
        Render current game state into graphics
        """

        self.screen.blit(self.board_background, (0, 0)) #draw board

        #update all cur positions of pieces
        #for piece in self.pieces:
        #    self.screen.blit(piece, (piece.col, piece.get_cur_coor()))

        pygame.display.update()

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
        if self.on_init():
            self.running = True

        # TODO: this is just a high-level overview
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            
            self.on_update()
            self.render()


        self.cleanup()


if __name__ == "__main__":
    # initializing and running the game for manual testing
    myGame = XiangQiGame()
    myGame.on_init()
    myGame.run()


    
