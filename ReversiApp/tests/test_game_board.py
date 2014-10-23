from unittest import TestCase

from ReversiApp.core.game_board import GameBoard, NoPiece, BlackPiece, WhitePiece, MovementPrognosis, OutOfBoardPiece


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

    def assert_neighbourhood_detected(self, expected, existing_enemies, row_of_new_piece, column_of_new_piece):
        for (y, x) in existing_enemies:
            self.game_board.insert_piece(y, x, WhitePiece())

        list_of_adjacent_enemies = self.movement_prognosis.phase_zero_validation_of_movement(row_of_new_piece,
                                                                                             column_of_new_piece,
                                                                                             BlackPiece())

        expected_with_directions = map(lambda neighbour:
                                       (neighbour[0], neighbour[1], (neighbour[0] - row_of_new_piece,
                                                                     neighbour[1] - column_of_new_piece)), expected)

        self.assertEquals(set(expected_with_directions), set(list_of_adjacent_enemies))
        self.game_board.reset_board()

    def test_phase_zero_prognosis_should_return_list_containing_enemy_neighbours(self):
        self.assert_neighbourhood_detected([], [], 2, 2)
        self.assert_neighbourhood_detected([], [(1, 1)], 2, 2)
        self.assert_neighbourhood_detected([(2, 1)], [(2, 1)], 2, 2)
        self.assert_neighbourhood_detected([(2, 3)], [(2, 3)], 2, 2)
        self.assert_neighbourhood_detected([(1, 2)], [(1, 2)], 2, 2)
        self.assert_neighbourhood_detected([(3, 2)], [(3, 2)], 2, 2)
        self.assert_neighbourhood_detected([(2, 1), (2, 3), (1, 2), (3, 2)],
                                           [(y, x) for x in range(1, 4) for y in range(1, 4) if x != 2 or y != 2], 2, 2)


class WhenPlayingGame(TestCase):
    def setUp(self):
        self.game_board = GameBoard()

    def test_when_placing_black_piece_on_empty_board__should_return_invalid_movement_prognosis(self):
        movement_prognosis = self.game_board.offer_piece(2, 3, BlackPiece())

        self.assertFalse(movement_prognosis.will_be_valid())
        self.assertEquals(0, movement_prognosis.converted_pieces)

    def when_placing_black_piece_next_to_white_and_black__should_return_valid_movement_prognosis(self):
        self.game_board.insert_piece(2, 2, WhitePiece())
        self.game_board.insert_piece(2, 3, BlackPiece())
        movement_prognosis = self.game_board.offer_piece(2, 1, BlackPiece())

        self.assertEquals(1, movement_prognosis.converted_pieces)
        self.assertTrue(movement_prognosis.will_be_valid())