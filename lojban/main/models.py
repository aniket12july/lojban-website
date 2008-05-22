
import re
from datetime import datetime

from django.db import models
from django.utils import dateformat

friendly_sumti_regexp = re.compile(r'\$?([a-z]+)_\{*(\d)\}*\$?')

class NewsItem(models.Model):
    title = models.CharField(max_length=50, blank=True)
    pub_date = models.DateTimeField("Date published")
    text = models.TextField()

    def get_absolute_url(self):
        return "/news/%d/#news-item-%d" % (self.pub_date.year, self.id)

    class Meta:
        ordering = ("-pub_date",)

    def __unicode__(self):
        return self.title or dateformat.format(self.pub_date, "l d F Y")

    class Admin:
        list_filter = ("pub_date",)
        date_hierarchy = "pub_date"

class FAQ(models.Model):
    question = models.CharField(max_length=250)
    short_title = models.CharField("Short title", max_length=150, blank=True)
    answer = models.TextField()
    position = models.IntegerField()
    slug = models.SlugField(prepopulate_from=("short_title",))

    class Meta:
        ordering = ("position",)

    def __unicode__(self):
        return self.short_title or self.question

    class Admin:
        pass

class Weblog(models.Model):
    title = models.CharField(max_length=200)
    feed_uri = models.URLField(verify_exists=True)
    link = models.URLField(verify_exists=True)

    def __unicode__(self):
        return self.title

    class Admin:
        list_display = ("title", "link")
        search_fields = ("title",)

class WeblogEntry(models.Model):
    id = models.CharField(max_length=200, primary_key=True)
    weblog = models.ForeignKey(Weblog)
    title = models.CharField(max_length=200)
    link = models.URLField(verify_exists=True)
    pub_date = models.DateTimeField("Date published")

    class Meta:
        verbose_name_plural = "Weblog entries"
        ordering = ("-pub_date",)

    def __unicode__(self):
        return self.title

    class Admin:
        list_display = ("title", "weblog", "pub_date")
        list_filter = ("pub_date",)
        date_hierarchy = "pub_date"

class IRCChannel(models.Model):
    name = models.CharField(max_length=50, unique=True)
    server = models.CharField(max_length=100)
    port = models.IntegerField()
    last_activity = models.DateTimeField("Last activity")
    headcount = models.IntegerField()

    @property
    def last_activity_parsed(self):
        delta = datetime.now() - self.last_activity
        minutes = delta.seconds / 60
        hours = minutes / 60
        minutes = minutes % 60
        return delta.days, hours, minutes

    def _days_since_activity(self):
        return self.last_activity_parsed[0]
    _days_since_activity.short_description = "Days since activity"
    days_since_activity = property(_days_since_activity)

    def _hours_since_activity(self):
        return self.last_activity_parsed[1]
    _hours_since_activity.short_description = "Hours since activity"
    hours_since_activity = property(_hours_since_activity)

    def _minutes_since_activity(self):
        return self.last_activity_parsed[2] / 5 * 5 # Round down to nearest five minutes
    _minutes_since_activity.short_description = "Minutes since activity"
    minutes_since_activity = property(_minutes_since_activity)

    def _current_activity(self):
        try:
            days, hours, minutes = self.last_activity_parsed
            if days == 0 and hours == 0 and minutes < 5:
                return True
            else:
                return False
        except:
            return False
    _current_activity.short_description = "Current activity"
    current_activity = property(_current_activity)

    def __unicode__(self):
        return self.name

    class Admin:
        list_display = ("name", "server", "port", "headcount", "last_activity")

class Gismu(models.Model):
    name = models.CharField(max_length=5)
    cvc_rafsi = models.CharField("CVC rafsi", max_length=3, blank=True)
    ccv_rafsi = models.CharField("CCV rafsi", max_length=3, blank=True)
    cvv_rafsi = models.CharField("CVV rafsi", max_length=4, blank=True)
    english_keyword = models.CharField("English keyword", max_length=20, blank=True)
    hint = models.CharField(max_length=21, blank=True)
    definition = models.TextField()
    notes = models.TextField(blank=True)
    official = models.BooleanField(default=True)

    def _friendly_definition(self):
        return friendly_sumti_regexp.sub(r'\1\2', self.definition)
    _friendly_definition.short_description = "Definition"
    friendly_definition = property(_friendly_definition)

    def _friendly_notes(self):
        return friendly_sumti_regexp.sub(r'\1\2', self.notes)
    _friendly_notes.short_description = "Notes"
    friendly_notes = property(_friendly_notes)

    class Meta:
        verbose_name_plural = "gismu"
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    class Admin:
        list_display = ("name", "cvc_rafsi", "ccv_rafsi", "cvv_rafsi", "english_keyword", "hint", "_friendly_definition")
        search_fields = ("name", "cvc_rafsi", "ccv_rafsi", "cvv_rafsi", "english_keyword", "hint", "definition", "notes")

