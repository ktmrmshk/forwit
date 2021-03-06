from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
import urllib
from news.models  import *
import cinii, cinii_rdf
import json
import sys
from django.contrib.auth.models import User 
from django.contrib.auth import logout, authenticate, login
from news.models import UserProfileForm, UserForm
from django.core.paginator import Paginator
import pager
from datetime import datetime

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
        #print publist
        # INGEST to DB!!!
        ingest_publist(publist)
        
        #check if this user likes this pub
        if request.user.is_authenticated():
            likepub = request.user.likepub.pub
            for p in publist:
                try:
                    likepub.get(pubid__exact=p['id'])
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
                likepub.get(pubid__exact=p['id'])
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
        #print p
        #print '>>', p['title'].encode('utf-8')
        try:
            plist = Publication.objects.get(pubid=p['id'])
            print 'entry is already exists'
            continue
        except:
            plist = Publication(pubid=p['id'])
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
    
    #news = News.objects.filter(published=True).order_by('?')[:5]
    news = News.objects.filter(published=True)[:5]
    pub = Publication.objects.order_by('?')[:5]
    video = Video.objects.order_by('?')[:8]
    if request.user.is_authenticated():
        return redirect('/u/')
    else: 
        return render(request, 'tmp_index.html', {'news': news, 'pub':pub, 'video': video})
    
def make_youtube_url(videoid, width=480, height=360):
    return '<iframe width="%d" height="%d" src="//www.youtube.com/embed/%s" frameborder="0" allowfullscreen></iframe>' % (width, height, videoid)
def pubpage(request, pubid):
    prop='none'#none, memo or mine
    if request.user.is_authenticated():
        if Publication.objects.filter(pubid=pubid).filter(author=request.user).count() != 0:
            prop='mine'
        elif request.user.likepub.pub.filter(pubid=pubid).count() != 0:
            prop='memo'
    
    
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
        pub = Publication.objects.get(pubid=pubid)
        #json.loads(a2.replace("u'", "'").replace("'", '"'))
        authors = json.loads(pub.authors.replace("u'", "'").replace("'", '"'))
        for a in authors:
            org = c.getAffiliation(a['name'])
            a['org'] = org
        try:
            if pub.video_set.all() != []:
                allvideo = pub.video_set.all()
                video = allvideo[len(allvideo)-1]
                video_url = make_youtube_url(video.video_id)
                return render(request, 'login/tmp_thesis-movie2.html', {'pub':pub, 'authors': authors, 'video_url': video_url, 'abst':abst, 'prop':prop})
        except:
            return render(request, 'login/tmp_thesis-movie2.html', {'pub':pub, 'authors': authors, 'abst':abst, 'prop':prop})
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
        news = News.objects.filter(published=True)[:5]
        pub = Publication.objects.order_by('?')[:5]
        video = Video.objects.order_by('?')[:8]
        return render(request, 'login/account-name/tmp_index.html', {'u':u, 'currentpage':'news', 'news': news, 'pub':pub, 'video': video} )
    except:
        print sys.exc_info()
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
        w = request.user.follower.members.filter(username__exact=u.username)
        following_user=False
        if len(w) != 0:
            following_user=True
        upub=[]
        for p in u.publication_set.all():
            if len( request.user.likepub.pub.all().filter(pubid=p.pubid) ):
                upub.append( {'in_mymemo': True, 'pub': p})
            else:
                upub.append( {'in_mymemo': False, 'pub': p})
        return render(request, 'login/account-name/tmp_research.html', {'u':u, 'following_user': following_user, 'upub':upub,'currentpage':'research'} )
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
        w = request.user.follower.members.filter(username__exact=u.username)
        following_user=False
        if len(w) != 0:
            following_user=True
        
        uvideo=[]
        for v in u.video_set.all():
            if len( request.user.likevideo.video.all().filter(video_id__exact=v.video_id) ) != 0:
                uvideo.append({'video':v, 'in_mymemo': True})
            else:
                uvideo.append({'video':v, 'in_mymemo': False})
        print uvideo

        return render(request, 'login/account-name/tmp_research-movie.html', {'u':u, 'uvideo': uvideo, 'following_user': following_user, 'currentpage':'research-video'} )
    except:
        print sys.exc_info()
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
        w = request.user.follower.members.filter(username__exact=u.username)
        following_user=False
        if len(w) != 0:
            following_user=True
        
        puball = u.likepub.pub.all()        
        uname=None
        if username != request.user.username:
            uname = username
        pub, pg = pager.getPager(puball, page, '/memo/', username=uname)
        lpub=[]
        for p in pub:
            if len( request.user.likepub.pub.filter(pubid__exact=p.pubid) ) != 0:
                lpub.append({'in_mymemo': True, 'pub': p})
            else:
                lpub.append({'in_mymemo': False, 'pub': p})
        return render(request, 'login/account-name/tmp_memo.html', {'u':u,  'following_user': following_user, 'lpub':lpub, 'puball':puball, 'pager':pg, 'currentpage':'memo'})
    except:
        print sys.exc_info()#[0]
        return HttpResponse('username=%s was not found' % username)
    
