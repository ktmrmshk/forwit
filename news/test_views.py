from django.shortcuts import render
from django.http import HttpResponse
import urllib
from news.models  import News, Publication
import cinii
import json


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
    if request.method == 'GET':
        callback = request.GET.get('callback', 'kitamu')
        dat = ['apple', 'orange', 'python']
        ret = '%s(%s)' % (callback, json.dumps(dat) )
        return HttpResponse(ret, mimetype='application/javascript')