from django.test import TestCase
from .models import Pokemon, Team

class PokemonModelTest(TestCase):
    def setUp(self):
        self.pokemon = Pokemon.objects.create(
            number=1,
            name="bulbasaur",
            sprite_url="http://example.com/sprite.png",
            types=["grass", "poison"],
            height=0.7,
            weight=6.9,
            stats={"hp": 45, "attack": 49}
        )

    def test_pokemon_creation(self):
        self.assertEqual(self.pokemon.name, "bulbasaur")
        self.assertEqual(self.pokemon.types[0], "grass")

class TeamModelTest(TestCase):
    def setUp(self):
        self.pokemon = Pokemon.objects.create(
            number=25,
            name="pikachu",
            sprite_url="http://example.com/pikachu.png",
            types=["electric"],
            height=0.4,
            weight=6.0,
            stats={"hp": 35, "attack": 55}
        )
        self.team = Team.objects.create(name="Ash's Team")

    def test_team_management(self):
        self.team.pokemons.add(self.pokemon)
        self.assertEqual(self.team.pokemons.count(), 1)
        self.assertEqual(self.team.pokemons.first().name, "pikachu")
        
        self.team.pokemons.remove(self.pokemon)
        self.assertEqual(self.team.pokemons.count(), 0)
