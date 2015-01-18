from ReversiApp.core.ai_player import AiPlayer, AiParams
from ReversiApp.core.game_logic import *
from ReversiApp.core.human_player import HumanPlayer
from ReversiApp.mocks.system_mocks import SystemMessageBusMockWithMessageLog


class MessageProvider(object):
    def __init__(self):
        self.prompt = '> '
        self.player_mode_prompt = 'Please specify controls for player{}: '
        self.player_surrendered = 'Player decided to surrender'
        self.player_passed = 'Player decided to pass'
        self.invalid_coordinates = 'Movement to those coordinates: {} {} is not valid!'
        self.invalid_command = 'Invalid command:'

        self.new_game_created_message = 'New game has been successfully created'
        self.black_turn_message = 'Black player move:'
        self.white_turn_message = 'White player move:'

        self.black_player_name = 'Black'
        self.white_player_name = 'White'
        self.human_player_movement_message = 'Please enter coordinates (example movements: "0 5", "pass", "surrender"'
        self.game_has_ended_message = 'Game has ended!'
        self.points_message = '{} has earned {} points.'

        self.surrender_command = 'surrender'
        self.pass_command = 'pass'

    def player_movement_message(self, color):
        return '{} player move:'.format(self.black_player_name if color == BlackPiece() else self.white_player_name)

    def player_name(self, color):
        return self.black_player_name if color == BlackPiece() else self.white_player_name


class MainConsole(object):
    def __init__(self, message_provider):
        self.message_manager = SystemMessageBusMockWithMessageLog()
        self.player_modes = {
            'human': lambda game, message_manager, color: HumanPlayer(game, message_manager),
            'ai': lambda game, message_manager, color: AiPlayer(game, AiParams(), color),
            'ai_corners_3': lambda game, message_manager, color: AiPlayer(game, AiParams(eval_functions=[
                AiParams.Evaluation.my_piece_count(10),
                AiParams.Evaluation.corners_are_better(3)]), color),
            'ai_corners_1': lambda game, message_manager, color: AiPlayer(game, AiParams(eval_functions=[
                AiParams.Evaluation.my_piece_count(10),
                AiParams.Evaluation.corners_are_better(1)]), color),
            'ai_middle_3': lambda game, message_manager, color: AiPlayer(game, AiParams(eval_functions=[
                AiParams.Evaluation.my_piece_count(10),
                AiParams.Evaluation.middle_is_better(3)]), color),
            'ai_middle_1': lambda game, message_manager, color: AiPlayer(game, AiParams(eval_functions=[
                AiParams.Evaluation.my_piece_count(10),
                AiParams.Evaluation.middle_is_better(1)]), color),
            'ai_corners_2_middle_1': lambda game, message_manager, color: AiPlayer(game, AiParams(eval_functions=[
                AiParams.Evaluation.my_piece_count(10),
                AiParams.Evaluation.corners_are_better(2),
                AiParams.Evaluation.middle_is_better(1)]), color),
            'ai_corners_1_middle_2': lambda game, message_manager, color: AiPlayer(game, AiParams(eval_functions=[
                AiParams.Evaluation.my_piece_count(10),
                AiParams.Evaluation.corners_are_better(1),
                AiParams.Evaluation.middle_is_better(2)]), color)
        }

        self.message_provider = message_provider

        self.player1 = None
        self.player2 = None
        self.game = None

    def read_player_mode(self, player_no):
        return self.player_modes.get(
            input(self.message_provider.player_mode_prompt.format(player_no))) or self.player_modes['human']

    def create_new_game(self):
        self.game = Game()
        self.game.perform_action(InitializeAction())
        print(self.message_provider.new_game_created_message)

    def start_game(self):
        self.game.perform_action(BlackTurnAction())

    def show_score(self):
        black, white = self.game.game_board.count_pieces(BlackPiece()), self.game.game_board.count_pieces(WhitePiece())

        print(self.message_provider.points_message.format(self.message_provider.player_name(BlackPiece()), black))
        print(self.message_provider.points_message.format(self.message_provider.player_name(WhitePiece()), white))

    def main(self):
        player1_creator = self.read_player_mode(1)
        player2_creator = self.read_player_mode(2)
        self.create_new_game()
        self.start_game()

        self.player1 = player1_creator(self.game, self.message_manager, BlackPiece())
        self.player2 = player2_creator(self.game, self.message_manager, WhitePiece())

        player_getter = lambda color: self.player1 if color == BlackPiece() else self.player2

        while not self.game.is_in_transient_state():
            current_color = self.game.game_state.get_current_player_color()
            player_getter(current_color).make_turn(self.message_provider)
            self.show_score()

        print(self.message_provider.game_has_ended_message)
        print(self.game.game_board)
        self.show_score()

if __name__ == '__main__':
    MainConsole(MessageProvider()).main()