from django.test import TestCase

from ReversiApp.core.ai_player import *
from ReversiApp.core.game_board import BlackPiece
from ReversiApp.core.game_logic import Game, InitializeAction
from ReversiApp.mocks.core.mock_game_logic import GameInvalidMoveMock


class AiParameters(object):
    def __init__(self):
        self.reward_for_own_piece = 1
        self.reward_for_enemy_piece = -1


class TestAiPlayer(TestCase):
    def setUp(self):
        self.game_board = Game()
        self.game_board.perform_action(InitializeAction())
        self.game_board.game_board.add_new_game_starting_pieces()
        self.player = AiPlayer(self.game_board, AiParams(), BlackPiece())

    def test_should_be_able_to_select_best_movement(self):
        self.player.ai_params.max_depth = 1
        self.player.ai_params.eval_function = \
            lambda row_index, col_index, board, my_color: \
            10 if row_index > 3 and board.game_board.fields[row_index][col_index] == my_color \
            else 0
        self.assertEquals(30, self.player.alpha_beta()[0])

    # def test_should_be_able_to_think_few_moves_ahead(self):
    #     self.player.ai_params.max_depth = 5
    #     self.player.ai_params.eval_function = \
    #         lambda row_index, col_index, board, my_color: \
    #         10 if row_index > 4 and board.game_board.fields[col_index][row_index] == my_color \
    #         else 0
    #     self.assertEquals(10, self.player.alpha_beta()[1].game_board)