from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import urllib
from news.models  import News, Publication, Video, UserProfile, Follower, LikePub, LikeVideo
import cinii, cinii_rdf
import json
import sys
from django.contrib.auth.models import User 
from django.contrib.auth import logout, authenticate, login
from news.models import UserProfileForm, UserForm
from django.core.paginator import Paginator
import pager


# Create your views here.
def test_news(request):
    #news = News.objects.all()
    news = News.objects.filter(published=True)
    return render(request, 'tmp_index.html', {'news': news})

def search_pub(request):
    if 'q' in request.GET:
        q = request.GET['q']
        page = int( request.GET.get('page', '1') )
        q_for_navi = 'http://' + request.get_host()
        q_for_navi += request.path
        q_for_navi += '?'
        q_for_navi += 'q=%s' % q
        
        start = (page-1) * 20
        pub = cinii.Publist()
        pub.q = q
        pub.setparam(count=20, start=start)
        pub.get()
        publist = pub.parse_dat_all()
        # INGEST to DB!!!
        ingest_publist(publist)
        
        #check if this user likes this pub
        if request.user.is_authenticated():
            likepub = request.user.likepub.pub
            for p in publist:
                try:
                    likepub.get(id__exact=p['id'])
                    p['mine'] = True
                except:
#                     print p['id'], 'not mine'
                    p['mine'] = False
        
        lastpage=(pub.cnt_ret-1)/20 + 1
        pagelist=[]
        next='t'
        before='t'
        if lastpage == 1:
            assert page == lastpage
            next='f'
            before='f'
        elif lastpage == 2:
            if page == 1:
                before = 'f'
            else:
                assert page == 2
                next = 'f'
            pagelist = [1, 2]
        else:
            assert lastpage > 2
            if page == 1:
                before='f'
                pagelist = [1, 2, 3]
            elif page == lastpage:
                next = 'f'
                pagelist = [lastpage-2, lastpage-1, lastpage]
            else:
                pagelist = [page-1, page, page+1]
        
        #print pagelist
        offset=(page-1)*20
        return render(request, 'tmp_search-result.html',
                       {'cnt_ret': pub.cnt_ret, 'publist': publist, 'len_publist': len(publist), 'page': page, 'q_for_navi': q_for_navi,
                        'pagelist' : pagelist, 'next':next, 'before':before, 'offset':offset })        
        
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
        # INGEST to DB!!!
        ingest_publist(publist)
        
        #check if this user likes this pub
        likepub = request.user.likepub.pub
        
        for p in publist:
            try:
                likepub.get(id__exact=p['id'])
                p['mine'] = True
            except:
#                 print p['id'], 'not mine'
                p['mine'] = False

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
                        'pagelist' : pagelist, 'len_publist': len(publist), 'next':next, 'before':before })

    return render(request, 'tmp_search-result.html')

def ingest_publist(publist):
    for p in publist:
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
            
def test_getpub(request):
    pub=cinii.Publist()
    pub.setparam(author='%s %s' % (request.user.last_name, request.user.first_name), count=30)
    pub.get()
    ret = pub.parse_dat_all()
#     for p in ret:
#         try:
#             plist = Publication.objects.get(id=p['id'])
#             print 'entry is already exists'
#             continue
#         except:
#             plist = Publication(id=p['id'])
#             plist.link = p['link']
#             plist.title = p['title']
#             plist.authors = p['authors']
#             plist.publisher = p['publisher']
#             plist.publicationname = p['prism_publicationname'] 
#             plist.volume = p['prism_volume']
#             plist.number = p['prism_number']
#             plist.pagerange = p['prism_pagerange']
#             plist.publicationdate = p['prism_publicationdate']
#             plist.issn = p['prism_issn']
#             plist.save()
    ingest_publist(ret)
            
    return HttpResponse('%s pubs were found' % len(ret) )
#     return HttpResponse(json.dumps(ret))
    
def test_userpage(request):
    #return render(request, 'login/account-name/tmp_index.html', {'u':request.user})
    return userpage(request, request.user.username)


    
def test_watch(request):
    return render(request, 'login/account-name/tmp_watch.html') 
    
    
    
def toppage(request):
    #news = News.objects.all()
    
    news = News.objects.filter(published=True).order_by('?')[:5]
    pub = Publication.objects.order_by('?')[:5]
    video = Video.objects.order_by('?')[:8]
    if request.user.is_authenticated():
        return redirect('/u/')
    else: 
        return render(request, 'tmp_index.html', {'news': news, 'pub':pub, 'video': video})
    
