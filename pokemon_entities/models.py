from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon_id = models.ForeignKey(Pokemon, on_delete=models.CASCADE, blank=True, default=1)
    lat = models.FloatField()
    lon = models.FloatField()
