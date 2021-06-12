# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from django.apps import AppConfig
from .models import Pokemon, Evolution


class PokemonConfig(AppConfig):
	name = 'pokemon'


class PokemonAdmin (admin.ModelAdmin):
	list_display = ('poke_id', 'name', 'evolution')
	list_filter = ['poke_id']

admin.site.register (Pokemon, PokemonAdmin)


class EvolutionnConfig(AppConfig):
	name = 'evolution'


class EvolutionAdmin (admin.ModelAdmin):
	list_display = ('evo_id','evolution')
	list_filter = ['evo_id']

admin.site.register (Evolution, EvolutionAdmin)
