from django.db import models
import uuid

class Instituicao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Categoria(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    sigla = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class AcoesAfirmativas(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome

class Endereco(models.Model):
    cidade = models.CharField(max_length=255)
    estado = models.CharField(max_length=255)
    logradouro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    cep = models.CharField(max_length=20)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f'{self.logradouro}, {self.numero} - {self.cidade}'

class Campus(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    link = models.URLField()
    endereco = models.OneToOneField(Endereco, on_delete=models.CASCADE)
    instituicao = models.ForeignKey(Instituicao, on_delete=models.CASCADE)
    acoes_afirmativas = models.ManyToManyField(AcoesAfirmativas)

    def __str__(self):
        return self.nome

class Fotos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField()
    altura = models.IntegerField()
    largura = models.IntegerField()
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)

    def __str__(self):
        return f'Foto de {self.campus.nome}'

class Curso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    resumo = models.TextField()
    mercado = models.TextField()

    def __str__(self):
        return self.nome

class Turno(models.TextChoices):
    MATUTINO = 'matutino', 'Matutino'
    VESPERTINO = 'vespertino', 'Vespertino'
    NOTURNO = 'noturno', 'Noturno'
    INTEGRAL = 'integral', 'Integral'

class Modalidade(models.TextChoices):
    PRESENCIAL = 'presencial', 'Presencial'
    EAD = 'ead', 'EAD'

class TipoIngresso(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    descricao = models.TextField()

    def __str__(self):
        return self.nome

class CursoCampus(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE)
    campus = models.ForeignKey(Campus, on_delete=models.CASCADE)
    vagas = models.IntegerField()
    link = models.URLField()
    turno = models.CharField(max_length=50, choices=Turno.choices)
    modalidade = models.CharField(max_length=50, choices=Modalidade.choices)
    tipo_ingresso = models.ForeignKey(TipoIngresso, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.curso.nome} no {self.campus.nome}'
