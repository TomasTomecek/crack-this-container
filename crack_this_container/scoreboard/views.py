from .models import Game, Solution

from django.shortcuts import render
from django.http.response import HttpResponse
from django.shortcuts import redirect


def index(request):
    game = Game.objects.latest_game()
    solutions = game.ordered_solutions
    print(solutions)
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


def api_submit_solution(request):
    game = Game.objects.latest_game()
    solution = Solution.create(game)
    return HttpResponse(solution.message)
