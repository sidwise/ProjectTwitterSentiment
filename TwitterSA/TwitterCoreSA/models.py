# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django_neomodel import DjangoNode
from neomodel import StructuredNode, StringProperty, DateProperty, IntegerProperty, FloatProperty, Relationship
from . import twitter_search
from TwitterCoreSA.tasks import TwitterSearch
# Create your models here.


class Search(models.Model):
    title = models.CharField(name="Titre", max_length=40)
    tweet_number = models.IntegerField(name="Nombre de Tweet")
    search_query = models.CharField(name="Recherche", max_length=40)

    def __unicode__(self):
        return self.title

    def run_search(self):
        TwitterSearch.delay(self.search_query, self.tweet_number)


class TweetSAAnalytics(models.Model):
    # search = models.ForeignKey(Search, on_delete=models.CASCADE)
    title = models.CharField(name="Titre", max_length=40)
    number_positive_tweets = models.IntegerField(name="Positive Tweets")
    number_negative_tweets = models.IntegerField(name="Negative Tweets")


class Source(StructuredNode):
    name = StringProperty()


class Tweet(StructuredNode):

    id_str = IntegerProperty()
    text = StringProperty()
    retweet_count = IntegerProperty()
    favourites_count = IntegerProperty()
    created_at = StringProperty()
    lemm = StringProperty()
    valence = FloatProperty()
    arousal = FloatProperty()
    emotion = StringProperty()

    retweets = Relationship('Tweet', 'retweets')
    reply_to = Relationship('Tweet', 'reply_to')
    contains = Relationship('Url', 'contains')
    mentions = Relationship('User', 'mentions')
    using = Relationship('Source', 'using')


class User(StructuredNode):

    name = StringProperty()
    screen_name = StringProperty()
    location = StringProperty()
    lang = StringProperty()
    favourites_count = IntegerProperty()
    followers_count = IntegerProperty()
    friends_count = IntegerProperty()
    description = StringProperty()

    posts = Relationship('Tweet', 'posts')


class Hashtag(StructuredNode):
    name = StringProperty()


class Url(StructuredNode):
    tweet_url = StringProperty()
