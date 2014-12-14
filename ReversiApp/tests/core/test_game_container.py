from django.test import TestCase
from ReversiApp.core.game_container import GameContainer
from ReversiApp.mocks.system_mocks import SystemMessageBusMockWithMessageLog


class WhenManagingGame(TestCase):
    def setUp(self):
        pass

    def test_should_be_able_to_create_game_container(self):
        game_container = GameContainer.create(
            SystemMessageBusMockWithMessageLog(),
            SystemMessageBusMockWithMessageLog())