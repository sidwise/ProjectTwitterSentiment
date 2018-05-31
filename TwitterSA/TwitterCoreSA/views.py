# Create your views here.
# Create your views here.
from django.template import RequestContext
from django.shortcuts import render_to_response
from . import twitter_search
import logging

logger = logging.getLogger(__name__)


def index(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details,
    # for example.

    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the
    # template!
    # context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response(
        'TwitterCoreSA/index.html')


def search(request):
    # Request the context of the request.
    # The context contains information such as the client's machine details,
    # for example.
    if(request.GET.get('submit_but')):
        twitter_search.TwitterSearch(
            str(request.GET.get('tag')), str(request.GET.get('nbr')))
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the
    # template!
    # context_dict = {'boldmessage': "I am bold font from the context"}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    return render_to_response(
        'TwitterCoreSA/recherche.html')


def submit(request):
    # info = request.POST['tag']
    # nbr = request.POST['nbr']
    # logger.info(info)
    # if(request.GET.get('submit_but')):
    # context = RequestContext(request)
    twitter_search.TwitterSearch(
        str(request.POST.get('tag')), str(request.POST.get('nbr')))
    return render_to_response(
        'TwitterCoreSA/recherche.html')
