from django.shortcuts import render
from django.http import HttpResponse
import urllib
from news.models  import News, Publication
import cinii
import json

# Create your views here.
def test_news(request):
    #news = News.objects.all()
    news = News.objects.filter(published=True)
    return render(request, 'tmp_index.html', {'news': news})


def test_search(request):
#     if request.method == 'POST':
#         print request.POST['q']
#         pub = cinii.Publist()
#         pub.q = request.POST['q']
    #print request.get_host()
    if 'q' in request.GET:
        q = request.GET['q']
        #page starts from 1 not from 0
        page = int( request.GET.get('page', '1') )
        
#         query={}
#         query['q'] = q
        q_for_navi = 'http://' + request.get_host()
        q_for_navi += request.path
        q_for_navi += '?'
        #q_for_navi += urllib.urlencode(query)
        q_for_navi += 'q=%s' % q
        
        start = (page-1) * 20
        #DEBUG
        #print 'start=%d' % start
        pub = cinii.Publist()
        pub.q = q
        pub.setparam(count=20, start=start)
        pub.get()
        publist = pub.parse_dat_all()
        lastpage=(pub.cnt_ret-1)/20 + 1
        pagelist=[]
        next='t'
        before='t'
        if page == 1:
            before='f'
            if (page+10) < lastpage:
                pagelist=[1, 2, page+10, lastpage]
            elif (page+2) < lastpage:
                pagelist={1, 2, 3, lastpage}
            else:
                pagelist=[1, 2, lastpage]
        elif page == 2:
            if (page+10) < lastpage:
                pagelist=[1, 2, 3, lastpage]
            elif (page+2) < lastpage:
                pagelist=[1, 2, 3, lastpage]
            else:
                pagelist=[1, 2, lastpage]
        elif page == lastpage:
            next='f'
            if 1 < (lastpage-1):
                pagelist = [1, lastpage-1, lastpage]
            else:
                pagelist = [1, lastpage]
        
        
        else:
            if (page+10) < lastpage:
                pagelist=[1, page, page+10, lastpage]
            elif (page+1) < lastpage:
                pagelist=[1, page, page+1, lastpage]
            else:
                pagelist=[1, page-1, page, lastpage]
        
        print pagelist
        return render(request, 'tmp_search-result.html',
                       {'cnt_ret': pub.cnt_ret, 'publist': publist, 'page': page, 'q_for_navi': q_for_navi,
                        'pagelist' : pagelist, 'next':next, 'before':before })

    return render(request, 'tmp_search-result.html')

def test_getpub(request):
    pub=cinii.Publist()
    pub.setparam(author='%s %s' % (request.user.last_name, request.user.first_name), count=30)
    pub.get()
    ret = pub.parse_dat_all()
    for p in ret:
        try:
            plist = Publication.objects.get(id=p['id'])
            print 'entry is already exists'
            continue
        except:
            plist = Publication(id=p['id'])
            plist.link = p['link']
            plist.title = p['title']
            plist.authors = p['authors']
            plist.publisher = p['publisher']
            plist.publicationname = p['prism_publicationname'] 
            plist.volume = p['prism_volume']
            plist.number = p['prism_number']
            plist.pagerange = p['prism_pagerange']
            plist.publicationdate = p['prism_publicationdate']
            plist.issn = p['prism_issn']
            plist.save()
            
    return HttpResponse('%s pubs were found' % len(ret) )
#     return HttpResponse(json.dumps(ret))
    
def test_userpage(request):
    return render(request, 'login/account-name/tmp_index.html')
    
def test_watch(request):
    return render(request, 'login/account-name/tmp_watch.html') 
    
    
def make_youtube_url(videoid, width=480, height=360):
    return '<iframe width="%d" height="%d" src="//www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>' % (width, height, videoid)
def pubpage(request, pubid):
    try:
        pub = Publication.objects.get(id=pubid)
        #json.loads(a2.replace("u'", "'").replace("'", '"'))
        authors = json.loads(pub.authors.replace("u'", "'").replace("'", '"'))
        if pub.video_set.all() == []:
            return render(request, 'tmp_thesis.html', {'pub':pub, 'authors': authors})
        else:
            video = pub.video_set.all()[0]
            video_url = make_youtube_url(video.video_id)
            return render(request, 'login/tmp_thesis-movie.html', {'pub':pub, 'authors': authors, 'video_url': video_url})

        
    except:
        return HttpResponse('pubid=%s is not found' % pubid )
