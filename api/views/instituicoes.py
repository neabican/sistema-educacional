from rest_framework.decorators import api_view
from rest_framework.response import Response
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