from gym_xiangqi.agents import RandomAgent

import gym

MAX_ROUNDS = 500


def test_random_agent_play_itself():
    """
    Test integration between agent and env by
    playing a game against itself.
    """
    env = gym.make('gym_xiangqi:xiangqi-v0')
    agent = RandomAgent()

    done = False
    round_count = 0
    while not done:
        action = agent.move(env)
        _, _, done, _ = env.step(action)
        round_count += 1
        if round_count > MAX_ROUNDS:
            break
    env.close()
