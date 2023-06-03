import django.utils.timezone
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    title_en = models.CharField(null=True, max_length=200)
    title_jp = models.CharField(null=True, max_length=200)
    image = models.ImageField(null=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon_id = models.ForeignKey(Pokemon, on_delete=models.CASCADE, blank=True, default=1)
    lat = models.FloatField()
    lon = models.FloatField()
    appeared_at = models.DateTimeField(default=django.utils.timezone.now())
    disappeared_at = models.DateTimeField(default=django.utils.timezone.now())
    level = models.IntegerField(blank=True, null=True)
    health = models.IntegerField(blank=True, null=True)
    strength = models.IntegerField(blank=True, null=True)
    defence = models.IntegerField(blank=True, null=True)
    stamina = models.IntegerField(blank=True, null=True)
