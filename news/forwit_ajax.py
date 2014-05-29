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