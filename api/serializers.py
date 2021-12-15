from rest_framework import serializers
from cadastros.models import *

class InstituicaoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Instituicao
    fields = ['pk', 'nome']

class CursoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Curso
    fields = ['nome', 'descricao']

class CursoCampusSerializer(serializers.ModelSerializer):
  curso = CursoSerializer()

  class Meta:
    model = CursoCampus
    fields = ['pk', 'link', 'curso']

class EnderecoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Endereco
    fields = [
      'cidade', 'estado', 'logradouro',
      'numero', 'cep', 'latitude', 'longitude',
    ]

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

class CampusSerializer(serializers.Serializer):
  pk = serializers.IntegerField()
  nome = serializers.CharField(max_length=300)
  instituicao = InstituicaoSerializer()
  endereco = EnderecoSerializer()
  cursos = CursoCampusSerializer(many=True)