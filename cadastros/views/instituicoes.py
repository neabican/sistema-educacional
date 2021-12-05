from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Instituicao, Campus

@login_required
def instituicoes(request):
  instituicoes = Instituicao.objects.all()

  return render(request, 'cadastros/instituicoes/listagem.html', { 'instituicoes': instituicoes })