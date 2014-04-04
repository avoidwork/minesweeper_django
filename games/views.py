from games.models import *
from django.shortcuts import redirect, render, render_to_response
from django.http import HttpResponse, Http404
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import datetime, json

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
        new_move = True
        flag = False
        visited = False
        maybe = False
        matches = 0
        mines = 0
        response_data = {}
        response_data['moves'] = list()
        response_data['complete'] = False

        if request.POST.get('flag', None) == 'true':
            flag = True

        if request.POST.get('visited', None) == 'true':
            visited = True

        if request.POST.get('maybe', None) == 'true':
            maybe = True

        if Mine.objects.filter(game=game, x=x, y=y).count() > 0:
            is_mine = True

        try:
            move = Move.objects.get(game=game, x=x, y=y)
            new_move = False

        except Move.DoesNotExist:
            if flag == True:
                click = False

            move = Move(game=game, x=x, y=y, click=click, flag=flag, is_mine=is_mine, visited=visited)

        if game.started == False:
            game.create_mines(x, y)

        move.mines = move.count_mines()

        if (new_move and flag) or is_mine == False or move.flag != flag:
            is_mine = False

            if move.flag and flag == False and maybe == True:
                move.flag = False
                move.click = False
                move.maybe = True
                click = False
                had_flag = True

            elif move.flag == False and flag:
                move.flag = True
                click = False

            elif move.maybe == True and maybe == False:
                move.maybe = False
                had_flag = True

            else:
                move.click = True

        else:
            move.is_mine = True
            move.click = True

        move.save()

        if flag == False:
            mines = move.mines

        if is_mine:
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
            
            response_data['moves'].insert(0, {"x": x, "y": y, "mines": mines, "click": click, "visited": visited, "flag": flag, "maybe": maybe})
            response_data['moves'] = list(itertools.chain(response_data['moves'], moves))
            response_data['result'] = 'success'
            response_data['complete'] = game.completed

        response_data['message'] = 'Move has been processed'
    except Game.DoesNotExist:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type="application/json")
