# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import datetime
import json
import requests
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from .models import Pokemon, Evolution


# Create your views here.
def Insert(request, id):
    #url base
    url_evolution = 'https://pokeapi.co/api/v2/evolution-chain/' + str(id)
    url_pokemon = 'https://pokeapi.co/api/v2/pokemon/'

    # first requests
    response_evolution = requests.get(url_evolution)
    evo_chain = response_evolution.json()

    #Data pokemon
    pokemon_data = {
        "id": '',
        "name": '',
        "base_stats": '',
        "height": '',
        "weight": '',
        "evolutions": '',
    }

    #Data Evolution chain
    evolution_data = {
    }

    pokemon_data['name'] = evo_chain['chain']['species']['name']
    url_pokemon += pokemon_data['name']
    number = 0
    evolutions = evo_chain['chain']['evolves_to']

    # Requests origin pokemon
    response_pokemon = requests.get(url_pokemon)
    poke_data = response_pokemon.json()
    pokemon_data['id'] = poke_data['id']

    base_stats = {}
    for stats in poke_data['stats']:
        base_stats[stats['stat']['name']]=stats['base_stat']
    pokemon_data['base_stats'] = base_stats
    pokemon_data['weight'] = poke_data['weight']
    pokemon_data['height'] = poke_data['height']
    pokemon_data['evolutions'] = evo_chain['id']
    evolution_data[number] = pokemon_data

    SavePokemon(pokemon_data, evo_chain['id'])

    while len(evolutions) > 0:
        url_pokemon2 = 'https://pokeapi.co/api/v2/pokemon/'
        pokemon_data2 = {
            "id": '',
            "name": '',
            "base_stats": '',
            "height": '',
            "weight": '',
        }
        number += 1
        pokemon_data2['name'] = evolutions[0]['species']['name']
        url_pokemon2 += pokemon_data2['name']
        response_pokemon = requests.get(url_pokemon2)
        poke_data2 = response_pokemon.json()

        # loop requests
        pokemon_data2['id'] = poke_data2['id']
        base_stats = {}
        for stats in poke_data2['stats']:
            base_stats[stats['stat']['name']]=stats['base_stat']
        pokemon_data2['base_stats'] = base_stats
        pokemon_data2['weight'] = poke_data2['weight']
        pokemon_data2['height'] = poke_data2['height']
        evolution_data[number] = pokemon_data2
        SavePokemon(pokemon_data2, evo_chain['id'])
        evolutions = evolutions[0]['evolves_to'] # Considering only one type of evolution

    try:

        evolution = Evolution.objects.get(evo_id=evo_chain['id'])
    except Evolution.DoesNotExist:
        evolution = Evolution(evo_id=evo_chain['id'])
        evolution.evolution = evolution_data
        evolution.save()

    return JsonResponse(evolution_data)


def SavePokemon(poke_data, evo_chain):
    try:
        pokemon = Pokemon.objects.get(poke_id=poke_data['id'])
    except Pokemon.DoesNotExist:
        pokemon = Pokemon(poke_id=poke_data['id'])
        pokemon.name = poke_data['name']
        pokemon.base_stats = poke_data['base_stats']
        pokemon.height = poke_data['height']
        pokemon.weight = poke_data['weight']
        pokemon.evolution = evo_chain
        pokemon.save()
    return True


class TemplatePokemonView(TemplateView):
	template_name = './index_pokemon.html'


def Search(request):
    data = {}

    if request.method == 'POST':
        post = request.POST
        poke_name = post['poke_name']

        try:
            pokemon = Pokemon.objects.get(name=poke_name)
            data['id'] = pokemon.poke_id
            data['name'] = pokemon.name
            data['base_stats'] = pokemon.base_stats
            data['height'] = pokemon.height
            data['weight'] = pokemon.weight
            data['evolution'] = pokemon.evolution

            try:
                evolution = Evolution.objects.get(evo_id=data['evolution'])
                data['evolution'] = evolution.evolution

            except Evolution.DoesNotExist:
                data['evolution'] = {''}
        except Pokemon.DoesNotExist:
            data = {'error':True}

    else:
        data = {'error':True}
    return JsonResponse(data)
