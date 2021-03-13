import unittest
import random
import string

from gym_xiangqi.envs.xiangqi_env import XiangQiEnv
from gym_xiangqi.constants import (
    BOARD_ROWS, BOARD_COLS,
    RED, BLACK, DEAD,
    ILLEGAL_MOVE, PIECE_POINTS,
    EMPTY, GENERAL, CANNON_1, SOLDIER_3,
    AGENT, ENEMY,
)


class TestXiangQiEnv(unittest.TestCase):

    def setUp(self):
        self.env = XiangQiEnv()

    def test_env_initialization(self):
        self.assertEqual(self.env.agent_color, RED)
        self.assertEqual(self.env.enemy_color, BLACK)

        self.env = XiangQiEnv(agent_color=BLACK)
        self.assertEqual(self.env.agent_color, BLACK)
        self.assertEqual(self.env.enemy_color, RED)

        self.assertIsNone(self.env.game)
        self.assertIsNotNone(self.env.state)
        self.assertIsNotNone(self.env.observation_space)
        self.assertIsNotNone(self.env.action_space)
        self.assertIsNotNone(self.env.agent_actions)
        self.assertIsNotNone(self.env.enemy_actions)

    def test_env_step_invalid_action(self):
        """
        verify action input
        """
        with self.assertRaises(AssertionError):
            # Test using a random negative int.
            action = random.randint(-10000, -1)
            self.env.step(action)

            # Test using a random float.
            action = random.uniform(-10000, 10000)
            self.env.step(action)

            # Test using a random string.
            length = random.randint(0, 15)
            choices = (string.ascii_letters +
                    string.punctuation +
                    string.digits)
            action = "".join(random.choice(choices) for i in range(length))
            self.env.step(action)

    def test_env_step_illegal_move(self):
        """
        verify agent with illegal move
        """
        obs = self.env.state
        new_obs, reward, done, info = self.env.step(0)

        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.assertEqual(obs[i][j], new_obs[i][j])
        self.assertEqual(reward, ILLEGAL_MOVE)
        self.assertEqual(done, False)

    def test_env_step_one_round(self):
        """
        verify one round of agent and enemy turns
        78727: Agent CANNON_1 (7, 1) -> (7, 4)
        75172: Enemy CANNON_1 (2, 7) -> (2, 4)
        """
        actions = [(78727, CANNON_1, (7, 1), (7, 4), 0, ENEMY),
                   (75172, CANNON_1, (2, 7), (2, 4), 0, AGENT)]

        for action, pid, (r1, c1), (r2, c2), points, next_turn in actions:
            obs, reward, done, info = self.env.step(action)
            self.assertEqual(obs[r1][c1], EMPTY)
            self.assertEqual(obs[r2][c2], pid * self.env.turn * -1)
            self.assertEqual(reward, points)
            self.assertEqual(done, False)
            self.assertEqual(self.env.turn, next_turn)

    def test_env_step_reward(self):
        """
        Simulates Agent (red) cannon taking a black soldier
        78727: Agent CANNON_1 (7, 1) -> (7, 4)
        75172: Enemy CANNON_1 (2, 7) -> (2, 4)
        78961: Agent CANNON_1 (7, 4) -> (3, 4)
        """
        actions = [78727, 75172, 78961]
        for action in actions:
            obs, reward, done, info = self.env.step(action)
        self.assertEqual(obs[7][4], EMPTY)
        self.assertEqual(obs[3][4], CANNON_1)
        self.assertEqual(reward, PIECE_POINTS[SOLDIER_3])
        self.assertEqual(done, False)
        self.assertEqual(self.env.enemy_piece[SOLDIER_3].state, DEAD)

    def test_env_step_done(self):
        """
        verify environment termination due to death of black general
        78727: Agent CANNON_1 (7, 1) -> (7, 4)
        75172: Enemy CANNON_1 (2, 7) -> (2, 4)
        78961: Agent CANNON_1 (7, 4) -> (3, 4)
        123966: Enemy SOLDIER_5 (3, 0) -> (4, 0)
        75694: Agent CANNON_1 (3, 4) -> (0, 4) -- takes black general
        """
        actions = [78727, 75172, 78961, 123966, 75694]
        for action in actions:
            obs, reward, done, info = self.env.step(action)
        self.assertEqual(done, True)
        self.assertEqual(reward, PIECE_POINTS[GENERAL])
        self.assertEqual(self.env.enemy_piece[GENERAL].state, DEAD)


if __name__ == "__main__":
    unittest.main()
