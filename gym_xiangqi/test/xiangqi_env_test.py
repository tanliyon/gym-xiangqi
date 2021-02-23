import unittest
from gym_xiangqi.envs.xiangqi_env import XiangQiEnv


class TestXiangQiEnv(unittest.TestCase):

    def test_init(self):
        env = XiangQiEnv(agent_color=0)
        self.assertEqual(env.agent_color, 0)
        self.assertEqual(env.enemy_color, 1)

        env = XiangQiEnv(agent_color=1)
        self.assertEqual(env.agent_color, 1)
        self.assertEqual(env.enemy_color, 0)

        self.assertIsNotNone(env.game)
        self.assertIsNotNone(env.state)
        self.assertIsNotNone(env.observation_space)
        self.assertIsNotNone(env.action_space)


if __name__ == "__main__":
    unittest.main()
