from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [
  path('', views.dashboard, name='dashboard'),

  # Instituições
  path('instituicoes', views.instituicoes, name='instituicoes'),
  path('instituicoes/detalhes/<int:pk>', views.detalhes_instituicao, name='detalhes_instituicao'),
 
  path('instituicoes/detalhes/<int:pk_instituicao>/cadastrar_cota', views.cadastrar_cota, name='cadastrar_cota'),
  path('instituicoes/detalhes/<int:pk_instituicao>/editar_cota/<int:pk_cota>', views.editar_cota, name='editar_cota'),
  path('instituicoes/detalhes/<int:pk_instituicao>/deletar_cota/<int:pk_cota>', views.deletar_cota, name='deletar_cota'),


  # Cursos
  path('cursos', views.cursos, name='cursos'),
  path('cursos/cadastrar', views.cadastrar_curso, name='cadastrar_curso'),
  path('cursos/editar/<int:pk>', views.editar_curso, name='editar_curso'),

  # Câmpus
  path('campus', views.campus, name='campus'),
  path('campus/cadastrar', views.cadastrar_campus, name='cadastrar_campus'),
  path('campus/editar/<int:pk>', views.editar_campus, name='editar_campus'),
  path('campus/detalhes/<int:pk>', views.detalhes_campus, name='detalhes_campus'),

  # Cursos Câmpus
  path(
    'campus/detalhes/<int:pk>/cadastrar-curso', 
    views.cadastrar_curso_campus, 
    name='cadastrar_curso_campus'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/editar-curso/<int:pk>', 
    views.editar_curso_campus, 
    name='editar_curso_campus'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/deletar-curso/<int:pk>', 
    views.deletar_curso_campus, 
    name='deletar_curso_campus'
  ),
  
  # Imagens
  path(
    'campus/detalhes/<int:pk_campus>/cadastrar-imagem', 
    views.cadastrar_imagem, 
    name='cadastrar_imagem'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/editar-imagem/<int:pk>', 
    views.editar_imagem, 
    name='editar_imagem'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/deletar-imagem/<int:pk>', 
    views.deletar_imagem, 
    name='deletar_imagem'
  ),

  # Programas
  path(
    'campus/detalhes/<int:pk_campus>/cadastrar-programa', 
    views.cadastrar_programa, 
    name='cadastrar_programa'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/editar-programa/<int:pk>', 
    views.editar_programa, 
    name='editar_programa'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/deletar-programa/<int:pk>', 
    views.deletar_programa, 
    name='deletar_programa'
  ),

  # Projetos
  path(
    'campus/detalhes/<int:pk_campus>/cadastrar-projeto', 
    views.cadastrar_projeto, 
    name='cadastrar_projeto'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/editar-projeto/<int:pk>', 
    views.editar_projeto, 
    name='editar_projeto'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/deletar-projeto/<int:pk>', 
    views.deletar_projeto, 
    name='deletar_projeto'
  ),

  # Projetos
  path(
    'campus/detalhes/<int:pk_campus>/cadastrar-acao-afirmativa', 
    views.cadastrar_acao_afirmativa, 
    name='cadastrar_acao_afirmativa'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/editar-acao-afirmativa/<int:pk>', 
    views.editar_acao_afirmativa, 
    name='editar_acao_afirmativa'
  ),
  path(
    'campus/detalhes/<int:pk_campus>/deletar-acao-afirmativa/<int:pk>', 
    views.deletar_acao_afirmativa, 
    name='deletar_acao_afirmativa'
  ),

  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
]