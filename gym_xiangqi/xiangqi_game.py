import pygame
import os
from gym_xiangqi.constants import BLACK, RED
from gym_xiangqi.board import Board
from gym_xiangqi.piece import General, Advisor, Elephant
from gym_xiangqi.piece import Horse, Chariot, Cannon, Soldier


import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

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
        self.FPS = 30  #for frame control in loop
        self.winWidth = 521
        self.winHeight = 577
        self.boardWidth = 521
        self.boardHeight = 577
        self.piece_width = 58
        self.piece_height = 58
        self.dim = (self.winWidth, self.winHeight)
        self.display_surf = None
        self.agent_piece = None
        self.enemy_piece = None
        self.cur_selected = None

    def on_init(self, agent_piece, enemy_piece):
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

        # set caption
        self.screen = pygame.display.set_mode(self.dim)
        pygame.display.set_caption("AI Xiangqi(Chinese Chess) Game")

        # init board
        self.board_background = self.init_board()

        # load piece images
        self.load_piece_images(agent_piece)
        self.load_piece_images(enemy_piece)
        self.agent_piece = agent_piece
        self.enemy_piece = enemy_piece

        return True

    def init_board(self):

        #set board_background
        board = Board().board_background
        board = pygame.transform.scale(board, (self.boardWidth, self.boardHeight))

        return board
        
    def on_event(self, event):
        """
        This routine is triggered when some kind of user/game event is detected
        ex. when user closes the PyGame window
            (mostly any keyboard/mouse input)
        """
        if event.type == pygame.QUIT:
            self.running = False

        # elif event.type == pygame.MOUSEBUTTONDOWN:

        #     if self.agent_turn: #!@

        #         is_left_clicked = pygame.mouse.get_pressed()[0] #clicked: 1 not_clicked: 0
                
        #         if is_left_clicked:

        #             self.clicked_x, self.clicked_y = pygame.mouse.get_pos()
        #             self.clicked_coor = (self.click_x, self.click_y)

        #             if self.clicked_coor in self.r_pieces:
                        
        #                 self.target_piece = self.get_target_piece(self.clicked_coor) #identify the piece
        #                 self.target_piece.image = self.load_selected_image(Piece) #switch to the image for the selected piece

        #             elif self.target_piece != None and self.can_it_move(self.target_piece, self.clicked_coor):
                        
        #                 self.target_piece.set_new_pos(self.clicked_coor) #update piece_coord
        #                 self.target_piece = None #reset target selection
        #                 self.agent_turn = False #turn switch

    def on_update(self):
        pass
    # get list of Piece objects and draw on board
    def render(self):
        """
        Render current game state into graphics
        """
        # draw board
        self.screen.blit(self.board_background, (0, 0)) 
        
        # update all cur positions of pieces 
        # used separated loops because the number of pieces may differ
        for i in range(1, len(self.agent_piece)):
            
            if self.agent_piece[i].is_alive:
                self.screen.blit(self.agent_piece[i].basic_image, self.agent_piece[i].get_pygame_coor())
            if self.enemy_piece[i].is_alive:
                self.screen.blit(self.enemy_piece[i].basic_image, self.enemy_piece[i].get_pygame_coor())

        if self.cur_selected is not None and self.cur_selected.is_alive:
            self.screen.blit(self.cur_selected.select_image, self.cur_selected.get_pygame_coor())


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
        if self.on_init(self.agent_piece, self.enemy_piece):
            clock = pygame.time.Clock()
            self.running = True

        # TODO: this is just a high-level overview
        while self.running:
            clock.tick(self.FPS)
            for event in pygame.event.get():
                self.on_event(event)
        
            self.render()

        self.cleanup()

# -----------------------------temp init_pieces before link to envs-------------------------------------------- #
    def load_image(self, filename:str, color:int):

        file_path = os.path.split(os.path.relpath(__file__))[0]
        sub_path = "/images/black_pieces/" if color else "/images/red_pieces/"
        file_path += sub_path
        target_file = file_path + filename
        try:
            image = pygame.image.load(target_file).convert_alpha()
            image = pygame.transform.scale(image, (self.piece_width, self.piece_height))
        except pygame.error:
            raise SystemExit('Image Load Failure: "%s" %s' %(target_file, pygame.get_error()))
        return image

    def set_basic_image(self, name:str, color:int): 
        filename = name + ".PNG"
        return self.load_image(filename, color)

    def set_select_image(self, name:str, color:int):
        filename = name + "_S.PNG"
        return self.load_image(filename, color)

    def load_piece_images(self, pieces: list):
        
        for i in range(len(pieces)):
            
            if  isinstance(pieces[i], General):
                pieces[i].basic_image = self.set_basic_image(name="GEN", color=pieces[i].color)
                pieces[i].select_image = self.set_select_image(name="GEN", color=pieces[i].color)
            elif isinstance(pieces[i], Advisor):
                pieces[i].basic_image = self.set_basic_image(name="ADV", color=pieces[i].color)
                pieces[i].select_image = self.set_select_image(name="ADV", color=pieces[i].color)
            elif isinstance(pieces[i], Elephant):
                pieces[i].basic_image = self.set_basic_image(name="ELE", color=pieces[i].color)
                pieces[i].select_image = self.set_select_image(name="ELE", color=pieces[i].color)
            elif isinstance(pieces[i], Horse):
                pieces[i].basic_image = self.set_basic_image(name="HRS", color=pieces[i].color)
                pieces[i].select_image = self.set_select_image(name="HRS", color=pieces[i].color)
            elif isinstance(pieces[i], Chariot):
                pieces[i].basic_image = self.set_basic_image(name="CHR", color=pieces[i].color)
                pieces[i].select_image = self.set_select_image(name="CHR", color=pieces[i].color)
            elif isinstance(pieces[i], Cannon):
                pieces[i].basic_image = self.set_basic_image(name="CAN", color=pieces[i].color)
                pieces[i].select_image = self.set_select_image(name="CAN", color=pieces[i].color)
            elif isinstance(pieces[i], Soldier):
                pieces[i].basic_image = self.set_basic_image(name="SOL", color=pieces[i].color)
                pieces[i].select_image = self.set_select_image(name="SOL", color=pieces[i].color)


#-------------------------------------end--------------------------------------------#

if __name__ == "__main__":
    # initializing and running the game for manual testing
    from gym_xiangqi.envs import XiangQiEnv
    env = XiangQiEnv()
    env.game.run()
    #myGame = XiangQiGame()
    #myGame.on_init()
    #myGame.run()
