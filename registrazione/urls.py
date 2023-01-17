from registrazione.views import registrazione
from django.urls import path

urlpatterns = [
   
    path('registrazione/',registrazione,name='registrazione')
]
