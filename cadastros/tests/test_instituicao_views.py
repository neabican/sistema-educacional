from django.test import TestCase, TransactionTestCase, RequestFactory, client
from django.urls import reverse
from django.test import Client

from cadastros.models import Instituicao, Campus, Endereco
from cadastros.views.instituicoes import instituicoes
from .test_usuario import criar_usuario

class InstituicaoTestCase(TransactionTestCase):
  fixtures = ['enderecos']

  def setUp(self):
    self.factory = RequestFactory()
    self.user = criar_usuario('teste@ifsc.edu.br')
    self.client = Client()
    self.client.login(username='teste@ifsc.edu.br', password='teste123')

    Instituicao.objects.create(nome='Instituto Federal de Santa Catarina')
    Instituicao.objects.create(nome='Universidade Federal de Santa Catarina')

  def test_listar_instituicoes(self):
    # Criando uma requesição GET na rota 'instituicoes'
    request = self.factory.get(reverse('cadastros:instituicoes'))
    request.user = self.user
    request.GET = request.GET.copy()

    response = instituicoes(request)

    self.assertIs(response.status_code, 200)

  def test_cadastrar_instituicao(self):
    dados = {'nome': 'Instituto Federal do Paraná'}

    # Criando uma requesição POST na rota 'instituicoes'
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    self.assertEqual(response.status_code, 201)

    # Tentando criar uma instituição com o nome repetido
    dados = {'nome': 'Instituto Federal de Santa Catarina'}
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    self.assertEqual(response.status_code, 400)
    self.assertIs(Instituicao.objects.all().count(), 3)

  def test_editar_instituicao(self):
    # Buscando por uma instituição
    instituicao = Instituicao.objects.get(nome='Instituto Federal de Santa Catarina')

    dados = {'nome': 'Instituto Federal do Rio Grande do Sul', 'pk': instituicao.pk}

    # Editando uma instituição
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    self.assertEqual(response.status_code, 201)

    dados = {'nome': 'Instituto Federal do Rio Grande do Sul', 'pk': instituicao.pk}

    # Editando uma instituição, mas colocando o mesmo nome
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    self.assertEqual(response.status_code, 201)

    dados = {'nome': 'Universidade Federal de Santa Catarina', 'pk': instituicao.pk}

    # Tentando editar uma instituição com um nome já existente
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    self.assertEqual(response.status_code, 400)

  def test_deletar_instituicoes(self):
    # Buscando por uma instituição
    instituicao = Instituicao.objects.get(nome='Universidade Federal de Santa Catarina')

    dados = {'pk': instituicao.pk}

    # Deletando uma instituição
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    self.assertEqual(response.status_code, 200)
    self.assertIs(Instituicao.objects.all().count(), 1)

    # Tentando deletar um instituição inexistente
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    self.assertEqual(response.status_code, 404)

    # Adicionando um câmpus à instituição
    instituicao = Instituicao.objects.get(nome='Instituto Federal de Santa Catarina')
    Campus.objects.create(
      nome='Câmpus Canoinhas',
      instituicao=instituicao,
      endereco=Endereco.objects.get(pk=1)
    )

    dados = {'pk': instituicao.pk}

    # Tentando deletar uma instituição que possui relação 
    # com um ou mais câmpus
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    self.assertEqual(response.status_code, 400)
    self.assertIs(Instituicao.objects.all().count(), 1)