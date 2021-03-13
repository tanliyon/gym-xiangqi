from agents.random_agent import RandomAgent
from gym_xiangqi.constants import AGENT, PIECE_ID_TO_NAME
from gym_xiangqi.utils import action_space_to_move

import gym
import time


def test_random_agent_play_itself():
    """
    Test integration between agent and env by
    playing a game against itself.
    """
    env = gym.make('gym_xiangqi:xiangqi-v0')
    agent = RandomAgent()

    done = False
    while not done:
        action = agent.move(env)
        _, _, done, _ = env.step(action)
    env.close()
