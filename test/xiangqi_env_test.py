import unittest
from unittest.mock import patch
import random
import string

from gym_xiangqi.envs.xiangqi_env import XiangQiEnv
from gym_xiangqi.xiangqi_game import XiangQiGame
from gym_xiangqi.constants import (
    BOARD_ROWS, BOARD_COLS,
    RED, BLACK, DEAD,
    ILLEGAL_MOVE, PIECE_POINTS, LOSE,
    EMPTY, GENERAL, CANNON_1, HORSE_2,
    ALLY, ENEMY,
    INITIAL_BOARD,
)


class TestXiangQiEnv(unittest.TestCase):

    def assertStateEqual(self, obs, new_obs):
        for i in range(BOARD_ROWS):
            for j in range(BOARD_COLS):
                self.assertEqual(obs[i][j], new_obs[i][j])

    def setUp(self):
        self.env = XiangQiEnv()

    def tearDown(self):
        self.env.close()

    def test_env_initialization(self):
        self.assertEqual(self.env.ally_color, RED)
        self.assertEqual(self.env.enemy_color, BLACK)

        self.env = XiangQiEnv(ally_color=BLACK)
        self.assertEqual(self.env.ally_color, BLACK)
        self.assertEqual(self.env.enemy_color, RED)

        self.assertIsNotNone(self.env.game)
        self.assertIsNotNone(self.env.state)
        self.assertIsNotNone(self.env.observation_space)
        self.assertIsNotNone(self.env.action_space)
        self.assertIsNotNone(self.env.ally_actions)
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

    def test_flying_general(self):
        """
        Verification of flying general condition checker
        Given an action that results in flying general, the environment has
        to reject and penalize the agent
        """
        # pre-defined actions tht will result in a flying general situation
        actions = [78727, 75172, 78961, 74938, 75720, 78177]

        for action in actions:
            obs = self.env.state
            new_obs, reward, _, _ = self.env.step(action)

        # check that our state is preserved and the reward is a penalty
        self.assertStateEqual(obs, new_obs)
        self.assertEqual(reward, ILLEGAL_MOVE)

    def test_env_step_illegal_move(self):
        """
        verify agent with illegal move
        """
        obs = self.env.state
        new_obs, reward, done, info = self.env.step(0)

        self.assertStateEqual(obs, new_obs)
        self.assertEqual(reward, ILLEGAL_MOVE)
        self.assertEqual(done, False)

    def test_env_step_one_round(self):
        """
        verify one round of ally and enemy turns
        78727: Ally CANNON_1 (7, 1) -> (7, 4)
        75172: Enemy CANNON_1 (2, 7) -> (2, 4)
        """
        actions = [(78727, CANNON_1, (7, 1), (7, 4), 0, ENEMY),
                   (75172, CANNON_1, (2, 7), (2, 4), 0, ALLY)]

        for action, pid, (r1, c1), (r2, c2), points, next_turn in actions:
            obs, reward, done, info = self.env.step(action)
            self.assertEqual(obs[r1][c1], EMPTY)
            self.assertEqual(obs[r2][c2], pid * self.env.turn * -1)
            self.assertEqual(reward, points)
            self.assertEqual(done, False)
            self.assertEqual(self.env.turn, next_turn)

    def test_env_step_reward(self):
        """
        Simulates Ally (red) cannon taking a black horse
        78661: Ally CANNON_1 (7, 1) -> (0, 1)
        """
        action = 78661
        obs, reward, done, info = self.env.step(action)
        self.assertEqual(obs[7][1], EMPTY)
        self.assertEqual(obs[0][1], CANNON_1)
        self.assertEqual(reward, PIECE_POINTS[HORSE_2])
        self.assertEqual(done, False)
        self.assertEqual(self.env.enemy_piece[HORSE_2].state, DEAD)

    def test_env_step_done(self):
        """
        verify environment termination due to death of black general
        78727: Ally CANNON_1 (7, 1) -> (7, 4)
        75172: Enemy CANNON_1 (2, 7) -> (2, 4)
        78961: Ally CANNON_1 (7, 4) -> (3, 4)
        123966: Enemy SOLDIER_5 (3, 0) -> (4, 0)
        75694: Ally CANNON_1 (3, 4) -> (0, 4) -- takes black general
        """
        actions = [78727, 75172, 78961, 123966, 75694]
        for action in actions:
            obs, reward, done, info = self.env.step(action)
        self.assertEqual(done, True)
        self.assertEqual(reward, PIECE_POINTS[GENERAL])
        self.assertEqual(self.env.enemy_piece[GENERAL].state, DEAD)

    def test_env_reset(self):
        """
        verify environment properly resets after an episode has terminated

        Performs these series of actions:
        78727: Ally CANNON_1 (7, 1) -> (7, 4)
        75172: Enemy CANNON_1 (2, 7) -> (2, 4)
        78961: Ally CANNON_1 (7, 4) -> (3, 4)
        123966: Enemy SOLDIER_5 (3, 0) -> (4, 0)
        75694: Ally CANNON_1 (3, 4) -> (0, 4) -- takes black general

        and resets the environment.
        """
        actions = [78727, 75172, 78961, 123966, 75694]
        for action in actions:
            obs, reward, done, info = self.env.step(action)
        self.assertEqual(done, True)
        self.assertEqual(reward, PIECE_POINTS[GENERAL])
        self.assertEqual(self.env.enemy_piece[GENERAL].state, DEAD)

        obs = self.env.reset()
        self.assertFalse(self.env._done)
        self.assertStateEqual(INITIAL_BOARD, obs)

    def test_perpetual_check(self):
        """
        simulate a perpetual checking situation
        64062:      Chariot 1 (red)     (9, 0) -> (8, 0)
        57437:      Chariot 1 (black)   (0, 8) -> (1, 8)
        63255:      Chariot 1 (red)     (8, 0) -> (8, 3)
        373:        General (black)     (0, 4) -> (1, 4)
        63462:      Chariot 1 (red)     (8, 3) -> (1, 3)
        --------------- REPETITION START ---------------
        1192:       General (black)     (1, 4) -> (2, 4)
        57801:      Chariot 1 (red)     (1, 3) -> (2, 3)
        1993:       General (black)     (2, 4) -> (1, 4)
        58602:      Chariot 1 (red)     (2, 3) -> (1, 3)
        ---------------- REPETITION END ----------------
        """
        for action in [64062, 57437, 63255, 373, 63462]:
            obs, reward, done, _ = self.env.step(action)
            self.assertFalse(done)

        for _ in range(3):
            for action in [1192, 57801, 1993, 58602]:
                _, reward, done, _ = self.env.step(action)
        self.assertEqual(reward, LOSE)
        self.assertTrue(done)

    def test_env_close(self):
        self.env.render()
        self.env.close()

    def test_env_seed(self):
        seed_list = self.env.seed()
        self.assertIsNotNone(seed_list)
        self.assertIsInstance(seed_list, list)
        self.assertIsInstance(seed_list[0], int)

    def test_env_state_hash_check(self):
        self.env._state[0][7], self.env._state[2][1] = (
            self.env._state[2][1], self.env._state[0][7])
        with self.assertRaises(AssertionError):
            self.env.step(300)

    def test_env_step_user(self):
        def mock_run(this):
            this.cur_selected_pid = CANNON_1
            this.end_pos = (0, 1)

        with patch.object(XiangQiGame, 'run', new=mock_run):
            obs, reward, done, _ = self.env.step_user()

        self.assertEqual(self.env.user_move_info, (CANNON_1, (7, 1), (0, 1)))
        self.assertEqual(obs[7][1], EMPTY)
        self.assertEqual(obs[0][1], CANNON_1)
        self.assertEqual(reward, PIECE_POINTS[HORSE_2])
        self.assertFalse(done)


if __name__ == "__main__":
    unittest.main()
