# Generated by Django 2.1.5 on 2022-10-12 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_recensionepostmodel_titolo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='catalogo',
            name='numero_bacelli',
        ),
        migrations.AddField(
            model_name='catalogo',
            name='media_recensioni',
            field=models.FloatField(default=3.5),
            preserve_default=False,
        ),
    ]
