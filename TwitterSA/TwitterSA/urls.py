from django.conf.urls import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^SA/', include('TwitterCoreSA.urls')),
    # Examples:
    # url(r'^$', 'TwitterSA.views.home', name='home'),
    # url(r'^TwitterSA/', include('TwitterSA.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
]
