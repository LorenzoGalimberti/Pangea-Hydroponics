# Generated by Django 2.1.5 on 2022-10-17 12:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0029_recensionepostmodel_immagini'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recensionepostmodel',
            name='immagini',
        ),
    ]
