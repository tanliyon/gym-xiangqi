import time

import pygame

from gym_xiangqi.sound import Sound
from gym_xiangqi.board import Board
from gym_xiangqi.constants import (
    COOR_DELTA, COOR_OFFSET,      # variables for coordinate conversion
    DEAD,                         # dead state for piece object
    WINDOW_WIDTH, WINDOW_HEIGHT,  # window size for pygame display
    FPS,                          # fps for pygame while loop
    COUNT,                        # initial time for timer
    PIECE_CNT,                    # total number of pieces in each side
)


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
        self.dim = (WINDOW_WIDTH, WINDOW_HEIGHT)
        self.display_surf = None
        self.ally_piece = None
        self.enemy_piece = None
        self.cur_selected = None
        self.ally_turn = True
        self.counter = COUNT
        self.ally_kills = []
        self.enemy_kills = []
        self.cur_selected_pid = 0
        self.end_pos = None
        self.quit = False

    def on_init(self, ally_piece, enemy_piece):
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

        # init timer
        self.init_timer()

        # set caption
        self.screen = pygame.display.set_mode(self.dim)
        pygame.display.set_caption("AI Xiangqi(Chinese Chess)")

        # init board
        self.board_background = self.init_board()

        # load piece images
        self.load_piece_images(ally_piece)
        self.load_piece_images(enemy_piece)
        self.ally_piece = ally_piece
        self.enemy_piece = enemy_piece

        # play bgm
        self.init_sound("piece_move.wav", "bgm.wav")

        return True

    def init_board(self):
        '''
        Initializes Board() and load the board image
        '''
        # set board_background
        board = Board()
        board_image = pygame.transform.scale(
            board.board_background, (board.boardWidth, board.boardHeight)
        )
        return board_image

    def init_sound(self, piece_move, bgm):
        """
        initialize game sound
        """
        sound = Sound(piece_move, bgm)

        # play bgm
        pygame.mixer.music.play(-1)

        # load move_sound and set it to piece objects
        for i in range(1, PIECE_CNT+1):
            self.ally_piece[i].move_sound = sound.piece_move
            self.enemy_piece[i].move_sound = sound.piece_move

    def update_pos_next_moves(self):
        if self.cur_selected is None:
            return

        opacity = 128
        cur_sel_basic_img = self.cur_selected.basic_image.copy()
        cur_sel_basic_img.set_alpha(opacity)

        for _, (row, col) in self.cur_selected.legal_moves:
            pygame_y = row*COOR_DELTA + COOR_OFFSET
            pygame_x = col*COOR_DELTA + COOR_OFFSET
            self.screen.blit(cur_sel_basic_img, (pygame_x, pygame_y))

    def on_event(self, event):
        """
        This routine is triggered when some kind of user/game event is detected
        ex. when user closes the PyGame window
            (mostly any keyboard/mouse input)

        Parameter:
            event: PyGame event object that represents keyboard inputs, mouse
                   inputs and etc.
        """
        if event.type == pygame.QUIT:
            self.running = False
            self.quit = True

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # clicked: 1 not_clicked: 0
            left_clicked = pygame.mouse.get_pressed()[0]

            if left_clicked:
                # get clicked coordinate
                clicked_x, clicked_y = pygame.mouse.get_pos()
                clicked_coor = (clicked_x, clicked_y)

                # select any ally pieces that is in the clicked range
                self.find_target_piece(clicked_coor)

                # if another click is made while an ally piece is selected,
                # this must be a piece movement
                if self.cur_selected is not None:
                    # convert to real coordinate
                    real_clicked_coor = self.to_real_coor(clicked_coor)

                    # define the piece movement as start to end position
                    s = [self.cur_selected.row, self.cur_selected.col]
                    e = list(real_clicked_coor[::-1])

                    # validate the piece movement
                    is_legal = (s, e) in self.cur_selected.legal_moves

                    if is_legal:
                        self.end_pos = tuple(real_clicked_coor[::-1])

                        # reset counter after ally turn is over
                        self.counter = COUNT

                        # reset piece selection and end my turn
                        self.cur_selected = None
                        self.running = False
        """
        # timer decrement every second
        elif event.type == pygame.USEREVENT + 1:
            self.counter -= 1

            # timeout event
            if self.counter == 0:
                self.running = False
        """

    def on_update(self):
        pass

    def render(self):
        """
        Render current game state into graphics
        """
        # draw white background, board, timer, and pieces consecutively
        self.screen.fill((250, 250, 250))
        self.update_timer()
        self.update_kills()
        self.screen.blit(self.board_background, (0, 0))

        # update all cur positions of pieces
        for i in range(1, len(self.ally_piece)):
            if self.ally_piece[i].is_alive():
                self.screen.blit(self.ally_piece[i].basic_image,
                                 self.ally_piece[i].get_pygame_coor())
            if self.enemy_piece[i].is_alive():
                self.screen.blit(self.enemy_piece[i].basic_image,
                                 self.enemy_piece[i].get_pygame_coor())

        # if a piece is selected and alive, load select_image instead
        if self.cur_selected is not None and self.cur_selected.is_alive():
            self.screen.blit(self.cur_selected.select_image,
                             self.cur_selected.get_pygame_coor())

        self.update_pos_next_moves()
        self.render_kills()

        # draw all on screen
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
        clock = pygame.time.Clock()
        self.running = True

        while self.running:
            clock.tick(FPS)
            for event in pygame.event.get():
                self.on_event(event)
            self.render()

    def load_piece_images(self, pieces: list):
        """
        load the image files to the corresponding piece objects
        """
        for i in range(1, len(pieces)):
            pieces[i].set_basic_image()
            pieces[i].set_select_image()
            pieces[i].set_mini_image()

    def to_real_coor(self, clicked_coor):
        """
        convert clicked coordinate to real coordinate
        """
        clicked_real_x = (clicked_coor[0] - COOR_OFFSET) // COOR_DELTA
        clicked_real_y = (clicked_coor[1] - COOR_OFFSET) // COOR_DELTA

        return clicked_real_x, clicked_real_y

    def find_target_piece(self, clicked_coor):
        """
        search for the currently selected piece object
        if the object is found, return True
        if not, return False
        """
        # get clicked coordinate
        clicked_x, clicked_y = clicked_coor

        # find the piece where the clicked coord is within its range
        for piece_id, piece in enumerate(self.ally_piece[1:], 1):
            if piece.state == DEAD:
                continue

            piece_x, piece_y = piece.get_pygame_coor()

            x_min = piece_x - piece.piece_width/2 + 25
            x_max = piece_x + piece.piece_width/2 + 25

            valid_x = x_min < clicked_x < x_max

            y_min = piece_y - piece.piece_height/2 + 25
            y_max = piece_y + piece.piece_height/2 + 25

            valid_y = y_min < clicked_y < y_max

            # if the clicked coord is within the piece range, select it
            if valid_x and valid_y:
                self.cur_selected = piece
                self.cur_selected_pid = piece_id
                break

    def init_timer(self):
        """
        initialize the timer
        """
        self.font = pygame.font.SysFont(None, 40)
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)

    def update_timer(self):
        """
        update the remaining time and blit
        """
        timer_text = "timer: " + str(self.counter)
        final_text = self.font.render(timer_text, True, (128, 128, 0))
        text_rect = final_text.get_rect(centerx=665, bottom=50)
        self.screen.blit(final_text, text_rect)

    def init_kills(self):
        """
        write 'ally kills: ' and 'enemy kills: ' on screen
        """
        self.kill_font = pygame.font.SysFont(None, 40)

        kill_text = "ally kills: "
        final_text = self.kill_font.render(kill_text, True, (128, 128, 0))
        text_rect = final_text.get_rect(centerx=610, bottom=350)
        self.screen.blit(final_text, text_rect)

        kill_text = "enemy kills: "
        final_text = self.kill_font.render(kill_text, True, (128, 128, 0))
        text_rect = final_text.get_rect(centerx=610, bottom=150)
        self.screen.blit(final_text, text_rect)

    def update_kills(self):
        """
        update the kills for both side
        """
        self.init_kills()

        self.ally_kills = ([enemy.mini_image for enemy in self.enemy_piece[1:]
                            if enemy.state == DEAD])
        self.enemy_kills = ([ally.mini_image for ally in self.ally_piece[1:]
                            if ally.state == DEAD])

    def render_kills(self):
        """
        This method renders capture logs for both sides.

        The coordinates (x,y) with in GUI are determined based on the number
        of current kills that the ally or the enemy side has during the game.

        These are implemented in two different loops because
        the number of dead pieces on both sides may differ during the game.

        x:
        - The x offsets 530 indicate the starting x coordinate on screen.

        - (i * 35) indicates the step size that considers both PIECE_WIDTH
            and proper spacing between the pieces to be listed.

        - Modulo 245 is from the following calculation.
            (WINDOW_WIDTH - BOARD_WIDTH - PIECE_WIDTH/2 - 5).
            This modulo only allows the max number of pieces in each row to 7,
            therefore keeps the listed pieces within the pygame screen.

        y:
        - The y offsets 360 and 160 indicate the starting y coordinate
            for 'ally kills' and 'enemy kills' respectively on screen.

        - (i // 7) * 35 indicates that every piece in the position of
            multiple of 8 (ex] 8, 16), has to start a new line.
            Otherwise, the pieces will overlap and turn invisible.

        The modulo for y needed not to be set since we have enough spaces
        on the screen to handle the pieces even if they were all dead.
        """
        for i in range(len(self.ally_kills)):
            # keep minimis within the box
            x = 530 + (i * 35) % 245
            y = 360 + (i // 7) * 35
            self.screen.blit(self.ally_kills[i], (x, y))

        for i in range(len(self.enemy_kills)):
            # keep minimis within the box
            x = 530 + (i * 35) % 245
            y = 160 + (i // 7) * 35
            self.screen.blit(self.enemy_kills[i], (x, y))

    def kill_piece(self, real_clicked_coor):
        """
        kill the enemy piece object in the given coordinate
        """
        for piece_id, enemy in enumerate(self.enemy_piece[1:], 1):
            if real_clicked_coor == enemy.coor and enemy.is_alive():
                enemy.state = DEAD
                break
        return piece_id

    def game_over(self):
        """
        write the "game over" message on screen and wait for 3 seconds
        """
        game_over = "GAME OVER"
        font = pygame.font.SysFont(None, 100)
        game_over_text = font.render(game_over, True, (128, 250, 128))
        t_rect = game_over_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(game_over_text, t_rect)
        pygame.display.update()
        time.sleep(3)
