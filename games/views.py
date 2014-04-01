from games.models import *
from django.shortcuts import redirect, render, render_to_response
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import datetime, random

def index(request):
    latest_game_list = Game.objects.all().order_by('-start_date')[:5]
    return render_to_response('games/index.html', {'latest_game_list': latest_game_list})

def new(request):
    g = Game(end_date=None)
    g.save()

    i = 0
    while (i < 9):
        x = random.randint(0, g.max_x - 1)
        y = random.randint(0, g.max_y - 1)
        m = Mine(game=g, x=x, y=y);
        m.save()
        i = i + 1

    return redirect(g)

def details(request, game_id):
    try:
        g = Game.objects.get(pk=game_id)
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/detail.html', {'game': g})

def move(request, game_id):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def moves(request, game_id):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def recently_completed(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)