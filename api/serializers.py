from rest_framework import serializers
from cadastros.models import *

class InstituicaoSerializer(serializers.ModelSerializer):
  campus = serializers.SerializerMethodField()

  def get_campus(self, obj):
    return CampusSerializerSemInstituicao(Campus.objects.filter(instituicao=obj), many=True).data

  class Meta:
    model = Instituicao
    fields = ['pk', 'nome', 'sigla', 'campus']

class CursoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Curso
    fields = ['pk', 'nome', 'descricao']

class CursoCampusSerializer(serializers.ModelSerializer):
  curso = CursoSerializer()

  class Meta:
    model = CursoCampus
    fields = ['pk', 'link', 'vagas', 'descricao', 'curso']

class EnderecoSerializer(serializers.ModelSerializer):
  class Meta:
    model = Endereco
    fields = [
      'pk', 'cidade', 'estado', 'logradouro',
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
      'pk', 'nome', 'foto', 'instituicao',
      'endereco', 'cursos', 'programas',
      'projetos', 'acoes_afirmativas',
    ]

class CampusSerializerSemInstituicao(serializers.ModelSerializer):
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
      'pk', 'nome', 'foto', 'link', 'instituicao',
      'endereco', 'descricao', 'cursos', 'programas',
      'projetos', 'acoes_afirmativas',
    ]
