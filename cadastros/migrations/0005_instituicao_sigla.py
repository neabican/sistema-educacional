# Generated by Django 3.2.9 on 2022-01-25 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0004_alter_campus_foto'),
    ]

    operations = [
        migrations.AddField(
            model_name='instituicao',
            name='sigla',
            field=models.CharField(default='', max_length=20),
        ),
    ]
