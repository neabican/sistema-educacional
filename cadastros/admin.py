from django.contrib import admin
from .models import *

class InstituicaoAdmin(admin.ModelAdmin):
  list_display = ('nome', 'numero_campus',)
  search_fields = ('nome',)

  def numero_campus(self, obj):
    return Campus.objects.filter(instituicao=obj).count()

class CampusAdmin(admin.ModelAdmin):
  list_display = (
    'nome', 'endereco', 'numero_programas', 
    'numero_projetos', 'numero_acoes_afirmativas',
  )
  search_fields = ('nome',)

  def numero_programas(self, obj):
    return Programa.objects.filter(campus=obj).count()

  def numero_projetos(self, obj):
    return Projeto.objects.filter(campus=obj).count()

  def numero_acoes_afirmativas(self, obj):
    return AcaoAfirmativa.objects.filter(campus=obj).count()

class ProgramaAdmin(admin.ModelAdmin):
  list_display = ('nome', 'link', 'campus')
  search_fields = ('nome',)

class ProjetoAdmin(admin.ModelAdmin):
  list_display = ('nome', 'link', 'campus')
  search_fields = ('nome',)

class AcaoAfirmativaAdmin(admin.ModelAdmin):
  list_display = ('nome', 'link', 'campus')
  search_fields = ('nome',)

class CursoAdmin(admin.ModelAdmin):
  list_display = ('nome', 'descricao',)
  search_fields = ('nome',)

admin.site.register(Instituicao, InstituicaoAdmin)
admin.site.register(Campus, CampusAdmin)
admin.site.register(Programa, ProgramaAdmin)
admin.site.register(Projeto, ProjetoAdmin)
admin.site.register(AcaoAfirmativa, AcaoAfirmativaAdmin)
admin.site.register(Curso, CursoAdmin)
admin.site.register(Imagem)
admin.site.register(Endereco)