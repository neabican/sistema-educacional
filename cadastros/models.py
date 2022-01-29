from django.db import models
from ckeditor.fields import RichTextField

from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import sys

class Instituicao(models.Model):
  nome = models.CharField(max_length=250, unique=True)
  sigla = models.CharField(max_length=20, default='')

  def __str__(self):
    return self.nome

class Curso(models.Model):
  nome = models.CharField(max_length=250, unique=True)
  descricao = RichTextField('Descrição')

  def __str__(self):
    return self.nome

class CursoCampus(models.Model):
  curso = models.ForeignKey('Curso', on_delete=models.CASCADE)
  link = models.CharField(max_length=500)

  def __str__(self):
    return self.curso.nome

class Endereco(models.Model):
  ESTADOS_CHOICES = (
    ('AC', 'Acre'),
    ('AL', 'Alagoas'),
    ('AP', 'Amapá'),
    ('AM', 'Amazonas'),
    ('BA', 'Bahia'),
    ('CE', 'Ceará'),
    ('DF', 'Distrito Federal'),
    ('ES', 'Espírito Santo'),
    ('GO', 'Goiás'),
    ('MA', 'Maranhão'),
    ('MT', 'Mato Grosso'),
    ('MS', 'Mato Grosso do Sul'),
    ('MG', 'Minas Gerais'),
    ('PA', 'Pará'),
    ('PB', 'Paraíba'),
    ('PR', 'Paraná'),
    ('PE', 'Pernambuco'),
    ('PI', 'Piauí'),
    ('RJ', 'Rio de Janeiro'),
    ('RN', 'Rio Grande do Norte'),
    ('RS', 'Rio Grande do Sul'),
    ('RO', 'Rondônia'),
    ('RR', 'Roraima'),
    ('SC', 'Santa Catarina'),
    ('SP', 'São Paulo'),
    ('SE', 'Sergipe'),
    ('TO', 'Tocantins'),
  )

  cidade = models.CharField(max_length=100)
  estado = models.CharField(max_length=50, choices=ESTADOS_CHOICES)
  logradouro = models.CharField(max_length=300)
  numero = models.CharField('Número', max_length=10)
  cep = models.CharField('CEP', max_length=10)
  latitude = models.DecimalField(max_digits=22, decimal_places=16)
  longitude = models.DecimalField(max_digits=22, decimal_places=16)

  def __str__(self):
    return f'{self.logradouro}, {self.numero}'

class Programa(models.Model):
  nome = models.CharField(max_length=300)
  descricao = RichTextField('Descrição')
  link = models.CharField(max_length=500, blank=True, null=True)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class Projeto(models.Model):
  nome = models.CharField(max_length=300)
  descricao = RichTextField('Descrição')
  link = models.CharField(max_length=500, blank=True, null=True)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class AcaoAfirmativa(models.Model):
  nome = models.CharField(max_length=300)
  descricao = RichTextField('Descrição')
  link = models.CharField(max_length=500, blank=True, null=True)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class Campus(models.Model):
  nome = models.CharField(max_length=300)
  foto = models.ImageField(blank=True, default=None, upload_to='fotos_campus/')
  link = models.CharField(max_length=500, default='')
  endereco = models.ForeignKey('Endereco', on_delete=models.PROTECT)
  instituicao = models.ForeignKey('Instituicao', on_delete=models.PROTECT)
  cursos = models.ManyToManyField('CursoCampus')

  def __str__(self):
    return self.nome

  def save(self, arquivo_antigo, *args, **kwargs):
    if self.foto:
      if self.foto != arquivo_antigo:
        im = Image.open(self.foto)

        if (im.format == 'RGBA'):
          im = im.convert('RGB')

        output = BytesIO()

        im.save(output, format='PNG', quality=100)
        output.seek(0)

        self.foto = InMemoryUploadedFile(
          output, 
          'ImageField', 
          "%s.jpg" %self.foto.name.split('.')[0], 
          'image/jpeg', 
          sys.getsizeof(output), 
          None
        )
    
    super(Campus, self).save()