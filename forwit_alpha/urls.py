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
    
    
    url(r'^$', 'news.views.toppage'),
    
    url(r'^pub/(?P<pubid>\d+)/$', 'news.views.pubpage'),
    
    url(r'^u/$', 'news.views.my_userpage'),
    url(r'^u/(?P<username>\w+)$', 'news.views.userpage'),
    
    url(r'^research/$', 'news.views.my_research'),
    url(r'^research/(?P<username>\w+)$', 'news.views.research'),
    
    url(r'^research-video/$', 'news.views.my_researchvideo'),
    url(r'^research-video/(?P<username>\w+)$', 'news.views.researchvideo'),
    
    url(r'^memo/$', 'news.views.my_memopage'),
    url(r'^memo/(?P<username>\w+)$', 'news.views.memopage'),
    url(r'^memo-video/$', 'news.views.my_memovideopage'),
    url(r'^memo-video/(?P<username>\w+)$', 'news.views.memovideopage'),
    
    url(r'^watching/$', 'news.views.my_watchingpage'),
    url(r'^watching/(?P<username>\w+)$', 'news.views.watchingpage'),
    
    url(r'^watched/$', 'news.views.my_watchedpage'),
    url(r'^watched/(?P<username>\w+)$', 'news.views.watchedpage'),
    
    url(r'^login/$', 'news.views.do_login'),
    url(r'^logout/$', 'news.views.do_logout'),

) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
