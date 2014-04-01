from games.models import Game
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
import datetime

def index(request):
    latest_game_list = Game.objects.all().order_by('-start_date')[:5]
    return render_to_response('games/index.html', {'latest_game_list': latest_game_list})

def details(request, game_id):
    try:
        g = Game.objects.get(pk=game_id)
    except Poll.DoesNotExist:
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