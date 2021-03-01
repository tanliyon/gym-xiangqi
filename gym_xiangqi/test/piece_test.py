import unittest
import numpy as np

from gym_xiangqi.piece import (
    Piece, General, Advisor, Elephant,
    Horse, Chariot, Cannon, Soldier
)
from gym_xiangqi.utils import (
    action_space_to_move
)
from gym_xiangqi.constants import RED, BLACK, GENERAL
from gym_xiangqi.envs.xiangqi_env import XiangQiEnv


class TestPieceClasses(unittest.TestCase):

    def setUp(self) -> None:
        self.classes = [Piece, General, Advisor, Elephant,
                        Horse, Chariot, Cannon, Soldier]
    
    def diff_move_list(self, env, piece_id, expected):
        result = []
        for action in env.get_possible_actions_by_piece(piece_id):
            result.append(action_space_to_move(action))
        result.sort()
        expected.sort()
        self.assertEqual(result, expected)

    def test_piece_initialization(self):
        for piece_class in self.classes:
            piece = piece_class(0, 0, 0)
            self.assertIsInstance(piece, piece_class)
            self.assertEqual(piece.color, RED)
            self.assertEqual(piece.row, 0)
            self.assertEqual(piece.col, 0)
            piece.color = 1
            self.assertEqual(piece.color, BLACK)
    
    def test_general_can_move_within_palace(self):
        env = XiangQiEnv()
        # Test red general can only move forward 1 position from
        # starting position.
        self.diff_move_list(
            env=env,
            piece_id=GENERAL,
            expected=[(GENERAL, [9, 4], [8, 4])]
        )
        
        # Move general to the center of the palace.
        env.agent_piece[GENERAL].row -= 1
        env.state[8][4] = env.state[9][4]
        env.state[9][4] = 0

        # Test again with general in the center of the palace.
        self.diff_move_list(
            env=env,
            piece_id=GENERAL,
            expected=[
                (GENERAL, [8, 4], [7, 4]),
                (GENERAL, [8, 4], [9, 4]),
                (GENERAL, [8, 4], [8, 5]),
                (GENERAL, [8, 4], [8, 3]),
            ]
        )

    def test_general_cannnot_move_out_of_palace(self):
        env = XiangQiEnv()

        # Move general to the top right hand corner of palace.
        env.agent_piece[GENERAL].row -= 2
        env.agent_piece[GENERAL].col += 1
        env.state[7][5] = env.state[9][4]
        env.state[9][4] = 0

        self.diff_move_list(
            env=env,
            piece_id=GENERAL,
            expected=[
                (GENERAL, [7, 5], [7, 4]),
                (GENERAL, [7, 5], [8, 5]),
            ]
        )


if __name__ == "__main__":
    unittest.main()
