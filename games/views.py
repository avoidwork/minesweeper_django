from games.models import *
from django.shortcuts import redirect, render, render_to_response
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
import datetime, json, random

def details(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        moves = Move.objects.filter(game_id=game_id)
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/detail.html', {'game': game, 'moves': moves})

def index(request):
    return redirect('/');

def new(request):
    g = Game(end_date=None)
    g.save()

    i = 0;
    while i < 10:
        x = random.randint(0, g.max_x - 1)
        y = random.randint(0, g.max_y - 1)
        t = Mine.objects.filter(game=g, x=x, y=y).count()
        if t == 0:
            m = Mine(game=g, x=x, y=y)
            m.save()
            i = i + 1

    return redirect(g)

def move(request, game_id):
    try:
        x = int(request.POST['x'])
        y = int(request.POST['y'])

        game = Game.objects.get(pk=game_id)
        mine = Mine.objects.filter(game=game, x=x, y=y).count()

        response_data = {}
        response_data['clear'] = list()
        response_data['complete'] = False

        if mine == 0:
            move = Move(game=game, x=x, y=y)
            move.save()
            cleared = move.clear()
            response_data['clear'].insert(0, {"x": x, "y": y})
            response_data['clear'] = list(itertools.chain(response_data['clear'], cleared))
            response_data['result'] = 'success'
            response_data['complete'] = game.completed
        else:
            response_data['result'] = 'failure'
            response_data['complete'] = True
            game.complete(False)

        response_data['message'] = 'Move has been processed'
    except Game.DoesNotExist:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")
