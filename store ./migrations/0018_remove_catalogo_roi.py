# Generated by Django 2.1.5 on 2022-10-13 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0017_auto_20221013_0940'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogo',
            name='roi',
        ),
    ]
