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

class CampusSerializer(serializers.ModelSerializer):
  instituicao = InstituicaoSerializer()
  endereco = EnderecoSerializer()
  cursos = CursoCampusSerializer(many=True)
  programas = serializers.SerializerMethodField()
  projetos = serializers.SerializerMethodField()
  acoes_afirmativas = serializers.SerializerMethodField()

  def get_programas(self, obj):
    return ProgramaSerializer(Programa.objects.filter(campus=obj), many=True).data

  def get_projetos(self, obj):
    return ProjetoSerializer(Projeto.objects.filter(campus=obj), many=True).data

  def get_acoes_afirmativas(self, obj):
    return AcaoAfirmativaSerializer(AcaoAfirmativa.objects.filter(campus=obj), many=True).data

  class Meta:
    model = Campus
    fields = [
      'pk', 'nome', 'instituicao',
      'endereco', 'cursos', 'programas',
      'projetos', 'acoes_afirmativas',
    ]
