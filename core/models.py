from pyexpat import model
from django.db import models

# modello catalogo.
class Catalogo(models.Model):
    nome=models.CharField(max_length=50)
    categoria=models.CharField(max_length=20)
    sconto=models.IntegerField()
    prezzo=models.FloatField()
    prezzo_finale=models.FloatField()
    prezzo_buy=models.FloatField()

    def __str__(self):
        return self.nome