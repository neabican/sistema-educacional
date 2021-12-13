from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
  path('campus', views.listar_campus, name='listar_campus'),
  path('campus/<int:pk>', views.detalhes_campus, name='detalhes_campus'),
  path(
    'campus/<int:pk_campus>/programas', 
    views.listar_programas, 
    name='listar_programas'
  ),
  path(
    'campus/<int:pk_campus>/programas/<int:pk>', 
    views.detalhes_programa, 
    name='detalhes_programa'
  ),
]