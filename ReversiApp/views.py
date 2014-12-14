from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from ReversiApp.models import Question


def index(request):
    return render(request, 'ReversiApp/index.html', {})


def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'ReversiApp/detail.html', {'question': question})


def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def new_game(request):
    return render(request, 'ReversiApp/new/index.html', {})


def new_game_creation_result(request):

    return render(request, 'ReversiApp/new/creation_result.html', {})