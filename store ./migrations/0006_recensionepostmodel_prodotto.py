# Generated by Django 2.1.5 on 2022-09-21 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_recensionepostmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='recensionepostmodel',
            name='prodotto',
            field=models.CharField(default='torre idroponica delux', max_length=50),
            preserve_default=False,
        ),
    ]
