from random_agent import RandomAgent

import gym
import pytest
from pytest_mock import mocker


@pytest.fixture
def agent():
    """
    Create the agent which returns random moves.
    """
    return RandomAgent()


@pytest.fixture
def ongoing_env(mocker):
    """
    Create an environment where the game is
    still ongoing and there are possible actions.
    """
    def mock_possible_actions(self):
        return [
            ((2, 4), (1, 3)),
            ((5, 2), (5, 4)),
            ((1, 6), (3, 3)),
        ]
    mocker.patch(
        "gym_xiangqi.envs.XiangQiEnv.get_possible_actions",
        mock_possible_actions)
    env = gym.make('gym_xiangqi:xiangqi-v0')
    return env


@pytest.fixture
def ended_env(mocker):
    """
    Create an environment where the game has already
    ended and there's no possible actions.
    """
    def mock_possible_actions(self):
        return []
    mocker.patch(
        "gym_xiangqi.envs.XiangQiEnv.get_possible_actions",
        mock_possible_actions)
    env = gym.make('gym_xiangqi:xiangqi-v0')
    return env


def test_make_valid_move(agent, ongoing_env):
    action = agent.move(ongoing_env)
    assert action in ongoing_env.get_possible_actions()


def test_no_error_when_no_valid_move(agent, ended_env):
    action = agent.move(ended_env)
    assert action is None
