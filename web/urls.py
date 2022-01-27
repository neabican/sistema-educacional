from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
  path('', views.listar_campus, name='listar_campus'),
  path('campus/<int:pk>', views.detalhes_campus, name='detalhes_campus'),
]