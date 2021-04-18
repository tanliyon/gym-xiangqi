import unittest

from gym_xiangqi.piece import (
    Piece, General, Advisor, Elephant,
    Horse, Chariot, Cannon, Soldier
)
from gym_xiangqi.constants import (
    ALLY, ENEMY,
    RED, BLACK, GENERAL, ADVISOR_1,
    HORSE_1, ELEPHANT_1, SOLDIER_1,
    CHARIOT_1, CANNON_1
)
from gym_xiangqi.utils import is_ally
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
        if is_ally(piece_id):
            pieces = env.ally_piece
            env.get_possible_actions(ALLY)
        else:
            pieces = env.enemy_piece
            env.get_possible_actions(ENEMY)

        env.get_possible_actions_by_piece(piece_id)
        result = pieces[abs(piece_id)].legal_moves
        result.sort()
        expected.sort()
        self.assertEqual(result, expected)

    def move_piece(self, env, piece_id, destination):
        """
        Simple helper function to move a piece to a destination.
        """
        source = (env.ally_piece[piece_id].row,
                  env.ally_piece[piece_id].col)
        env.ally_piece[piece_id].row = destination[0]
        env.ally_piece[piece_id].col = destination[1]
        env.state[destination[0]][destination[1]] = (
            env.state[source[0]][source[1]])
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
            expected=[([9, 4], [8, 4])]
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
                ([8, 4], [7, 4]),
                ([8, 4], [9, 4]),
                ([8, 4], [8, 5]),
                ([8, 4], [8, 3]),
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
                ([7, 5], [7, 4]),
                ([7, 5], [8, 5]),
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
                ([8, 4], [9, 3]),
                ([8, 4], [7, 3]),
                ([8, 4], [7, 5]),
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
                ([7, 3], [8, 4]),
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
                ([5, 4], [3, 5]),
                ([5, 4], [3, 3]),
                ([5, 4], [4, 6]),
                ([5, 4], [4, 2]),
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
                ([6, 1], [4, 0]),
                ([6, 1], [4, 2]),
            ]
        )

    def test_elephant_can_move(self):
        env = XiangQiEnv()

        self.diff_move_list(
            env=env,
            piece_id=ELEPHANT_1,
            expected=[
                ([9, 2], [7, 4]),
                ([9, 2], [7, 0]),
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
                ([5, 2], [7, 4]),
                ([5, 2], [7, 0]),
            ]
        )

    def test_soldier_can_move(self):
        env = XiangQiEnv()

        self.diff_move_list(
            env=env,
            piece_id=SOLDIER_1,
            expected=[
                ([6, 0], [5, 0]),
            ]
        )

    def test_soldier_can_move_sideways_after_river(self):
        env = XiangQiEnv()

        # Move soldier across the river.
        self.move_piece(env=env,
                        piece_id=SOLDIER_1,
                        destination=(4, 0))

        self.diff_move_list(
            env=env,
            piece_id=SOLDIER_1,
            expected=[
                ([4, 0], [3, 0]),
                ([4, 0], [4, 1]),
            ]
        )

    def test_chariot_can_move(self):
        env = XiangQiEnv()

        # Move chariot to front of cannon.
        self.move_piece(env=env,
                        piece_id=CHARIOT_1,
                        destination=(6, 1))

        self.diff_move_list(
            env=env,
            piece_id=CHARIOT_1,
            expected=[
                ([6, 1], [5, 1]),
                ([6, 1], [4, 1]),
                ([6, 1], [3, 1]),
                ([6, 1], [2, 1]),
            ]
        )

    def test_cannon_can_skip_enemy_piece(self):
        env = XiangQiEnv()

        # Move cannon forward 1 position and put
        # chariot behind to limit possible moves.
        self.move_piece(env=env,
                        piece_id=CANNON_1,
                        destination=(6, 1))
        self.move_piece(env=env,
                        piece_id=CHARIOT_1,
                        destination=(7, 1))

        self.diff_move_list(
            env=env,
            piece_id=CANNON_1,
            expected=[
                ([6, 1], [5, 1]),
                ([6, 1], [4, 1]),
                ([6, 1], [3, 1]),
                ([6, 1], [0, 1]),
            ]
        )

    def test_cannon_can_skip_ally_piece(self):
        env = XiangQiEnv()

        # Move cannon and put horse in front of it.
        self.move_piece(env=env,
                        piece_id=CANNON_1,
                        destination=(6, 1))
        self.move_piece(env=env,
                        piece_id=HORSE_1,
                        destination=(5, 1))

        self.diff_move_list(
            env=env,
            piece_id=CANNON_1,
            expected=[
                ([6, 1], [2, 1]),
                ([6, 1], [7, 1]),
                ([6, 1], [8, 1]),
                ([6, 1], [9, 1]),
            ]
        )


if __name__ == "__main__":
    unittest.main()
