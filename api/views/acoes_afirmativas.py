from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..serializers import AcaoAfirmativaSerializer
from cadastros.models import *

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listar_acoes_afirmativas(request, pk_campus):
  if request.method == 'GET':
    acoes_afirmativas = AcaoAfirmativa.objects.filter(campus__pk=pk_campus)
    serializador = AcaoAfirmativaSerializer(acoes_afirmativas, many=True)

    return Response(serializador.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detalhes_acao_afirmativa(request, pk, pk_campus):
  if request.method == 'GET':
    try:
      acao_afirmativa = AcaoAfirmativa.objects.get(pk=pk, campus__pk=pk_campus)
      serializador = AcaoAfirmativaSerializer(acao_afirmativa)

      return Response(serializador.data)
    except:
      return Response(None, status=404)
    