def my_memovideopage(request):
    return memovideopage(request, request.user.username)
def memovideopage(request, username):
    print 'HELLO WORLD'
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')   
    try:
        u = User.objects.get(username__exact=username)
        w = request.user.follower.members.filter(username__exact=u.username)
        following_user=False
        if len(w) != 0:
            following_user=True
        uvideo=[]
        for v in u.likevideo.video.all():
            if len( request.user.likevideo.video.all().filter(video_id__exact=v.video_id) ) != 0:
                uvideo.append({'video':v, 'in_mymemo': True})
            else:
                uvideo.append({'video':v, 'in_mymemo': False})
        #print uvideo
        return render(request, 'login/account-name/tmp_memo-movie.html', {'u':u, 'uvideo': uvideo, 'following_user': following_user, 'currentpage':'memo-video'} )
    except:
        return HttpResponse('username=%s was not found' % username)
    
def my_watchingpage(request):
    return watchingpage(request, request.user.username)
def watchingpage(request, username):
    if not request.user.is_authenticated():
        return HttpResponse('Log-in is required. Please log-in')
    try:
        u = User.objects.get(username__exact=username)
        w = request.user.follower.members.filter(username__exact=u.username)
        f = []
        for m in u.follower.members.all():
            if len( request.user.follower.members.filter(id__exact=m.id) ) != 0:
                f.append({'is_follow':True, 'user':m})
            else:
                f.append({'is_follow':False, 'user':m})
        #print 'hoge', f
        
        following_user=False
        if len(w) != 0:
            following_user=True
        return render(request, 'login/account-name/tmp_watch.html', {'u':u, 'f':f, 'following_user': following_user, 'currentpage':'watching'} )
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
        #w = request.user.follower.members.filter(username__exact=u.username)
        f=[]
        for m in u.followed.all():
            if len( request.user.follower.members.filter(id__exact=m.id) ) != 0:
                f.append({'is_follow':True, 'user':m})
            else:
                f.append({'is_follow':False, 'user':m})  

        print f
        return render(request, 'login/account-name/tmp_watcher.html', {'u':u, 'f':f, 'currentpage':'watched'} )
    except:
        print sys.exc_info()
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

def do_social_login(request):
    if request.user.is_authenticated():
        return redirect('/u/')
    else:
        return render(request, 'forwit-login0508/login_a.html', {})


from django import forms
class ImageUploadForm(forms.Form):
    image = forms.ImageField()
    #get from request.FILE
