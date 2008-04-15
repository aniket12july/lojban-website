
from django.db import models
from django.utils import dateformat

class NewsItem(models.Model):
    title = models.CharField(max_length=50, blank=True)
    pub_date = models.DateTimeField("Date published")
    text = models.TextField()

    class Meta:
        ordering = ("-pub_date",)

    def __unicode__(self):
        if self.title:
            return self.title
        else:
            return dateformat.format(self.pub_date, "l d F Y")

    class Admin:
        pass

class Gismu(models.Model):
    name = models.CharField(max_length=5)
    cvc_rafsi = models.CharField("CVC rafsi", max_length=3, blank=True)
    ccv_rafsi = models.CharField("CCV rafsi", max_length=3, blank=True)
    cvv_rafsi = models.CharField("CVV rafsi", max_length=4, blank=True)
    english_keyword = models.CharField("English keyword", max_length=20, blank=True)
    hint = models.CharField(max_length=21, blank=True)
    place_structure = models.CharField("Place structure", max_length=91)

    class Meta:
        ordering = ("name",)

    def __unicode__(self):
        return self.name

    class Admin:
        pass

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













