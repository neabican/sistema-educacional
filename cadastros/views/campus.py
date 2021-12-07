from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Campus
from ..forms import FormCampus, FormEndereco
from .utilitarios import gerar_paginacao

@login_required
def campus(request):
  if request.method == 'POST':
    try:
      pk = request.POST['pk']
      campus = Campus.objects.get(pk=pk)

      try:
        campus.delete()
        messages.success(request, 'Câmpus deletado com sucesso.')
      except:
        messages.error(request, 'Erro ao tentar deletar o câmpus. Tente novamente mais tarde.')  
    except Campus.DoesNotExist:
      messages.error(request, 'Erro ao tentar deletar o câmpus. O câmpus não foi encontrado.')

  campus = Campus.objects.all().order_by('id')
  # Paginando resultados
  campus, paginas = gerar_paginacao(request, campus, 10)

  return render(request, 'cadastros/campus/listagem.html', {
    'lista_campus': campus, 'paginas': paginas
  })

@login_required
def cadastrar_campus(request):
  form = FormCampus(request.POST or None)
  form_endereco = FormEndereco(request.POST or None)

  if request.method == 'POST':
    if form.is_valid() and form_endereco.is_valid():
      try:
        # Tenta buscar um câmpus com o mesmo nome que pertença à mesma instituição
        campus_repetido = Campus.objects.get(
          nome=form.cleaned_data['nome'],
          instituicao=form.cleaned_data['instituicao']
        )

        messages.error(request, 'Este câmpus desta instituição já foi cadastrado.')
      except:
        # Caso não seja um câmpus repetido, tenta cadastrá-lo
        try:
          campus = form.save(commit=False)
          endereco = form_endereco.save()

          campus.endereco = endereco
          campus.save()
          messages.success(request, 'Câmpus cadastrado com sucesso.')

          return redirect('cadastros:campus')
        except:
          messages.error(request, 'Erro ao tentar cadastrar o câmpus. Tente novamente mais tarde.')
    else:
      messages.error(request, 'Erro ao tentar cadastrar o câmpus. Verifique se todos câmpus foram preenchidos corretamente.')

  return render(request, 'cadastros/campus/cadastro.html', {
    'tipo': 'Cadastro', 'form': form, 'form_endereco': form_endereco
  })
