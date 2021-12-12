from django.test import TestCase, TransactionTestCase, RequestFactory, Client
from django.urls import reverse

from cadastros.models import Programa, Campus
from cadastros.views.programas import *
from .test_usuario import criar_usuario

class ProgramaTestCase(TransactionTestCase):
  fixtures = [
    'instituicoes',
    'enderecos',
    'campus'
  ]

  def setUp(self):
    self.factory = RequestFactory()
    self.user = criar_usuario('teste@ifsc.edu.br')
    self.client = Client()
    self.client.login(username='teste@ifsc.edu.br', password='teste123')

    Programa.objects.create(
      nome='Programa 1',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

  def test_cadastrar_programa(self):
    dados = {
      'nome': 'Programa 2',
      'descricao': 'Outra descrição maneira...',
      'link': 'https://www.google.com.br'
    }

    # Cadastrando um programa em câmpus
    response = self.client.post(reverse(
      'cadastros:cadastrar_programa',
      kwargs={'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 302)
    self.assertIs(Programa.objects.all().count(), 2)

    # Tentando cadastrar um programa repetido em câmpus
    response = self.client.post(reverse(
      'cadastros:cadastrar_programa',
      kwargs={'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 400)
    self.assertIs(Programa.objects.all().count(), 2)

    dados = {
      'nome': 'Programa 1',
      'descricao': 'Outra descrição maneira...',
      'link': 'https://www.youtube.com.br'
    }

    # Tentando cadastrar um programa em câmpus inexistente
    response = self.client.post(reverse(
      'cadastros:cadastrar_programa',
      kwargs={'pk_campus': 999}
    ), dados)
    self.assertEqual(response.status_code, 404)
    self.assertIs(Programa.objects.all().count(), 2)

  def test_editar_programa(self):
    programa = Programa.objects.create(
      nome='Programa 2',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    dados = {
      'nome': 'Programa 50',
      'descricao': 'Um programa diferente...',
      'link': 'https://www.linkatualizado.com.br'
    }

    # Editando um programa de um câmpus
    response = self.client.post(reverse(
      'cadastros:editar_programa',
      kwargs={'pk': programa.pk, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 302)

    Programa.objects.create(
      nome='Programa 10',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    dados = {
      'nome': 'Programa 10',
      'descricao': 'Um programa diferente...',
      'link': 'https://www.linkatualizado.com.br'
    }

    # Tentando editar um programa repetido em um câmpus
    response = self.client.post(reverse(
      'cadastros:editar_programa',
      kwargs={'pk': programa.pk, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 400)

    # Tentando editar um programa inexistente
    response = self.client.post(reverse(
      'cadastros:editar_programa',
      kwargs={'pk': 999, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 404)

    # Tentando editar um programa de um câmpus inexistente
    response = self.client.post(reverse(
      'cadastros:editar_programa',
      kwargs={'pk': programa.pk, 'pk_campus': 999}
    ), dados)
    self.assertEqual(response.status_code, 404)

  def test_deletar_programa(self):
    programa = Programa.objects.create(
      nome='Programa 10',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    # Deletando um programa de um câmpus
    response = self.client.post(reverse(
      'cadastros:deletar_programa',
      kwargs={'pk': programa.pk, 'pk_campus': 1}
    ))
    self.assertEqual(response.status_code, 302)

    # Tentando deletar um programa inexistente
    response = self.client.post(reverse(
      'cadastros:deletar_programa',
      kwargs={'pk': 999, 'pk_campus': 1}
    ))
    self.assertEqual(response.status_code, 404)