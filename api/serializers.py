from rest_framework import serializers
from cadastros.models import *

class InstituicaoSerializer(serializers.Serializer):
  pk = serializers.IntegerField()
  nome = serializers.CharField(max_length=250)

class EnderecoSerializer(serializers.Serializer):
  cidade = serializers.CharField(max_length=100)
  estado = serializers.CharField(max_length=50)
  logradouro = serializers.CharField(max_length=300)
  numero = serializers.CharField(max_length=10)
  cep = serializers.CharField(max_length=10)
  latitude = serializers.DecimalField(max_digits=22, decimal_places=16)
  longitude = serializers.DecimalField(max_digits=22, decimal_places=16)

class CursoSerializer(serializers.Serializer):
  nome = serializers.CharField(max_length=250)
  descricao = serializers.CharField()

class CursoCampusSerializer(serializers.Serializer):
  curso = CursoSerializer()
  link = serializers.CharField(max_length=500)

class CampusSerializer(serializers.Serializer):
  pk = serializers.IntegerField()
  nome = serializers.CharField(max_length=300)
  instituicao = InstituicaoSerializer()
  endereco = EnderecoSerializer()
  cursos = CursoCampusSerializer(many=True)

class ProgramaSerializer(serializers.ModelSerializer):
  class Meta:
    model = Programa
    fields = [
      'pk', 'nome', 'descricao', 
      'link', 'campus'
    ]

class ProjetoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Projeto
    fields = [
      'pk', 'nome', 'descricao', 
      'link', 'campus'
    ]

class AcaoAfirmativaSerializer(serializers.ModelSerializer):
  class Meta:
    model = AcaoAfirmativa
    fields = [
      'pk', 'nome', 'descricao', 
      'link', 'campus'
    ]