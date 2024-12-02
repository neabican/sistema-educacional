from django.contrib import admin
from .models import (Instituicao, Categoria, AcoesAfirmativas, Endereco, Campus, 
                     Fotos, Curso, TipoIngresso, CursoCampus)

admin.site.register(Instituicao)
admin.site.register(Categoria)
admin.site.register(AcoesAfirmativas)
admin.site.register(Endereco)
admin.site.register(Campus)
admin.site.register(Fotos)
admin.site.register(Curso)
admin.site.register(TipoIngresso)
admin.site.register(CursoCampus)
class InstituicaoAdmin(admin.ModelAdmin):
    pass