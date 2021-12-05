from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

UserModel = get_user_model()

class EmailBackend(ModelBackend):
  def authenticate(self, request, username=None, password=None, **kwargs):
    try:
      usuario = UserModel.objects.get(email__iexact=username)
    except UserModel.DoesNotExist:
      UserModel().set_password(password)
      return
    except UserModel.MultipleObjectsReturned:
      usuario = UserModel.objects.filter(email__iexact=username).order_by('id').first()

    if usuario.check_password(password) and self.user_can_authenticate(usuario):
      return usuario