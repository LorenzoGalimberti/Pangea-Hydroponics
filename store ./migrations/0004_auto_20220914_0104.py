# Generated by Django 2.1.5 on 2022-09-13 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_auto_20220914_0049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogo',
            name='slug',
            field=models.SlugField(),
        ),
    ]
