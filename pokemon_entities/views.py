import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
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
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon in pokemons:
        for pokemon_entity in pokemon_entities:
            img_url = None

            if pokemon.image:
                img_url = request.build_absolute_uri(pokemon.image.url)

            if pokemon_entity.appeared_at <= localtime() <= pokemon_entity.disappeared_at:
                add_pokemon(
                    folium_map, pokemon_entity.lat,
                    pokemon_entity.lon,
                    img_url
                )

    pokemons_on_page = []

    for pokemon in pokemons:
        img_url = None

        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemons = Pokemon.objects.all()
    pokemon_entities = PokemonEntity.objects.all()

    for pokemon in pokemons:
        img_url = None

        if pokemon.image:
            img_url = request.build_absolute_uri(pokemon.image.url)

        if pokemon.id == int(pokemon_id):
            requested_pokemon = pokemon

            pokemon_data = {
                "title_ru": requested_pokemon.title,
                "title_en": requested_pokemon.title_en,
                "title_jp": requested_pokemon.title_jp,
                "description": requested_pokemon.description,
                "img_url": img_url,
            }

            if pokemon.evolution_from:
                pokemon_data["previous_evolution"] = {
                    "title_ru": pokemon.evolution_from.title,
                    "pokemon_id": pokemon.evolution_from.id,
                    "img_url": request.build_absolute_uri(pokemon.evolution_from.image.url)
                }

            break
    else:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        if pokemon_entity.appeared_at <= localtime() <= pokemon_entity.disappeared_at:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                img_url
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })
