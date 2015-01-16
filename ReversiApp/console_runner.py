from ReversiApp.core.ai_player import AiPlayer
from ReversiApp.core.game_logic import *
from ReversiApp.core.human_player import HumanPlayer


class MessageProvider(object):
    def __init__(self):
        self.player_mode_prompt = 'Please specify controls for player{}: '


class MainConsole(object):
    def __init__(self, message_provider):
        self.player_modes = {
            'human': lambda game, message_manager, color: HumanPlayer(game, message_manager),
            'ai': lambda game, message_manager, color: AiPlayer(game, message_manager, color)
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

    def start_game(self):
        self.game.perform_action(BlackTurnAction())

    def main(self):
        player1_creator = self.read_player_mode(1)
        player2_creator = self.read_player_mode(2)
        self.create_new_game()
        self.start_game()




if __name__ == '__main__':
    MainConsole(MessageProvider()).main()