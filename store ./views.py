from email import header
from multiprocessing import context
from django.shortcuts import render,get_object_or_404,redirect
from .models import Catalogo,RecensionePostModel,Price,Cart
from pagamenti.models import Vendite
from .forms import RecensionePostModelForm,VasiFiltriModelForm
from django.http import Http404, HttpResponse, HttpResponseForbidden,HttpResponseRedirect
from math import modf
from django.db.models import Q

# VIEW DELLA PRODUCT PAGE

def productpage(request,slug):
    #prodotto=Catalogo.objects.get(pk=pk) 
    prodotto = Catalogo.objects.get(slug=slug)
    #prodotto=get_object_or_404(Catalogo,slug=slug)
    prices = Price.objects.filter(product=prodotto)
    if "4stella" in request.GET:
      
       recensioni=RecensionePostModel.objects.filter(prodotto_id=prodotto.id ,valutazione=4 )
    elif "3stella" in request.GET:
      
       recensioni=RecensionePostModel.objects.filter(prodotto_id=prodotto.id,valutazione=3 )  
    elif "2stella" in request.GET:
      
       recensioni=RecensionePostModel.objects.filter(prodotto_id=prodotto.id,valutazione=3 )  
    elif "1stella" in request.GET:
      
       recensioni=RecensionePostModel.objects.filter(prodotto_id=prodotto.id,valutazione=3 )  
    else:
        recensioni=RecensionePostModel.objects.filter(prodotto_id=prodotto.id )
    counter=0
    voto_totale=0
    five_star=0
    four_star=0
    three_star=0
    two_star=0
    one_star=0
    voti_recensioni=[]
    user_recensioni=[]
    for recensione in recensioni  :
        
        user=request.user
        user_recensioni.append(user)
        list=range(1,recensione.valutazione)
        voti_recensioni.append(list)
        counter+= 1
        voto_totale+= recensione.valutazione
        if recensione.valutazione==5:
            five_star+=1
        if recensione.valutazione==4:
            four_star+=1
        if recensione.valutazione==3:
            three_star+=1
        if recensione.valutazione==2:
            two_star+=1
        if recensione.valutazione==1:
            one_star+=1      
              
    

    if counter >0:
       
        media_voto="{:.1f}".format(voto_totale/counter)
            
        media_voto=float(media_voto)
        media_voto_round=int(media_voto)
        prodotto.media_recensioni=media_voto
        prodotto.save(update_fields=["media_recensioni"])
    #print(prodotto.media_recensioni)


        media_voto_decimal="{:.1f}".format(media_voto-media_voto_round)
        media_voto_decimal=float(media_voto_decimal)
        media_voto_round_value=media_voto_round
        empty_star=range(1,5-media_voto_round)
        media_voto_round=range(0,media_voto_round)


        five_star=round(five_star*100/counter )
        four_star=round(four_star*100/counter)  
        three_star=round(three_star*100/counter)  
        two_star=round(two_star*100/counter)  
        one_star=round(one_star*100/counter)
        vendite=Vendite.objects.all()
    
        also_like=Catalogo.objects.all().exclude(nome=prodotto.nome)  #potrebbe anche piacerti

        context={"prices":prices,"prodotto":prodotto,"vendite":vendite,"also_like":also_like,"recensioni":recensioni,"voti_recensioni":voti_recensioni,"counter":counter,"media_voto":media_voto,"media_voto_round": media_voto_round,"media_voto_round_value": media_voto_round_value,"media_voto_decimal":media_voto_decimal,"empty_star":empty_star,"five_star":five_star,"four_star":four_star,"three_star":three_star,"two_star":two_star,"one_star":one_star}
        return render(request,"productpage.html",context)
    
    else :
        five_star=0
        four_star=0  
        three_star=0  
        two_star=0 
        one_star=0
        counter=0
        prodotto.media_recensioni=0
        prodotto.save(update_fields=["media_recensioni"])
        also_like=Catalogo.objects.all().exclude(nome=prodotto.nome)  #potrebbe anche piacerti
        context={"prices":prices,"prodotto":prodotto,"also_like":also_like,"counter":counter,"five_star":five_star,"four_star":four_star,"three_star":three_star,"two_star":two_star,"one_star":one_star}
        return render(request,"productpage.html",context)


# VIEW CREA RECENSIONE 

