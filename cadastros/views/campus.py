from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Campus, Programa, Projeto, AcaoAfirmativa, CursoCampus
from ..forms import FormCampus, FormEndereco, FormCursoCampus
from .utilitarios import gerar_paginacao


@login_required
def campus(request):
    status_code = 200

    if request.method == 'POST':
        try:
            pk = request.POST['pk']
            campus = Campus.objects.get(pk=pk)

            try:
                campus.delete()
                messages.success(request, 'Câmpus deletado com sucesso.')
            except:
                messages.error(request, 'Erro ao tentar deletar o câmpus. Tente novamente mais tarde.')
                status_code = 400
        except Campus.DoesNotExist:
            messages.error(request, 'Erro ao tentar deletar o câmpus. O câmpus não foi encontrado.')
            status_code = 404

    campus = Campus.objects.all().order_by('id')
    # Paginando resultados
    campus, paginas = gerar_paginacao(request, campus, 10)

    return render(request, 'cadastros/campus/listagem.html', {
        'lista_campus': campus, 'paginas': paginas
    }, status=status_code)


@login_required
def cadastrar_campus(request):
    form = FormCampus(request.POST or None)
    form_endereco = FormEndereco(request.POST or None)
    status_code = 200

    if request.method == 'POST':
        if form.is_valid() and form_endereco.is_valid():
            try:
                # Tenta buscar um câmpus com o mesmo nome que pertença à mesma instituição
                campus_repetido = Campus.objects.get(
                    nome=form.cleaned_data['nome'],
                    instituicao=form.cleaned_data['instituicao']
                )
                messages.error(request, 'Este câmpus desta instituição já foi cadastrado.')
                status_code = 400
            except:
                # Caso não seja um câmpus repetido, tenta cadastrá-lo
                try:
                    campus = form.save(commit=False)

                    try:
                        latitude, longitude = form_endereco.cleaned_data['coordenadas'].split(', ')
                    except:
                        messages.error(request, 'Erro ao tentar obter as coordenadas informadas.')
                        status_code = 400

                        return render(request, 'cadastros/campus/cadastro.html', {
                            'tipo': 'Cadastro', 'form': form, 'form_endereco': form_endereco
                        }, status=status_code)

                    endereco = form_endereco.save(commit=False)
                    endereco.latitude = latitude
                    endereco.longitude = longitude
                    endereco.save()

                    campus.endereco = endereco

                    arquivo_antigo = ''
                    campus.foto = request.FILES.get('foto')

                    campus.save(arquivo_antigo)
                    messages.success(request, 'Câmpus cadastrado com sucesso.')

                    return redirect('cadastros:campus')
                except:
                    messages.error(request, 'Erro ao tentar cadastrar o câmpus. Tente novamente mais tarde.')
                    status_code = 400
        else:
            messages.error(request,
                           'Erro ao tentar cadastrar o câmpus. Verifique se todos câmpus foram preenchidos corretamente.')
            status_code = 400

    return render(request, 'cadastros/campus/cadastro.html', {
        'tipo': 'Cadastro', 'form': form, 'form_endereco': form_endereco
    }, status=status_code)


@login_required
def editar_campus(request, pk):
    campus = get_object_or_404(Campus, pk=pk)
    status_code = 200

    if request.method == 'POST':
        form = FormCampus(request.POST, instance=campus)
        form_endereco = FormEndereco(request.POST, instance=campus.endereco)

        if form.is_valid() and form_endereco.is_valid():
            try:
                # Tenta buscar um câmpus com o mesmo nome que pertença à mesma instituição
                campus_repetido = Campus.objects.exclude(pk=pk).get(
                    nome=form.cleaned_data['nome'],
                    instituicao=form.cleaned_data['instituicao']
                )
                messages.error(request, 'Este câmpus desta instituição já foi cadastrado.')
                status_code = 400
            except:
                # Caso não seja um câmpus repetido, tenta cadastrá-lo
                try:
                    campus = form.save(commit=False)

                    try:
                        latitude, longitude = form_endereco.cleaned_data['coordenadas'].split(', ')
                    except:
                        messages.error(request, 'Erro ao tentar obter as coordenadas informadas.')
                        status_code = 400

                        return render(request, 'cadastros/campus/cadastro.html', {
                            'tipo': 'Cadastro', 'form': form, 'form_endereco': form_endereco
                        }, status=status_code)

                    endereco = form_endereco.save(commit=False)
                    endereco.latitude = latitude
                    endereco.longitude = longitude
                    endereco.save()

                    campus.endereco = endereco

                    arquivo_antigo = campus.foto

                    if request.FILES.get('foto') is not None:
                        campus.foto = request.FILES.get('foto')

                    campus.save(arquivo_antigo)
                    messages.success(request, 'Câmpus editado com sucesso.')

                    return redirect('cadastros:campus')
                except:
                    messages.error(request, 'Erro ao tentar editar o câmpus. Tente novamente mais tarde.')
                    status_code = 400
        else:
            messages.error(request,
                           'Erro ao tentar editar o câmpus. Verifique se todos câmpus foram preenchidos corretamente.')
            status_code = 400
    else:
        form = FormCampus(instance=campus)

        coordenadas = f'{str(campus.endereco.latitude)}, {str(campus.endereco.longitude)}'
        form_endereco = FormEndereco(
            instance=campus.endereco,
            initial={'coordenadas': coordenadas}
        )

    return render(request, 'cadastros/campus/cadastro.html', {
        'tipo': 'Edição', 'form': form, 'form_endereco': form_endereco
    }, status=status_code)


