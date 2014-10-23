from unittest import TestCase

from ReversiApp.fluent_flow.functional import *


class TestFunctionalFlow(TestCase):
    def setUp(self):
        pass

    def test_given_none__generator_len_should_return_none(self):
        self.assertIs(None, generator_len(None))

    def test_given_iterable__generator_len_should_return_its_length(self):
        self.assertEquals(1, generator_len((1 for _ in range(1))))
        self.assertEquals(1000, generator_len((1 for _ in range(1000))))