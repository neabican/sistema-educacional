from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as django_login, logout as django_logout, authenticate

def login(request):
  if request.method == 'POST':
    email = request.POST['email']
    senha = request.POST['senha']
    usuario = authenticate(request, username=email, password=senha)

    if usuario is not None:
      django_login(request, usuario)

      return redirect('cadastros:dashboard')
    else:
      messages.error(request, 'E-mail ou senha incorreta')

  return render(request, 'registration/login.html')

@login_required
def logout(request):
  django_logout(request)

  return redirect('cadastros:login')