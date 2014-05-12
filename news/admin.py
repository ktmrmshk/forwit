from django.contrib import admin
from news.models import News, Publication, UserProfile, Follower, Video, LikePub, LikeVideo
# Register your models here.

admin.site.register(News)
admin.site.register(Publication)
admin.site.register(UserProfile)
admin.site.register(Follower)
admin.site.register(Video)
admin.site.register(LikePub)
admin.site.register(LikeVideo)