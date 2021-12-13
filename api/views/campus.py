from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..serializers import CampusSerializer
from cadastros.models import *
from cadastros.views.utilitarios import gerar_paginacao

@api_view(['GET'])
def listar_campus(request):
  if request.method == 'GET':
    campus = Campus.objects.all()

    serializador = CampusSerializer(campus, many=True)

    return Response(serializador.data)