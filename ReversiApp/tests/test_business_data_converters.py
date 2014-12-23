from django.test import TestCase
from ReversiApp.business_data_converters import GameBoardConverter
from ReversiApp.core.game_board import NoPiece, WhitePiece, BlackPiece, GameBoard
from ReversiApp.models import GameBoardRecord


class WhenUsingBusinessDataConverters(TestCase):
    def setUp(self):
        self.board_symbols = \
            'W-------' + \
            '-W------' + \
            '--W-----' + \
            '---W----' + \
            '----W---' + \
            '-----W--' + \
            '------W-' + \
            '-------W'
        self.board_pieces = [[WhitePiece() if col == row else NoPiece() for col in range(0, 8)] for row in range(0, 8)]

    def test_data_to_game_board_conversion(self):
        data = GameBoardRecord()
        data.board = self.board_symbols
        self.assertEquals(self.board_pieces, GameBoardConverter.to_game_board(data).fields)

    def test_game_board_to_data_conversion(self):
        gameboard = GameBoard()
        gameboard.fields = self.board_pieces
        self.assertEquals(self.board_symbols, GameBoardConverter.from_game_board(gameboard))