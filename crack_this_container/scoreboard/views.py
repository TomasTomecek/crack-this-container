from .models import Game, Solution

from django.shortcuts import render

def index(request):
    return render(request, "index.html", {})


def api_submit_solution(request):
    game = Game.objects.latest_game()
    solution = Solution.create(
        game=game,
        name=request.POST["id"],
    )
    return JsonResponse({})
