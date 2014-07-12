from django.contrib import admin
from news.models import *
# Register your models here.

admin.site.register(News)
admin.site.register(Publication)
admin.site.register(UserProfile)
admin.site.register(Follower)
admin.site.register(Video)
admin.site.register(LikePub)
admin.site.register(LikeVideo)
admin.site.register(MyProject)
admin.site.register(PublicationDetail)
admin.site.register(FeedbackMessage)