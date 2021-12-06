from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Curso
from ..forms import FormCurso
from .utilitarios import gerar_paginacao

@login_required
def cursos(request):
  if request.method == 'POST':
    try:
      pk = request.POST['pk']
      curso = Curso.objects.get(pk=pk)

      try:
        curso.delete()
        messages.success(request, 'Curso deletado com sucesso.')
      except:
        messages.error(request, 'Erro ao tentar deletar o curso. Tente novamente mais tarde.')  
    except Curso.DoesNotExist:
      messages.error(request, 'Erro ao tentar deletar o curso. O curso não foi encontrado.')

  cursos = Curso.objects.all().order_by('id')
  # Paginando resultados
  cursos, paginas = gerar_paginacao(request, cursos, 10)

  return render(request, 'cadastros/cursos/listagem.html', {
    'cursos': cursos, 'paginas': paginas
  })

@login_required
def cadastrar_curso(request):
  form = FormCurso(request.POST or None)

  if request.method == 'POST':
    if form.is_valid():
      try:
        form.save()
        messages.success(request, 'Curso cadastrado com sucesso.')
        return redirect('cadastros:cursos')
      except:
        messages.error(request, 'Este curso já foi cadastrado.')
    else:
      messages.error(request, 'Erro ao tentar cadastrar o curso. Verifique se todos campos foram preenchidos corretamente.')

  return render(request, 'cadastros/cursos/cadastro.html', {
    'tipo': 'Cadastro', 'form': form
  })