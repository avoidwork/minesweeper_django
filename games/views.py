from games.models import *
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponse, Http404
import json


def details(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        moves = Move.objects.filter(game_id=game_id)
    except Game.DoesNotExist:
        raise Http404
    return render_to_response('games/detail.html', {'game': game, 'moves': moves})


def index(request):
    return redirect('/')


def new(request):
    g = Game(end_date=None)
    g.save()

    return redirect(g)


def move(request, game_id):
    try:
        game = Game.objects.get(pk=game_id)
        data = json.loads(request.body)
        x = data.get('x', 0)
        y = data.get('y', 0)
        flag = data.get('flag', False)
        visited = data.get('visited', False)
        maybe = data.get('maybe', False)
        moves = list()
        click = True
        had_flag = False
        is_mine = True if Mine.objects.filter(game=game, x=x, y=y).count() > 0 else False
        new_move = True
        matches = 0
        mines = 0
        response_data = dict(moves=list(), complete=False)

        try:
            move = Move.objects.get(game=game, x=x, y=y)
            new_move = False

        except Move.DoesNotExist:
            move = Move(game=game, x=x, y=y, click=click, is_mine=is_mine, visited=visited)

        if game.started is False:
            game.create_mines(x, y)

        move.mines = move.count_mines()

        if (new_move and flag) or is_mine is False or move.flag is not flag or move.maybe is not maybe:
            if move.flag and flag is False and maybe is True:
                move.flag = False
                move.maybe = True
                move.click = False
                click = False
                had_flag = True
                is_mine = False

            elif move.flag is False and flag:
                move.flag = True
                move.click = False
                click = False
                is_mine = False

            elif move.maybe is True and maybe is False:
                move.maybe = False
                had_flag = True

                if visited is False:
                    is_mine = False
                    move.click = False
                    click = False

            else:
                move.click = True

        else:
            move.is_mine = True
            move.click = True

        if visited is True:
            move.click = True

        move.save()

        if flag is False and maybe is False:
            mines = move.mines

        if is_mine:
            response_data['result'] = 'failure'
            response_data['complete'] = True
            game.complete(False)

        else:
            if visited or (flag is False and had_flag is False):
                moves = move.clear()

            else:
                matches = Move.objects.filter(game=game, is_mine=True, flag=True).count()

            if matches == 10:
                game.complete(True)

            response_data['moves'].insert(0, dict(x=x, y=y, mines=mines, click=click, visited=visited, flag=flag,
                                                  maybe=maybe))
            response_data['moves'] = list(itertools.chain(response_data['moves'], moves))
            response_data['result'] = 'success'
            response_data['complete'] = game.completed

        response_data['message'] = 'Move has been processed'
    except Game.DoesNotExist:
        raise Http404
    return HttpResponse(json.dumps(response_data), content_type='application/json')
