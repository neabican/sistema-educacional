from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Instituicao, Campus
from .utilitarios import gerar_paginacao

@login_required
def instituicoes(request):
  status_code = 200

  if request.method == 'POST':
    nome = request.POST.get('nome', None)
    pk = request.POST.get('pk', None)

    if nome is not None and pk is None:
      # Cadastrando nova instituição
      try:
        Instituicao.objects.create(nome=nome)
        messages.success(request, 'Instituição cadastrada com sucesso.')
        status_code = 201
      except:
        messages.error(request, 'Essa instituição já foi cadastrada.')
        status_code = 400
    elif nome is not None and pk is not None:
      # Editando instituição existente
      try:
        instituicao = Instituicao.objects.get(pk=pk)

        try:
          instituicao.nome = nome
          instituicao.save()
          
          messages.success(request, 'Instituição editada com sucesso.')
          status_code = 201
        except:
          messages.error(request, 'Essa instituição já foi cadastrada.')
          status_code = 400
      except Instituicao.DoesNotExist:
        messages.error(request, 'Erro ao tentar editar a instituição. Tente novamente mais tarde.')
        status_code = 400
    elif nome is None and pk is not None:
      # Deletando instituição existente
      try:
        instituicao = Instituicao.objects.get(pk=pk)

        try:
          instituicao.delete()
          messages.success(request, 'Instituição deletada com sucesso.')
          status_code = 200
        except:
          messages.error(request, 'Essa instituição não pode ser deletada pois tem vínculo com 1 ou mais câmpus.')
          status_code = 400
      except Instituicao.DoesNotExist:
        messages.error(request, 'Erro ao tentar deletar a instituição. Esta instituição não foi encontrada.')
        status_code = 404

  instituicoes = Instituicao.objects.all().order_by('id')
  # Paginando resultados
  instituicoes, paginas = gerar_paginacao(request, instituicoes, 10)

  return render(request, 'cadastros/instituicoes/listagem.html', { 
    'instituicoes': instituicoes, 'paginas': paginas
  }, status=status_code)