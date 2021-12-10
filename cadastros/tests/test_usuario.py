from django.test import TestCase
from django.contrib.auth import get_user_model

from usuarios.models import CustomUser

def criar_usuario(email):
  UserModel = get_user_model()

  if not UserModel.objects.filter(email=email).exists():
    user = UserModel.objects.create_user(
      username='teste',
      email=email,
      password='teste123',
      first_name='John',
      last_name='Doe'
    )
    user.is_superuser = True
    user.is_staff = True
    user.save()

    return user

class CustomUserTestCase(TestCase):
  def setUp(self):
    admin = criar_usuario('teste@ifsc.edu.br')

  def test_user(self):
    usuario = CustomUser.objects.get(email='teste@ifsc.edu.br')
    self.assertEqual(usuario.first_name, 'John')
    self.assertEqual(usuario.last_name, 'Doe')