from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from ..models import Curso
from .utilitarios import gerar_paginacao

@login_required
def cursos(request):
  if request.method == 'POST':
    pk = request.POST.get('pk', None)

    if pk is not None:
      try:
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