from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Projeto, Campus
from ..forms import FormProjeto

@login_required
def cadastrar_projeto(request, pk_campus):
  campus = get_object_or_404(Campus, pk=pk_campus)
  form = FormProjeto(request.POST or None)

  if request.method == 'POST':
    if form.is_valid():
      try:
        projeto_repetido = Projeto.objects.get(
          nome=form.cleaned_data['nome'],
          campus=campus
        )
        messages.error(request, 'Esse projeto já foi cadastrado no câmpus.')
      except:
        try:
          projeto = form.save(commit=False)
          projeto.campus = campus
          projeto.save()

          messages.success(request, 'Projeto cadastrado com sucesso.')
          return redirect('cadastros:detalhes_campus', pk_campus)
        except:
          messages.error(request, 'Erro ao tentar cadastrar o projeto. Tente novamente mais tarde.')
    else:
      messages.error(request, 'Erro ao tentar cadastrar o projeto. Verifique se todos campos foram preenchidos corretamente.')

  return render(request, 'cadastros/projetos/cadastro.html', {
    'tipo': 'Cadastro', 'form': form
  })

@login_required
def editar_projeto(request, pk, pk_campus):
  projeto = get_object_or_404(Projeto, pk=pk)
  campus = get_object_or_404(Campus, pk=pk_campus)

  if request.method == 'POST':
    form = FormProjeto(request.POST, instance=projeto)

    if form.is_valid():
      try:
        projeto_repetido = Projeto.objects.exclude(pk=pk).get(
          nome=form.cleaned_data['nome'],
          campus=campus
        )
        messages.error(request, 'Esse projeto já foi cadastrado no câmpus.')
      except:
        try:
          form.save()

          messages.success(request, 'Projeto editado com sucesso.')
          return redirect('cadastros:detalhes_campus', pk_campus)
        except:
          messages.error(request, 'Erro ao tentar editar o projeto. Tente novamente mais tarde.')
    else:
      messages.error(request, 'Erro ao tentar editar o projeto. Verifique se todos campos foram preenchidos corretamente.')
  else:
    form = FormProjeto(instance=projeto)

  return render(request, 'cadastros/projetos/cadastro.html', {
    'tipo': 'Edição', 'form': form
  })

@login_required
def deletar_projeto(request, pk, pk_campus):
  projeto = get_object_or_404(Projeto, pk=pk)

  try:
    projeto.delete()
    messages.success(request, 'Projeto deletado com sucesso.')
  except:
    messages.error(request, 'Erro ao tentar deletar o projeto. Tente novamente mais tarde.')

  return redirect('cadastros:detalhes_campus', pk_campus)