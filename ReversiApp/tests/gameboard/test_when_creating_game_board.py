from unittest import TestCase

from ReversiApp.gameboard.game_board import GameBoard, WhitePiece, BlackPiece


class WhenCreatingGameBoard(TestCase):
    def setUp(self):
        pass

    def test_newly_created_board_should_have_64_empty_fields(self):
        game_board = GameBoard()

        self.assertEquals(64, game_board.count_empty_fields())

    def test_board_with_five_pieces_should_have_59_empty_fields(self):
        game_board = GameBoard()
        game_board.fields[0][0] = WhitePiece()
        game_board.fields[1][0] = WhitePiece()
        game_board.fields[0][3] = WhitePiece()
        game_board.fields[0][6] = BlackPiece()
        game_board.fields[4][4] = BlackPiece()

        self.assertEquals(59, game_board.count_empty_fields())

    def test_after_initializing_board__there_should_be_2_white_and_2_black_pieces(self):
        game_board = GameBoard()

        game_board.add_new_game_starting_pieces()

        self.assertEquals(60, game_board.count_empty_fields())
        self.assertEquals(WhitePiece(), game_board.fields[3][3])
        self.assertEquals(BlackPiece(), game_board.fields[3][4])
        self.assertEquals(WhitePiece(), game_board.fields[4][4])
        self.assertEquals(BlackPiece(), game_board.fields[4][3])