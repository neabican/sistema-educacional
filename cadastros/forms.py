from django import forms
from django.forms import models, ModelForm, ModelChoiceField, ModelMultipleChoiceField

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, HTML, Submit

from .models import *

class FormCurso(ModelForm):
  class Meta:
    model = Curso
    fields = ['nome', 'descricao']

  def __init__(self, *args, **kwargs):
    super(FormCurso, self).__init__(*args, **kwargs)
    self.helper = FormHelper(self)
    self.helper.form_method = 'post'
    self.helper.form_tag = False
    self.helper.attrs = {'novalidate': ''}
    self.helper.layout = Layout(
      Row(
        Column('nome', css_class='col-xl-12')
      ),
      Row(
        Column('descricao', css_class='col-xl-12')
      )
    )

class FormCampus(ModelForm):
  class Meta:
    model = Campus
    fields = ['nome', 'instituicao']

  def __init__(self, *args, **kwargs):
    super(FormCampus, self).__init__(*args, **kwargs)
    self.helper = FormHelper(self)
    self.helper.form_method = 'post'
    self.helper.form_tag = False
    self.helper.attrs = {'novalidate': ''}
    self.helper.layout = Layout(
      Row(
        Column('nome', css_class='col-xl-8'),
        Column('instituicao', css_class='col-xl-4')
      )
    )

class FormEndereco(ModelForm):
  class Meta:
    model = Endereco
    fields = [
      'cidade', 'estado', 'logradouro', 'numero', 
      'cep', 'latitude', 'longitude',
    ]

  def __init__(self, *args, **kwargs):
    super(FormEndereco, self).__init__(*args, **kwargs)
    self.helper = FormHelper(self)
    self.helper.form_method = 'post'
    self.helper.form_tag = False
    self.helper.attrs = {'novalidate': ''}
    self.helper.layout = Layout(
      Row(
        Column('cidade', css_class='col-xl-3'),
        Column('estado', css_class='col-xl-2'),
        Column('logradouro', css_class='col-xl-5'),
        Column('numero', css_class='col-xl-2'),
      ),
      Row(
        Column('cep', css_class='col-xl-3'),
        Column('latitude', css_class='col-xl-2'),
        Column('longitude', css_class='col-xl-2'),
      )
    )