from agents.random_agent import RandomAgent

import gym


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
