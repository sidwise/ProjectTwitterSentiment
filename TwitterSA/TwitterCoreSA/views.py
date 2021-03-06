# from django.template import RequestContext
from django.shortcuts import render
from .models import Tweet
import logging
from TwitterCoreSA.tasks import TwitterSearch
import json

from matplotlib.pyplot import figure, title, bar, pie
import matplotlib.pyplot as plt
import numpy as np
import mpld3
import ast
# from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as plt
# import io
# from django.core.files.images import ImageFile
from collections import Counter
import operator

logger = logging.getLogger(__name__)


def dashboard(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details,

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the
    # template!

    tweets = Tweet.nodes.all()
    lemms = []
    emotions = []
    # define number of keywords to display in cloud
    NUMBER_OF_KEYWORDS = 500
    valence = []
    for t in tweets:
        if t.lemm:
            lemms += t.lemm.split()
        if t.valence:
            valence.append(t.valence)
        if t.emotion:
            for e in ast.literal_eval(t.emotion):
                # logger.warn(e)
                emotions.append(e)

    positive = sum(1 for i in valence if i > 5) * 100 / len(valence)
    negative = sum(1 for i in valence if i < 5) * 100 / len(valence)

    lemms = filter(lambda a: a != 'USER_MENTION' and a != 'URL', lemms)
    word = Counter(lemms)
    sorted_keywords = sorted(
        word.items(), key=operator.itemgetter(1), reverse=True)
    sorted_keywords = sorted_keywords[0:NUMBER_OF_KEYWORDS]
    word = dict(sorted_keywords)
    keywords = []
    for key, value in word.iteritems():
        keywords.append({'text': key.decode('utf-8'), 'size': value})

    word = Counter(emotions)
    emotions = {}
    emotions = dict(
        sorted(word.items(), key=operator.itemgetter(1), reverse=True))
    word = []
    for key, value in emotions.iteritems():
        word.append({'text': key.decode('utf-8'), 'size': value})

    # logger.warn(word)
    mpl_figure, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))
    xvalues = range(2)  # the x locations for the groups
    yvalues = [positive, negative]
    width = 0.5  # the width of the bars
    title(u'Positive and negative Emotions')
    # bar(xvalues, yvalues, width)
    labels = 'Positive', 'Negative'
    ax1.pie(yvalues,  labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)

    # fig_html = mpld3.fig_to_html(mpl_figure)

    # mpl_figure1 = figure(1, figsize=(6, 6))
    xvalues = range(len(word))
    yvalues = [x['size'] for x in word]
    tick_label = [x['text'] for x in word]
    width = 0.5  # the width of the bars
    title(u'Positive and negative Emotions')
    ax2.bar(xvalues, yvalues, width, tick_label=tick_label)
    fig_html = mpld3.fig_to_html(mpl_figure)
    context = {'tweets': json.dumps(
        keywords, ensure_ascii=False),
        'figure': fig_html,

        'sentiment': json.dumps(
        word, ensure_ascii=False)}

    # content_file = ImageFile(figure)
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request,
                  'TwitterCoreSA/index.html', context)


def search(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details,
    # for example.
    # tag = request.GET.get('tag')
    # nbr = request.GET.get('nbr')
    # if(request.GET.get('submit_but')):
    #     twitter_search.TwitterSearch(
    #         str(), str())
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the
    # template!
    # context_dict = {'boldmessage': "I am bold font from the context"}
    if request.method == 'POST':
        TwitterSearch.delay(
            str(request.POST['tag']), str(request.POST['nbr']))

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request,
                  'TwitterCoreSA/recherche.html')


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details,
    # for example.
    # tag = request.GET.get('tag')
    # nbr = request.GET.get('nbr')
    # if(request.GET.get('submit_but')):
    #     twitter_search.TwitterSearch(
    #         str(), str())
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the
    # template!
    # context_dict = {'boldmessage': "I am bold font from the context"}
    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render(request,
                  'TwitterCoreSA/dashboard.html')


# def submit(request):
#     # info = request.POST['tag']
#     # nbr = request.POST['nbr']
#     # logger.info(info)
#     # if(request.GET.get('submit_but')):
#     # context = RequestContext(request)
#     # return render(
#     #     'TwitterCoreSA/recherche.html')
