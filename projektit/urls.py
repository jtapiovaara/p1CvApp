from django.urls import path

from . import views

app_name = 'projektit'

urlpatterns = [
    path('projektit/', views.IndexView.as_view(), name='index'),
    path('projektit/<int:pk>/', views.DetailView.as_view(), name='detail'),
]

