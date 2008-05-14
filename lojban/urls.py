
from os.path import join, normpath

from django.conf.urls.defaults import *
from django.conf import settings

from lojban.main.feeds import NewsFeed

feeds = {
    "news": NewsFeed,
}

urlpatterns = patterns('lojban.main.views',
    (r'^$', 'home'),
    (r'^search/$', 'search'),
    (r'^news/((?P<year>.*)/)?$', 'news'),

    (r'^admin/', include('django.contrib.admin.urls')),
)

urlpatterns += patterns('',
    (r'^feeds/(?P<url>.*).atom$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
)

urlpatterns += patterns('django.views.generic.simple',
    (r'^learning/$', 'direct_to_template', {'template': 'learning.html'}),
    (r'^community/$', 'direct_to_template', {'template': 'community.html'}),
    (r'^about/$', 'direct_to_template', {'template': 'about.html'}),
    (r'^faq/$', 'direct_to_template', {'template': 'faq.html'}),
    (r'^notes/$', 'direct_to_template', {'template': 'notes.html'}),
    (r'^resources/$', 'direct_to_template', {'template': 'resources.html'}),
    (r'^word-of-the-day/(?P<year>.*)/(?P<month>.*)/(?P<day>.*)/$', 'direct_to_template', {'template': 'word-of-the-day.html'}),
)

if settings.DEVELOPMENT_HOST:
    urlpatterns += patterns('django.views.static',
        (r'^stylesheets/(?P<path>.*)$', 'serve', {'document_root': normpath(join(settings.LOCAL_PATH, 'static/stylesheets'))}),
        (r'^images/(?P<path>.*)$', 'serve', {'document_root': normpath(join(settings.LOCAL_PATH, 'static/images'))}),
        (r'^javascript/(?P<path>.*)$', 'serve', {'document_root': normpath(join(settings.LOCAL_PATH, 'static/javascript'))}),
        (r'^audio/(?P<path>.*)$', 'serve', {'document_root': normpath(join(settings.LOCAL_PATH, 'static/audio'))}),
    )
