from functools import reduce

__author__ = 'Michał'


class GameBoard(object):
    def __init__(self):
        self.fields = [[None for _ in range(8)] for _ in range(8)]

    @staticmethod
    def count_fields_in_row(field_type, row):
        return len(list(filter(lambda field: field is field_type, row)))

    def count_empty_fields(self):
        return reduce(lambda count, row:
                      count + self.count_fields_in_row(None, row), self.fields, 0)