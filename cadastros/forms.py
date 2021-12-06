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