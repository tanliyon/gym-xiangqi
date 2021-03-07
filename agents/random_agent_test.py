import gym
import pytest

from random_agent import RandomAgent
from gym_xiangqi.constants import (
    EMPTY, ADVISOR_1, ILLEGAL_MOVE,
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
    def mock_possible_actions(self):
        return 15736    # id: 2, start: [9, 3], end: [8, 4]
    mocker.patch(
        "gym.spaces.Discrete.sample",
        mock_possible_actions)
    env = gym.make('gym_xiangqi:xiangqi-v0')
    return env


@pytest.fixture
def illegal_env(mocker):
    """
    Create an environment where the game returns an illegal
    move out of action space.
    """
    def mock_possible_actions(self):
        return 15734    # id: 2, start: [9, 3], end: [8, 2]
    mocker.patch(
        "gym.spaces.Discrete.sample",
        mock_possible_actions)
    env = gym.make('gym_xiangqi:xiangqi-v0')
    return env


def test_make_legal_move(agent, legal_env):
    action = agent.move(legal_env)
    assert legal_env.action_space.contains(action)
    assert legal_env.agent_actions[action] == 1

    state, reward, done, _ = legal_env.step(action)
    assert state[9][3] == EMPTY
    assert state[8][4] == ADVISOR_1
    assert reward == 0
    assert done is False


def test_make_illegal_move(agent, illegal_env):
    action = agent.move(illegal_env)
    assert illegal_env.action_space.contains(action)
    assert illegal_env.agent_actions[action] == 0

    state, reward, done, _ = illegal_env.step(action)
    assert state[9][3] == ADVISOR_1
    assert state[8][2] == EMPTY
    assert reward == ILLEGAL_MOVE
    assert done is False
