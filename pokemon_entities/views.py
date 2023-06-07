import folium

from django.shortcuts import render, get_object_or_404
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
    pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=localtime(),
                                                    disappeared_at__gt=localtime())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon_entities:
        pokemon_image = request.build_absolute_uri(get_pokemon_image_url(pokemon_entity.pokemon))

        add_pokemon(
            folium_map, pokemon_entity.lat,
            pokemon_entity.lon,
            pokemon_image
        )

    pokemons = Pokemon.objects.all()
    pokemons_on_page = []

    for pokemon in pokemons:

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(get_pokemon_image_url(pokemon)),
            'title_ru': pokemon.title,
        })

    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)

    if pokemon.id == int(pokemon_id):
        requested_pokemon = pokemon

        pokemon_data = {
            "title_ru": requested_pokemon.title,
            "title_en": requested_pokemon.title_en,
            "title_jp": requested_pokemon.title_jp,
            "description": requested_pokemon.description,
            "img_url": request.build_absolute_uri(get_pokemon_image_url(requested_pokemon)),
        }

        if pokemon.previous_evolution is not None:
            pokemon_data["previous_evolution"] = {
                "title_ru": pokemon.previous_evolution.title,
                "pokemon_id": pokemon.previous_evolution.id,
                "img_url": request.build_absolute_uri(get_pokemon_image_url(pokemon))
            }

        if pokemon.next_evolutions.all():
            next_evolutions = pokemon.next_evolutions.all()[0]
            pokemon_data["next_evolution"] = {
                "title_ru": next_evolutions.title,
                "pokemon_id": next_evolutions.id,
                "img_url": request.build_absolute_uri(get_pokemon_image_url(next_evolutions))
            }

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon.entities.all():
        if pokemon_entity.appeared_at <= localtime() <= pokemon_entity.disappeared_at:
            add_pokemon(
                folium_map, pokemon_entity.lat,
                pokemon_entity.lon,
                request.build_absolute_uri(get_pokemon_image_url(pokemon))
            )

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon_data
    })


def get_pokemon_image_url(pokemon: Pokemon):
    if pokemon.image:
        return pokemon.image.url
    else:
        return None
