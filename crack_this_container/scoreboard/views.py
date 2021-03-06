from .models import Game, Solution

from django.shortcuts import render
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from ws4redis.publisher import RedisPublisher
from ws4redis.redis_store import RedisMessage


@login_required
def index(request):
    def get_or_nothing(li, index):
        try:
            return li[index].listing_text
        except IndexError:
            return ""

    game = Game.objects.latest_game()
    solutions = game.ordered_solutions
    return render(request, "index.html", {
        "game": game,
        "first_solution": get_or_nothing(solutions, 0),
        "second_solution": get_or_nothing(solutions, 1),
        "third_solution": get_or_nothing(solutions, 2),
        "solutions_count": game.solutions_count,
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
    if not game.has_started:
        return HttpResponse("Game hasn't started yet. You can't be that quick.")
    solution = Solution.create(game)

    redis_publisher = RedisPublisher(facility='solution-submitted', broadcast=True)
    message = RedisMessage(solution.listing_text)
    redis_publisher.publish_message(message)

    return HttpResponse(solution.message)
