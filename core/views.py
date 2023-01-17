from django.shortcuts import render
from store.models import Catalogo
from django.db.models import Count
from pagamenti.models import Vendite
from django.http import Http404

# Create your views here.
# HOMEPAGE VIEW
def home(request):
    catalogo=Catalogo.objects.all()
    new_products=Catalogo.objects.filter(new_product = True)
    trending=Vendite.objects.filter().values_list('prodotto',flat=True).annotate(Count('prodotto')).order_by('-prodotto__count')
    trending_tuple=tuple(trending)
    trending_products=Catalogo.objects.filter(id__in=trending_tuple)
    context={"catalogo":catalogo,"new_products":new_products,"trending_products":trending_products}
    return render(request,"homepage2.html",context)



# ADMIN PAGE VIEW

def admin_page(request):
    if request.user.is_staff:
        catalogo=Catalogo.objects.all()

        vendite=Vendite.objects.all()
         
        context={"vendite":vendite,"catalogo":catalogo}
        return render(request,'admin-page.html',context)
    else:
        raise  Http404