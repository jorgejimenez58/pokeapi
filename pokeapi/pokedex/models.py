# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Pokemon(models.Model):
    poke_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=30, unique=True)
    weight = models.IntegerField()
    height = models.IntegerField()
    base_stats = models.JSONField(default={})
    evolution = models.CharField(max_length=30, blank=True, null=True,
                                        verbose_name="Evolution Chain")

    def __unicode__(self):
    	return self.poke_id


class Evolution(models.Model):
    evo_id = models.IntegerField(unique=True)
    origin = models.BooleanField(default=True)
    evolution = models.JSONField(default={})

    def __unicode__(self):
    	return self.evo_id
