import json
from news.models import * 
from django.contrib.auth.models import User

def handle_watch(cmd, request):
    f = request.user.follower
    #print request.POST
    p = User.objects.get(username__exact=request.POST['username'])
    if cmd == 'add_watch':
        f.members.add(p)
    else:
        assert cmd == 'remove_watch'
        f.members.remove(p)
    ret = json.dumps({'ret': 'true', 'username': request.POST['username'] })
    #print ret
    return ret

def handle_likevideo(cmd, request):
    v = Video.objects.get(video_id__exact=request.POST['videoid'])
    print v.title
    print request.POST['videoid']
    if cmd == 'add_videomemo':
        request.user.likevideo.video.add(v)
    else:
        assert cmd == 'remove_videomemo'
        request.user.likevideo.video.remove(v)
    ret = json.dumps({'ret': 'true', 'videoid': request.POST['videoid'] })
    return ret

def handle_mypub(cmd, request):
    p = Publication.objects.get(id__exact=request.POST["pubid"])
    if cmd == 'add_mypub':
        p.author.add(request.user)
    else:
        assert cmd == 'remove_mypub'
        p.author.remove(request.user)
    ret = json.dumps({'ret': 'true', 'pubid': request.POST['pubid'] })
    return ret

def handle_pubvideo(cmd, request):
    p = Publication.objects.get(id__exact=request.POST["pubid"])
    vid = request.POST["videoid"]
    v=None
    if len( Video.objects.filter(video_id__exact=vid) ) ==0:
        v=Video(video_id=vid)
        v.save()
        v.owner.add(request.user)
    else:
        v= Video.objects.get(video_id__exact=vid)
    if cmd == 'add_pubvideo':
        v.pub.add(p)
    else:
        assert cmd == 'remove_pubvideo'
        v.pub.remove(p)
    v.save()
   
    
    ret = json.dumps({'ret': 'true', 'pubid': request.POST['pubid'] , 'videoid': request.POST["videoid"]})
    print ret
    return ret
    
    
    