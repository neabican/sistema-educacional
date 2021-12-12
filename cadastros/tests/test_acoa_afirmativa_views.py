from django.test import TestCase, TransactionTestCase, RequestFactory, Client
from django.urls import reverse

from cadastros.models import AcaoAfirmativa, Campus
from cadastros.views.acoes_afirmativas import *
from .test_usuario import criar_usuario

class AcaoAfirmativaTestCase(TransactionTestCase):
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

    AcaoAfirmativa.objects.create(
      nome='Ação Afirmativa 1',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

  def test_cadastrar_acao_afirmativa(self):
    dados = {
      'nome': 'Ação Afirmativa 2',
      'descricao': 'Outra descrição maneira...',
      'link': 'https://www.google.com.br'
    }

    # Cadastrando uma ação afirmativa em um câmpus
    response = self.client.post(reverse(
      'cadastros:cadastrar_acao_afirmativa',
      kwargs={'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 302)
    self.assertIs(AcaoAfirmativa.objects.all().count(), 2)

    # Tentando cadastrar uma ação afirmativa repetido em câmpus
    response = self.client.post(reverse(
      'cadastros:cadastrar_acao_afirmativa',
      kwargs={'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 400)
    self.assertIs(AcaoAfirmativa.objects.all().count(), 2)

    dados = {
      'nome': 'Ação Afirmativa 1',
      'descricao': 'Outra descrição maneira...',
      'link': 'https://www.youtube.com.br'
    }

    # Tentando cadastrar uma ação afirmativa em câmpus inexistente
    response = self.client.post(reverse(
      'cadastros:cadastrar_acao_afirmativa',
      kwargs={'pk_campus': 999}
    ), dados)
    self.assertEqual(response.status_code, 404)
    self.assertIs(AcaoAfirmativa.objects.all().count(), 2)

  def test_editar_acao_afirmativa(self):
    acao_afirmativa = AcaoAfirmativa.objects.create(
      nome='Ação Afirmativa 2',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    dados = {
      'nome': 'Ação Afirmativa 50',
      'descricao': 'Uma ação afirmativa diferente...',
      'link': 'https://www.linkatualizado.com.br'
    }

    # Editando uma ação afirmativa de um câmpus
    response = self.client.post(reverse(
      'cadastros:editar_acao_afirmativa',
      kwargs={'pk': acao_afirmativa.pk, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 302)

    AcaoAfirmativa.objects.create(
      nome='Ação Afirmativa 10',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    dados = {
      'nome': 'Ação Afirmativa 10',
      'descricao': 'Uma ação afirmativa diferente...',
      'link': 'https://www.linkatualizado.com.br'
    }

    # Tentando editar uma ação afirmativa repetido em um câmpus
    response = self.client.post(reverse(
      'cadastros:editar_acao_afirmativa',
      kwargs={'pk': acao_afirmativa.pk, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 400)

    # Tentando editar uma ação afirmativa inexistente
    response = self.client.post(reverse(
      'cadastros:editar_acao_afirmativa',
      kwargs={'pk': 999, 'pk_campus': 1}
    ), dados)
    self.assertEqual(response.status_code, 404)

    # Tentando editar uma ação afirmativa de um câmpus inexistente
    response = self.client.post(reverse(
      'cadastros:editar_acao_afirmativa',
      kwargs={'pk': acao_afirmativa.pk, 'pk_campus': 999}
    ), dados)
    self.assertEqual(response.status_code, 404)

  def test_deletar_acao_afirmativa(self):
    acao_afirmativa = AcaoAfirmativa.objects.create(
      nome='Ação Afirmativa 10',
      descricao='Uma descrição bem legal!',
      campus=Campus.objects.get(pk=1)
    )

    # Deletando uma ação afirmativa de um câmpus
    response = self.client.post(reverse(
      'cadastros:deletar_acao_afirmativa',
      kwargs={'pk': acao_afirmativa.pk, 'pk_campus': 1}
    ))
    self.assertEqual(response.status_code, 302)

    # Tentando deletar uma ação afirmativa inexistente
    response = self.client.post(reverse(
      'cadastros:deletar_acao_afirmativa',
      kwargs={'pk': 999, 'pk_campus': 1}
    ))
    self.assertEqual(response.status_code, 404)