from django.db import models


class Projekti(models.Model):
    """Kahdeksan CV projektia ja matkalla syntyneet 'spinoffit' tallettava taulu.
    Meta -datalinkissä ordering 'shortdescription', jolla voi helposti
    hallita projektilistan järjestystä (ei välttämättä P1-P8)"""
    PROJTYPE_CHOICES =[
        ('p', 'Pääprojekti'),
        ('s', 'SpinOff - Django'),
        ('j', 'SpinOff - JS'),
    ]
    title = models.CharField(max_length=32, blank=True)
    projtype = models.CharField(max_length=1, blank=True, choices=PROJTYPE_CHOICES)
    shortdescription = models.TextField()
    description = models.TextField(blank=True)
    app_image = models.ImageField(blank=True)
    image = models.ImageField(blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('shortdescription',)
