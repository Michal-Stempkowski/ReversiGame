from ReversiApp.gameboard.game_board import GameBoard

__author__ = 'Michał'

from django.test import TestCase


class WhenCreatingGameBoard(TestCase):
    def setUp(self):
        pass

    def test_should_be_able_to_create_empty_board(self):
        game_board = GameBoard()