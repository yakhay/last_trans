from django.urls import path
from . import Tournament
from . import four_players
from . import cons
# import chat.routing

websocket_urlpatterns = [
    # re_path(r'ws/socket-server/', consumers.ChatConsumer.as_asgi())
    # path('wss/socket-server/', game.RacetCunsumer.as_asgi()),
    path('wss/game/', cons.RacetCunsumer.as_asgi()),
    path('wss/tournament/', Tournament.Tournament.as_asgi()),
    path('wss/four_players/', four_players.four_players.as_asgi()),
]