from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [
  path('', views.dashboard, name='dashboard'),

  # Instituições
  path('instituicoes', views.instituicoes, name='instituicoes'),

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

  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
]