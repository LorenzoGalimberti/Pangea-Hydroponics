# Generated by Django 2.1.5 on 2022-10-12 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20221012_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogo',
            name='media_voto_round',
            field=models.IntegerField(default=3),
            preserve_default=False,
        ),
    ]
