import unittest

from gym_xiangqi.envs.xiangqi_env import XiangQiEnv
from gym_xiangqi.constants import RED, BLACK


class TestXiangQiEnv(unittest.TestCase):

    def test_env_initialization(self):
        env = XiangQiEnv(agent_color=RED)
        self.assertEqual(env.agent_color, RED)
        self.assertEqual(env.enemy_color, BLACK)

        env = XiangQiEnv(agent_color=1)
        self.assertEqual(env.agent_color, BLACK)
        self.assertEqual(env.enemy_color, RED)

        self.assertIsNotNone(env.game)
        self.assertIsNotNone(env.state)
        self.assertIsNotNone(env.observation_space)
        self.assertIsNotNone(env.action_space)
        self.assertIsNotNone(env.agent_actions)
        self.assertIsNotNone(env.enemy_actions)


if __name__ == "__main__":
    unittest.main()
