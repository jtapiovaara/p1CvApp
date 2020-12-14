from django.http import request
from django.shortcuts import render
from django.views import generic
from django.contrib import messages

from .models import Projekti


class IndexView(generic.ListView):
    """
    Listaa kaikki taulun kohteet :model:`projektit.Projekti` -taulusta ja välittää ne standardin mukaisesti
    generiselle templatelle. Spinoffit haetaan omaan muuttujaansa.
    Otsikkopalkissa on base.html tiedostoon laadittuja otsikkoelementtejä. Viimeisenä olevat
    About ja Privacy on toteutettu Django Flatpages -toiminnolla ja ovat ylläpidettävissä Admin -toiminnoilla.

    """
    model = Projekti

    def kahdeksan(self):
        return Projekti.objects.filter(projtype='p')

    def spinoffs(self):
        return Projekti.objects.filter(projtype='s').order_by('title')

    def fullstacks(self):
        return Projekti.objects.filter(projtype='j').order_by('title')

    def thonny(self):
        return Projekti.objects.filter(projtype='t').order_by('title')


class DetailView(generic.DetailView):
    """
    Projektilistalta valitun projektin yksityiskohtaiset tiedot.  Tässä tapauksessa projekti.id,
    jolla haetaan ao. projektin tietoja geneeriselle templatelle.

    """
    model = Projekti
