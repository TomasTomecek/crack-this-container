"""crack_this_container URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from scoreboard import views

from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^game/(?P<game_id>[0-9]+)/$', views.start_game, name='game-start'),
    url(r'^game/create/$', views.create_game, name='game-create'),
    url(r'^api/v0/solutions/$', views.api_submit_solution, name='api-submit-solution'),
    url(r'^api/v0/game/latest/start/$', views.api_start_latest_game, name='api-game-start'),
]
