from django.shortcuts import render, get_object_or_404

from pokemon_entities.models import Pokemon
from maps_helper import get_map_with_pokemon, prepare_pokemon_data
from maps_helper import get_map_with_pokemons, prepare_pokemons_data


def show_all_pokemons(request):
    pokemons = Pokemon.objects.prefetch_related('entities').all()

    folium_map_html = get_map_with_pokemons(pokemons, request)

    pokemons_on_page = prepare_pokemons_data(pokemons)

    return render(request, 'mainpage.html', context={
        'map': folium_map_html,
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(
        Pokemon.objects.prefetch_related('entities'), pk=pokemon_id
    )

    folium_map_html = get_map_with_pokemon(pokemon, request)

    pokemon_data = prepare_pokemon_data(pokemon)

    return render(request, "pokemon.html", context={
        'map': folium_map_html,
        'pokemon': pokemon_data
    })
