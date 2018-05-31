# -*- coding: utf-8 -*-

import time
import preprocess as pre
from twython import Twython, TwythonRateLimitError
from py2neo import authenticate, Graph  # , Node,  Relationship
from py2neo.ogm import GraphObject, Property, RelatedTo
from sentimentDic import sentiment_tweet
import preprocessor as p
# nltk.download('stopwords')
# nltk.download('wordnet')

authenticate("localhost:7474", "neo4j", "123")


class Tweet(GraphObject):
    __primarykey__ = "id_str"

    id_str = Property()
    text = Property()
    retweet_count = Property()
    favorite_count = Property()
    created_at = Property()
    lemm = Property()
    valence = Property()
    arousal = Property()
    emotion = Property()

    RETWEETS = RelatedTo("Tweet")
    REPLY_TO = RelatedTo("Tweet")
    CONTAINS = RelatedTo("Url")
    MENTIONS = RelatedTo("User")
    USING = RelatedTo("Source")

# -------------------------------------------------------------------------


class User(GraphObject):
    __primarykey__ = "name"

    # id = Property()
    # id_str = Property()
    name = Property()
    screen_name = Property()
    location = Property()
    favourites_count = Property()
    followers_count = Property()
    friends_count = Property()
    lang = Property()
    geo_enabled = Property()
    description = Property()

    POSTS = RelatedTo("Tweet")

# -------------------------------------------------------------------------


class Hashtag(GraphObject):
    __primarykey__ = "hashtag"

    hashtag = Property()

    TAGS = RelatedTo("Tweet")

# -------------------------------------------------------------------------


class Source(GraphObject):

    __primarykey__ = "name"

    name = Property()

# -------------------------------------------------------------------------


class Url(GraphObject):
    __primarykey__ = "tweet_url"

    tweet_url = Property()

    # CONTAINS = RelatedTo("Tweet")
# -------------------------------------------------------------------------

# import json
#

TWITTER_APP_KEY = 'z0JO1aunGAWu0xgxtpOMiw2qx'
TWITTER_APP_KEY_SECRET = '8vwUONvjOAfBcnNU9X1mtg9YJGPvDLjGZsZnbgs0CWhbOxYZDc'
TWITTER_ACCESS_TOKEN = '3021210887-iKtdExGlsNC6JNGqsgKdSTgjaKVjyTDLMDLiXKM'
TWITTER_ACCESS_TOKEN_SECRET = 'GdeRJ504DoANMZqDuE02vO4XFPJcux4pUzzqTCa3Gg6Oj'

t = Twython(app_key=TWITTER_APP_KEY,
            app_secret=TWITTER_APP_KEY_SECRET,
            oauth_token=TWITTER_ACCESS_TOKEN,
            oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)

search = t.cursor(t.search, q='#java',
                  count=100, lang='en')


# count = 3
graph = Graph("http://localhost:7474/db/data/")
p.set_options(p.OPT.URL, p.OPT.EMOJI, p.OPT.SMILEY,
              p.OPT.MENTION, p.OPT.NUMBER)

i = 0
for tweet in search:
    try:
        i += 1
        print i
        t1 = Tweet()
        u = User()
        t1.id_str = tweet['id_str']
        t1.text = tweet['text']
        t1.retweet_count = tweet['retweet_count']
        t1.favorite_count = tweet['favorite_count']
        t1.created_at = tweet['created_at']

        t1.lemm = pre.preprocess_tweet(tweet['text'])
        # print t1.lemm
        sentiment_tweet(t1.lemm)

        for source in tweet['source']:
            s = Source()
            s.name = tweet['source']
            graph.push(s)
            t1.USING.add(s)

        for url in tweet['entities']['urls']:
            ul = Url()
            ul.tweet_url = url['url']
            graph.push(ul)
            t1.CONTAINS.add(ul)

        t1.RETWEETS.add(t1)
        t1.REPLY_TO.add(t1)
        graph.push(t1)

        for hashtag in tweet['entities']['hashtags']:
            h = Hashtag()
            t1 = Tweet()
            h.hashtag = hashtag['text']
            h.TAGS.add(t1)
            graph.push(h)

        for user in tweet['user']:
            u = User()
            t1 = Tweet()
            u.id = tweet['user']['id']
            u.id_str = tweet['user']['id_str']
            u.name = tweet['user']['name']
            u.screen_name = tweet['user']['screen_name']
            u.location = tweet['user']['location']
            u.favourites_count = tweet['user']['favourites_count']
            u.followers_count = tweet['user']['followers_count']
            u.friends_count = tweet['user']['friends_count']
            u.lang = tweet['user']['lang']
            u.geo_enabled = tweet['user']['geo_enabled']
            u.description = tweet['user']['description']
            u.POSTS.add(t1)

            graph.push(u)

        mentions = []
        for user_t in tweet['entities']['user_mentions']:
            if tweet['user']['screen_name'] != user_t['screen_name']:
                user = t.show_user(screen_name=user_t['screen_name'])
                u1 = User()
                u1.id = user['id']
                u1.id_str = user['id_str']
                u1.name = user['name']
                u1.screen_name = user['screen_name']
                u1.location = user['location']
                u1.favourites_count = user['favourites_count']
                u1.followers_count = user['followers_count']
                u1.friends_count = user['friends_count']
                u1.lang = user['lang']
                u1.geo_enabled = user['geo_enabled']
                u1.description = user['description']
                t1.MENTIONS.add(u1)
                graph.push(u1)

        # # is reply
        if tweet['in_reply_to_status_id']:
            status = t.show_status(id=tweet['in_reply_to_status_id'])
            t2 = Tweet()
            u1 = User()
            t2.text = status['text']

            t2.retweet_count = status['retweet_count']
            t2.favorite_count = status['favorite_count']
            t2.created_at = status['created_at']
            t2.lemm = pre.preprocess_tweet(tweet['text'])
            # t2.RETWEETS.add(t1)
            t1.REPLY_TO.add(t2)
            graph.push(t2)
            # t12.MENTIONS.add(u1)
            user = t.show_user(screen_name=tweet['in_reply_to_screen_name'])
            u1.id = user['id']
            u1.id_str = user['id_str']
            u1.name = user['name']
            u1.screen_name = user['screen_name']
            u1.location = user['location']
            u1.favourites_count = user['favourites_count']
            u1.followers_count = user['followers_count']
            u1.friends_count = user['friends_count']
            u1.lang = user['lang']
            u1.geo_enabled = user['geo_enabled']
            u1.description = user['description']
            u1.POSTS.add(t2)
            graph.push(u1)

        # if i==count:
        #     pass
    except TwythonRateLimitError as error:
        remainder = float(t.get_lastfunction_header(
            header='x-rate-limit-reset')) - time.time()
        t.disconnect()
        time.sleep(remainder)
        t = Twython(app_key=TWITTER_APP_KEY,
                    app_secret=TWITTER_APP_KEY_SECRET,
                    oauth_token=TWITTER_ACCESS_TOKEN,
                    oauth_token_secret=TWITTER_ACCESS_TOKEN_SECRET)
        continue
