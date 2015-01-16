from _collections_abc import Iterable
from functools import reduce
from ReversiApp.core.game_board import MovementPrognosis, GameBoard

infinity = 1.0e400


class AiResult(object):
    def __init__(self, state=None, value=-infinity, children=None):
        self.state = state
        self.value = value
        self.children = children or []

    @staticmethod
    def sorter(result):
        return result.value if result else -infinity


class AiParams(object):
    def __init__(self, cutoff_test=None, make_result=None,
                 max_depth=4, is_terminal_state=None, eval_functions=None):
        self.cutoff_test = cutoff_test or (lambda state, depth: depth > self.max_depth or self.is_terminal_state(state))
        self.make_result = make_result or (lambda points, prognosis: (points, prognosis))
        self.max_depth = max_depth
        self.is_terminal_state = is_terminal_state or (lambda state: None)
        self._eval_functions = eval_functions or AiParams.Evaluation.pack(AiParams.Evaluation.my_piece_count(1))

    @property
    def eval_function(self):
        return AiParams.Evaluation.pack(self._eval_functions)

    @eval_function.setter
    def eval_function(self, value):
        if not isinstance(value, Iterable):
            value = [value]
        self._eval_functions = value

    class Evaluation(object):
        @staticmethod
        def pack(functions):
            return lambda state, color: \
                sum((func(i, j, state, color)
                    for i in range(state.game_board.board_size())
                    for j in range(state.game_board.board_size())
                    for func in functions))

        @staticmethod
        def my_piece_count(mult):
            return lambda row_index, col_index, board, my_color: \
                mult if board[row_index][col_index] == my_color else 0


class AiPlayer(object):
    def __init__(self, game, ai_params, player_color):
        self.game = game
        self.ai_params = ai_params
        self.player_color = player_color

    def evaluate_all_states(self, states):
        return ((self.ai_params.eval_function(state, self.player_color), state) for state in states)

    def find_all_possible_moves(self, prognosis):
        all_moves = (prognosis.game_board.offer_piece(row, col, self.player_color.get_enemy_color())
                     for row in range(prognosis.game_board.board_size())
                     for col in range(prognosis.game_board.board_size()))

        possible_moves = filter(MovementPrognosis.will_be_valid, all_moves)
        evaluated_moves = self.evaluate_all_states(possible_moves)
        return sorted(evaluated_moves, key=lambda move: move[0])

    def max_value(self, state, alpha, beta, depth):
        children = self.find_all_possible_moves(GameBoard(state[1]))
        if not children or depth >= self.ai_params.max_depth:
            return state[0]

        best = None
        for child in children:
            best = max(best, self.min_value(child, alpha, beta, depth + 1), lambda x: x[0] if best else -infinity)

            if best > beta:
                return best

            alpha = max(best, alpha)

        return best

    def min_value(self, state, alpha, beta, depth):
        children = self.find_all_possible_moves(state[1])
        if not children or depth >= self.ai_params.max_depth:
            return state[0]

        best = None
        for child in children:
            best = min(best, self.max_value(child.game_board, alpha, beta, depth + 1), lambda x: x[0] if best else infinity)

            if best <= alpha:
                return best

            beta = min(best, beta)

        return best

    def alpha_beta(self):
        available_moves = self.find_all_possible_moves(MovementPrognosis(self.game))

        return AiPlayer.argmax(available_moves,
                               lambda arg: self.min_value(arg, -infinity, infinity, self.ai_params.max_depth))

    @staticmethod
    def argmin(seq, fn):
        best = seq[0]
        best_score = fn(best)
        for x in seq:
            x_score = fn(x)
            if x_score < best_score:
                best, best_score = x, x_score
        return best

    @staticmethod
    def argmax(seq, fn):
        return AiPlayer.argmin(seq, lambda x: -(fn(x)))
