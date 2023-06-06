import django.utils.timezone
from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(verbose_name="Имя на русском", max_length=200)
    description = models.TextField(verbose_name="Описание", null=True)
    previous_evolution = models.ForeignKey("self",
                                           on_delete=models.CASCADE,
                                           null=True,
                                           blank=True,
                                           related_name="next_evolutions",
                                           verbose_name="Предыдущая эволюция",
                                           )
    title_en = models.CharField(verbose_name="Имя на английском", blank=True, max_length=200)
    title_jp = models.CharField(verbose_name="Имя на японском", blank=True, max_length=200)
    image = models.ImageField(verbose_name="Картинка", null=True, blank=True)

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, blank=True, default=1,
                                   verbose_name="Покемон",)
    lat = models.FloatField(verbose_name="Широта",)
    lon = models.FloatField(verbose_name="Долгота",)
    appeared_at = models.DateTimeField(verbose_name="Время появления", default=django.utils.timezone.now)
    disappeared_at = models.DateTimeField(verbose_name="Время исчезновения", default=django.utils.timezone.now)
    level = models.IntegerField(verbose_name="Уровень", blank=True, null=True)
    health = models.IntegerField(verbose_name="Здоровье", blank=True, null=True)
    strength = models.IntegerField(verbose_name="Сила", blank=True, null=True)
    defence = models.IntegerField(verbose_name="Атака", blank=True, null=True)
    stamina = models.IntegerField(verbose_name="Выносливость", blank=True, null=True)
