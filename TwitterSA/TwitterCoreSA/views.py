from django.template import RequestContext
from django.shortcuts import render_to_response, render
from .models import Tweet
import logging
from TwitterCoreSA.tasks import TwitterSearch
import json
# from wordcloud import WordCloud, STOPWORDS
# import matplotlib.pyplot as plt
# import io
# from django.core.files.images import ImageFile
from collections import Counter
import operator

logger = logging.getLogger(__name__)


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details,
    # for example.

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the
    # template!
    # context_dict = {'boldmessage': "I am bold font from the context"}

    tweets = Tweet.nodes.all()
    lemms = []
    # define maximum rank as weight for CSS tags
    MAX_WEIGHT = 5
    # define number of keywords to display in cloud
    NUMBER_OF_KEYWORDS = 200
    for t in tweets:
        if t.lemm:
            lemms += t.lemm.split()
    lemms = filter(lambda a: a != 'USER_MENTION' and a != 'URL', lemms)
    word = Counter(lemms)
    # wordcloud = WordCloud(width=1000, height=500).generate(" ".join(lemms))
    sorted_keywords = sorted(
        word.items(), key=operator.itemgetter(1), reverse=True)
    sorted_keywords = sorted_keywords[0:NUMBER_OF_KEYWORDS]
    word = dict(sorted_keywords)

    # logger.info(word)
    # keywords = '['
    keywords = []
    for key, value in word.iteritems():
        # keywords += "{text: '" + key + "', " + "size: " + str(value) + "}"
        keywords.append({'text': key, 'size': value})
    #     i += 1
    #     if i < NUMBER_OF_KEYWORDS:
    #         keywords += ","
    #     # keywords.append({'text': key, 'size': value})
    # keywords += "]"
    # keywords = json.dumps(keywords)

    # min_count = max_count = keywords[0]['count']
    # for keyword in keywords:
    #     if keyword['count'] < min_count:
    #         min_count = keyword['count']
    #     if max_count < keyword['count']:
    #         max_count = keyword['count']
    # range = float(max_count - min_count)
    # if range == 0.0:
    #     range = 1.0
    # for keyword in keywords:
    #     # if keyword['count']
    #     keyword['weight'] = int(
    #         MAX_WEIGHT * (keyword['count'] - min_count) / range)
    context = {'tweets': json.dumps(keywords, ensure_ascii=False)}
    logger.info(context)

    # figure = io.BytesIO()
    # plt.savefig(figure, format="png")
    # logger.info(lemms)
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


# def submit(request):
#     # info = request.POST['tag']
#     # nbr = request.POST['nbr']
#     # logger.info(info)
#     # if(request.GET.get('submit_but')):
#     # context = RequestContext(request)
#     # return render(
#     #     'TwitterCoreSA/recherche.html')
