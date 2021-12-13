from django.core.paginator import Paginator, EmptyPage, InvalidPage

def gerar_paginacao(request, resultados, num_resultados):
  paginator = Paginator(resultados, num_resultados)

  try:
    page = int(request.GET.get('pagina', '1'))
  except:
    page = 1
  try:
    resultados_paginados = paginator.page(page)
  except(EmptyPage, InvalidPage):
    resultados_paginados = paginator.page(paginator.num_pages)

  paginas = {}
  
  paginas['total'] = paginator.num_pages - 2
  paginas['ultimo'] = paginator.num_pages
  paginas['anterior'] = 0
  paginas['proximo'] = page + 1

  if page >= 3:
    paginas['anterior'] = page - 1
  elif page == 1:
    paginas['proximo'] = page + 2

  return resultados_paginados, paginas