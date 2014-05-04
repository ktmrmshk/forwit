from django.shortcuts import render
import urllib
from news.models  import News
import cinii

# Create your views here.
def test_news(request):
    news = News.objects.all()
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
        
        query={}
        query['q'] = q
        q_for_navi = 'http://' + request.get_host()
        q_for_navi += request.path
        q_for_navi += '?'
        q_for_navi += urllib.urlencode(query)
        
        start = (page-1) * 20
        #DEBUG
        #print 'start=%d' % start
        pub = cinii.Publist()
        pub.q = q
        pub.setparam(count=20, start=start)
        pub.get()
        publist = pub.parse_dat_all()
        return render(request, 'tmp_search-result.html', {'cnt_ret': pub.cnt_ret, 'publist': publist, 'page': page, 'q_for_navi': q_for_navi })

    return render(request, 'tmp_search-result.html')