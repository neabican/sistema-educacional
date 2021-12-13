from django.urls import path
from . import views

app_name = 'api'

urlpatterns = [
  path('campus', views.listar_campus, name='listar_campus'),
  path('campus/<int:pk>', views.detalhes_campus, name='detalhes_campus'),

  # Programas
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

  # Projetos
  path(
    'campus/<int:pk_campus>/projetos', 
    views.listar_projetos, 
    name='listar_projetos'
  ),
  path(
    'campus/<int:pk_campus>/projetos/<int:pk>', 
    views.detalhes_projeto, 
    name='detalhes_projeto'
  ),

  # Ações Afirmativas
  path(
    'campus/<int:pk_campus>/acoes-afirmativas', 
    views.listar_acoes_afirmativas, 
    name='listar_acoes_afirmativas'
  ),
  path(
    'campus/<int:pk_campus>/acoes-afirmativas/<int:pk>', 
    views.detalhes_acao_afirmativa, 
    name='detalhes_acao_afirmativa'
  ),
]