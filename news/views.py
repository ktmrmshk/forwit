from django.shortcuts import render

from news.models  import News

# Create your views here.
def test_news(request):
    news = News.objects.all()
    return render(request, 'tmp_index.html', {'news': news})