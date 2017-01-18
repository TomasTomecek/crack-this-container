from .models import Game, Solution

from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage


def index(request):
    game = Game.objects.latest_game()
    solutions = game.ordered_solutions
    return render(request, "index.html", {
        "game": game,
        "solutions": solutions,
    })


def start_game(request, game_id):
    game = Game.objects.get(id=game_id)
    game.start_game()
    return redirect("index")


def create_game(request):
    game = Game.create()
    return redirect("index")


def api_start_latest_game(request):
    game = Game.objects.latest_game()
    game.start_game()
    return JsonResponse({})


def api_submit_solution(request):
    game = Game.objects.latest_game()
    solution = Solution.create(game)

    redis_publisher = RedisPublisher(facility='solution-submitted', broadcast=True)
    message = RedisMessage(solution.listing_text)
    redis_publisher.publish_message(message)

    return HttpResponse(solution.message)
