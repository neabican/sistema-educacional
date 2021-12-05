from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [
  path('', views.dashboard, name='dashboard'),

  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
]