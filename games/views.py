from games.models import *
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse
import itertools, json, random, time

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

    for i in range(10):
        x = random.randint(0, g.max_x - 1)
        y = random.randint(0, g.max_y - 1)
        m = Mine(game=g, x=x, y=y)
        m.save()

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
        response_data['epoch'] = None

        if mine == 0:
            move = Move(game=game, x=x, y=y)
            move.save()
            cleared = move.clear()
            response_data['clear'].insert(0, {"x": x, "y": y})
            response_data['clear'] = list(itertools.chain(response_data['clear'], cleared))
            response_data['result'] = 'success'
            response_data['complete'] = game.completed
            response_data['epoch'] = int(time.mktime(move.move_date.timetuple())*1000)/1000
        else:
            response_data['result'] = 'failure'
            response_data['complete'] = True
            game.complete(False)

        response_data['message'] = 'Move has been processed'
    except Game.DoesNotExist:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")