def crea_recensione_view(request,slug):
    lista=[]
    check_list=[]
    
    prodotto=get_object_or_404(Catalogo,slug=slug)
    recensioni=RecensionePostModel.objects.filter(prodotto_id=prodotto.id)
   
    for recensione in recensioni:
        check_list.append(recensione.user)
    
    print(check_list)
    # try:
    #     recensioni=get_object_or_404(RecensionePostModel,prodotto_id=prodotto.id)
    #     print(recensioni.user)
    # except:
    #     pass

    vendite=Vendite.objects.filter(prodotto_id=prodotto.id)
    for vendita in vendite:
        #print(vendita.email)
        lista.append(vendita.email)
    
    
    if request.user.is_authenticated:
        #print(request.user.email)
        
        if request.user.email in lista :
            if request.user not in check_list:
                
                if request.method =="POST" :
                    form=RecensionePostModelForm(request.POST,request.FILES)
                    #form.cleaned_data["prodotto"]=prodotto
                    if form.is_valid():
                        print('il form è valido ')
                        form.instance.prodotto = prodotto
                        form.instance.user=request.user
                        
                        new_post=form.save()  #salviamo nel db !!!
                        #print(new_post)

                        prodotto.numero_recensioni=prodotto.numero_recensioni +1
                        prodotto.save(update_fields=["numero_recensioni"])
                        context={"prodotto":prodotto,"check_list":check_list,}
                        return render(request,"ringraziamenti.html",context)
                else:
                    form=RecensionePostModelForm()
            else:
                return HttpResponse('<p> pensare ad una modifica  della recensione</p>')
        else:
            context={"prodotto": prodotto}
            return render(request,"errore_recensione.html",context) #renderizzo la pagina di errore 
    else:
        return render(request,"login.html")
    context={"form":form,"prodotto": prodotto}
    return render(request,"crea_recensione.html",context)




#VIEW PAGE VASI IDOPONICI

def vasi_page(request):
    
    form=VasiFiltriModelForm()
     # set up order by
    if "mintomax" in request.GET:
       querystring=request.GET.get("mintomax")

       if len(querystring)==0:
        return redirect("/vasi-idroponici/")

      
       prodotti=Catalogo.objects.filter(categoria="vasi idroponici").order_by("prezzo_finale")
        
       context={"prodotti":prodotti,"form":form} 
       return render(request,"vasi_homepage.html",context)
    
    # max to min
    if "maxtomin" in request.GET:
       querystring=request.GET.get("maxtomin")

       if len(querystring)==0:
        return redirect("/vasi-idroponici/")

       prodotti=Catalogo.objects.filter(categoria="vasi idroponici").order_by("-prezzo_finale")

       context={"prodotti":prodotti,"form":form} 
       return render(request,"vasi_homepage.html",context)
    
    #a to z 
    if "atoz" in request.GET:
       querystring=request.GET.get("atoz")

       if len(querystring)==0:
        return redirect("/vasi-idroponici/")

       prodotti=Catalogo.objects.filter(categoria="vasi idroponici").order_by("nome")

       context={"prodotti":prodotti,"form":form} 
       return render(request,"vasi_homepage.html",context)
    
    #z-a
    if "ztoa" in request.GET:
       querystring=request.GET.get("ztoa")

       if len(querystring)==0:
        return redirect("/vasi-idroponici/")

       prodotti=Catalogo.objects.filter(categoria="vasi idroponici").order_by("-nome")

       context={"prodotti":prodotti,"form":form} 
       return render(request,"vasi_homepage.html",context)

    # filter form    
    if "q" in request.GET:
       querystring=request.GET.get("q")

       if len(querystring)==0:
        return redirect("/vasi-idroponici/")

       prodotti=Catalogo.objects.filter(numero_bacelli=8)

       context={"prodotti":prodotti,"form":form} 
       return render(request,"vasi_homepage.html",context)
    else:
        prodotti=Catalogo.objects.filter(categoria="vasi idroponici")
        context={"prodotti":prodotti}
        return render(request,"vasi_homepage.html",context)
   
   
# VIEW SISTEMI IDROPONICI

