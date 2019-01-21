from django.urls import path

from . import views

urlpatterns = [
    path('', views.calendar_view, name='calendar'),
    path('myCalendar',views.calendar_view,name="myCalendar"),
    path('monthDetail',views.month_detail_view,name='monthDetail'),
    path('addGames',views.add_games_view,name='addGames'),
    path('searchGames',views.search_games_view,name='searchGames'),
    path('addGameToProfile',views.add_game_to_profile_view,name='addGameToProfile'),
    path('removeGameFromProfile',views.remove_game_from_profile_view,name='removeGameFromProfile'),
    path('addNewGame',views.add_new_game_view,name='addNewGame'),
    path('about',views.about_view,name='about'),
]