from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    created = models.DateTimeField()#(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    source = models.URLField(blank=True)
    published = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.title[:10]
    
class Publication(models.Model):
    id = models.IntegerField(primary_key=True)
    link = models.URLField()
    title = models.CharField(max_length=512)
    authors = models.CharField(max_length=1024)
    publisher = models.CharField(max_length=128, blank=True)
    publicationname = models.CharField(max_length=128, blank=True)
    volume = models.CharField(max_length=32, blank=True)
    number = models.CharField(max_length=32, blank=True)
    pagerange = models.CharField(max_length=32, blank=True)
    publicationdate = models.CharField(max_length=32, blank=True)
    issn = models.CharField(max_length=64, blank=True)
    
    author = models.ManyToManyField(User, blank=True, null=True)
    
    def __unicode__(self):
        return self.title[:10]#, self.id#, self.title[:10].encode('utf-8')

def upload_to(instance, filename):
    return 'images/%s/%s' %( instance.user.id, filename)
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    job = models.CharField(max_length=64, default='Current Affiliation')
    title = models.CharField(max_length=64, default='Current Title')
    school1 = models.CharField(max_length=64, default='Japan University')
    school_project = models.CharField(max_length=64, default='Lab')
    shoool_dept = models.CharField(max_length=64, default='Computer Science')
    qualification = models.CharField(max_length=64, default='Ph.D of Computer Science')
    interesting1 = models.CharField(max_length=64, default='ResearchArea1')
    interesting2 = models.CharField(max_length=64, default='ResearchArea2')
    interesting3 = models.CharField(max_length=64, default='ResearchArea3')
    
    facephoto = models.ImageField(upload_to=upload_to, blank=True, null=True)
    
    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.title)

class Follower(models.Model):
    user = models.OneToOneField(User)
    members = models.ManyToManyField(User, related_name='followed', blank=True, null=True)
    def __unicode__(self):
        return '%s' % self.user.username
    
class Video(models.Model):
    owner = models.ManyToManyField(User, blank=True, null=True, default=None)
    pub = models.ManyToManyField(Publication, blank=True, null=True)
    videosite = models.CharField(max_length=64, default='youtube')
    video_id = models.CharField(max_length=64)
    title = models.CharField(max_length=128)
    comment = models.TextField(max_length=1024)
    updated = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return '%s, %s' % (self.title, self.video_id)
    
#for "MEMO"
class LikePub(models.Model):  
    user = models.OneToOneField(User)
    pub = models.ManyToManyField(Publication)


    