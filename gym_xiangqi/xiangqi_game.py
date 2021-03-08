import pygame

from gym_xiangqi.board import Board


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
        self.FPS = 30   # for frame control in loop
        self.winWidth = 521
        self.winHeight = 577
        self.boardWidth = 521
        self.boardHeight = 577
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
        # set board_background
        board = Board().board_background
        board = pygame.transform.scale(
            board, (self.boardWidth, self.boardHeight)
        )

        return board

    def on_event(self, event):
        """
        This routine is triggered when some kind of user/game event is detected
        ex. when user closes the PyGame window
            (mostly any keyboard/mouse input)
        """
        if event.type == pygame.QUIT:
            self.running = False

    def on_update(self):
        pass

    def render(self):
        """
        Render current game state into graphics
        """
        # draw board
        self.screen.blit(self.board_background, (0, 0))

        # update all cur positions of pieces
        # used separated loops because the number of pieces may differ
        for i in range(1, len(self.agent_piece)):
            if self.agent_piece[i].is_alive():
                self.screen.blit(self.agent_piece[i].basic_image,
                                 self.agent_piece[i].get_pygame_coor())
            if self.enemy_piece[i].is_alive():
                self.screen.blit(self.enemy_piece[i].basic_image,
                                 self.enemy_piece[i].get_pygame_coor())

        if self.cur_selected is not None and self.cur_selected.is_alive():
            self.screen.blit(self.cur_selected.select_image,
                             self.cur_selected.get_pygame_coor())

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

    def load_piece_images(self, pieces: list):
        for i in range(1, len(pieces)):
            pieces[i].set_basic_image()
            pieces[i].set_select_image()


if __name__ == "__main__":
    # initializing and running the game for manual testing
    from gym_xiangqi.envs import XiangQiEnv
    env = XiangQiEnv()
    env.render()
    env.game.run()
