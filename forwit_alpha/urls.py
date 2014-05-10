from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'forwit_alpha.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/', 'news.views.test_news'),
    url(r'^search/', 'news.views.test_search'),
    url(r'^test_getpub/', 'news.views.test_getpub'),
    url(r'^test_upload/', 'news.test_views.upload_file'),
    url(r'^test_userpage/', 'news.views.test_userpage'),
    url(r'^test_watch/', 'news.views.test_watch'),
    url(r'^pub/(?P<pubid>\d+)/$', 'news.views.pubpage'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
