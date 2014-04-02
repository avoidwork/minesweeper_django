from games.models import *
from django.shortcuts import redirect, render, render_to_response
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import datetime, json, random

def index(request):
    return redirect('/');

def new(request):
    g = Game(end_date=None)
    g.save()

    i = 0
    while (i < 9):
        x = random.randint(0, g.max_x - 1)
        y = random.randint(0, g.max_y - 1)
        m = Mine(game=g, x=x, y=y)
        m.save()
        i = i + 1

    return redirect(g)

def details(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        moves = Move.objects.filter(game_id=game_id)
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/detail.html', {'game': game, 'moves': moves})

def move(request, game_id):
    try:
        i = request.POST['game']
        x = request.POST['x']
        y = request.POST['y']
        g = Game.objects.get(pk=i)
        m = Move(game=g, x=x, y=y)
        move.save()
    except Game.DoesNotExist:
        raise Http404
    return HttpResponse({result: 'ok'}, content_type="application/json")

def moves(request, game_id):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

def recently_completed(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)