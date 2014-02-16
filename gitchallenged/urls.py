from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'gitchallenged.views.home', name='home'),
    url(r'^login$', 'gitchallenged.views.login', name='login'),
    url(r'^logout$', 'gitchallenged.views.logout', name='logout'),
    url(r'^authorise$', 'gitchallenged.views.authorise', name='authorise'),
    url(r'^your-tasks$', 'gitchallenged.views.your_tasks', name='your_tasks'),
    url(r'^start/(?P<username>[^/]+)/(?P<repository>[^/]+)/(?P<number>\d+)$',
        'gitchallenged.views.start', name='start'),
    url(r'^api/repos/(?P<language>[^/]+)/(?P<difficulty>[^/]+)$',
        'gitchallenged.views.get_repos', name='get_repos'),
    url(r'^api/issues/(?P<username>[^/]+)/(?P<repository>[^/]+)$',
        'gitchallenged.views.get_issues', name='get_issues'),
    url(r'^admin/', include(admin.site.urls)),
)
