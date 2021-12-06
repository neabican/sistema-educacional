from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Instituicao, Campus
from .utilitarios import gerar_paginacao

@login_required
def instituicoes(request):
  if request.method == 'POST':
    nome = request.POST.get('nome', None)
    pk = request.POST.get('pk', None)

    if nome is not None and pk is None:
      # Cadastrando nova instituição
      try:
        Instituicao.objects.create(nome=nome)
        messages.success(request, 'Instituição cadastrada com sucesso.')
      except:
        messages.error(request, 'Essa instituição já foi cadastrada.')
    elif nome is not None and pk is not None:
      # Editando instituição existente
      try:
        instituicao = Instituicao.objects.get(pk=pk)

        try:
          instituicao.nome = nome
          instituicao.save()
          messages.success(request, 'Instituição editada com sucesso.')
        except:
          messages.error(request, 'Essa instituição já foi cadastrada.')
      except Instituicao.DoesNotExist:
        messages.error(request, 'Erro ao tentar editar a instituição. Tente novamente mais tarde.')
    elif nome is None and pk is not None:
      # Deletando instituição existente
      try:
        instituicao = Instituicao.objects.get(pk=pk)

        try:
          instituicao.delete()
          messages.success(request, 'Instituição deletada com sucesso.')
        except:
          messages.error(request, 'Essa instituição não pode ser deletada pois tem vínculo com 1 ou mais câmpus.')
      except Instituicao.DoesNotExist:
        messages.error(request, 'Erro ao tentar deletar a instituição. Tente novamente mais tarde.')

  instituicoes = Instituicao.objects.all().order_by('id')
  # Paginando resultados
  instituicoes, paginas = gerar_paginacao(request, instituicoes, 10)

  return render(request, 'cadastros/instituicoes/listagem.html', { 
    'instituicoes': instituicoes, 'paginas': paginas
  })