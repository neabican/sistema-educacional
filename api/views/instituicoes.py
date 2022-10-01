from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..serializers import InstituicaoSerializer
from cadastros.models import *

@api_view(['GET'])
def listar_instituicoes(request):
  if request.method == 'GET':
    instituicao = Instituicao.objects.all()

    if request.GET.get('pag') != None:
      pag_atual = int(request.GET.get('pag')) * 10
      instituicao = instituicao[pag_atual:pag_atual+10]

    serializador = InstituicaoSerializer(instituicao, many=True)
    return Response(serializador.data)