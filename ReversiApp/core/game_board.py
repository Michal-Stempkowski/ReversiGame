from ReversiApp.fluent_flow.functional import generator_len


class Piece(object):
    def __eq__(self, other):
        return self.__class__ is other.__class__

    def __repr__(self):
        return self.__class__.__name__


class NoPiece(Piece):
    pass


class BlackPiece(Piece):
    pass


class WhitePiece(Piece):
    pass


class GameBoard(object):
    def __init__(self):
        self.fields = None
        self.reset_board()

    def reset_board(self):
        self.fields = [[NoPiece() for _ in range(8)] for _ in range(8)]

    @staticmethod
    def count_fields_in_row(field_type, row):
        return generator_len(filter(lambda field: field == field_type, row))

    def count_empty_fields(self):
        return sum(self.count_fields_in_row(NoPiece(), row) for row in self.fields)

    def insert_piece(self, row, col, piece):
        self.fields[row][col] = piece

    def add_new_game_starting_pieces(self):
        self.insert_piece(3, 3, WhitePiece())
        self.insert_piece(3, 4, BlackPiece())
        self.insert_piece(4, 4, WhitePiece())
        self.insert_piece(4, 3, BlackPiece())

    def get_piece_from_field(self, row, col):
        return self.fields[row][col]