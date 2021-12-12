from django.test import TestCase, TransactionTestCase, RequestFactory, Client
from django.urls import reverse

from cadastros.models import Projeto, Campus
from cadastros.views.projetos import *
from .test_usuario import criar_usuario

class ProjetoTestCase(TransactionTestCase):
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

    Projeto.objects.create(
      nome='Projeto 1',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

  def test_cadastrar_projeto(self):
    dados = {
      'nome': 'Projeto 2',
      'descricao': 'Outra descrição maneira...',
      'link': 'https://www.google.com.br'
    }

    # Cadastrando um projeto em um câmpus
    response = self.client.post(reverse(
      'cadastros:cadastrar_projeto',
      kwargs={'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 302)
    self.assertIs(Projeto.objects.all().count(), 2)

    # Tentando cadastrar um projeto repetido em câmpus
    response = self.client.post(reverse(
      'cadastros:cadastrar_projeto',
      kwargs={'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 400)
    self.assertIs(Projeto.objects.all().count(), 2)

    dados = {
      'nome': 'Projeto 1',
      'descricao': 'Outra descrição maneira...',
      'link': 'https://www.youtube.com.br'
    }

    # Tentando cadastrar um projeto em câmpus inexistente
    response = self.client.post(reverse(
      'cadastros:cadastrar_projeto',
      kwargs={'pk_campus': 999}
    ), dados)
    self.assertEqual(response.status_code, 404)
    self.assertIs(Projeto.objects.all().count(), 2)

  def test_editar_projeto(self):
    projeto = Projeto.objects.create(
      nome='Projeto 2',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    dados = {
      'nome': 'Projeto 50',
      'descricao': 'Um projeto diferente...',
      'link': 'https://www.linkatualizado.com.br'
    }

    # Editando um projeto de um câmpus
    response = self.client.post(reverse(
      'cadastros:editar_projeto',
      kwargs={'pk': projeto.pk, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 302)

    Projeto.objects.create(
      nome='Projeto 10',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    dados = {
      'nome': 'Projeto 10',
      'descricao': 'Um projeto diferente...',
      'link': 'https://www.linkatualizado.com.br'
    }

    # Tentando editar um projeto repetido em um câmpus
    response = self.client.post(reverse(
      'cadastros:editar_projeto',
      kwargs={'pk': projeto.pk, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 400)

    # Tentando editar um projeto inexistente
    response = self.client.post(reverse(
      'cadastros:editar_projeto',
      kwargs={'pk': 999, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 404)

    # Tentando editar um projeto de um câmpus inexistente
    response = self.client.post(reverse(
      'cadastros:editar_projeto',
      kwargs={'pk': projeto.pk, 'pk_campus': 999}
    ), dados)
    self.assertEqual(response.status_code, 404)

  def test_deletar_projeto(self):
    projeto = Projeto.objects.create(
      nome='Projeto 10',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    # Deletando um projeto de um câmpus
    response = self.client.post(reverse(
      'cadastros:deletar_projeto',
      kwargs={'pk': projeto.pk, 'pk_campus': 1}
    ))
    self.assertEqual(response.status_code, 302)

    # Tentando deletar um projeto inexistente
    response = self.client.post(reverse(
      'cadastros:deletar_projeto',
      kwargs={'pk': 999, 'pk_campus': 1}
    ))
    self.assertEqual(response.status_code, 404)