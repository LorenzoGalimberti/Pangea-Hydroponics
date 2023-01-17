from django import forms
from django.contrib.auth.models import User

# MODEL FORM DELLA REGISTRAZIONE

class FormRegistrazioneUser(forms.ModelForm):
    username=forms.CharField(widget=forms.TextInput())
    email=forms.CharField(widget=forms.EmailInput())
    password=forms.CharField(widget=forms.PasswordInput())
    conferma_password=forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model=User
        fields=["username","email","password","conferma_password"]

    def clean(self):
        super().clean()
        password=self.cleaned_data["password"]
        conferma_password=self.cleaned_data["conferma_password"]
        if password!= conferma_password:
            raise forms.ValidationError(" le password non combaciano!")
        
        return self.cleaned_data
       