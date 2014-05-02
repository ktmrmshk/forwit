from django.db import models

# Create your models here.

class News(models.Model):
    title = models.CharField(max_length=128)
    content = models.TextField()
    created = models.DateTimeField()#(auto_now=True)
    updated = models.DateTimeField(auto_now=True)
    source = models.URLField(blank=True)
    
    def __unicode__(self):
        return self.title[:10]