from django.test import TestCase
from django.db.utils import IntegrityError

from cadastros.models import *

class InstituicaoTestCase(TestCase):
  def setUp(self):
    Instituicao.objects.create(nome='Instituto Federal de Santa Catarina')
    Instituicao.objects.create(nome='Instituto Federal do Paraná')

  def test_instituicao_attrs(self):
    instituicoes = Instituicao.objects.all().count()
    self.assertIs(instituicoes, 2)

    # # Verificando se ele impede o cadastro de uma
    # # instituição com o nome repetido
    # self.assertRaises(IntegrityError, Instituicao.objects.create(nome='Instituto Federal de Santa Catarina'))
    # self.assertRaises(IntegrityError, Instituicao.objects.create(nome='Instituto Federal do Paraná'))

    Instituicao.objects.create(nome='Universidade Federal de Santa Catarina')

    # Contando as instituições que possuem
    # 'Santa Catarina' no nome
    instituicoes_sc = Instituicao.objects.filter(nome__contains='Santa Catarina').count()
    self.assertIs(instituicoes_sc, 2)

class CursoTestCase(TestCase):
  def setUp(self):
    Curso.objects.create(nome='Medicina', descricao='Ajude a salvar vidas')
    Curso.objects.create(nome='Direito', descricao='Faça a justiça valer')
    Curso.objects.create(nome='Agronomia', descricao='Cuide de sua fazenda da maneira correta')

  def test_curso_attrs(self):
    cursos = Curso.objects.all().count()
    self.assertIs(cursos, 3)

    curso = Curso.objects.get(nome='Medicina')
    self.assertEqual(curso.descricao, 'Ajude a salvar vidas')
    curso = Curso.objects.get(nome='Direito')
    self.assertEqual(curso.descricao, 'Faça a justiça valer')
    curso = Curso.objects.get(nome='Agronomia')
    self.assertNotEqual(curso.descricao, 'Descrição errada')

    # # Verificando se ele impede o cadastro de um
    # # curso com o nome repetido
    # self.assertRaises(IntegrityError, Curso.objects.create(nome='Medicina', descricao='Descrição diferente'))
    # self.assertRaises(IntegrityError, Curso.objects.create(nome='Agronomia', descricao='Descrição diferente'))

class EnderecoTestCase(TestCase):
  def setUp(self):
    Endereco.objects.create(
      cidade='Canoinhas',
      estado='Santa Catarina',
      logradouro='Avenida dos Expedicionários',
      numero='2150',
      latitude=-26.18393397322644,
      longitude=-50.36807243859915
    )

  def test_endereco_attrs(self):
    enderecos = Endereco.objects.all().count()
    self.assertIs(enderecos, 1)

    Endereco.objects.create(
      cidade='Tubarão',
      estado='Santa Catarina',
      logradouro='Rua Deputado Olices Pedro de Caldas',
      numero='480',
      latitude=-28.474168469891794,
      longitude=-49.02507087906978
    )

    Endereco.objects.create(
      cidade='Canoas',
      estado='Rio Grande do Sul',
      logradouro='Rua Dra. Maria Zélia Carneiro de Figueredo',
      numero='870',
      latitude=-29.899663865619075,
      longitude=-51.15002978883284
    )

    # Contando os endereços que são
    # do estado 'Santa Catarina'
    enderecos_sc = Endereco.objects.filter(estado='Santa Catarina').count()
    self.assertIs(enderecos_sc, 2)

    # Contando os endereços que são
    # do estado 'Rio Grande do Sul'
    enderecos_rs = Endereco.objects.filter(estado='Rio Grande do Sul').count()
    self.assertIs(enderecos_rs, 1)

    enderecos = Endereco.objects.all().count()
    self.assertIs(enderecos, 3)

class CampusTestCase(TestCase):
  fixtures = [
    'instituicoes',
    'enderecos'
  ]

  def setUp(self):
    Campus.objects.create(
      nome='Câmpus Canoinhas',
      instituicao=Instituicao.objects.get(pk=1),
      endereco=Endereco.objects.get(pk=1)
    )

    Campus.objects.create(
      nome='Câmpus Tubarão',
      instituicao=Instituicao.objects.get(pk=1),
      endereco=Endereco.objects.get(pk=2)
    )

  def test_campus_attrs(self):
    campus = Campus.objects.all().count()
    self.assertIs(campus, 2)

    Campus.objects.create(
      nome='Câmpus Canoas',
      instituicao=Instituicao.objects.get(pk=2),
      endereco=Endereco.objects.get(pk=4)
    )

    campus = Campus.objects.all().count()
    self.assertIs(campus, 3)

    # Contando os câmpus que pertencem à instituicão
    # 'Instituto Federal de Santa Catarina'
    campus_ifsc = Campus.objects.filter(instituicao__nome='Instituto Federal de Santa Catarina').count()
    self.assertIs(campus_ifsc, 2)

    # Testando se os campos foram cadastrados de
    # forma correta
    campus_canoinhas = Campus.objects.get(
      nome='Câmpus Canoinhas', 
      instituicao__nome='Instituto Federal de Santa Catarina'
    )
    self.assertEqual(campus_canoinhas.nome, 'Câmpus Canoinhas')
    self.assertEqual(campus_canoinhas.endereco.logradouro, 'Avenida dos Expedicionários')
    self.assertEqual(campus_canoinhas.endereco.estado, 'Santa Catarina')

class ProgramaTestCase(TestCase):
  fixtures = [
    'instituicoes',
    'enderecos',
    'campus'
  ]

  def setUp(self):
    Programa.objects.create(
      nome='Programa 1',
      descricao='Imagine uma descrição incrível aqui...',
      campus=Campus.objects.get(pk=1)
    )
    
    Programa.objects.create(
      nome='Programa 2',
      descricao='Imagine uma descrição incrível aqui...',
      campus=Campus.objects.get(pk=1)
    )

    Programa.objects.create(
      nome='Programa 3',
      descricao='Imagine uma descrição incrível aqui...',
      campus=Campus.objects.get(pk=2)
    )

  def test_programa_attrs(self):
    programas = Programa.objects.all().count()
    self.assertIs(programas, 3)

    # Buscando os programas do 'Câmpus Canoinhas'
    # da instituição 'Instituto Federal de Santa Catarina'
    prog_canoinhas = Programa.objects.filter(
      campus__nome='Câmpus Canoinhas',
      campus__instituicao__nome='Instituto Federal de Santa Catarina'
    ).count()
    self.assertIs(prog_canoinhas, 2)

    Programa.objects.create(
      nome='Programa 4',
      descricao='Um programa responsável por distribuir alimento para os alunos',
      campus=Campus.objects.get(pk=3)
    )

    programas = Programa.objects.all().count()
    self.assertIs(programas, 4)

    prog_4 = Programa.objects.get(nome='Programa 4', campus__pk=3)
    self.assertEqual(prog_4.descricao, 'Um programa responsável por distribuir alimento para os alunos')
    self.assertEqual(prog_4.campus.nome, 'Câmpus Telêmaco Borba')