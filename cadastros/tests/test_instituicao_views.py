from django.test import TestCase, RequestFactory
from django.urls import reverse

from cadastros.models import Instituicao
from cadastros.views.instituicoes import instituicoes
from .test_usuario import criar_usuario

class InstituicaoTestCase(TestCase):
  def setUp(self):
    self.factory = RequestFactory()
    self.user = criar_usuario('teste@ifsc.edu.br')

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
    request = self.factory.post(reverse('cadastros:instituicoes'), dados)
    request.user = self.user
    request.POST = request.POST.copy()

    # Criando uma nova instituição
    response = instituicoes(request)
    self.assertIs(response.status_code, 200)

    # Tentando criar uma instituição com o nome repetido
    # response = instituicoes(request, {'nome': 'Instituto Federal de Santa Catarina'})
    # self.assertIs(response.status_code, 400)