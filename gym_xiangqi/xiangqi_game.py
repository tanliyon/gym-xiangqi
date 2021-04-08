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
    BOARD_Y_OFFSET,               # board y offset
    BOARD_WIDTH, BOARD_HEIGHT     # board width, height
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
        self.sound = None
        self.ally_piece = None
        self.enemy_piece = None
        self.cur_selected = None
        self.ally_turn = True
        self.counter = COUNT
        self.ally_kills = []
        self.enemy_kills = []
        self.cur_selected_pid = 0
        self.end_pos = None
        self.bgm_switch = True
        self.quit = False
        self.compart_color = (153, 102, 75)

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

        # init timer
        # self.init_timer() # hidden for now

        # set caption
        self.screen = pygame.display.set_mode(self.dim)
        pygame.display.set_caption("AI Xiangqi(Chinese Chess)")

        # init board
        self.board_background = self.init_board()

        # load game sound components
        self.init_sound("piece_move.wav", "bgm.wav")

    def on_init_pieces(self, ally_piece, enemy_piece):
        # load piece images
        self.load_piece_images(ally_piece)
        self.load_piece_images(enemy_piece)
        self.ally_piece = ally_piece
        self.enemy_piece = enemy_piece

        # load move_sound and set it to piece objects
        for i in range(1, PIECE_CNT+1):
            self.ally_piece[i].move_sound = self.sound.piece_move
            self.enemy_piece[i].move_sound = self.sound.piece_move

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
        Initialize game sound
        """
        self.sound = Sound(piece_move, bgm)

        # play bgm
        pygame.mixer.music.play(-1)

    def update_pos_next_moves(self):
        if self.cur_selected is None:
            return

        opacity = 128
        cur_sel_basic_img = self.cur_selected.basic_image.copy()
        cur_sel_basic_img.set_alpha(opacity)

        for _, (row, col) in self.cur_selected.legal_moves:
            pygame_y = row*COOR_DELTA + COOR_OFFSET + BOARD_Y_OFFSET
            pygame_x = col*COOR_DELTA + COOR_OFFSET
            self.screen.blit(cur_sel_basic_img, (pygame_x, pygame_y))

    def toggle_bgm(self):
        """
        This is a toggle switch for bgm.
        If self.bgm_switch is True, BGM plays, otherwise it stops.
        """
        self.bgm_switch = not self.bgm_switch
        if self.bgm_switch:
            pygame.mixer.music.play(-1)
        else:
            pygame.mixer.music.stop()

    def update_bgm_state(self):
        """
        Show whether the bgm is on or off
        """
        bgm_text = " BGM(B)"
        bgm_font = pygame.font.SysFont('bradleyhand', 20)
        bgm_state_font = pygame.font.SysFont('bradleyhand', 25)
        border_font = pygame.font.SysFont('bradleyhand', 30)

        if self.bgm_switch:
            color = (230, 100, 100)

            # Write ON in RED
            bgm_state_text = "ON"
            final_text = bgm_state_font.render(bgm_state_text, True, color)
            text_rect = final_text.get_rect(centerx=466, bottom=85)
            self.screen.blit(final_text, text_rect)
        else:
            color = (100, 100, 200)

            # Write ON in BLUE
            bgm_state_text = "OFF"
            final_text = bgm_state_font.render(bgm_state_text, True, color)
            text_rect = final_text.get_rect(centerx=466, bottom=85)
            self.screen.blit(final_text, text_rect)

        # Write BGM(B) in RED or BLUE
        final_text = bgm_font.render(bgm_text, True, color)
        text_rect = final_text.get_rect(centerx=466, bottom=50)
        self.screen.blit(final_text, text_rect)

        # Draw border line in RED or BLUE
        border_text = "|"
        final_text = border_font.render(border_text, True, color)
        text_rect = final_text.get_rect(centerx=WINDOW_WIDTH-100, bottom=60)
        self.screen.blit(final_text, text_rect)
        text_rect = final_text.get_rect(centerx=WINDOW_WIDTH-100, bottom=90)
        self.screen.blit(final_text, text_rect)

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

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_b:
                self.toggle_bgm()

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
        # draw background & compartment lines
        self.draw_background()

        # self.update_timer() # hidden for now
        self.update_kills()
        self.update_bgm_state()
        self.screen.blit(self.board_background, (0, BOARD_Y_OFFSET))

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
        Terminate current game and create a new game
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

    def draw_background(self):
        """
        This method draws the background
        and the compartment lines on the game screen.
        """
        # fill the background with white
        self.screen.fill((255, 255, 255))

        # horizontal compartment lines
        line_info = (0, 0, BOARD_WIDTH, 5)
        self.screen.fill(self.compart_color, line_info)
        line_info = (0, BOARD_Y_OFFSET-5, BOARD_WIDTH, BOARD_HEIGHT+10)
        self.screen.fill(self.compart_color, line_info)
        line_info = (0, WINDOW_HEIGHT-5, BOARD_WIDTH, 5)
        self.screen.fill(self.compart_color, line_info)

        # vertical compartment lines
        line_info = (0, 0, 10, WINDOW_HEIGHT)
        self.screen.fill(self.compart_color, line_info)
        line_info = (WINDOW_WIDTH-10, 0, 10, WINDOW_HEIGHT)
        self.screen.fill(self.compart_color, line_info)

    def load_piece_images(self, pieces: list):
        """
        Load the image files to the corresponding piece objects
        """
        for i in range(1, len(pieces)):
            pieces[i].set_basic_image()
            pieces[i].set_select_image()
            pieces[i].set_mini_image()

    def to_real_coor(self, clicked_coor):
        """
        Convert clicked coordinate to real coordinate
        """
        clicked_real_x = (clicked_coor[0] - COOR_OFFSET) // COOR_DELTA

        adj_y_offset = (COOR_OFFSET + BOARD_Y_OFFSET)
        clicked_real_y = (clicked_coor[1] - adj_y_offset) // COOR_DELTA

        return int(clicked_real_x), int(clicked_real_y)

    def find_target_piece(self, clicked_coor):
        """
        Search for the currently selected piece object
        # if the object is found, return True
        # else, return False
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
        Initialize the timer
        """
        self.time_font = pygame.font.SysFont('cochin', 20)
        self.timer_event = pygame.USEREVENT + 1
        pygame.time.set_timer(self.timer_event, 1000)

    def update_timer(self):
        """
        Update the remaining time and blit
        """
        timer_text = "Timer: " + str(self.counter)
        if self.counter <= 10:
            color = (230, 100, 100)  # Red
        else:
            color = (0, 0, 0)  # Black
        final_text = self.time_font.render(timer_text, True, color)
        text_rect = final_text.get_rect(centerx=460, bottom=720)
        self.screen.blit(final_text, text_rect)

    def init_kills(self):
        """
        Write 'Ally Kills: ' and 'Enemy Kills: ' on screen
        """
        kill_font = pygame.font.SysFont('cochin', 20)

        # Write Ally
        ally_text = "Ally"
        final_text = kill_font.render(ally_text, True, (20, 20, 0))
        text_rect = final_text.get_rect(centerx=55, bottom=740)
        self.screen.blit(final_text, text_rect)

        # Write Enemy
        enemy_text = "Enemy"
        final_text = kill_font.render(enemy_text, True, (20, 20, 0))
        text_rect = final_text.get_rect(centerx=55, bottom=50)
        self.screen.blit(final_text, text_rect)

        # Write Kills
        kill_text = " Kills"
        final_text = kill_font.render(kill_text, True, (20, 20, 0))

        text_rect = final_text.get_rect(centerx=55, bottom=770)
        self.screen.blit(final_text, text_rect)

        text_rect = final_text.get_rect(centerx=55, bottom=80)
        self.screen.blit(final_text, text_rect)

        # Draw border line
        border_font = pygame.font.SysFont('cochin', 30)
        border_text = "|"
        final_text = border_font.render(border_text, True, (20, 20, 0))
        text_rect = final_text.get_rect(centerx=90, bottom=755)
        self.screen.blit(final_text, text_rect)
        text_rect = final_text.get_rect(centerx=90, bottom=775)
        self.screen.blit(final_text, text_rect)
        text_rect = final_text.get_rect(centerx=90, bottom=65)
        self.screen.blit(final_text, text_rect)
        text_rect = final_text.get_rect(centerx=90, bottom=85)
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
        - The x offsets 100 indicate the starting x coordinate on screen.

        - (i * 35) indicates the step size that considers both PIECE_WIDTH
            and proper spacing between the pieces to be listed.

        - Modulo 280 only allows the max number of pieces in each row to 8,
            therefore keeps the listed pieces within the pygame screen.

        y:
        - The y offsets 23 and 713 indicate the starting y coordinate
            for 'Enemy Kills' and 'Ally Kills' respectively on screen.

        - (i // 8) * 35 indicates that every piece in the position of
            multiple of 9 (ex] 9, 18), has to start a new line.
            Otherwise, the pieces will overlap and turn invisible.

        The modulo for y needed not to be set since we have enough spaces
        on the screen to handle the pieces even if they were all dead.
        """
        for i in range(len(self.ally_kills)):
            # keep minimis within the box
            x = 100 + (i * 35) % 280
            y = 713 + (i // 8) * 35
            self.screen.blit(self.ally_kills[i], (x, y))

        for i in range(len(self.enemy_kills)):
            # keep minimis within the box
            x = 100 + (i * 35) % 280
            y = 23 + (i // 8) * 35
            self.screen.blit(self.enemy_kills[i], (x, y))

    def kill_piece(self, real_clicked_coor):
        """
        Kill the enemy piece object in the given coordinate
        """
        for piece_id, enemy in enumerate(self.enemy_piece[1:], 1):
            if real_clicked_coor == enemy.coor and enemy.is_alive():
                enemy.state = DEAD
                break
        return piece_id

    def game_over(self):
        """
        Write the "game over" message on screen and wait for 3 seconds
        """
        game_over = "GAME OVER"
        font = pygame.font.SysFont('impact', 100)
        game_over_text = font.render(game_over, True, (128, 250, 128))
        t_rect = game_over_text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(game_over_text, t_rect)
        pygame.display.update()
        time.sleep(3)
