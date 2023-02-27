from django.db import models  # noqa F401


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name="название")
    title_en = models.CharField(max_length=200, blank=True, verbose_name="название на английском")
    title_jp = models.CharField(max_length=200, blank=True, verbose_name="название на японском")
    image = models.ImageField(upload_to='photos', null=True, blank=True, verbose_name="изображение")
    description = models.TextField(blank=True, verbose_name="описание")
    previous_evolution = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL,
                                           verbose_name='Из кого эволюционировал', related_name='previous_pokemon')

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, related_name='entity', verbose_name="покемон")
    lat = models.FloatField(blank=True, verbose_name="широта")
    lon = models.FloatField(blank=True, verbose_name="долгота")
    appeared_at = models.DateTimeField(null=True, blank=True, verbose_name="время появления")
    disappeared_at = models.DateTimeField(null=True, blank=True, verbose_name="время исчезновения")
    level = models.IntegerField(null=True, blank=True, verbose_name="уровень")
    health = models.IntegerField(null=True, blank=True, verbose_name="здоровье")
    strength = models.IntegerField(null=True, blank=True, verbose_name="сила")
    defence = models.IntegerField(null=True, blank=True, verbose_name="защита")
    stamina = models.IntegerField(null=True, blank=True, verbose_name="выносливость")

    def __str__(self):
        return self.pokemon.title
