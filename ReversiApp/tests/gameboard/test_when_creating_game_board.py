from unittest import TestCase

from ReversiApp.gameboard.game_board import GameBoard


class WhenCreatingGameBoard(TestCase):
    def setUp(self):
        pass

    def test_should_be_able_to_create_empty_board(self):
        game_board = GameBoard()

    def test_newly_created_board_should_have_64_empty_fields(self):
        game_board = GameBoard()

        self.assertEquals(64, game_board.count_empty_fields())