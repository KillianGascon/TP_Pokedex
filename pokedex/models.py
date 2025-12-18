from django.db import models

class Pokemon(models.Model):
    number = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    sprite_url = models.URLField()
    types = models.JSONField(default=list)  # Storing list of types
    height = models.FloatField()
    weight = models.FloatField()
    # Stats stored as JSON: {"hp": 30, "attack": 50, ...}
    stats = models.JSONField(default=dict)

    def __str__(self):
        return f"#{self.number} {self.name}"

class Team(models.Model):
    name = models.CharField(max_length=100)
    pokemons = models.ManyToManyField(Pokemon, related_name='teams')

    def __str__(self):
        return self.name
