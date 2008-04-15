
from django.template import RequestContext
from django.shortcuts import render_to_response

from lojban.main.models import NewsItem

def home(request):
    news_items = NewsItem.objects.all()[:2]
    return render_to_response("home.html", {"news_items": news_items}, context_instance=RequestContext(request))

def news(request):
    news_items = NewsItem.objects.all()
    return render_to_response("news.html", {"news_items": news_items}, context_instance=RequestContext(request))

def search(request):
    return render_to_response("search.html", context_instance=RequestContext(request))






