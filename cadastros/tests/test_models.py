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