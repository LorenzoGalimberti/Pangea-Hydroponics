from django import forms
from .models import RecensionePostModel,VasiFiltriModel
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# MODEL FORM PER LE RECENSIONI
class RecensionePostModelForm(forms.ModelForm):
    immagine_1=forms.ImageField(required=False)
    immagine_2=forms.ImageField(required=False)
    immagine_3=forms.ImageField(required=False)
    class Meta:
        model=RecensionePostModel
        fields=["nome","contenuto","valutazione","titolo","immagine_1","immagine_2","immagine_3"]
        exclude = ['prodotto',"user","data"]

    def clean_contenuto(self):
        dati=self.cleaned_data["contenuto"]
        if "parola" in dati:
            raise ValidationError("il contenuto inserito viola le norme del sito")
        else:
            return dati


# form per i filirri dei vasi idroponici 

class VasiFiltriModelForm(forms.ModelForm):

    class Meta:
        model=VasiFiltriModel
        fields=["sei_bacelli","otto_bacelli","dodici_bacelli"]
      