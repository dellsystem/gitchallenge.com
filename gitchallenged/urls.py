from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'gitchallenged.views.home', name='home'),
    url(r'^login$', 'gitchallenged.views.login', name='login'),
    url(r'^logout$', 'gitchallenged.views.logout', name='logout'),
    url(r'^authorise$', 'gitchallenged.views.authorise', name='authorise'),
    url(r'^admin/', include(admin.site.urls)),
)
