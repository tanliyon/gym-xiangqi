import random


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
        actions = env.get_possible_actions()
        # Return None if there are no valid actions.
        if not actions:
            return None
        random_index = random.randint(0, len(actions)-1)
        return actions[random_index]
        