@login_required
def detalhes_campus(request, pk):
    campus = get_object_or_404(Campus, pk=pk)

    campus.programas = Programa.objects.filter(campus=campus)
    campus.projetos = Projeto.objects.filter(campus=campus)
    campus.acoes_afirmativas = AcaoAfirmativa.objects.filter(campus=campus)

    coordenadas = {
        'latitude': campus.endereco.latitude,
        'longitude': campus.endereco.longitude
    }

    return render(request, 'cadastros/campus/detalhes.html', {
        'campus': campus, 'coordenadas': coordenadas
    })


@login_required
def cadastrar_curso_campus(request, pk):
    form = FormCursoCampus(request.POST or None)
    campus = get_object_or_404(Campus, pk=pk)
    status_code = 200

    if request.method == 'POST':
        if form.is_valid():
            try:
                curso_repetido = campus.cursos.get(curso=form.cleaned_data['curso'])
                messages.error(request, 'Este curso já foi cadastrado neste câmpus.')
                status_code = 400
            except:
                try:
                    campus.cursos.add(form.save())
                    messages.success(request, 'Curso cadastrado com sucesso.')
                    return redirect('cadastros:detalhes_campus', campus.pk)
                except:
                    messages.error(request, 'Erro ao tentar cadastrar o curso. Tente novamente mais tarde.')
                    status_code = 400
        else:
            messages.error(request,
                           'Erro ao tentar cadastrar o curso. Verifique se todos campos foram preenchidos corretamente.')
            status_code = 400

    return render(request, 'cadastros/cursos_campus/cadastro.html', {
        'tipo': 'Cadastro', 'form': form
    }, status=status_code)


@login_required
def editar_curso_campus(request, pk, pk_campus):
    curso = get_object_or_404(CursoCampus, pk=pk)
    campus = get_object_or_404(Campus, pk=pk_campus)
    status_code = 200

    if request.method == 'POST':
        form = FormCursoCampus(request.POST, instance=curso)

        if form.is_valid():
            try:
                curso_repetido = campus.cursos.exclude(pk=pk).get(curso=form.cleaned_data['curso'])
                messages.error(request, 'Este curso já foi cadastrado neste câmpus.')
                status_code = 400
            except:
                try:
                    campus.cursos.add(form.save())
                    messages.success(request, 'Curso editado com sucesso.')
                    return redirect('cadastros:detalhes_campus', campus.pk)
                except:
                    messages.error(request, 'Erro ao tentar editar o curso. Tente novamente mais tarde.')
                    status_code = 400
        else:
            messages.error(request,
                           'Erro ao tentar editar o curso. Verifique se todos campos foram preenchidos corretamente.')
            status_code = 400
    else:
        form = FormCursoCampus(instance=curso)

    return render(request, 'cadastros/cursos_campus/cadastro.html', {
        'tipo': 'Edição', 'form': form
    }, status=status_code)


@login_required
def deletar_curso_campus(request, pk, pk_campus):
    curso = get_object_or_404(CursoCampus, pk=pk)

    try:
        curso.delete()
        messages.success(request, 'Curso deletado com sucesso.')
    except:
        messages.error(request, 'Erro ao tentar deletar o curso. Tente novamente mais tarde.')

    return redirect('cadastros:detalhes_campus', pk_campus)
