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
        flag = request.POST.get('flag', None)
        moves = list()

        if flag == 'true':
            flag = True
        else:
            flag = False

        print flag

        game = Game.objects.get(pk=game_id)
        mine = Mine.objects.filter(game=game, x=x, y=y).count()

        response_data = {}
        response_data['moves'] = list()
        response_data['complete'] = False

        if mine == 0:
            mines = Mine.objects.filter(game=game, x__in=[x - 1, x, x + 1], y__in=[y - 1, y, y + 1]).count()

            try:
                move = Move.objects.get(game=game, x=x, y=y)
                move.click = True

                if move.flag == True and flag == False:
                    move.flag = False

            except Move.DoesNotExist:
                move = Move(game=game, x=x, y=y, mines=mines, click=True, is_mine=False, flag=flag)

            move.save()

            if flag == False:
                moves = move.clear()

            else:
                matches = Move.objects.filter(game=game, x=x, y=y, is_mine=True).count()

                if matches == 10:
                    game.complete(True)

            response_data['moves'].insert(0, {"x": x, "y": y, "mines": mines, "click": True, "flag": flag})
            response_data['moves'] = list(itertools.chain(response_data['moves'], moves))
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
