from unittest import TestCase

from ReversiApp.core.game_board import *


def list_of_coordinates(start, direction, count):
    return [(start[0] + direction[0] * i, start[1] + direction[1] * i) for i in range(count)]


class WhenCreatingGameBoard(TestCase):
    def setUp(self):
        self.game_board = GameBoard()
        self.board_size = self.game_board.board_size() * self.game_board.board_size()

    def test_newly_created_board_should_have_64_empty_fields(self):
        self.assertEquals(self.board_size, self.game_board.count_empty_fields())

    def test_when_calling_reset__board_should_be_emptied(self):
        self.game_board.insert_piece(0, 0, WhitePiece())
        self.game_board.insert_piece(4, 4, BlackPiece())

        self.game_board.reset_board()

        self.assertEquals(self.board_size, self.game_board.count_empty_fields())

    def test_board_with_five_pieces_should_have_59_empty_fields(self):
        self.game_board.insert_piece(0, 0, WhitePiece())
        self.game_board.insert_piece(0, 1, WhitePiece())
        self.game_board.insert_piece(3, 0, WhitePiece())
        self.game_board.insert_piece(6, 0, BlackPiece())
        self.game_board.insert_piece(4, 4, BlackPiece())

        self.assertEquals(self.board_size - 5, self.game_board.count_empty_fields())

    def test_after_initializing_board__there_should_be_2_white_and_2_black_pieces(self):
        self.game_board.add_new_game_starting_pieces()

        self.assertEquals(self.board_size - 4, self.game_board.count_empty_fields())
        self.assertEquals(WhitePiece(), self.game_board.fields[3][3])
        self.assertEquals(BlackPiece(), self.game_board.fields[3][4])
        self.assertEquals(WhitePiece(), self.game_board.fields[4][4])
        self.assertEquals(BlackPiece(), self.game_board.fields[4][3])

    def test_should_be_able_to_get_piece_from_board(self):
        self.game_board.insert_piece(0, 0, WhitePiece())
        self.game_board.insert_piece(2, 5, BlackPiece())
        self.game_board.insert_piece(7, 7, WhitePiece())

        self.assertEquals(WhitePiece(), self.game_board.get_piece_from_field(0, 0))
        self.assertEquals(BlackPiece(), self.game_board.get_piece_from_field(2, 5))
        self.assertEquals(WhitePiece(), self.game_board.get_piece_from_field(7, 7))
        self.assertEquals(NoPiece(), self.game_board.get_piece_from_field(3, 4))

    def test_get_piece_out_of_field_should_return_out_of_board(self):
        self.assertEquals(OutOfBoardPiece(), self.game_board.get_piece_from_field(-1, -1))


