from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import AcaoAfirmativa, Campus
from ..forms import FormAcaoAfirmativa

@login_required
def cadastrar_acao_afirmativa(request, pk_campus):
  campus = get_object_or_404(Campus, pk=pk_campus)
  form = FormAcaoAfirmativa(request.POST or None)
  status_code = 200

  if request.method == 'POST':
    if form.is_valid():
      try:
        acao_repetida = AcaoAfirmativa.objects.get(
          nome=form.cleaned_data['nome'],
          campus=campus
        )
        messages.error(request, 'Essa ação afirmativa já foi cadastrada no câmpus.')
        status_code = 400
      except:
        try:
          acao_afirmativa = form.save(commit=False)
          acao_afirmativa.campus = campus
          acao_afirmativa.save()

          messages.success(request, 'Ação afirmativa cadastrada com sucesso.')
          return redirect('cadastros:detalhes_campus', pk_campus)
        except:
          messages.error(request, 'Erro ao tentar cadastrar a ação afirmativa. Tente novamente mais tarde.')
          status_code = 400
    else:
      messages.error(request, 'Erro ao tentar cadastrar a ação afirmativa. Verifique se todos campos foram preenchidos corretamente.')
      status_code = 400

  return render(request, 'cadastros/acoes_afirmativas/cadastro.html', {
    'tipo': 'Cadastro', 'form': form
  }, status=status_code)

@login_required
def editar_acao_afirmativa(request, pk, pk_campus):
  acao_afirmativa = get_object_or_404(AcaoAfirmativa, pk=pk)
  campus = get_object_or_404(Campus, pk=pk_campus)
  status_code = 200

  if request.method == 'POST':
    form = FormAcaoAfirmativa(request.POST, instance=acao_afirmativa)

    if form.is_valid():
      try:
        acao_repetida = AcaoAfirmativa.objects.exclude(pk=pk).get(
          nome=form.cleaned_data['nome'],
          campus=campus
        )
        messages.error(request, 'Essa ação afirmativa já foi cadastrada no câmpus.')
        status_code = 400
      except:
        try:
          form.save()

          messages.success(request, 'Ação afirmativa editada com sucesso.')
          return redirect('cadastros:detalhes_campus', pk_campus)
        except:
          messages.error(request, 'Erro ao tentar editar a ação afirmativa. Tente novamente mais tarde.')
          status_code = 400
    else:
      messages.error(request, 'Erro ao tentar editar a ação afirmativa. Verifique se todos campos foram preenchidos corretamente.')
      status_code = 400
  else:
    form = FormAcaoAfirmativa(instance=acao_afirmativa)

  return render(request, 'cadastros/acoes_afirmativas/cadastro.html', {
    'tipo': 'Edição', 'form': form
  }, status=status_code)

@login_required
def deletar_acao_afirmativa(request, pk, pk_campus):
  acao_afirmativa = get_object_or_404(AcaoAfirmativa, pk=pk)

  try:
    acao_afirmativa.delete()
    messages.success(request, 'Ação afirmativa deletada com sucesso.')
  except:
    messages.error(request, 'Erro ao tentar deletar a ação afirmativa. Tente novamente mais tarde.')

  return redirect('cadastros:detalhes_campus', pk_campus)