from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [
  path('', views.dashboard, name='dashboard'),
  path('instituicoes', views.instituicoes, name='instituicoes'),

  path('cursos', views.cursos, name='cursos'),

  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
]