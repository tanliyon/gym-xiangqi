import unittest

from gym_xiangqi.piece import (
    Piece, General, Advisor, Elephant,
    Horse, Chariot, Cannon, Soldier
)
from gym_xiangqi.utils import (
    action_space_to_move
)
from gym_xiangqi.constants import (
    RED, BLACK, GENERAL, ADVISOR_1,
    HORSE_1, ELEPHANT_1
)
from gym_xiangqi.envs.xiangqi_env import XiangQiEnv


class TestPieceClasses(unittest.TestCase):

    def setUp(self) -> None:
        self.classes = [Piece, General, Advisor, Elephant,
                        Horse, Chariot, Cannon, Soldier]

    def diff_move_list(self, env, piece_id, expected):
        """
        Helper function to sort then diff possible moves list of a piece.

        Parameters:
            env (XiangQiEnv): Environment used to diff the move list.
            piece_id (int): ID of the piece to test.
            expected (List[Tuple]): Expected moves from the piece in
                the format: [
                    (piece_id, [src_x, src_y], [dest_x, dest_y]),
                    (...)]
        """
        result = []
        for action in env.get_possible_actions_by_piece(piece_id):
            result.append(action_space_to_move(action))
        result.sort()
        expected.sort()
        self.assertEqual(result, expected)

    def move_piece(self, env, piece_id, destination):
        """
        Simple helper function to move a piece to a destination.
        """
        source = (env.agent_piece[piece_id].row, env.agent_piece[piece_id].col)
        env.agent_piece[piece_id].row = destination[0]
        env.agent_piece[piece_id].col = destination[1]
        env.state[destination[0]][destination[1]] = env.state[source[0]][source[1]]
        env.state[source[0]][source[1]] = 0

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
        self.move_piece(env=env,
                        piece_id=GENERAL,
                        destination=(8, 4))

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
        self.move_piece(env=env,
                        piece_id=GENERAL,
                        destination=(7, 5))

        self.diff_move_list(
            env=env,
            piece_id=GENERAL,
            expected=[
                (GENERAL, [7, 5], [7, 4]),
                (GENERAL, [7, 5], [8, 5]),
            ]
        )

    def test_advisor_can_move_within_palace(self):
        env = XiangQiEnv()
        # Move the left advisor to the center of palace.
        self.move_piece(env=env,
                        piece_id=ADVISOR_1,
                        destination=(8, 4))

        self.diff_move_list(
            env=env,
            piece_id=ADVISOR_1,
            expected=[
                (ADVISOR_1, [8, 4], [9, 3]),
                (ADVISOR_1, [8, 4], [7, 3]),
                (ADVISOR_1, [8, 4], [7, 5]),
            ]
        )

    def test_advisor_cannot_move_out_of_palace(self):
        env = XiangQiEnv()
        # Move the left advisor to the top left of palace.
        self.move_piece(env=env,
                        piece_id=ADVISOR_1,
                        destination=(7, 3))

        self.diff_move_list(
            env=env,
            piece_id=ADVISOR_1,
            expected=[
                (ADVISOR_1, [7, 3], [8, 4]),
            ]
        )

    def test_horse_can_move(self):
        env = XiangQiEnv()
        # Move horse to an open space.
        self.move_piece(env=env,
                        piece_id=HORSE_1,
                        destination=(5, 4))

        self.diff_move_list(
            env=env,
            piece_id=HORSE_1,
            expected=[
                (HORSE_1, [5, 4], [3, 5]),
                (HORSE_1, [5, 4], [3, 3]),
                (HORSE_1, [5, 4], [4, 6]),
                (HORSE_1, [5, 4], [4, 2]),
            ]
        )

    def test_horse_will_be_blocked_by_pieces(self):
        env = XiangQiEnv()

        # Move horse to be in between 2 soldiers
        # and in front of cannon.
        self.move_piece(env=env,
                        piece_id=HORSE_1,
                        destination=(6, 1))

        self.diff_move_list(
            env=env,
            piece_id=HORSE_1,
            expected=[
                (HORSE_1, [6, 1], [4, 0]),
                (HORSE_1, [6, 1], [4, 2]),
            ]
        )

    def test_elephant_can_move(self):
        env = XiangQiEnv()

        self.diff_move_list(
            env=env,
            piece_id=ELEPHANT_1,
            expected=[
                (ELEPHANT_1, [9, 2], [7, 4]),
                (ELEPHANT_1, [9, 2], [7, 0]),
            ]
        )

    def test_elephant_cannot_cross_river(self):
        env = XiangQiEnv()

        # Move elephant to edge of river.
        self.move_piece(env=env,
                        piece_id=ELEPHANT_1,
                        destination=(5, 2))

        self.diff_move_list(
            env=env,
            piece_id=ELEPHANT_1,
            expected=[
                (ELEPHANT_1, [5, 2], [7, 4]),
                (ELEPHANT_1, [5, 2], [7, 0]),
            ]
        )


if __name__ == "__main__":
    unittest.main()
