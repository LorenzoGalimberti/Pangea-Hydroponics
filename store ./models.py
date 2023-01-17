from email.mime import image
from email.policy import default
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator # validatori per la valutazione delle recensioni
from django.contrib.auth.models import User
from datetime import datetime



# cATALOGO MODELS
class Catalogo(models.Model):
    
    nome=models.CharField(max_length=50)
    stripe_product_id = models.CharField(max_length=100)
    categoria=models.CharField(max_length=20)
    sconto=models.IntegerField()
    prezzo=models.FloatField()
    prezzo_finale=models.FloatField()
    prezzo_buy=models.FloatField()
    slug=models.SlugField(max_length=50)
    spedizione=models.IntegerField()
    new_product=models.BooleanField()
    media_recensioni=models.FloatField()
    media_voto_round=models.IntegerField()

    media_voto_decimal=models.FloatField()
    numero_recensioni=models.IntegerField()
    descrizione=models.TextField()


    def __str__(self):
        return self.nome
    
    def save(self, *args, **kwargs):
        self.media_voto_round = int(self.media_recensioni)
        self.media_voto_decimal = self.media_recensioni-int(self.media_recensioni)
        super(Catalogo, self).save(*args, **kwargs) # Call the "real" save() method


#PRICE MODEL FOR A GIVEN PRODUCT

class Price(models.Model):
    product = models.ForeignKey(Catalogo, on_delete=models.CASCADE)
    stripe_price_id = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # cents
    
    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)



# classe filtri
# classe recensione post
class RecensionePostModel(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    nome=models.CharField(max_length=20)
    #cognome=models.CharField(max_length=20)
    prodotto=models.ForeignKey(Catalogo,on_delete=models.CASCADE )
    valutazione=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(5)])
    titolo=models.CharField(max_length=140)
    contenuto=models.TextField()
    data= models.DateField(default=datetime.today)
    immagine_1=models.ImageField(upload_to='static/revisioni', null=True, blank=True)
    immagine_2=models.ImageField(upload_to='static/revisioni', null=True, blank=True)
    immagine_3=models.ImageField(upload_to='static/revisioni', null=True, blank=True)
    def __str__(self):
        return self.nome

# modello per i filtri dei vasi

class VasiFiltriModel(models.Model):
    sei_bacelli=models.BooleanField()
    dodici_bacelli=models.BooleanField()
    otto_bacelli=models.BooleanField()


#modello colori 
class Color(models.Model):
    colore=models.CharField(max_length=15)
    codice=models.CharField(max_length=15)
    prodotto=models.ManyToManyField(Catalogo)

    def __str__(self):
        return self.colore


#  CARRELLO 
class Cart(models.Model):
    prezzo=models.ForeignKey(Price,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    quantity=models.IntegerField()
    
    
    def __str__(self):
        return self.user.username