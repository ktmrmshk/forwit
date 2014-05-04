from django.shortcuts import render

from news.models  import News
import cinii

# Create your views here.
def test_news(request):
    news = News.objects.all()
    return render(request, 'tmp_index.html', {'news': news})


def test_search(request):
    if request.method == 'POST':
        print request.POST['q']
        pub = cinii.Publist()
        pub.q = request.POST['q']
        pub.setparam()
        pub.get()
        publist = pub.parse_dat_all()
        return render(request, 'tmp_search-result.html', {'publist': publist[:20]})

    return render(request, 'tmp_search-result.html')