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
    authors = models.CharField(max_length=128)
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
    