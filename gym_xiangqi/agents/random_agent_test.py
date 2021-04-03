import gym
import pytest

from gym_xiangqi.agents import RandomAgent
from gym_xiangqi.constants import (
    EMPTY, ADVISOR_1
)


@pytest.fixture
def agent():
    """
    Create the agent which returns random moves.
    """
    return RandomAgent()


@pytest.fixture
def legal_env(mocker):
    """
    Create an environment where the game is
    still ongoing and there are possible actions.
    """
    env = gym.make('gym_xiangqi:xiangqi-v0')
    env.ally_actions.fill(0)
    # id: 2 (ADVISOR_1), start: [9, 3], end: [8, 4]
    env.ally_actions[15736] = 1
    return env


def test_make_legal_move(agent, legal_env):
    action = agent.move(legal_env)
    assert legal_env.action_space.contains(action)
    assert legal_env.ally_actions[action] == 1

    state, reward, done, _ = legal_env.step(action)
    assert state[9][3] == EMPTY
    assert state[8][4] == ADVISOR_1
    assert reward == 0
    assert done is False
