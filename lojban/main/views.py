
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect

from lojban.main.models import *

def home(request):
    news_items = NewsItem.objects.all()[:2]
    return render_to_response("home.html", {"news_items": news_items}, context_instance=RequestContext(request))

def news(request):
    news_items = NewsItem.objects.all()
    return render_to_response("news.html", {"news_items": news_items}, context_instance=RequestContext(request))

def search(request):
    keywords = request.GET.get("keywords", "").split()
    matches = []
    for keyword in keywords:
        keyword = keyword.replace(".", " ").strip()
        for Valsi in Gismu, Cmavo, Lujvo, Fuhivla:
            try:
                valsi = Valsi.objects.get(name=keyword)
                valsi_type = type(valsi).__name__.lower()
                if valsi_type == "fuhivla":
                    valsi_type = "fu'ivla"
                autolink_regexp = re.compile(r'\{([a-zA-Z\']+)\}')
                valsi.notes = valsi.notes.replace("&", "&amp;").replace("<", "&lt;")
                valsi.notes = autolink_regexp.sub(r'<a href="/search/?keywords=\1">\1</a>', valsi.notes)
                matches.append((valsi, valsi_type))
            except Valsi.DoesNotExist:
                pass
    return render_to_response("search.html", {"matches": matches}, context_instance=RequestContext(request))

def heard(request):
    heard_story = FirstTimeStory(text=request.POST['heard'], referrer=request.POST['referrer'])
    heard_story.save()
    return HttpResponseRedirect("/")