def make_youtube_url(videoid, width=480, height=360):
    return '<iframe width="%d" height="%d" src="//www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>' % (width, height, videoid)
def pubpage(request, pubid):
    #get abstraction
    abst=''
    try:
        c=cinii_rdf.CiniiRDF('http://ci.nii.ac.jp/naid/%s.rdf' % pubid)
        abst = c.abst
    except:
        print sys.exc_info()
        abst='Not Available Now'
    if abst == '':
        abst='Not Available Now'
    
    try:
        pub = Publication.objects.get(id=pubid)
        #json.loads(a2.replace("u'", "'").replace("'", '"'))
        authors = json.loads(pub.authors.replace("u'", "'").replace("'", '"'))
        for a in authors:
            org = c.getAffiliation(a['name'])
            a['org'] = org
        try:
            if pub.video_set.all() != []:
                video = pub.video_set.all()[0]
                video_url = make_youtube_url(video.video_id)
                return render(request, 'login/tmp_thesis-movie.html', {'pub':pub, 'authors': authors, 'video_url': video_url, 'abst':abst})
        except:
            return render(request, 'tmp_thesis.html', {'pub':pub, 'authors': authors, 'abst':abst})
    except:
        print sys.exc_info()
        return HttpResponse('pubid=%s is not found' % pubid )


def my_userpage(request):
#    return userpage(request, request.user.username)
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')
    try:
#         u = User.objects.get(username__exact=username)
        u = request.user
        news = News.objects.filter(published=True).order_by('?')[:5]
        pub = Publication.objects.order_by('?')[:5]
        video = Video.objects.order_by('?')[:8]
        return render(request, 'login/account-name/tmp_index.html', {'u':u, 'currentpage':'news', 'news': news, 'pub':pub, 'video': video} )
    except:
#         print sys.exc_info()[0]
        return HttpResponse('username=%s was not found' % request.user.username)

def userpage(request, username):
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')
    try:
#         u = User.objects.get(username__exact=username)
#         return render(request, 'login/account-name/tmp_index.html', {'u':u, 'currentpage':'news'} )
        return HttpResponseRedirect('/research/%s' % username)
    except:
        return HttpResponse('username=%s was not found' % username)



def my_research(request):
    return research(request, request.user.username)
def research(request, username):
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')
    try:
        u = User.objects.get(username__exact=username)
        return render(request, 'login/account-name/tmp_research.html', {'u':u, 'currentpage':'research'} )
    except:
#         print sys.exc_info()[0]
        return HttpResponse('username=%s was not found' % username)

def my_researchvideo(request):
    return researchvideo(request, request.user.username)
def researchvideo(request, username):
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')
    try:
        u = User.objects.get(username__exact=username)
        return render(request, 'login/account-name/tmp_research-movie.html', {'u':u, 'currentpage':'research-video'} )
    except:
        return HttpResponse('username=%s was not found' % username)

def my_memopage(request):
    return memopage(request, request.user.username)
def memopage(request, username):
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')
    try:
        page=1
        if request.method == 'GET':
            page = int( request.GET.get('page', '1') )
        u = User.objects.get(username__exact=username)
        puball = u.likepub.pub.all()
        uname=None
        if username != request.user.username:
            uname = username
        pub, pg = pager.getPager(puball, page, '/memo/', username=uname)
        return render(request, 'login/account-name/tmp_memo.html', {'u':u, 'pub':pub, 'puball':puball, 'pager':pg, 'currentpage':'memo'})
    except:
        print sys.exc_info()#[0]
        return HttpResponse('username=%s was not found' % username)
    
def my_memovideopage(request):
    return memovideopage(request, request.user.username)
def memovideopage(request, username):
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')   
    try:
        u = User.objects.get(username__exact=username)
        return render(request, 'login/account-name/tmp_memo-movie.html', {'u':u, 'currentpage':'memo-video'} )
    except:
        return HttpResponse('username=%s was not found' % username)
    
def my_watchingpage(request):
    return watchingpage(request, request.user.username)
def watchingpage(request, username):
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')
    try:
        u = User.objects.get(username__exact=username)
        return render(request, 'login/account-name/tmp_watch.html', {'u':u, 'currentpage':'watching'} )
    except:
        return HttpResponse('username=%s was not found' % username)    
    return render(request, 'login/account-name/tmp_watch.html') 

