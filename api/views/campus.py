from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from ..serializers import CampusSerializer
from cadastros.models import *

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def listar_campus(request):
  if request.method == 'GET':
    if 'campus' in request.GET:
      campus = Campus.objects.filter(nome__contains=request.GET.get('campus'))
    else:
      campus = Campus.objects.all()

    serializador = CampusSerializer(campus, many=True)

    return Response(serializador.data)

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def detalhes_campus(request, pk):
  if request.method == 'GET':
    try:
      campus = Campus.objects.get(pk=pk)
      serializador = CampusSerializer(campus)

      return Response(serializador.data)
    except:
      return Response(None, status=404)