import requests
import datetime
from django.http import request
from django.shortcuts import render
from django.views import generic
from django.contrib import messages

from .models import Projekti

from p1CvApp.ei_gittiin import OURA_API


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


def ouraapi(request):
    ouraapi = OURA_API
    today = datetime.date.today()
    eilinen = str(today - datetime.timedelta(days=1))

    url_user = 'https://api.ouraring.com/v1/userinfo?access_token=' + ouraapi
    url_sleep = 'https://api.ouraring.com/v1/sleep?start=' + eilinen + '&access_token=' + ouraapi
    url_active = 'https://api.ouraring.com/v1/activity?access_token=' + ouraapi
    url_ready = 'https://api.ouraring.com/v1/readiness?start=' + eilinen + '&access_token=' + ouraapi
    url_bedtime = 'https://api.ouraring.com/v1/bedtime?access_token=' + ouraapi
    u = requests.get(url_user).json()
    s = requests.get(url_sleep).json()
    a = requests.get(url_active).json()
    r = requests.get(url_ready).json()
    b = requests.get(url_bedtime).json()

    # BMI
    height = float(u['height']) / 100
    weight = float(u['weight'])
    bmi = round(weight / (height * height), 2)

    # Syvän unen määrä viime yönä
    sleepdata = s['sleep'][0]['deep'] / 60
    # sd = s['sleep'][-1]['deep']/60

    # Aktiivisuus, viimeiset 2h
    a_kappyra = a['activity'][-1]['class_5min']
    a_2h = a_kappyra[-24:]
    print(a_kappyra)

    # Kävellyt kilometrit eilen
    activedata = a['activity'][-2]['daily_movement']

    # Kävellyt kilometrit tänään
    activedata_2 = a['activity'][-1]['daily_movement']

    # Kävellyt kilometrit tänään miinus eilen.  Onko käyrä ylös vai alas?
    plusmiinus = int(activedata_2) - int(activedata)

    # Askelet tänään
    steps = a['activity'][-1]['steps']

    # Valmislukema
    readydata = r['readiness'][0]['score']
    r_yesterday = r['readiness'][0]['score_previous_day']
    valmiusero = readydata - r_yesterday

    # Ihanteellinen nukkumaanmenoaika
    nukkumaan = b['ideal_bedtimes'][0]['status']
    unille = b['ideal_bedtimes'][-1]['bedtime_window']['start']
    # unille = 1200
    tyynyaika = ''

    if unille != None:
        seconds_input = unille
        conversion = datetime.timedelta(seconds=seconds_input)
        ta = str(conversion)
        tyynyaika = ta[-8:-3]

    context = {
        'bmi': bmi,
        'sleepdata': sleepdata,
        'a_2h': a_2h,
        'plusmiinus': plusmiinus,
        'steps': steps,
        'readydata': readydata,
        'nukkumaan': nukkumaan,
        'unille': unille,
        'tyynyaika': tyynyaika,
        'valmiusero': valmiusero,
    }
    return render(request, 'projektit/ouraring.html', {'context': context})
