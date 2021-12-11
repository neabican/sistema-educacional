from django.test import TestCase, TransactionTestCase, RequestFactory, client
from django.urls import reverse
from django.test import Client

from cadastros.models import Curso
from cadastros.views.cursos import *
from .test_usuario import criar_usuario

class CursoTestCase(TransactionTestCase):
  def setUp(self):
    self.factory = RequestFactory()
    self.user = criar_usuario('teste@ifsc.edu.br')
    self.client = Client()
    self.client.login(username='teste@ifsc.edu.br', password='teste123')

    Curso.objects.create(nome='Medicina', descricao='Uma descrição sobre medicina...')
    Curso.objects.create(nome='Direito', descricao='Uma descrição sobre direito...')

  def test_listar_cursos(self):
    response = self.client.get(reverse('cadastros:cursos'))
    self.assertEqual(response.status_code, 200)

  def test_cadastrar_curso(self):
    dados = {
      'nome': 'Agronomia',
      'descricao': 'Uma descrição sobre agronomia...'
    }

    response = self.client.post(reverse('cadastros:cadastrar_curso'), dados)
    self.assertEqual(response.status_code, 302)
    self.assertIs(Curso.objects.all().count(), 3)

    dados = {
      'nome': 'Medicina',
      'descricao': 'Outra descrição sobre medicina...'
    }

    # Tentando cadastrar um curso repetido
    response = self.client.post(reverse('cadastros:cadastrar_curso'), dados)
    self.assertEqual(response.status_code, 400)
    self.assertIs(Curso.objects.all().count(), 3)

  def test_editar_curso(self):
    curso = Curso.objects.get(nome='Medicina')
    dados = {
      'nome': 'Medicina Veterinária',
      'descricao': curso.descricao
    }

    # Editando somente o nome do curso
    response = self.client.post(
      reverse('cadastros:editar_curso', kwargs={'pk': curso.pk}), dados
    )
    self.assertEqual(response.status_code, 302)

    dados = {
      'nome': curso.nome,
      'descricao': 'Uma descrição bem legal!'
    }

    # Editando somente a descrição do curso
    response = self.client.post(
      reverse('cadastros:editar_curso', kwargs={'pk': curso.pk}), dados
    )
    self.assertEqual(response.status_code, 302)

    dados = {
      'nome': 'Direito',
      'descricao': curso.descricao
    }

    # Tentando editar um curso com um nome já existente
    response = self.client.post(
      reverse('cadastros:editar_curso', kwargs={'pk': curso.pk}), dados
    )
    self.assertEqual(response.status_code, 400)

  def test_deletar_curso(self):
    curso = Curso.objects.get(nome='Direito')
    dados = {'pk': curso.pk}

    response = self.client.post(reverse('cadastros:cursos'), dados)
    self.assertEqual(response.status_code, 200)
    self.assertIs(Curso.objects.all().count(), 1)

    # Tentando deletar um curso inexistente
    response = self.client.post(reverse('cadastros:cursos'), dados)
    self.assertEqual(response.status_code, 404)
    self.assertIs(Curso.objects.all().count(), 1)