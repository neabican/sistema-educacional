from django.urls import path
from . import views

app_name = 'cadastros'

urlpatterns = [
  path('', views.dashboard, name='dashboard'),
  path('instituicoes', views.instituicoes, name='instituicoes'),

  path('cursos', views.cursos, name='cursos'),
  path('cursos/cadastrar', views.cadastrar_curso, name='cadastrar_curso'),
  path('cursos/editar/<int:pk>', views.editar_curso, name='editar_curso'),

  path('campus', views.campus, name='campus'),
  path('campus/cadastrar', views.cadastrar_campus, name='cadastrar_campus'),
  path('campus/editar/<int:pk>', views.editar_campus, name='editar_campus'),

  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
]