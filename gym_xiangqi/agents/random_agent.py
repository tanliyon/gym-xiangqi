import numpy as np
import random

from gym_xiangqi.constants import ALLY


class RandomAgent:
    """
    This is the implementation of the simplest
    agent possible to play the game of Xiang Qi.
    The agent will simply choose a random move
    out of all the possible moves and return that.
    """
    def __init__(self):
        pass

    def move(self, env):
        """
        Make a random move based on the environment.
        """
        actions = (env.ally_actions if env.turn == ALLY
                   else env.enemy_actions)
        legal_moves = np.where(actions == 1)[0]
        ind = random.randint(0, len(legal_moves)-1)
        return legal_moves[ind]
