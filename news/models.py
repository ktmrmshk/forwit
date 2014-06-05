from django.db import models
from django import forms
from django.contrib.auth.models import User
# Create your models here.
from django.conf import settings

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

class PublicationDetail(models.Model):
    pub = models.OneToOneField(Publication)
    description = models.TextField(max_length=4096, blank=True, default='')
    def __unicode__(self):
        return self.pub.title[:64]#, self.id#, self.title[:10].encode('utf-8')
    # graph
    # slide
    # photo
    

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
    
    facephoto = models.ImageField(upload_to=upload_to, blank=True, null=True, default='%s/img/dummy/nobody.png' % settings.STATIC_URL)
    
    kana_first_name = models.CharField(max_length=64, blank=True, default='')
    kana_last_name = models.CharField(max_length=64, blank=True, default='')
    
    def __unicode__(self):
        return '%s, %s' % (self.user.username, self.title)

class Follower(models.Model):
    user = models.OneToOneField(User)
    members = models.ManyToManyField(User, related_name='followed', blank=True, null=True)
    def __unicode__(self):
        return '%s' % self.user.username

class VideoManager(models.Manager):
    def get_video_image(self):
        return 'http://img.youtube.com/vi/%s/0.jpg' % self.video_id
        
class Video(models.Model):
    owner = models.ManyToManyField(User, blank=True, null=True, default=None)
    pub = models.ManyToManyField(Publication, blank=True, null=True)
    videosite = models.CharField(max_length=64, default='youtube')
    video_id = models.CharField(max_length=64)
    title = models.CharField(max_length=128, blank=True, default='')
    comment = models.TextField(max_length=1024, blank=True, default='')
    updated = models.DateTimeField(auto_now=True)
    #url = models.URLField(blank=True, default='')
    emburl = models.CharField(max_length=512, blank=True, default='')
    def __unicode__(self):
        return '%s, %s' % (self.title, self.video_id)
    objects = VideoManager()
    
#for "MEMO"
class LikePub(models.Model):  
    user = models.OneToOneField(User)
    pub = models.ManyToManyField(Publication, blank=True, null=True)
    def __unicode__(self):
        return '%s' % self.user.username

class LikeVideo(models.Model):
    user = models.OneToOneField(User)
    video = models.ManyToManyField(Video, blank=True, null=True)
    def __unicode__(self):
        return '%s' % self.user.username

class UserForm(forms.ModelForm):
    #password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        #fields = ('first_name', 'last_name', 'email')
        fields = ('first_name', 'last_name')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('kana_first_name', 'kana_last_name', 'job', 'title',
                  'interesting1', 'interesting2', 'interesting3',
                  'school1', 'school_project', 'facephoto' )

class MyProject(models.Model):
    user = models.OneToOneField(User)
    description = models.TextField(max_length=4096, blank=True, default='')
    #material = image?
    def __unicode__(self):
        return '%s' % self.user.username

class MyProjectForm(forms.ModelForm):
    class Meta:
        model = MyProject
        fields = ('description',)
        
class FeedbackMessage(models.Model):
    msg = models.TextField(max_length=4096, blank=True, default='')
    created = models.DateTimeField()#(auto_now=True)
    user = models.ForeignKey(User, blank=True, null=True)
    checked = models.BooleanField(default=False)
    