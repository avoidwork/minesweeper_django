from games.models import *
from django.shortcuts import redirect, render, render_to_response
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import datetime, json, random

@csrf_exempt
def details(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        moves = Move.objects.filter(game_id=game_id)
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/detail.html', {'game': game, 'moves': moves})

@csrf_exempt
def index(request):
    return redirect('/');

@csrf_exempt
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

@csrf_exempt
def move(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        x = int(request.POST['x'])
        y = int(request.POST['y'])
        moves = list()
        click = True
        had_flag = False
        is_mine = False
        matches = 0
        flag = False

        if request.POST.get('flag', None) == 'true':
            flag = True

        response_data = {}
        response_data['moves'] = list()
        response_data['complete'] = False

        if Mine.objects.filter(game=game, x=x, y=y).count() > 0:
            is_mine = True

        try:
            move = Move.objects.get(game=game, x=x, y=y)

            if is_mine == False:
                if move.flag == True and flag == False:
                    move.flag = False
                    is_mine = False
                    had_flag = True

                elif move.flag == False and flag == True:
                    move.flag = True
                    is_mine = False

                else:
                    move.click = True

            else:
                move.is_mine = True
                move.click = True

        except Move.DoesNotExist:
            if flag == True:
                click = False

            move = Move(game=game, x=x, y=y, click=click, flag=flag)
            move.count_mines()

        move.save()

        if is_mine == True:
            response_data['result'] = 'failure'
            response_data['complete'] = True
            game.complete(False)

        else:
            if flag == False and had_flag == False:
                moves = move.clear()

            else:
                matches = Move.objects.filter(game=game, is_mine=True, flag=True).count()

            if matches == 10:
                game.complete(True)
            
            response_data['moves'].insert(0, {"x": x, "y": y, "mines": move.mines, "click": True, "flag": flag})
            response_data['moves'] = list(itertools.chain(response_data['moves'], moves))
            response_data['result'] = 'success'
            response_data['complete'] = game.completed

        response_data['message'] = 'Move has been processed'
    except Game.DoesNotExist:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")
