#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.syndication.feeds import Feed
from django.utils.feedgenerator import Atom1Feed

from lojban.main.models import NewsItem

class NewsFeed(Feed):
    feed_type = Atom1Feed
    title = "News from Lojbanistan"
    link = "/news/"
    subtitle = "News about Lojban, the logical language."

    def items(self):
        return NewsItem.objects.order_by('-pub_date')[:5]

    def item_pubdate(self, item):
        return item.pub_date







