# Generated by Django 2.1.5 on 2022-10-17 14:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0041_auto_20221017_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recensionepostmodel',
            name='immagine_2',
            field=models.ImageField(blank=True, upload_to='static/revisioni'),
        ),
        migrations.AlterField(
            model_name='recensionepostmodel',
            name='immagine_3',
            field=models.ImageField(blank=True, upload_to='static/revisioni'),
        ),
    ]
