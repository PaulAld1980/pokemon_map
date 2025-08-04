from django.contrib import admin
from .models import Pokemon, PokemonEntity

admin.site.register(Pokemon)

@admin.register(PokemonEntity)
class PokemonEntityAdmin(admin.ModelAdmin):
    list_display = ('pokemon', 'lat', 'lon', 'appeared_at', 'disappeared_at', 'level', 'health', 'strength', 'defence', 'stamina')