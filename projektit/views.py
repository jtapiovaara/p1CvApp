from django.views import generic
from .models import Projekti


class IndexView(generic.ListView):
    model = Projekti


class DetailView(generic.DetailView):
    model = Projekti
