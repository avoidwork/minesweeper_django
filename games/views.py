from games.models import Game
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
import datetime

@require_http_methods(["GET", "HEAD", "OPTIONS"])
def index(request):
    latest_game_list = Game.objects.all().order_by('-start_date')[:5]
    return render_to_response('games/index.html', {'latest_game_list': latest_game_list})

@require_http_methods(["GET", "HEAD", "OPTIONS"])
def details(request, game_id):
    try:
        g = Game.objects.get(pk=game_id)
    except Poll.DoesNotExist:
        raise Http404
    return render_to_response('games/detail.html', {'game': g})

@require_http_methods(["GET", "HEAD", "OPTIONS"])
def move(request, game_id):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

@require_http_methods(["GET", "HEAD", "OPTIONS"])
def moves(request, game_id):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

@require_http_methods(["GET", "HEAD", "OPTIONS"])
def recently_completed(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)