def handle_uploaded_file(f, filename):
    with open('%s' % filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

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
            print request.POST['grade']
            up.degree = request.POST['grade']
            
            imageform = ImageUploadForm(request.POST, request.FILES)
            print 'checking pics', request.FILES
            if imageform.is_valid():
                print 'saving pics'
                up.facephoto = imageform.cleaned_data['image']
            else:
                print imageform.errors
            up.save()
            u.save()
            msg='saved!'
            #return render(request, 'login/tmp_setting2.html', {'uf': uf, 'upf': upf, 'msg': msg})
            return redirect('/')
        else:
            msg =  'INVAID'
            return render(request, 'login/tmp_setting2.html', {'uf': uf, 'upf': upf, 'msg': msg})
    uf = UserForm(instance=u)
    upf = UserProfileForm(instance=up)
    return render(request, 'login/tmp_setting2.html', {'u': u,'uf': uf, 'upf': upf})

def memberlist(request):
    #alluser = User.objects.all()
    alluser=[]
    for up in UserProfile.objects.all():
        alluser.append(up.user)
    return render(request, 'login/tmp_memberlist.html', {'alluser': alluser})

def movielist(request):
    video = Video.objects.all()
    return render(request, 'login/tmp_movielist.html', {'video': video})

def loggedin(request):
    u = request.user
    try:
        uf = u.userprofile
        f = u.follower
        lp = u.likepub
        lv = u.likevideo
        mp = u.myproject
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
            mp = MyProject(user=u)
            mp.save()
            return redirect('/u/')
        return HttpResponse('Error happened!')
    else:
        uf = UserForm(instance=u)
        upf = UserProfileForm()
        return render(request, 'login/tmp_setting2.html', {'uf': uf, 'upf': upf, 'agreement':'yes'})
    
    
def edit_project(request):
    u = request.user
    mypub = Publication.objects.filter(author=u)
    mp = u.myproject
    if request.method == 'POST':
        mpf = MyProjectForm(request.POST, instance=mp)
        if mpf.is_valid():
            mpf.save()
            return redirect('/edit_project/') # this page
    mpf = MyProjectForm(instance=mp)
    return render(request, 'login/account-name/tmp_edit_project.html', {'mpf': mpf, 'mypub':mypub})

def edit_research(request, pubid):
    # check if publication-detail objects of this exists
    pub = Publication.objects.get(pubid=pubid)
    if len( PublicationDetail.objects.filter(pub=pub) ) == 0:
        pubdetail = PublicationDetail(pub=pub)
        pubdetail.save()
    else:
        pubdetail = PublicationDetail.objects.get(pub=pub)
    
    if request.method == 'POST':
#         print request.POST['exposition']
        pubdetail.description=request.POST['exposition']
        pubdetail.save()
        pub.author.add(request.user)
        
        pub.save()
        return redirect('/pub/%s/' % pubid)
    
    
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
        #json.loads(a2.replace("u'", "'").replace("'", '"'))
        authors = json.loads(pub.authors.replace("u'", "'").replace("'", '"'))
        for a in authors:
            org = c.getAffiliation(a['name'])
            a['org'] = org
        try:
            if pub.video_set.all() != []:
                allvideo = pub.video_set.all()
                video = allvideo[len(allvideo)-1]
                video_url = make_youtube_url(video.video_id)
                return render(request, 'login/tmp_edit-research.html', {'pub':pub, 'pubdetail':pubdetail, 'authors': authors, 'video': video,'video_url': video_url, 'abst':abst})
        except:
            return render(request, 'login/tmp_edit-research.html', {'pub':pub, 'pubdetail':pubdetail, 'authors': authors, 'abst':abst})
    except:
        print sys.exc_info()
        return HttpResponse('pubid=%s is not found' % pubid )

#     return render(request, 'login/tmp_edit-research.html', {'pub':pub})

def feedback(request):

    u = request.user
    up = UserProfile(user=u)
    if request.method == 'POST':
        if request.POST['feedback'] != '':
            fb = FeedbackMessage()
            fb.created = datetime.now()
            fb.msg = request.POST['feedback']
            fb.user = request.user
            fb.save()
            return render(request, 'login/account-name/tmp_feedback-thanks.html',{'u': u,})
    #else
    return render(request, 'login/account-name/tmp_feedback.html',{'u': u,})



#for ajax handling     
def add_memopub(request):
    try:
        if request.method == 'POST':
    #         print 'POST'
            pubid = request.POST.get('pubid', False)
            cmd = request.POST.get('cmd', False)
            assert cmd == 'add' or cmd == 'remove'
            if pubid and cmd:
                lp = request.user.likepub
                pub = Publication.objects.get(pubid__exact=str(pubid))
                if cmd == 'add':
                    lp.pub.add(pub)
                    print 'added new pub'
                elif cmd == 'remove':
                    lp.pub.remove(pub)
                    print 'remove pub'
                else:
                    raise Exception('cmd error', 'cmd=%s' % cmd)
                lp.save()
                
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

import forwit_ajax
import traceback
def handle_ajax(request):
    try:
        if request.method == 'POST':
            cmd = request.POST['cmd']
            ret=''
            if cmd == 'add_watch' or cmd== 'remove_watch':
                ret = forwit_ajax.handle_watch(cmd, request)
            if cmd == 'add_videomemo' or cmd == 'remove_videomemo':
                ret = forwit_ajax.handle_likevideo(cmd, request)
            if cmd == 'add_mypub' or cmd == 'remove_mypub':
                ret = forwit_ajax.handle_mypub(cmd, request)
            if cmd == 'add_pubvideo' or cmd == 'remove_pubvideo':
                ret = forwit_ajax.handle_pubvideo(cmd, request)
            else:
                raise Exception('cmd error', 'cmd=%s' % (cmd,))
            print ret
            return HttpResponse(ret, content_type = "application/json")
    except:
        tbinfo = traceback.format_tb( sys.exc_info()[2] )
        emsg =''
        for tbi in tbinfo:
            emsg += tbi
            emsg +='\n'
        dat = {'ret': 'false', 'msg': 'method error', 'info': '%s / %s \n %s' % (sys.exc_info()[0], sys.exc_info()[1], emsg)}
        ret = '%s' % json.dumps(dat) 
        print ret
        return HttpResponse(ret, content_type = "application/json")
        
  
        
        
        