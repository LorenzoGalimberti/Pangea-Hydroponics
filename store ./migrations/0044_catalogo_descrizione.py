# Generated by Django 2.1.5 on 2022-12-22 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0043_auto_20221029_1613'),
    ]

    operations = [
        migrations.AddField(
            model_name='catalogo',
            name='descrizione',
            field=models.TextField(default='cc'),
            preserve_default=False,
        ),
    ]