from django.db import models


class Pokemon(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    image = models.ImageField(null=True, blank=True, upload_to='poko_images', verbose_name='Изображение')
    description = models.TextField(blank=True, verbose_name='Описание')
    title_en = models.CharField(max_length=200, blank=True, verbose_name='Английское название')
    title_ja = models.CharField(max_length=200, blank=True, verbose_name='Японское название')
    previous_evolution = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='next_evolution', verbose_name='Предыдущая эволюция')

    class Meta:
        verbose_name = 'Покемон'
        verbose_name_plural = 'Покемоны'

    def __str__(self):
        return self.title


class PokemonEntity(models.Model):
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE, verbose_name='Вид покемона')
    lat = models.FloatField(verbose_name='Широта места появления')
    lon = models.FloatField(verbose_name='Долгота места появления')
    appeared_at = models.DateTimeField(verbose_name='Время появления')
    disappeared_at = models.DateTimeField(verbose_name='Время исчезновения')
    level = models.IntegerField(null=True, blank=True, verbose_name='Уровень')
    health = models.IntegerField(null=True, blank=True, verbose_name='Здоровье')
    strength = models.IntegerField(null=True, blank=True, verbose_name='Сила')
    defence = models.IntegerField(null=True, blank=True, verbose_name='Защита')
    stamina = models.IntegerField(null=True, blank=True, verbose_name='Выносливость')

    class Meta:
        verbose_name = 'Характеристика покемона'
        verbose_name_plural = 'Характеристики покемонов'

    def __str__(self):
        return f"{self.pokemon.title} ({self.lat}, {self.lon})"
