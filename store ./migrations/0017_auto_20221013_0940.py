# Generated by Django 2.1.5 on 2022-10-13 07:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0016_catalogo_media_voto_decimal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='catalogo',
            old_name='risparmia',
            new_name='roi',
        ),
    ]
