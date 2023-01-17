
from django.urls import path
from .views import productpage,crea_recensione_view,new_products,vasi_page,torri_page,offerte,cart,add_to_cart,delete_element,add_quantity,dec_quantity,cart_in_progress

urlpatterns = [
    path('catalogo/<str:slug>/',productpage,name="productpage"),
    path('catalogo/<str:slug>/recensione/',crea_recensione_view,name="recensione"),
    path('nuovi-arrivi/',new_products,name="nuovi-prodotti"),
    path('vasi-idroponici/',vasi_page,name="page-vasi"),
    path('sistemi-idroponici/',torri_page,name="page-torri"),
    path('offerte/',offerte,name="offerte"),
    path('carrello/<str:username>/',cart,name='cart-view'),
    path('checkout/cart/work-in-progress/',cart_in_progress,name='cart-in-progress-view'),
    path('elimina/<int:pk>/',delete_element,name='delete-from-cart'),
    path('add-quantity/<int:pk>/',add_quantity,name="add-quantity"),
    path('dec-quantity/<int:pk>/',dec_quantity,name="dec-quantity"),
    path('add-to-cart/<int:pk>/',add_to_cart,name="add-to-cart"),

]
