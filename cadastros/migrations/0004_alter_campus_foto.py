# Generated by Django 3.2.9 on 2022-01-24 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cadastros', '0003_campus_foto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campus',
            name='foto',
            field=models.ImageField(blank=True, default=None, upload_to='fotos_campus/'),
        ),
    ]