class WhenMakingMovementPrognosis(TestCase):
    def setUp(self):
        self.game_board = GameBoard()
        self.movement_prognosis = MovementPrognosis(self.game_board)

    def insert_many_pieces(self, pieces):
        for (y, x, color) in pieces:
            self.movement_prognosis.game_board.insert_piece(y, x, color)

    def assert_neighbourhood_detected(self, expected, existing_enemies, row_of_new_piece, column_of_new_piece):
        self.insert_many_pieces(existing_enemies)

        list_of_adjacent_enemies = self.movement_prognosis.find_all_adjacent_enemies(row_of_new_piece,
                                                                                     column_of_new_piece,
                                                                                     BlackPiece())

        expected_with_directions = map(lambda neighbour:
                                       (neighbour[0], neighbour[1], (neighbour[0] - row_of_new_piece,
                                                                     neighbour[1] - column_of_new_piece)), expected)

        self.assertEquals(set(expected_with_directions), set(list_of_adjacent_enemies))
        self.movement_prognosis.game_board.reset_board()

    def test_should_be_able_to_find_all_adjacent_enemies(self):
        self.assert_neighbourhood_detected([], [], 2, 2)
        self.assert_neighbourhood_detected([(1, 1)], [(1, 1, WhitePiece())], 2, 2)
        self.assert_neighbourhood_detected([(2, 1)], [(2, 1, WhitePiece())], 2, 2)
        self.assert_neighbourhood_detected([(2, 3)], [(2, 3, WhitePiece())], 2, 2)
        self.assert_neighbourhood_detected([(1, 2)], [(1, 2, WhitePiece())], 2, 2)
        self.assert_neighbourhood_detected([(3, 2)], [(3, 2, WhitePiece())], 2, 2)

        all_surrounding = [(y, x, WhitePiece()) for x in range(1, 4) for y in range(1, 4) if x != 2 or y != 2]
        self.assert_neighbourhood_detected(all_surrounding, all_surrounding, 2, 2)

    def assert_conversions_detected(self, expected_result, neighbour, white_pieces, black_pieces):
        # noinspection PyTypeChecker
        to_be_inserted = [(y, x, WhitePiece()) for (y, x) in white_pieces] + \
                         [(y, x, BlackPiece()) for (y, x) in black_pieces]
        self.insert_many_pieces(to_be_inserted)
        self.assertEquals(expected_result, self.movement_prognosis.try_expanding_conversion(neighbour, BlackPiece()))

    def test_should_find_all_pieces_to_be_converted_in_given_direction(self):
        self.assert_conversions_detected([], (2, 3, (0, 1)), [(2, 3)], [])
        self.assert_conversions_detected([], (2, 7, (0, 1)), [(2, 7)], [])
        self.assert_conversions_detected([], (2, 0, (0, -1)), [(2, 0)], [(2, 7)])
        self.assert_conversions_detected([(2, 3)], (2, 3, (0, 1)), [(2, 3)], [(2, 4)])

        self.assert_conversions_detected(list_of_coordinates((2, 3), (0, 1), 2), (2, 3, (0, 1)),
                                         list_of_coordinates((2, 3), (0, 1), 2), [(2, 5)])

        self.assert_conversions_detected(list_of_coordinates((3, 2), (1, 0), 2), (3, 2, (1, 0)),
                                         list_of_coordinates((3, 2), (1, 0), 2), [(5, 2)])

    def assert_find_all_pieces_returns(self, expected, piece_to_be_inserted, pieces_before_movement):
        self.movement_prognosis.game_board.reset_board()

        self.insert_many_pieces(pieces_before_movement)
        list_of_adjacent_enemies = self.movement_prognosis.find_all_adjacent_enemies(*piece_to_be_inserted)
        self.assertEquals(expected, set(self.movement_prognosis.find_all_pieces_to_be_converted(
            list_of_adjacent_enemies, piece_to_be_inserted[2])))

        self.movement_prognosis.game_board.reset_board()

    def test_should_find_all_pieces_to_be_converted_in_all_directions(self):
        self.assert_find_all_pieces_returns(set(), (2, 2, BlackPiece()), [])
        self.assert_find_all_pieces_returns({(2, 3)}, (2, 2, BlackPiece()),
                                            [(2, 3, WhitePiece()), (2, 4, BlackPiece())])
        self.assert_find_all_pieces_returns({(2, 3), (3, 2)}, (2, 2, BlackPiece()),
                                            [(2, 3, WhitePiece()), (2, 4, BlackPiece()),
                                             (3, 2, WhitePiece()), (4, 2, BlackPiece())])

        self.assert_find_all_pieces_returns({(2, 3)}, (2, 2, BlackPiece()),
                                            [(2, 3, WhitePiece()), (2, 4, BlackPiece()),
                                             (3, 2, WhitePiece())])

    def test_should_be_able_to_tell_if_movement_is_valid(self):
        self.movement_prognosis.make_prognosis(2, 2, BlackPiece())
        self.assertFalse(self.movement_prognosis.will_be_valid())

        self.insert_many_pieces([(2, 3, WhitePiece()), (2, 4, BlackPiece())])
        self.movement_prognosis.make_prognosis(2, 2, BlackPiece())
        self.assertTrue(self.movement_prognosis.will_be_valid())

    def test_should_update_prognosis_map_but_not_current_map(self):
        self.insert_many_pieces([(2, 3, WhitePiece()), (2, 4, BlackPiece())])
        self.movement_prognosis.make_prognosis(2, 2, BlackPiece())

        self.assertTrue(self.movement_prognosis.game_board.get_piece_from_field(2, 3) == BlackPiece())
        self.assertTrue(self.movement_prognosis.game_board.get_piece_from_field(2, 2) == BlackPiece())

        self.assertTrue(self.game_board.get_piece_from_field(2, 3) == NoPiece())

    def test_should_be_able_to_tell_how_many_pieces_will_be_converted(self):
        self.insert_many_pieces([(2, 3, WhitePiece()), (2, 4, WhitePiece()), (2, 5, BlackPiece()),
                                 (3, 2, WhitePiece()), (4, 2, BlackPiece())])
        self.movement_prognosis.make_prognosis(2, 2, BlackPiece())

        self.assertEquals(3, self.movement_prognosis.converted_pieces)