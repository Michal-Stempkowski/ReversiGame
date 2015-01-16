from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from ReversiApp.core.game_container import GameContainer
from ReversiApp.core.game_logic import InitializeAction, UnreachableGameStateException
from ReversiApp.mocks.system_mocks import SystemMessageBusMockWithMessageLog
# from ReversiApp.models import Question
from ReversiApp.models import GameBoardRecord


def index(request):
    return render(request, 'ReversiApp/index.html', {})


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'ReversiApp/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def new_game(request):
    return render(request, 'ReversiApp/new/index.html', {})


def new_game_creation_result(request):
    message_bus1 = SystemMessageBusMockWithMessageLog()
    message_bus2 = SystemMessageBusMockWithMessageLog()

    game_container = GameContainer.create(message_bus1, message_bus2)

    try:
        game_container.game_logic.perform_action(InitializeAction())
    except UnreachableGameStateException:
        return render(request, 'ReversiApp/new/creation_result__initialization_has_failed.html', {})

    return render(request, 'ReversiApp/new/creation_result__OK.html', {})


def load_game(request):
    return render(request, 'ReversiApp/meta/meta_table_1d.html', {'meta_table' : GameBoardRecord.objects.all()})