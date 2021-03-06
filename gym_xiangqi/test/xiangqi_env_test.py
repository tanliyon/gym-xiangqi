import unittest

from gym_xiangqi.envs.xiangqi_env import XiangQiEnv
from gym_xiangqi.constants import (
    BOARD_ROWS, BOARD_COLS,
    RED, BLACK, DEAD,
    ILLEGAL_MOVE, PIECE_POINTS,
    EMPTY, GENERAL, CANNON_1, SOLDIER_3,
    AGENT, ENEMY,
)


class TestXiangQiEnv(unittest.TestCase):

    def test_env_initialization(self):
        env = XiangQiEnv(agent_color=RED)
        self.assertEqual(env.agent_color, RED)
        self.assertEqual(env.enemy_color, BLACK)

        env = XiangQiEnv(agent_color=BLACK)
        self.assertEqual(env.agent_color, BLACK)
        self.assertEqual(env.enemy_color, RED)

        self.assertIsNotNone(env.game)
        self.assertIsNotNone(env.state)
        self.assertIsNotNone(env.observation_space)
        self.assertIsNotNone(env.action_space)
        self.assertIsNotNone(env.agent_actions)
        self.assertIsNotNone(env.enemy_actions)

    def test_env_step(self):
        env = XiangQiEnv()

        # verify action input
        with self.assertRaises(AssertionError):
            env.step(-1)

        # verify agent with illegal move
        obs = env.state
        new_obs, reward, done, info = env.step(0)

        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.assertEqual(obs[i][j], obs[i][j])
        self.assertEqual(reward, ILLEGAL_MOVE)
        self.assertEqual(done, False)

        # verify one round of agent and enemy turns
        actions = [(78727, CANNON_1, (7, 1), (7, 4), 0, ENEMY),
                   (75172, CANNON_1, (2, 7), (2, 4), 0, AGENT)]

        for action, pid, (r1, c1), (r2, c2), points, next_turn in actions:
            obs, reward, done, info = env.step(action)
            self.assertEqual(obs[r1][c1], EMPTY)
            self.assertEqual(obs[r2][c2], pid * env.turn * -1)
            self.assertEqual(reward, points)
            self.assertEqual(done, False)
            self.assertEqual(env.turn, next_turn)

        # verify points reward when taking opponent's piece
        action = 78961      # Agent CANNON_1 (7, 4) -> (3, 4)
        obs, reward, done, info = env.step(action)
        self.assertEqual(obs[7][4], EMPTY)
        self.assertEqual(obs[3][4], CANNON_1)
        self.assertEqual(reward, PIECE_POINTS[SOLDIER_3])
        self.assertEqual(done, False)
        self.assertEqual(env.enemy_piece[SOLDIER_3].state, DEAD)

        # verify environment termination due to death of black general
        for action in [123966, 75694]:  # first move has no particular meaning
            obs, reward, done, info = env.step(action)
        self.assertEqual(done, True)
        self.assertEqual(reward, PIECE_POINTS[GENERAL])
        self.assertEqual(env.enemy_piece[GENERAL].state, DEAD)


if __name__ == "__main__":
    unittest.main()
