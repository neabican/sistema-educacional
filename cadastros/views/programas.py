from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Programa, Campus
from ..forms import FormPrograma

@login_required
def cadastrar_programa(request, pk_campus):
  campus = get_object_or_404(Campus, pk=pk_campus)
  form = FormPrograma(request.POST or None)

  if request.method == 'POST':
    if form.is_valid():
      try:
        programa_repetido = Programa.objects.get(
          nome=form.cleaned_data['nome'],
          campus=campus
        )
        messages.error(request, 'Esse programa já foi cadastrado no câmpus.')
      except:
        try:
          programa = form.save(commit=False)
          programa.campus = campus
          programa.save()

          messages.success(request, 'Programa cadastrado com sucesso.')
          return redirect('cadastros:detalhes_campus', pk_campus)
        except:
          messages.error(request, 'Erro ao tentar cadastrar o programa. Tente novamente mais tarde.')
    else:
      messages.error(request, 'Erro ao tentar cadastrar o programa. Verifique se todos campos foram preenchidos corretamente.')

  return render(request, 'cadastros/programas/cadastro.html', {
    'tipo': 'Cadastro', 'form': form
  })

@login_required
def editar_programa(request, pk, pk_campus):
  programa = get_object_or_404(Programa, pk=pk)
  campus = get_object_or_404(Campus, pk=pk_campus)

  if request.method == 'POST':
    form = FormPrograma(request.POST, instance=programa)

    if form.is_valid():
      try:
        programa_repetido = Programa.objects.exclude(pk=pk).get(
          nome=form.cleaned_data['nome'],
          campus=campus
        )
        messages.error(request, 'Esse programa já foi cadastrado no câmpus.')
      except:
        try:
          form.save()

          messages.success(request, 'Programa editado com sucesso.')
          return redirect('cadastros:detalhes_campus', pk_campus)
        except:
          messages.error(request, 'Erro ao tentar editar o programa. Tente novamente mais tarde.')
    else:
      messages.error(request, 'Erro ao tentar editar o programa. Verifique se todos campos foram preenchidos corretamente.')
  else:
    form = FormPrograma(instance=programa)

  return render(request, 'cadastros/programas/cadastro.html', {
    'tipo': 'Edição', 'form': form
  })

@login_required
def deletar_programa(request, pk, pk_campus):
  programa = get_object_or_404(Programa, pk=pk)

  try:
    programa.delete()
    messages.success(request, 'Programa deletado com sucesso.')
  except:
    messages.error(request, 'Erro ao tentar deletar o programa. Tente novamente mais tarde.')

  return redirect('cadastros:detalhes_campus', pk_campus)