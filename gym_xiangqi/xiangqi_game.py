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

    def __init__(self):
        # PyGame components
        self.running = False
        self.winWidth = 900
        self.winHeight = 1000
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
        return True

    def on_event(self, event):
        """
        This routine is triggered when some kind of user/game event is detected
        ex. when user closes the PyGame window
            (mostly any keyboard/mouse input)
        """
        if event.type == pygame.QUIT:
            self.running = False

    def on_update(self):
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
        if self.on_init():
            self.running = True

        # TODO: this is just a high-level overview
        while self.running:
            for event in pygame.event.get():
                self.on_event(event)
            self.on_update()
        self.cleanup()


if __name__ == "__main__":
    # initializing and running the game for manual testing
    from gym_xiangqi.piece import Piece
    myGame = XiangQiGame()
    myGame.on_init()
    myGame.run()
