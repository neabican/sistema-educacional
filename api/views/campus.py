from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..serializers import CampusSerializer
from cadastros.models import *

@api_view(['GET'])
def listar_campus(request):
  if request.method == 'GET':
    if 'campus' in request.GET:
      pesquisa = request.GET.get('campus')
      campus = Campus.objects.filter(
        Q(nome__icontains=pesquisa) |
        Q(instituicao__sigla__icontains=pesquisa) |
        Q(cursos__curso__nome__icontains=pesquisa)
      )
    else:
      campus = Campus.objects.all()

    if request.GET.get('pag') != None:
      pag_atual = int(request.GET.get('pag')) * 10
      campus = campus[pag_atual:pag_atual+10]

    serializador = CampusSerializer(campus, many=True)
    return Response(serializador.data)

@api_view(['GET'])
def detalhes_campus(request, pk):
  if request.method == 'GET':
    try:
      campus = Campus.objects.get(pk=pk)
      serializador = CampusSerializer(campus)

      return Response(serializador.data)
    except:
      return Response(None, status=404)