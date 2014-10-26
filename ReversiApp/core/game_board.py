from functools import reduce
from ReversiApp.fluent_flow.functional import generator_len


class Piece(object):
    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __repr__(self):
        return self.__class__.__name__


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
    def __init__(self):
        self.fields = None
        self.reset_board()

    @staticmethod
    def board_size():
        return 8

    def reset_board(self):
        self.fields = [[NoPiece() for _ in range(self.board_size())] for _ in range(self.board_size())]

    @staticmethod
    def count_fields_in_row(field_type, row):
        return generator_len(filter(lambda field: field == field_type, row))

    def count_empty_fields(self):
        return sum(self.count_fields_in_row(NoPiece(), row) for row in self.fields)

    def insert_piece(self, row, col, piece):
        self.fields[row][col] = piece

    def offer_piece(self, row, col, player_color):
        movement_prognosis = MovementPrognosis(self)
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


class MovementPrognosis(object):
    def __init__(self, game_board):
        self.converted_pieces = 0
        self.game_board = game_board

    @staticmethod
    def all_possible_directions():
        return [(y, x) for y in [-1, 0, 1] for x in [-1, 0, 1]]

    def will_be_valid(self):
        return False

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
