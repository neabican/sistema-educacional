from django.test import TestCase, TransactionTestCase, RequestFactory, client
from django.urls import reverse
from django.test import Client

from cadastros.models import Campus, Instituicao, Endereco, Curso
from cadastros.views.campus import *
from .test_usuario import criar_usuario

class CampusTestCase(TransactionTestCase):
  fixtures = [
    'instituicoes',
    'cursos',
    'enderecos'
  ]

  def setUp(self):
    self.factory = RequestFactory()
    self.user = criar_usuario('teste@ifsc.edu.br')
    self.client = Client()
    self.client.login(username='teste@ifsc.edu.br', password='teste123')

    Campus.objects.create(
      nome='Câmpus Canoinhas',
      instituicao=Instituicao.objects.get(pk=1),
      endereco=Endereco.objects.get(pk=1)
    )
    Campus.objects.create(
      nome='Câmpus Canoas',
      instituicao=Instituicao.objects.get(pk=2),
      endereco=Endereco.objects.get(pk=4)
    )

  def test_listar_campus(self):
    response = self.client.get(reverse('cadastros:campus'))
    self.assertEqual(response.status_code, 200)

  def test_cadastrar_campus(self):
    dados = {
      'nome': 'Câmpus Tubarão',
      'instituicao': 1,
      'cidade': 'Tubarão',
      'estado': 'SC',
      'logradouro': 'Rua Dep. Olices Pedro de Caldas',
      'numero': '480',
      'cep': '88704-296',
      'latitude': -28.47374409193984,
      'longitude': -49.02416965503321
    }

    # Cadastrando um câmpus
    response = self.client.post(reverse('cadastros:cadastrar_campus'), dados)
    self.assertEqual(response.status_code, 302)
    self.assertIs(Campus.objects.all().count(), 3)

    # Tentando cadastrar um câmpus repetido
    response = self.client.post(reverse('cadastros:cadastrar_campus'), dados)
    self.assertEqual(response.status_code, 400)
    self.assertIs(Campus.objects.all().count(), 3)

  def test_editar_campus(self):
    campus = Campus.objects.get(nome='Câmpus Canoinhas', instituicao__pk=1)

    dados = {
      'nome': 'Câmpus Florianópolis',
      'instituicao': 1,
      'cidade': 'Florianópolis',
      'estado': 'SC',
      'logradouro': 'Avenida Mauro Ramos',
      'numero': '950',
      'cep': '88020-300',
      'latitude': -27.594033124793164,
      'longitude': -48.5431253169986
    }

    # Editando um câmpus
    response = self.client.post(
      reverse('cadastros:editar_campus', kwargs={'pk': campus.pk}), dados
    )
    self.assertEqual(response.status_code, 302)

    # Tentando editar um câmpus inexistente
    response = self.client.post(
      reverse('cadastros:editar_campus', kwargs={'pk': 999}), dados
    )
    self.assertEqual(response.status_code, 404)

    dados = {
      'nome': 'Câmpus Canoas',
      'instituicao': 2,
      'cidade': 'Canoas',
      'estado': 'RS',
      'logradouro': 'Avenida Mauro Ramos',
      'numero': '950',
      'cep': '88020-300',
      'latitude': -27.594033124793164,
      'longitude': -48.5431253169986
    }

    # Tentando editar um câmpus com o nome repetido
    response = self.client.post(
      reverse('cadastros:editar_campus', kwargs={'pk': campus.pk}), dados
    )
    self.assertEqual(response.status_code, 400)

  def test_deletar_campus(self):
    campus = Campus.objects.get(nome='Câmpus Canoinhas', instituicao__pk=1)
    dados = {'pk': campus.pk}

    # Deletando um câmpus
    response = self.client.post(reverse('cadastros:campus'), dados)
    self.assertEqual(response.status_code, 200)

    # Tentando deletar um câmpus inexistente
    response = self.client.post(reverse('cadastros:campus'), dados)
    self.assertEqual(response.status_code, 404)

  def test_detalhes_campus(self):
    campus = Campus.objects.get(nome='Câmpus Canoinhas', instituicao__pk=1)

    # Buscando detalhes de um câmpus
    response = self.client.post(reverse('cadastros:detalhes_campus', kwargs={'pk': campus.pk}))
    self.assertEqual(response.status_code, 200)

    # Tentando buscar detalhes de um câmpus inexistente
    response = self.client.post(reverse('cadastros:detalhes_campus', kwargs={'pk': 999}))
    self.assertEqual(response.status_code, 404)

  def test_cadastrar_curso_campus(self):
    campus = Campus.objects.get(nome='Câmpus Canoinhas', instituicao__pk=1)

    dados = {
      'curso': 1,
      'link': 'https://google.com.br',
    }

    # Cadastrando um curso no câmpus
    response = self.client.post(
      reverse('cadastros:cadastrar_curso_campus', kwargs={'pk': campus.pk}), dados
    )
    self.assertEqual(response.status_code, 302)
    self.assertIs(CursoCampus.objects.all().count(), 1)

    # Tentando cadastrar um curso repetido no mesmo câmpus
    response = self.client.post(
      reverse('cadastros:cadastrar_curso_campus', kwargs={'pk': campus.pk}), dados
    )
    self.assertEqual(response.status_code, 400)
    self.assertIs(CursoCampus.objects.all().count(), 1)

    dados = {
      'curso': 2,
      'link': 'https://google.com.br',
    }

    # Tentando cadastrar um curso em um câmpus inexistente
    response = self.client.post(
      reverse('cadastros:cadastrar_curso_campus', kwargs={'pk': 999}), dados
    )
    self.assertEqual(response.status_code, 404)
    self.assertIs(CursoCampus.objects.all().count(), 1)
    
    dados = {
      'curso': 999,
      'link': 'https://google.com.br',
    }

    # Tentando cadastrar um curso inexistente em um câmpus
    response = self.client.post(
      reverse('cadastros:cadastrar_curso_campus', kwargs={'pk': campus.pk}), dados
    )
    self.assertEqual(response.status_code, 400)
    self.assertIs(CursoCampus.objects.all().count(), 1)

  def test_editar_curso_campus(self):
    campus = Campus.objects.get(nome='Câmpus Canoinhas', instituicao__pk=1)
    curso_campus = CursoCampus.objects.create(
      curso=Curso.objects.get(pk=1), 
      campus=campus, 
      link='https://google.com.br'
    )

    dados = {
      'curso': 2,
      'link': 'https://facebook.com.br'
    }

    # Editando um curso no câmpus
    response = self.client.post(
      reverse(
        'cadastros:editar_curso_campus', 
        kwargs={'pk': curso_campus.pk, 'pk_campus': campus.pk}
      ), dados
    )
    self.assertEqual(response.status_code, 302)

    CursoCampus.objects.create(
      curso=Curso.objects.get(pk=1), 
      campus=campus, 
      link='https://google.com.br'
    )

    dados = {
      'curso': 1,
      'link': 'https://facebook.com.br'
    }

    # Tentando editar um curso que já foi cadastro no câmpus
    # response = self.client.post(
    #   reverse(
    #     'cadastros:editar_curso_campus', 
    #     kwargs={'pk': curso_campus.pk, 'pk_campus': campus.pk}
    #   ), dados
    # )
    # self.assertEqual(response.status_code, 400)

    dados = {
      'curso': 3,
      'link': 'https://facebook.com.br'
    }

    # Tentando editar um curso em um câmpus inexistente
    response = self.client.post(
      reverse(
        'cadastros:editar_curso_campus', 
        kwargs={'pk': curso_campus.pk, 'pk_campus': 999}
      ), dados
    )
    self.assertEqual(response.status_code, 404)

    # Tentando editar um curso em um câmpus com um ID inexistente
    # na relação curso_campus
    response = self.client.post(
      reverse(
        'cadastros:editar_curso_campus', 
        kwargs={'pk': 999, 'pk_campus': campus.pk}
      ), dados
    )
    self.assertEqual(response.status_code, 404)

    dados = {
      'curso': 999,
      'link': 'https://facebook.com.br'
    }

    # Tentando editar um curso inexistente no câmpus
    response = self.client.post(
      reverse(
        'cadastros:editar_curso_campus', 
        kwargs={'pk': curso_campus.pk, 'pk_campus': campus.pk}
      ), dados
    )
    self.assertEqual(response.status_code, 400)