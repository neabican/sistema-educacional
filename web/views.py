from django.shortcuts import render, get_object_or_404
from json import dumps

from cadastros.models import Campus, Programa, Projeto, AcaoAfirmativa

def listar_campus(request):
  return render(request, 'web/listar_campus.html')

def detalhes_campus(request, pk):
  campus = get_object_or_404(Campus, pk=pk)

  programas = Programa.objects.filter(campus=campus)
  projetos = Projeto.objects.filter(campus=campus)
  acoes_afirmativas = AcaoAfirmativa.objects.filter(campus=campus)

  coordenadas = {
    'latitude': campus.endereco.latitude,
    'longitude': campus.endereco.longitude
  }
  
  return render(request, 'web/detalhes_campus.html', {
    'campus': campus, 'programas': programas,
    'projetos': projetos, 'acoes_afirmativas': acoes_afirmativas,
    'coordenadas': coordenadas
  })