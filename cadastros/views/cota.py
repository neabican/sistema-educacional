from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from ..forms import FormCota
from ..models import Cota, Instituicao

@login_required
def cadastrar_cota(request, pk_instituicao):
    form = FormCota(request.POST or None)
    instituicao = get_object_or_404(Instituicao, pk=pk_instituicao)
    status_code = 200

    if request.method == 'POST':
        if form.is_valid():
            try:
                cota = form.save(commit=False)
                cota.instituicao_id = instituicao.pk
                cota.save()
                messages.success(request, 'Cota cadastrada com sucesso.')
                return redirect('cadastros:detalhes_instituicao', instituicao.pk)
            except Exception as exc:
                print(exc)
                messages.error(request, 'Erro ao tentar cadastrar a cota. Tente novamente mais tarde.')
                status_code = 400
        else:
            messages.error(request, 'Erro ao tentar cadastrar a cota. Verifique se todos campos foram preenchidos corretamente.')
            status_code = 400

    return render(request, 'cadastros/cota/cadastro.html', {
      'tipo': 'Cadastro',
      'form': form
    }, status=status_code)

@login_required
def editar_cota(request, pk_cota, pk_instituicao):
    cota = get_object_or_404(Cota, pk=pk_cota)
    instituicao = get_object_or_404(Instituicao, pk=pk_instituicao)
    status_code = 200

    if request.method == 'POST':
      form = FormCota(request.POST, instance=cota)

      if form.is_valid():
        try:
            form.save()
            messages.success(request, 'Cota editado com sucesso.')
            return redirect('cadastros:detalhes_instituicao', instituicao.pk)
        except:
            messages.error(request, 'Erro ao tentar editar a cota. Tente novamente mais tarde.')
            status_code = 400
      else:
        messages.error(request, 'Erro ao tentar editar a cota. Verifique se todos campos foram preenchidos corretamente.')
        status_code = 400
    else:
      form = FormCota(instance=cota)

    return render(request, 'cadastros/cota/cadastro.html', {
      'tipo': 'Edição',
      'form': form
    }, status=status_code)


@login_required
def deletar_cota(request, pk_cota, pk_instituicao):
    cota = get_object_or_404(Cota, pk=pk_cota)

    try:
        cota.delete()
        messages.success(request, 'Cota removida com sucesso.')
    except:
        messages.error(request, 'Erro ao tentar remover a cota. Tente novamente mais tarde.')

    return redirect('cadastros:detalhes_instituicao', pk_instituicao)
