# Generated by Django 2.1.5 on 2022-09-17 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0004_auto_20220914_0104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vendite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('prodotto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articoli', to='store.Catalogo')),
            ],
        ),
    ]