def torri_page(request):
    form=VasiFiltriModelForm()
     # set up order by
    if "mintomax" in request.GET:
       querystring=request.GET.get("mintomax")

       if len(querystring)==0:
        return redirect("/torri-idroponiche/")

      
       prodotti=Catalogo.objects.filter(categoria="torri idroponiche").order_by("prezzo_finale")
       context={"prodotti":prodotti,"form":form} 
       return render(request,"torri_homepage.html",context)
    
    # max to min
    if "maxtomin" in request.GET:
       querystring=request.GET.get("maxtomin")

       if len(querystring)==0:
        return redirect("/torri-idroponiche/")

       prodotti=Catalogo.objects.filter(categoria="torri idroponiche").order_by("-prezzo_finale")

       context={"prodotti":prodotti,"form":form} 
       return render(request,"torri_homepage.html",context)
    
    #a to z 
    if "atoz" in request.GET:
       querystring=request.GET.get("atoz")

       if len(querystring)==0:
        return redirect("/torri-idroponiche/")

       prodotti=Catalogo.objects.filter(categoria="torri idroponiche").order_by("nome")

       context={"prodotti":prodotti,"form":form} 
       return render(request,"torri_homepage.html",context)
    
    #z-a
    if "ztoa" in request.GET:
       querystring=request.GET.get("ztoa")

       if len(querystring)==0:
        return redirect("/torri-idroponiche/")

       prodotti=Catalogo.objects.filter(categoria="torri idroponiche").order_by("-nome")

       context={"prodotti":prodotti,"form":form} 
       return render(request,"torri_homepage.html",context)

    # filter form    
    if "q" in request.GET:
       querystring=request.GET.get("q")

       if len(querystring)==0:
        return redirect("/torri-idroponiche/")

       prodotti=Catalogo.objects.filter(numero_bacelli=8)

       context={"prodotti":prodotti,"form":form} 
       return render(request,"torri_homepage.html",context)
    else:
        prodotti=Catalogo.objects.filter(categoria="torri idroponiche")
        context={"prodotti":prodotti}
        return render(request,"torri_homepage.html",context)
     


""" questo è un esempio , serve solo per vedere le product cards"""

def new_products(request):
    new_products=Catalogo.objects.filter(new_product=True)
    context={"new_products":new_products}
    return render(request,"nuovi_arrivi.html",context)



# VIEW DELLE OFFERTE 

def offerte(request):
    offerte=Catalogo.objects.all().exclude(sconto=0)
    context={"offerte":offerte}
    return render(request,"offerte.html",context)






# view carrello --> mostra gli elementi del carrello 

def cart(request,username):
    if request.user.is_authenticated:
        catalogo=Catalogo.objects.all()
        username=request.user
        elementi=Cart.objects.filter(user=username)
        sum=0
        for el in elementi:
           sum+= (el.prezzo.price*el.quantity)/100
        context={'elementi':elementi , 'sum' :sum,'catalogo':catalogo}
        return render(request,'cart.html',context)

    else:
        return render(request,'login.html')

def cart_in_progress(request):
    return render(request,"cart-progress.html")

def add_to_cart(request,pk):
     
     if request.user.is_authenticated :
        # l' user è autenticato, può aggiungere al carrello
        element=Catalogo.objects.get(pk=pk)
        price=Price.objects.get(product=element)
        print(Cart.objects.filter(prezzo=price,user=request.user).values_list())
        print(Cart.objects.all().values())
        if not Cart.objects.filter(prezzo=price,user=request.user).values() :
            object = Cart.objects.create(prezzo=price, user=request.user, quantity=1)

        
        return redirect(request.META.get('HTTP_REFERER'))


# VIEWS DEL CARRELLO -->  delete_element , modify_quantity , checkout (da gestire in stripepayments)


def delete_element(request,pk):
    if request.user.is_authenticated:
            

        # l' user è autenticato, può aggiungere al carrello
        element=Catalogo.objects.get(pk=pk)
        price=Price.objects.get(product=element)
        object = Cart.objects.get(prezzo=price, user=request.user)
        object.delete()
        return redirect(request.META.get('HTTP_REFERER'))


def add_quantity(request,pk):
    if request.user.is_authenticated:
            
        element=Catalogo.objects.get(pk=pk)
        price=Price.objects.get(product=element)
        object = Cart.objects.get(prezzo=price, user=request.user)
        object.quantity=object.quantity + 1 
        object.save()
        return redirect(request.META.get('HTTP_REFERER'))

def dec_quantity(request,pk):
    if request.user.is_authenticated:
        element=Catalogo.objects.get(pk=pk)
        price=Price.objects.get(product=element)
        object = Cart.objects.get(prezzo=price, user=request.user)
        object.quantity=object.quantity - 1 
        if object.quantity >= 1:
            object.save()
        return redirect(request.META.get('HTTP_REFERER'))