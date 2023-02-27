import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render

from pokemon_entities.models import Pokemon
from django.utils import timezone

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
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    now = timezone.localtime(timezone.now())
    pokemons = Pokemon.objects.all()
    print(pokemons)
    pokemons_on_page = []
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        pokemon_image_url = request.build_absolute_uri(pokemon.image.url) if pokemon.image else DEFAULT_IMAGE_URL
        pokemon_entities = pokemon.entity.filter(appeared_at__lte=now, disappeared_at__gte=now)
        for pokemon_entity in pokemon_entities:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                pokemon_image_url
            )
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': pokemon_image_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        requested_pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')
    pokemon_image_url = request.build_absolute_uri(
        requested_pokemon.image.url) if requested_pokemon.image else DEFAULT_IMAGE_URL
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemon_specs = {
        'pokemon_id': requested_pokemon.id,
        'img_url': pokemon_image_url,
        'title_ru': requested_pokemon.title,
    }
    for pokemon_entity in requested_pokemon.entity.all():
        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_image_url
        )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_specs
    })
