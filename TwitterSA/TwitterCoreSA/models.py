# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from . import twitter_search
# Create your models here.


class Search(models.Model):
    title = models.CharField(name="Titre", max_length=40)
    tweet_number = models.IntegerField(name="Nombre de Tweet")
    search_query = models.CharField(name="Recherche", max_length=40)

    def __unicode__(self):
        return self.title

    def run_search(self):
        twitter_search.TwitterSearch(self.search_query, self.tweet_number)


class TweetSAAnalytics(models.Model):
    title = models.CharField(name="Titre", max_length=40)
    number_positive_tweets = models.IntegerField(name="Positive Tweets")
    number_negative_tweets = models.IntegerField(name="Negative Tweets")
