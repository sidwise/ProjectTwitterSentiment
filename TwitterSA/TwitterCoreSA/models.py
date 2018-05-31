# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
# Create your models here.


class Search(models.Model):
    Title = models.CharField(name="Recherche", max_length=40)
    tweet_number = models.IntegerField(name="Nombre de Tweet")

    def __unicode__(self):
        return self.name
