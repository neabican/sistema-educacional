from django.db import models

class Instituicao(models.Model):
  nome = models.CharField(max_length=300)

  def __str__(self):
    return self.nome

class Curso(models.Model):
  nome = models.CharField(max_length=300)
  descricao = models.TextField()

  def __str__(self):
    return self.nome

class Endereco(models.Model):
  logradouro = models.CharField(max_length=300)
  numero = models.CharField(max_length=10)
  cep = models.CharField(max_length=10)
  altitude = models.DecimalField(max_digits=22, decimal_places=16)
  latitude = models.DecimalField(max_digits=22, decimal_places=16)

  def __str__(self):
    return f'{self.logradouro}, {self.numero}'

class Programa(models.Model):
  nome = models.CharField(max_length=300)
  descricao = models.TextField()
  link = models.CharField(max_length=500)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class Projeto(models.Model):
  nome = models.CharField(max_length=300)
  descricao = models.TextField()
  link = models.CharField(max_length=500)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class AcaoAfirmativa(models.Model):
  nome = models.CharField(max_length=300)
  descricao = models.TextField()
  link = models.CharField(max_length=500)
  campus = models.ForeignKey('Campus', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome

class Campus(models.Model):
  nome = models.CharField(max_length=300)
  endereco = models.ForeignKey('Endereco', on_delete=models.PROTECT)
  instituicao = models.ForeignKey('Instituicao', on_delete=models.CASCADE)

  def __str__(self):
    return self.nome