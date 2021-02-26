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
        self.assertIsNotNone(env.possible_actions)

    def test_move_to_action_space(self):
        env = XiangQiEnv()
        i = 0

        for pid in range(1, 17):
            for r1 in range(10):
                for c1 in range(9):
                    for r2 in range(10):
                        for c2 in range(9):
                            action_idx = env.move_to_action_space(
                                pid, (r1, c1), (r2, c2)
                            )
                            self.assertEqual(action_idx, i)
                            i += 1

    def test_action_space_to_move(self):
        def info_gen():
            for piece in range(1, 17):
                for r1 in range(10):
                    for c1 in range(9):
                        for r2 in range(10):
                            for c2 in range(9):
                                yield piece, (r1, c1), (r2, c2)

        env = XiangQiEnv()
        gen = info_gen()
        n = pow(10 * 9, 2) * 16

        for i in range(n):
            pid, start, end = env.action_space_to_move(i)
            ans_pid, ans_start, ans_end = next(gen)
            self.assertEqual(pid, ans_pid)
            self.assertEqual(start[0], ans_start[0])
            self.assertEqual(start[1], ans_start[1])
            self.assertEqual(end[0], ans_end[0])
            self.assertEqual(end[1], ans_end[1])


if __name__ == "__main__":
    unittest.main()