def my_watchedpage(request):
    return watchedpage(request, request.user.username)
def watchedpage(request, username):
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')
    try:
        u = User.objects.get(username__exact=username)
        return render(request, 'login/account-name/tmp_watcher.html', {'u':u, 'currentpage':'watched'} )
    except:
        return HttpResponse('username=%s was not found' % username)    
    return render(request, 'login/account-name/tmp_watcher.html') 

def do_logout(request):
    if request.user.is_authenticated():
        logout(request)
    return redirect('/login/')

def do_login(request):
    if request.user.is_authenticated():
        return redirect('/u/')
    else:
        if request.method == 'POST':
            username = request.POST['l_username']
            password = request.POST['l_pass']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/u')
                else:
                    return HttpResponse('username=%s was blocked' % username)    
            else:
                return render(request, 'forwit-login0508/login.html', {})
        return render(request, 'forwit-login0508/login.html', {})

def usersetting(request):
    up = request.user.userprofile
    u = request.user
    if request.method == 'POST':
        uf = UserForm(request.POST, instance=u)
        upf = UserProfileForm(request.POST, instance=up)
        if  uf.is_valid() and upf.is_valid():
#             u.first_name = uf.cleaned_data['first_name']
#             u.last_name = uf.cleaned_data['last_name']
#             up.kana_first_name = upf.cleaned_data['kana_first_name']
#             up.kana_last_name = upf.cleaned_data['kana_last_name']
#             
            up.save()
            u.save()
            msg='saved!'
            return render(request, 'login/tmp_setting2.html', {'uf': uf, 'upf': upf, 'msg': msg})
        else:
            msg =  'INVAID'
            return render(request, 'login/tmp_setting2.html', {'uf': uf, 'upf': upf, 'msg': msg})
    uf = UserForm(instance=u)
    upf = UserProfileForm(instance=up)
    return render(request, 'login/tmp_setting2.html', {'uf': uf, 'upf': upf})

def memberlist(request):
    alluser = User.objects.all()
    return render(request, 'login/tmp_memberlist.html', {'alluser': alluser})

def loggedin(request):
    u = request.user
    try:
        uf = u.userprofile
        f = u.follower
        lp = u.likepub
        lv = u.likevideo
        return redirect('/u/')
    except:
        return redirect('/new_socialuser/')

def new_socialuser(request):
    u = request.user
    up = UserProfile(user=u)
    if request.method == 'POST':
        uf = UserForm(request.POST, instance=u)
        upf = UserProfileForm(request.POST, instance=up)
        if  uf.is_valid() and upf.is_valid():
            upf.save()
            uf.save()
            f = Follower(user=u)
            f.save()
            lp = LikePub(user=u)
            lp.save()
            lv = LikeVideo(user=u)
            lv.save()
            return redirect('/u/')
        return HttpResponse('Error happened!')
    else:
        uf = UserForm(instance=u)
        upf = UserProfileForm()
        return render(request, 'login/tmp_setting2.html', {'uf': uf, 'upf': upf})
    
    
def add_memopub(request):
    try:
        if request.method == 'POST':
    #         print 'POST'
            pubid = request.POST.get('pubid', False)
            cmd = request.POST.get('cmd', False)
            assert cmd == 'add' or cmd == 'remove'
            if pubid and cmd:
                lp = request.user.likepub
                pub = Publication.objects.get(id__exact=int(pubid))
                if cmd == 'add':
                    lp.pub.add(pub)
                elif cmd == 'remove':
                    lp.pub.remove(pub)
                else:
                    raise Exception('cmd error', 'cmd=%s' % cmd)
                lp.save()
                print 'added new pub'
            else:
                raise Exception('cmd error2', 'cmd=%s, pubid=%s' % (cmd, pubid))
            dat = {'ret': 'true', 'pubid':pubid}
            ret = '%s' % json.dumps(dat) 
    #         print ret
            return HttpResponse(ret, content_type = "application/json")
        else:
            raise Exception('cmd error', 'some error happened')
    except:
        dat = {'ret': 'false', 'msg': 'method error', 'info': '%s / %s' % (sys.exc_info()[0], sys.exc_info()[1])}
        ret = '%s' % json.dumps(dat) 
        print ret
        return HttpResponse(ret, content_type = "application/json")
    

    
