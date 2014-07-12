from django.shortcuts import render
from django.http import HttpResponse
import urllib
from news.models  import News, Publication
import cinii
import json
from django.contrib.auth.models import User 
from datetime import datetime


from django import forms
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=64)
    file = forms.FileField()
    #get from request.FILE


    
def handle_uploaded_file(f, filename):
    with open('%s' % filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'], form.cleaned_data['title'])
            return HttpResponse('uploaded successfully...')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form':form})

def test_ajax(request):
    callback='_func'
    if request.method == 'GET':
        callback = request.GET.get('callback', 'kitamu')
        dat = ['apple', 'orange', 'python']
        ret = '%s(%s)' % (callback, json.dumps(dat) )
        print ret
        return HttpResponse(ret, mimetype='application/javascript')
    elif request.method == 'POST':
        print 'POST'
        pubid = request.POST.get('pubid', 9876)
        dat = {'pubid':pubid}
        ret = '%s' % json.dumps(dat) 
        print ret
        return HttpResponse(ret, content_type = "application/json")
    else:
        return HttpResponse('error')
    

def ajax_get_randuser(request):
    if request.method == 'GET':
        callback = request.GET.get('callback', 'hogefoo')
        user = User.objects.all().order_by('?')
        ret=[]
        for u in user:
            tmp={}
            tmp['username'] = u.username
            tmp['name'] = '%s %s' % ( u.last_name, u.first_name)
            tmp['facephoto'] = 'dummy.jpg'#u.userprofile.facephoto.url
            ret.append(tmp)
        retjson = '%s(%s)' % (callback, json.dumps(ret) )
        return HttpResponse(retjson, mimetype='application/javascript')
    
def newuser(request):
    user = request.user
    try:
        up = user.userprofile
    
        f = user.follower
        lb = user.likepub
        lv = user.likevideo
    except:
        return HttpResponse('related model does not exist')
    
    return HttpResponse('thanks!')