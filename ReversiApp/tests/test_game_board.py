from unittest import TestCase

from ReversiApp.core.game_board import GameBoard, NoPiece, BlackPiece, WhitePiece


class WhenCreatingGameBoard(TestCase):
    def setUp(self):
        self.game_board = GameBoard()

    def test_newly_created_board_should_have_64_empty_fields(self):
        self.assertEquals(64, self.game_board.count_empty_fields())

    def test_when_calling_reset__board_should_be_emptied(self):
        self.game_board.insert_piece(0, 0, WhitePiece())
        self.game_board.insert_piece(4, 4, BlackPiece())

        self.game_board.reset_board()

        self.assertEquals(64, self.game_board.count_empty_fields())

    def test_board_with_five_pieces_should_have_59_empty_fields(self):
        self.game_board.insert_piece(0, 0, WhitePiece())
        self.game_board.insert_piece(0, 1, WhitePiece())
        self.game_board.insert_piece(3, 0, WhitePiece())
        self.game_board.insert_piece(6, 0, BlackPiece())
        self.game_board.insert_piece(4, 4, BlackPiece())

        self.assertEquals(59, self.game_board.count_empty_fields())

    def test_after_initializing_board__there_should_be_2_white_and_2_black_pieces(self):
        self.game_board.add_new_game_starting_pieces()

        self.assertEquals(60, self.game_board.count_empty_fields())
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