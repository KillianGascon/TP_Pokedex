from django.core.management.base import BaseCommand
import requests
from pokedex.models import Pokemon

class Command(BaseCommand):
    help = 'Imports the first 251 Pokemon from PokeAPI'

    def handle(self, *args, **kwargs):
        self.stdout.write('Starting Pokemon import...')
        
        # Using 5 for test to save time, then 252 for real
        # Requirements say 251.
        for i in range(1, 252):
            url = f"https://pokeapi.co/api/v2/pokemon/{i}"
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    types = [t['type']['name'] for t in data['types']]
                    stats = {s['stat']['name']: s['base_stat'] for s in data['stats']}
                    
                    pokemon, created = Pokemon.objects.update_or_create(
                        number=data['id'],
                        defaults={
                            'name': data['name'].capitalize(),
                            'sprite_url': data['sprites']['front_default'],
                            'types': types,
                            'height': data['height'] / 10,
                            'weight': data['weight'] / 10,
                            'stats': stats,
                        }
                    )
                    if i % 10 == 0:
                        self.stdout.write(f"Processed {i}/251")
                else:
                    self.stdout.write(self.style.ERROR(f"Failed to fetch Pokemon #{i}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error fetching #{i}: {e}"))

        self.stdout.write(self.style.SUCCESS('Successfully imported Pokemon'))
