from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'projektit'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('projektit/', views.IndexView.as_view(), name='index'),
    path('projektit/<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('oura/', views.ouraapi, name='ouracall')
]

