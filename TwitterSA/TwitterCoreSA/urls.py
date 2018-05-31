from django.conf.urls import *
from TwitterCoreSA import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^recherche/', views.search),

    # url(r'^search/', views.recherche),

]
