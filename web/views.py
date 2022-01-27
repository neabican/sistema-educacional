from django.shortcuts import render

def listar_campus(request):
  return render(request, 'web/listar_campus.html')