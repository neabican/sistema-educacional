from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Imagem, Campus
from ..forms import FormImagem


@login_required
def cadastrar_imagem(request, pk_campus):
    campus = get_object_or_404(Campus, pk=pk_campus)
    form = FormImagem(request.POST or None, request.FILES or None)
    status_code = 200

    if request.method == 'POST':
        if form.is_valid():
            try:
                imagem = form.save(commit=False)
                arquivo_antigo = ''
                imagem.campus = campus
                imagem.save(arquivo_antigo)

                messages.success(request, 'Imagem cadastrada com sucesso.')
                return redirect('cadastros:detalhes_campus', pk_campus)
            except Exception as e:
                print(e)
                messages.error(
                    request, 'Erro ao tentar cadastrar a imagem. Tente novamente mais tarde.')
                status_code = 400
        else:
            messages.error(
                request, 'Erro ao tentar cadastrar a imagem. Verifique se todos campos foram preenchidos corretamente.')
            status_code = 400

    return render(request, 'cadastros/imagens/cadastro.html', {
        'tipo': 'Cadastro', 'form': form
    }, status=status_code)


@login_required
def editar_imagem(request, pk, pk_campus):
    imagem = get_object_or_404(Imagem, pk=pk)
    campus = get_object_or_404(Campus, pk=pk_campus)
    status_code = 200

    if request.method == 'POST':
        form = FormImagem(request.POST, request.FILES or None, instance=imagem)

        if form.is_valid():
            try:
                imagem = form.save(commit=False)
                imagem.campus = campus
                arquivo_antigo = imagem.foto
                imagem.save(arquivo_antigo)

                messages.success(request, 'Imagem editada com sucesso.')
                return redirect('cadastros:detalhes_campus', pk_campus)
            except Exception as e:
                messages.error(
                    request, 'Erro ao tentar editar a imagem. Tente novamente mais tarde.')
                status_code = 400
        else:
            messages.error(
                request, 'Erro ao tentar editar a imagem. Verifique se todos campos foram preenchidos corretamente.')
            status_code = 400
    else:
        form = FormImagem(instance=imagem)

    return render(request, 'cadastros/imagens/cadastro.html', {
        'tipo': 'Edição', 'form': form
    }, status=status_code)


@login_required
def deletar_imagem(request, pk, pk_campus):
    imagem = get_object_or_404(Imagem, pk=pk)

    try:
        imagem.delete()
        messages.success(request, 'Imagem deletada com sucesso.')
    except:
        messages.error(
            request, 'Erro ao tentar deletar a imagem. Tente novamente mais tarde.')

    return redirect('cadastros:detalhes_campus', pk_campus)