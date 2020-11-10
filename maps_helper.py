from typing import List

import folium
from django.http import HttpRequest
from folium import Map
from django.conf import settings

from pokemon_entities.models import Pokemon


def add_pokemon(_map: Map, lat: float, lon: float, name: str, image_url: str = settings.DEFAULT_IMAGE_URL) -> None:
    """
    Set pokemon params on folium map instance
    :param _map: folium map instance
    :param lat: pokemon latitude
    :param lon: pokemon longitude
    :param name: pokemon name
    :param image_url: pokemon image url
    :return: folium map instance with pokemon params
    """
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        tooltip=name,
        icon=icon,
    ).add_to(_map)


def get_map_with_pokemons(pokemons: List[Pokemon], request: HttpRequest) -> str: # noqa
    """
    Create new folium map instance with pokemon entities
    :param pokemons: list of pokemons
    :param request: django http request object
    :return: folium map instance string representation
    """
    folium_map = folium.Map(location=settings.MOSCOW_CENTER, zoom_start=12)

    for pokemon in pokemons:
        for pokemon_entity in pokemon.entities.all():
            add_pokemon(
                folium_map, pokemon_entity.lat, pokemon_entity.lon,
                pokemon.title_en, request.build_absolute_uri(pokemon.image.url)
            )

    return folium_map._repr_html_() # noqa


def prepare_pokemons_data(pokemons: List[Pokemon]) -> List[dict]:  # noqa
    """
    Convert Pokemon's list to dict {'pokemon_id': '', 'title_ru': '', 'img_url': ''}
    :param pokemons:
    :return: dict with pokemon id, title & img_url
    """
    result = []
    for pokemon in pokemons:
        pokemon_data = {
            'pokemon_id': pokemon.pk,
            'title_ru': pokemon.title,
        }
        if pokemon.image:
            pokemon_data['img_url'] = pokemon.image.url

        result.append(pokemon_data)
    return result


def get_map_with_pokemon(pokemon: Pokemon, request: HttpRequest) -> str:  # noqa
    """
    Create new folium map instance with pokemon detail
    :param pokemon: Pokemon instance
    :param request: django http request object
    :return: folium map instance string representation
    """
    folium_map = folium.Map(location=settings.MOSCOW_CENTER, zoom_start=12)

    for pokemon_entity in pokemon.entities.all():
        add_pokemon(
            folium_map, pokemon_entity.lat, pokemon_entity.lon,
            pokemon.title_en, request.build_absolute_uri(pokemon.image.url)
        )

    return folium_map._repr_html_() # noqa


def serialize_pokemon(pokemon: Pokemon) -> dict:
    """
    Create python dict with json like pokemon data
    :param pokemon: Pokemon instance
    :return: dict with pokemon data {'pokemon_id': '', 'title_ru': '',
    'img_url': '', description: '', title_en: '', title_jp: ''}
    """
    return {
        'pokemon_id': pokemon.pk,
        'title_ru': pokemon.title,
        'description': pokemon.description,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'img_url': pokemon.image.url if pokemon.image else None,
    }


def prepare_pokemon_data(pokemon: Pokemon) -> dict:
    """
    Collect pokemon data to dict
    :param pokemon: Pokemon instance
    :return: dict with pokemon data
    """
    pokemon_data = serialize_pokemon(pokemon)

    if pokemon.previous_evolution:
        pokemon_data['previous_evolution'] = serialize_pokemon(
            pokemon.previous_evolution
        )

    if pokemon.next_evolution:
        pokemon_data['next_evolution'] = serialize_pokemon(
            pokemon.next_evolution
        )

    return pokemon_data
