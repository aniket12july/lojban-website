
import re

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










