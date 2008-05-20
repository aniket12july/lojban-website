
from datetime import datetime
from time import mktime

import feedparser

from django.core.management.base import NoArgsCommand

from lojban.main.models import *

class Command(NoArgsCommand):

    def handle_noargs(self, **options):

        for weblog in Weblog.objects.all():
            feed_dict = feedparser.parse(weblog.feed_uri)
            weblog.title = feed_dict.feed["title"]
            weblog.link = feed_dict.feed["link"]
            weblog.save()
            for entry in feed_dict.entries:
                WeblogEntry.objects.create(
                    id=entry.id,
                    weblog=weblog,
                    title=entry.title,
                    link=entry.link,
                    pub_date=datetime.fromtimestamp(mktime(entry.published_parsed))
                )


