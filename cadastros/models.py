from django.db import models

class Instituicao(models.Model):
  nome = models.CharField(max_length=250, unique=True)

  def __str__(self):
    return self.nome

class Curso(models.Model):
  nome = models.CharField(max_length=250, unique=True)
  descricao = models.TextField('Descrição')

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
  descricao = models.TextField('Descrição')
  link = models.CharField(max_length=500, blank=True, null=True)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class Projeto(models.Model):
  nome = models.CharField(max_length=300)
  descricao = models.TextField('Descrição')
  link = models.CharField(max_length=500, blank=True, null=True)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class AcaoAfirmativa(models.Model):
  nome = models.CharField(max_length=300)
  descricao = models.TextField('Descrição')
  link = models.CharField(max_length=500, blank=True, null=True)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class Campus(models.Model):
  nome = models.CharField(max_length=300)
  endereco = models.ForeignKey('Endereco', on_delete=models.PROTECT)
  instituicao = models.ForeignKey('Instituicao', on_delete=models.CASCADE)
  cursos = models.ManyToManyField('CursoCampus')

  def __str__(self):
    return self.nome