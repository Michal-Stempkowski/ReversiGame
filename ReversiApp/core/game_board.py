from copy import deepcopy
from functools import reduce
from ReversiApp.fluent_flow.functional import generator_len


class Piece(object):
    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __repr__(self):
        return self.__class__.__name__

    def __hash__(self):
        return self.__class__.__name__.__hash__()


class NoPiece(Piece):
    pass


class BlackPiece(Piece):
    def get_enemy_color(self):
        return WhitePiece()


class WhitePiece(Piece):
    def get_enemy_color(self):
        return BlackPiece()


class OutOfBoardPiece(Piece):
    pass


class GameBoard(object):
    def __init__(self, fields=None):
        self.fields = fields
        if fields is None:
            self.reset_board()

    @staticmethod
    def board_size():
        return 8

    def __repr__(self):
        show = lambda piece: 'W' if piece == WhitePiece() else ('B' if piece == BlackPiece() else '.')
        append_row = lambda row: reduce(lambda line, cell: line + show(cell), row, '')

        first_line = reduce(lambda line, num: line + str(num), (x for x in range(self.board_size())), 'X|') + '\n'
        # second_line = reduce(lambda line, num: line + '_', range(self.board_size() + 2), '') + '\n'
        return first_line +  \
            reduce(lambda result, row_num: result + str(row_num) + '|' + append_row(self.fields[row_num]) + '\n',
                   range(self.board_size()), '')

    def reset_board(self):
        self.fields = [[NoPiece() for _ in range(self.board_size())] for _ in range(self.board_size())]

    def is_ready_for_new_game(self):
        return self.get_piece_from_field(3, 3) == WhitePiece() and \
               self.get_piece_from_field(3, 4) == BlackPiece() and \
               self.get_piece_from_field(4, 4) == WhitePiece() and \
               self.get_piece_from_field(4, 3) == BlackPiece() and \
               self.count_empty_fields() == self.board_size() * self.board_size() - 4

    @staticmethod
    def count_fields_in_row(field_type, row):
        return generator_len(filter(lambda field: field == field_type, row))

    def count_empty_fields(self):
        return sum(self.count_fields_in_row(NoPiece(), row) for row in self.fields)

    def count_pieces(self, piece):
        return sum(self.count_fields_in_row(piece, row) for row in self.fields)

    def insert_piece(self, row, col, piece):
        self.fields[row][col] = piece

    def offer_piece(self, row, col, player_color):
        movement_prognosis = MovementPrognosis(self)
        movement_prognosis.make_prognosis(row, col, player_color)
        return movement_prognosis

    def add_new_game_starting_pieces(self):
        self.insert_piece(3, 3, WhitePiece())
        self.insert_piece(3, 4, BlackPiece())
        self.insert_piece(4, 4, WhitePiece())
        self.insert_piece(4, 3, BlackPiece())

    def get_piece_from_field(self, row, col):
        if row < 0 or col < 0 or row >= self.board_size() or col >= self.board_size():
            return OutOfBoardPiece()
        else:
            return self.fields[row][col]

    def is_movement_possible(self, color):
        safety_boundary = self.board_size() * self.board_size() // 4
        return True if self.count_empty_fields() > safety_boundary else \
            any((self.offer_piece(row, col, color)
                     .will_be_valid()
                 for col in range(self.board_size())
                 for row in range(self.board_size())))


class MovementPrognosis(object):
    def __init__(self, game_board):
        self.converted_pieces = 0
        self.game_board = deepcopy(game_board)
        self.row = None
        self.col = None

    @staticmethod
    def all_possible_directions():
        return [(y, x) for y in [-1, 0, 1] for x in [-1, 0, 1]]

    def will_be_valid(self):
        return self.converted_pieces > 0

    def is_enemy(self, player_color, piece):
        return self.game_board.get_piece_from_field(piece[0], piece[1]) == player_color.get_enemy_color()

    def is_friend(self, player_color, piece):
        return self.game_board.get_piece_from_field(piece[0], piece[1]) == player_color

    def find_all_adjacent_enemies(self, row, column, player_color):
        adjacent_enemies = []

        neighbour_coordinates = [(row + y, column + x, (y, x)) for (y, x) in self.all_possible_directions()]

        for (y, x, direction) in neighbour_coordinates:
            if self.is_enemy(player_color, (y, x)):
                adjacent_enemies.append((y, x, direction))
        return adjacent_enemies

    def try_expanding_conversion(self, neighbour, player_color):
        to_be_converted = []

        direction = neighbour[2]
        piece = (neighbour[0], neighbour[1])

        next_field = piece
        while True:
            if self.is_enemy(player_color, next_field):
                to_be_converted.append(next_field)
            elif self.is_friend(player_color, next_field):
                return to_be_converted
            else:
                return []

            next_field = (next_field[0] + direction[0], next_field[1] + direction[1])

    def find_all_pieces_to_be_converted(self, list_of_adjacent_enemies, player_color):
        return reduce(lambda found, neighbour:
                      found + self.try_expanding_conversion(neighbour, player_color),
                      list_of_adjacent_enemies,
            [])

    def make_prognosis(self, row, column, player_color):
        if self.game_board.get_piece_from_field(row, column) != NoPiece():
            return

        adjacent_enemies = self.find_all_adjacent_enemies(row, column, player_color)
        pieces_to_be_converted = self.find_all_pieces_to_be_converted(adjacent_enemies, player_color)
        for (y, x) in pieces_to_be_converted:
            self.game_board.insert_piece(y, x, player_color)

        self.converted_pieces = len(pieces_to_be_converted)
        self.game_board.insert_piece(row, column, player_color)
        self.row = row
        self.col = column

    def next_movement_prognosis(self, row, column, player_color):
        return self.game_board.offer_piece(row, column, player_color.get_enemy_color())
