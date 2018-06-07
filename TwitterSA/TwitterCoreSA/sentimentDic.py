# -*- coding: utf-8 -*-
import csv
import os
from nltk.stem import WordNetLemmatizer
import logging
logger = logging.getLogger(__name__)


def csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csvreader = csv.reader(utf8_data, delimiter=',', dialect=dialect, **kwargs)
    for row in csvreader:
        yield [unicode(cell, 'utf-8') for cell in row]


def get_Anew():
    abspath = os.path.abspath('all.csv')
    cr = csv_reader(open(abspath))
    anew = {}
    lemmatizer = WordNetLemmatizer()
    for row in cr:
        description = lemmatizer.lemmatize(row[0])

        vals = {'valence_mean': float(row[2]),
                'valence_SD':  float(row[3]),
                'arousel_mean': float(row[4]),
                'arousel_SD': float(row[5])}
        anew.update({description: vals})
    logger.warn("ANEW===================")
    logger.warn(anew.keys())
    return anew


def sentiment_tweet(lemm_tab, anew):
    v1 = 0
    v2 = 0
    v3 = 0
    v4 = 0
    v5 = 0
    v6 = 0
    sentiment = []
    emotion = []
    sentiment_str = [['sad', 'unhappy', 'depressed', 'bored'],
                     ['upset', 'stressed', 'nervous', 'tense'],
                     ['calm', 'relaxed', 'serene', 'contented'],
                     ['alert', 'excited', 'elated', 'happy']]
    logger.warn("============= term")

    for term in lemm_tab:
        logger.warn(term)
        if term in anew.keys():
            v1 += anew[term]['valence_mean'] / anew[term]['valence_SD']
            v2 += 1 / anew[term]['valence_SD']
            v3 += anew[term]['arousel_mean'] / anew[term]['arousel_SD']
            v4 += 1 / anew[term]['arousel_SD']
            v5 = v1 / v2
            v6 = v3 / v4
    sentiment.append(v5)
    sentiment.append(v6)
    if len(sentiment) > 0:
        if v5 < 5 and v6 < 5:
            emotion.append(sentiment_str[0][int(v5) - 1])
            if int(v5) != int(v6):
                emotion.append(sentiment_str[0][int(v6) - 1])
        elif v5 < 5 and v6 > 5:
            emotion.append(sentiment_str[1][int(v5) - 1])
            if int(v5) != int(v6):
                emotion.append(sentiment_str[1][int(v6) - 5])
        elif v5 > 5 and v6 < 5:
            emotion.append(sentiment_str[2][int(v5) - 5])
            if int(v5) != int(v6):
                emotion.append(sentiment_str[2][int(v6) - 1])
        else:
            emotion.append(sentiment_str[3][int(v5) - 5])
            if int(v5) != int(v6):
                emotion.append(sentiment_str[3][int(v6) - 5])

        return sentiment, emotion
    else:
        return False, False