class Selmaho(models.Model):
    name = models.CharField(max_length=10)

    class Meta:
        verbose_name_plural = "selma'o"
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    class Admin:
        search_fields = ("name",)

class Cmavo(models.Model):
    name = models.CharField(max_length=10)
    definition = models.TextField()
    notes = models.TextField(blank=True)
    selmaho = models.ForeignKey(Selmaho, verbose_name="selma'o")
    official = models.BooleanField(default=True)

    def _friendly_definition(self):
        return friendly_sumti_regexp.sub(r'\1\2', self.definition)
    _friendly_definition.short_description = "Definition"
    friendly_definition = property(_friendly_definition)

    def _friendly_notes(self):
        return friendly_sumti_regexp.sub(r'\1\2', self.notes)
    _friendly_notes.short_description = "Notes"
    friendly_notes = property(_friendly_notes)

    class Meta:
        verbose_name_plural = "cmavo"
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    class Admin:
        list_display = ("name", "selmaho", "_friendly_definition")
        list_filter = ("selmaho",)
        search_fields = ("name", "selmaho", "definition", "notes")

class Lujvo(models.Model):
    name = models.CharField(max_length=50)
    definition = models.TextField()
    notes = models.TextField(blank=True)

    def _friendly_definition(self):
        return friendly_sumti_regexp.sub(r'\1\2', self.definition)
    _friendly_definition.short_description = "Definition"
    friendly_definition = property(_friendly_definition)

    def _friendly_notes(self):
        return friendly_sumti_regexp.sub(r'\1\2', self.notes)
    _friendly_notes.short_description = "Notes"
    friendly_notes = property(_friendly_notes)

    class Meta:
        verbose_name_plural = "lujvo"
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    class Admin:
        list_display = ("name", "_friendly_definition")
        search_fields = ("name", "definition", "notes")

class Fuhivla(models.Model):
    name = models.CharField(max_length=50)
    definition = models.TextField()
    notes = models.TextField(blank=True)

    def _friendly_definition(self):
        return friendly_sumti_regexp.sub(r'\1\2', self.definition)
    _friendly_definition.short_description = "Definition"
    friendly_definition = property(_friendly_definition)

    def _friendly_notes(self):
        return friendly_sumti_regexp.sub(r'\1\2', self.notes)
    _friendly_notes.short_description = "Notes"
    friendly_notes = property(_friendly_notes)

    class Meta:
        verbose_name_plural = "fu'ivla"
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    class Admin:
        list_display = ("name", "_friendly_definition")
        search_fields = ("name", "definition", "notes")

class WordOfTheDay(models.Model):
    gismu = models.ForeignKey(Gismu)
    pub_date = models.DateField("Date published", auto_now_add=True)
    example_jbo = models.CharField("Lojban example", max_length=200, blank=True)
    example_en = models.CharField("English example", max_length=200, blank=True)
    status = models.IntegerField(choices=[(0, "Unapproved"), (1, "Approved")])
    credits = models.TextField()

    class Meta:
        ordering = ("-pub_date",)

    def __unicode__(self):
        return self.gismu.name

    class Admin:
        list_display = ("gismu", "pub_date")
        search_fields = ["example_en"]
        date_hierarchy = "pub_date"

class FirstTimeStory(models.Model):
    text = models.CharField("Where the user heard about lojban", max_length=500)
    pub_date = models.DateField("Date entered", auto_now_add=True)
    referrer = models.CharField("HTTP Referrer at time of 'report'", max_length=500)

    class Meta:
        ordering = ("-pub_date",)

    class Admin:
        list_display   = ("text", "pub_date", "referrer")
        search_fields  = ("text", "referrer")
        date_hierarchy = "pub_date"










