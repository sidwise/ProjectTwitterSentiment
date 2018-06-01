from django.conf.urls import *
from TwitterCoreSA import views


urlpatterns = [
    url(r'^$', views.index),
    url(r'^recherche/', views.search),
    # url(r'^submit', views.submit)
    # url(r'^search/', views.recherche),

]
