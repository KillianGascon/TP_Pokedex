from django.urls import path
from . import views

app_name = 'pokedex'

urlpatterns = [
    path('', views.index, name='index'),
    path('pokemon/<int:pokemon_id>/', views.pokemon_detail, name='pokemon_detail'),
    path('teams/', views.team_list, name='team_list'),
    path('teams/create/', views.create_team, name='create_team'),
    path('teams/<int:team_id>/add/', views.add_pokemon_to_team, name='add_pokemon_to_team'),
    path('teams/<int:team_id>/remove/<int:pokemon_id>/', views.remove_pokemon_from_team, name='remove_pokemon_from_team'),
    path('combat/', views.combat, name='combat'),
    path('combat/start/', views.start_combat, name='start_combat'),
    path('combat/<int:team1_id>/vs/<int:team2_id>/', views.team_battle, name='team_battle'),
    path('teams/<int:team_id>/delete/', views.delete_team, name='delete_team'),
]
