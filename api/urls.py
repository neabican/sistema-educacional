from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
  path('campus', views.listar_campus, name='listar_campus'),
]