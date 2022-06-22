from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..serializers import ProjetoSerializer
from cadastros.models import *

@api_view(['GET'])
def listar_projetos(request, pk_campus):
  if request.method == 'GET':
    projetos = Projeto.objects.filter(campus__pk=pk_campus)
    serializador = ProjetoSerializer(projetos, many=True)

    return Response(serializador.data)

@api_view(['GET'])
def detalhes_projeto(request, pk, pk_campus):
  if request.method == 'GET':
    try:
      projeto = Projeto.objects.get(pk=pk, campus__pk=pk_campus)
      serializador = ProjetoSerializer(projeto)

      return Response(serializador.data)
    except:
      return Response(None, status=404)
    
