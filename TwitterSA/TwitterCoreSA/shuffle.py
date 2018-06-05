import random
from django import template
register = template.Library()


@register.filter
def shuffle(arg):
    if arg:
        tmp = arg[:]
        random.shuffle(tmp)
        return tmp
