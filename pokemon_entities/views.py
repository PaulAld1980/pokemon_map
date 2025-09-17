import folium

from django.http import HttpResponseNotFound
from django.shortcuts import render
from .models import Pokemon, PokemonEntity
from django.utils.timezone import localtime


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = localtime()
    pokemons = Pokemon.objects.all()
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in PokemonEntity.objects.filter(appeared_at__lte=now, disappeared_at__gte=now):
            img_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url) if pokemon_entity.pokemon.image else DEFAULT_IMAGE_URL
            add_pokemon(
                folium_map,
                pokemon_entity.lat,
                pokemon_entity.lon,
                img_url,
            )
    pokemons_on_page = []
    for pokemon in pokemons:
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'title_ru': pokemon.title,
            'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL
        })
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    now = localtime()
    for pokemon_entity in PokemonEntity.objects.filter(pokemon=pokemon, appeared_at__lte=now, disappeared_at__gte=now):
        img_url = request.build_absolute_uri(pokemon_entity.pokemon.image.url) if pokemon_entity.pokemon.image else DEFAULT_IMAGE_URL
        add_pokemon(
            folium_map,
            pokemon_entity.lat,
            pokemon_entity.lon,
            img_url
        )

    pokemon_data = {
        'pokemon_id': pokemon.id,
        'title_ru': pokemon.title,
        'title_en': pokemon.title_en if pokemon.title_en else '',
        'title_ja': pokemon.title_ja if pokemon.title_ja else '',
        'img_url': request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL,
        'description': pokemon.description if pokemon.description else '',
        'previous_evolution': {
            'pokemon_id': pokemon.previous_evolution.id,
            'title_ru': pokemon.previous_evolution.title,
            'img_url': request.build_absolute_uri(pokemon.previous_evolution.image.url) if pokemon.previous_evolution.image else DEFAULT_IMAGE_URL
            } if pokemon.previous_evolution else None,
        'next_evolution': {
            'pokemon_id': pokemon.next_evolutions.first().id,
            'title_ru': pokemon.next_evolutions.first().title,
            'img_url': request.build_absolute_uri(pokemon.next_evolutions.first().image.url) if pokemon.next_evolutions.first().image else DEFAULT_IMAGE_URL
            } if pokemon.next_evolutions.first() else None
        }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(),
        'pokemon': pokemon_data
    })
