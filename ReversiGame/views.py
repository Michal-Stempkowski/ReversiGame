from django.http import HttpResponse
from django.template import loader, Context


def game(request):
    template = loader.get_template('game.html')
    context = Context({

    })
    return HttpResponse(template.render(context))