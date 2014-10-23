from ReversiApp.fluent_flow.functional import generator_len


class Piece(object):
    def __eq__(self, other):
        return self.__class__ is other.__class__


class WhitePiece(Piece):
    pass


class BlackPiece(Piece):
    pass


class NoPiece(Piece):
    pass


class GameBoard(object):
    def __init__(self):
        self.fields = [[NoPiece() for _ in range(8)] for _ in range(8)]

    @staticmethod
    def count_fields_in_row(field_type, row):
        return generator_len(filter(lambda field: field == field_type, row))

    def count_empty_fields(self):
        return sum(self.count_fields_in_row(NoPiece(), row) for row in self.fields)

    def add_new_game_starting_pieces(self):
        self.fields[3][3] = WhitePiece()
        self.fields[3][4] = BlackPiece()
        self.fields[4][4] = WhitePiece()
        self.fields[4][3] = BlackPiece()