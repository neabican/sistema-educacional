from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Instituicao, Campus, Curso

@login_required
def dashboard(request):
  instituicoes = Instituicao.objects.count()
  campus = Campus.objects.count()
  cursos = Curso.objects.count()

  dados = {
    'instituicoes': instituicoes,
    'campus': campus,
    'cursos': cursos
  }

  return render(request, 'dashboard.html', {'dados': dados})