import email
from django.db import models
from store.models import Catalogo

# MODELLO DELLE VENDITE

class Vendite(models.Model):
    email=models.EmailField()
    prodotto=models.ForeignKey(Catalogo,on_delete=models.CASCADE )
   
    def __str__(self):

        return self.email
