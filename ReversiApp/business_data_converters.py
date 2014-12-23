from ReversiApp.core.game_board import NoPiece, OutOfBoardPiece
from ReversiApp.core.game_logic import *
from ReversiApp.fluent_flow.functional import chunks, reversed_map


class GameBoardConverter(object):
    symbol_to_piece_table = {
        '-': NoPiece(),
        'W': WhitePiece(),
        'B': BlackPiece(),
        '*': OutOfBoardPiece()
    }

    piece_to_symbol_table = reversed_map(symbol_to_piece_table)

    @classmethod
    def from_symbol(cls, symbol):
        return cls.symbol_to_piece_table[symbol]

    @classmethod
    def from_piece(cls, piece):
        return cls.piece_to_symbol_table[piece]

    @classmethod
    def to_game_board(cls, data):
        result = GameBoard()
        result.fields = [[cls.from_symbol(cell) for cell in row] for row in chunks(data.board, data.board_size)]
        return result

    @classmethod
    def from_game_board(cls, game_board):
        return ''.join(map(lambda row:
                           ''.join(map(lambda cell: cls.from_piece(cell), row)),
                        game_board.fields))


class GameLogicConverter(object):
    string_to_state_table = {state.name(): state for state in [
        GameStateNew(),
        GameStateDead(),
        GameStateInitialized(),
        GameStateBlackTurn(),
        GameStateWhiteTurn(),
        GameStateBlackVictory(),
        GameStateWhiteVictory()
    ]}

    @classmethod
    def from_string(cls, symbol):
        return cls.string_to_state_table[symbol]

    @classmethod
    def from_state(cls, state):
        return state.name()

    @classmethod
    def to_game_logic(cls, data):
        result = Game()
        result.game_board = GameBoardConverter.to_game_board(data)
        result.game_state = cls.from_string(data.game_state)
        return result