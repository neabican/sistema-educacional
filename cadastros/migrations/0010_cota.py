# Generated by Django 4.1.2 on 2022-10-25 22:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0009_rename_info_complementar_cursocampus_descricao'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cota',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=250)),
                ('porcentagem', models.IntegerField()),
                ('instituicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cadastros.instituicao')),
            ],
        ),
    ]