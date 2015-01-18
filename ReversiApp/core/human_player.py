from ReversiApp.core.game_logic import *
from ReversiApp.message_manager import *


class HumanPlayer(object):
    def __init__(self, game, message_manager):
        self.message_bus = message_manager
        self.game = game

    def make_move(self, row, column):
        prognosis_action = MakeOwnMovementPrognosisAction(row, column)
        self.game.perform_action(prognosis_action)
        prognosis = prognosis_action.result.value

        movement_action = MakeMoveAction(prognosis)
        self.game.perform_action(movement_action)

        message = MoveDoneMessage() if movement_action.result else MoveWasNotPossibleMessage()
        self.message_bus.dispatch_message(message)
        return movement_action.result.value

    def pass_move(self):
        self.game.perform_action(PassAction())
        self.message_bus.dispatch_message(MovePassedMessage())

    def surrender(self):
        self.game.perform_action(SurrenderAction())
        self.message_bus.dispatch_message(PlayerSurrenderedMessage())

    def make_turn(self, messagge_provider):
        print(self.game.game_board)
        print(messagge_provider.player_movement_message(self.game.game_state.get_current_player_color()))
        print(messagge_provider.human_player_movement_message)
        command = input(messagge_provider.prompt)

        try:
            if command == messagge_provider.surrender_command:
                print(messagge_provider.player_surrendered)
                self.surrender()
                return
            elif command == messagge_provider.pass_command:
                print(messagge_provider.player_passed)
                self.pass_move()
                return
            else:
                row, col = map(int, command.split())
        except Exception:
            print(messagge_provider.invalid_command, repr(command))
            return

        self.make_move(row, col)
