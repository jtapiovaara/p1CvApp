import requests
import datetime

from django.shortcuts import render
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.admin import User
from django.conf import settings
from django.contrib.auth.decorators import login_required

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


# def ouraapi(request):
    '''2021-01-09 Päätös hakea aina kaikista rajapinnoista 'kaikki' data. Vaihtoehtona olisi hakea vain eilisestä eteenpäin.
    Oli käytössä Sleep- ja Readiness- rajapinnoissa.  Voi muuttaa takaisin jos tarvis, toiminnot #-merkitty'''

#TODO käyttäjän lisääminen.  Myös OURA_ID taulu ja sen hyödyntäminen. SUora linkki palveluun (p1CvApp/projektit/ouracall)
def logout(request):
    logout(request)
    # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

@login_required
# def index(request):
def ouraapi(request):
    rooms = User.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'projektit/ouraring.html', context)

    global sleepstory
    ouraapi = OURA_API
    today = datetime.date.today()
    eilinen = str(today - datetime.timedelta(days=1))

    url_user = 'https://api.ouraring.com/v1/userinfo?access_token=' + ouraapi
    # url_sleep = 'https://api.ouraring.com/v1/sleep?start=' + eilinen + '&access_token=' + ouraapi
    url_sleep = 'https://api.ouraring.com/v1/sleep?&access_token=' + ouraapi
    url_active = 'https://api.ouraring.com/v1/activity?access_token=' + ouraapi
    # url_ready = 'https://api.ouraring.com/v1/readiness?start=' + eilinen + '&access_token=' + ouraapi
    url_ready = 'https://api.ouraring.com/v1/readiness?&access_token=' + ouraapi
    url_bedtime = 'https://api.ouraring.com/v1/bedtime?access_token=' + ouraapi
    u = requests.get(url_user).json()
    s = requests.get(url_sleep).json()
    a = requests.get(url_active).json()
    r = requests.get(url_ready).json()
    b = requests.get(url_bedtime).json()

    # BMI (u)
    height = float(u['height']) / 100
    weight = float(u['weight'])
    bmi = round(weight / (height * height), 2)

    # Syvän unen määrä viime yönä (s)
    sleeptotal = s['sleep'][0]['total']/60
    deepsleepamount = s['sleep'][-1]['deep']/60
    deepscore = s['sleep'][0]['score_deep']
    deepsleeppercentage = round(deepsleepamount/sleeptotal*100, 1)
    if deepsleeppercentage < 12:
        sleepstory = ', mikä on liian vähän'
    if 12 <= deepsleeppercentage < 17:
        sleepstory = ', mikä on melkein riittävästi'
    if deepsleeppercentage >= 17:
        sleepstory = ', hyvät syvät!'

    # Aktiivisuus, viimeiset 2h (a)
    a_kappyra = a['activity'][-1]['class_5min']
    a_2h = a_kappyra[-24:]

    # Kävellyt kilometrit eilen
    activedata = a['activity'][-2]['daily_movement']

    # Kävellyt kilometrit tänään
    activedata_2 = a['activity'][-1]['daily_movement']

    # Kävellyt kilometrit tänään miinus eilen.  Onko käyrä ylös vai alas?
    plusmiinus = int(activedata_2) - int(activedata)

    # Otetut askeleet, total (5 vrk)
    stepsit = a['activity'][-7:]

    # Askelet tänään
    steps = a['activity'][-1]['steps']

    # Valmislukema (r)
    readydata = r['readiness'][-1]['score']
    readydatahistory = r['readiness'][-7:]

    # score_previous_day vaihdettu '-2' koska en tiedä, mitä se tekee
    # r_yesterday = r['readiness'][-1]['score_previous_day']
    r_yesterday = r['readiness'][-2]['score']
    valmiusero = readydata - r_yesterday

    # Ihanteellinen nukkumaanmenoaika (b)
    nukkumaanko = b['ideal_bedtimes'][0]['status']
    unille = b['ideal_bedtimes'][-1]['bedtime_window']['start']
    # unille = 1200
    pillowtime = ''

    if unille != None:
        seconds_input = unille
        conversion = datetime.timedelta(seconds=seconds_input)
        ta = str(conversion)
        pillowtime = ta[-8:-3]

    context = {
        'bmi': bmi,
        'deepsleepamount': deepsleepamount,
        'deepsleeppercentage': deepsleeppercentage,
        'sleepstory': sleepstory,
        'a_2h': a_2h,
        'readydatahistory': readydatahistory,
        'plusmiinus': plusmiinus,
        'stepsit': stepsit,
        'steps': steps,
        'readydata': readydata,
        'nukkumaanko': nukkumaanko,
        'unille': unille,
        'pillowtime': pillowtime,
        'valmiusero': valmiusero,
    }
    return render(request, 'projektit/ouraring.html', {'context': context})
