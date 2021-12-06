from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Instituicao, Campus
from .utilitarios import gerar_paginacao

@login_required
def instituicoes(request):
  instituicoes = Instituicao.objects.all()
  instituicoes, paginas = gerar_paginacao(request, instituicoes, 10)

  return render(request, 'cadastros/instituicoes/listagem.html', { 
    'instituicoes': instituicoes, 'paginas': paginas
  })