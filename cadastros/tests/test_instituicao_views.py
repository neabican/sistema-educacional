from django.test import TestCase, TransactionTestCase, RequestFactory, client
from django.urls import reverse
from django.test import Client

from cadastros.models import Instituicao
from cadastros.views.instituicoes import instituicoes
from .test_usuario import criar_usuario

class InstituicaoTestCase(TransactionTestCase):
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
    self.assertIs(response.status_code, 200)

    # Tentando criar uma instituição com o nome repetido
    dados = {'nome': 'Instituto Federal do Paraná'}
    response = self.client.post(reverse('cadastros:instituicoes'), dados)
    
    # O seu codigo retorno 200 mesmo se for com nome repetido. O que voce faz eh enviar uma message de erro
    # self.assertIs(response.status_code, 400)
    # Voce pode testar usando as mensagens, por exemplo:
    messages = list(response.context['messages'])
    # Voce pode criar uma constante com a string de erro na views.py e importar para verificar aqui
    # Outra sugestao eh mudar sua logica e forcar o status_code corretamente na view
    # Voce tambem pode verificar a quantidade de linhas (instituicoes) inseridas no banco


    # response = instituicoes(request, {'nome': 'Instituto Federal de Santa Catarina'})