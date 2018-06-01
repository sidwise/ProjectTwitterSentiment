# Create your views here.
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response, render
from .models import Tweet
import logging
from TwitterCoreSA.tasks import TwitterSearch

logger = logging.getLogger(__name__)


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details,
    # for example.

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the
    # template!
    # context_dict = {'boldmessage': "I am bold font from the context"}
    context = {'tweets': Tweet.nodes.all()}
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
