from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from ..models import Campus
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