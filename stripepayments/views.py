
from django.core.mail import send_mail
import stripe
from django.conf import settings
from django.http import JsonResponse,HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from store.models import Catalogo,Price,Cart
from pagamenti.models import Vendite
from django.shortcuts import redirect
 
stripe.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        price = Price.objects.get(id=self.kwargs["pk"]) #
        product_id=price.product.pk
        domain = "https://pangeahydroponics.com"
        if settings.DEBUG:
            domain = "http://127.0.0.1:8000"
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            shipping_address_collection={"allowed_countries": ["US", "IT"]},

            line_items=[
                {
                    'price': price.stripe_price_id,
                    "adjustable_quantity": {"enabled": True, "minimum": 1, "maximum": 100},

                    'quantity': 1,
                },
                
            ],
            metadata={
                "product_id":product_id,
                

            },
            mode='payment',
            success_url=domain + '/success/',
            cancel_url=domain + '/cancel/',
        )
        return redirect(checkout_session.url)

@csrf_exempt # make the view not require a csrf token 
def stripe_webhook(request):
  payload = request.data
  sig_header = request.headers.get('stripe-signature')
  #sig_header = request.META['HTTP_STRIPE_SIGNATURE']
  event = None
  
  try:
    event = stripe.Webhook.construct_event(
        payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
    )
  except ValueError as e:
    # Invalid payload
    return HttpResponse(status=400)
  except stripe.error.SignatureVerificationError as e:
    # Invalid signature
    return HttpResponse(status=400)


  
  # Handle the checkout.session.completed event
 # if event and event['type'] == 'checkout.session.completed':
  if event['type'] == 'checkout.session.completed':
    # Retrieve the session. If you require line items in the response, you may include them by expanding line_items.
   
    session =event['data']['object']
    quantity=event['data']['quantity']
    email=session["customer_details"]["email"] #costumer email
    #adress=session["customer_details"]["address"]["city"]
    citta=session["customer_details"]["address"]["city"]
    stato=session["customer_details"]["address"]["country"]
    via1=session["customer_details"]["address"]["line1"]
    via2=session["customer_details"]["address"]["line2"]
    codice_postale=session["customer_details"]["address"]["postal_code"]
    provincia=session["customer_details"]["address"]["state"]
    nome=session["customer_details"]["name"]
    id=session["metadata"]["product_id"]
    line_items = stripe.checkout.Session.list_line_items(session["id"])

    stripe_price_id = line_items["data"][0]["price"]["id"]
    price = Price.objects.get(stripe_price_id=stripe_price_id)
    prodotto = price.product

    #email to us   
    send_mail(
        subject="ordine",
        message=f"NOME: {nome} \nCITTA' :  {citta} \nINDIRIZZO : {via1} \nCAP : {codice_postale}  \nPROVINCIA : {provincia} \nPRODOTTO : {prodotto} {quantity}   ",
        recipient_list=['pangeahydroponics@gmail.com'],
        from_email='pangeahydroponics@gmail.com',
    )
    #email to costumer checkout session completed
    send_mail(
        subject="Grazie per il supporto",
        message=f"gentile {nome} .\n Il team di Pangea ti ringrazia per aver acquistato il {prodotto}.\n Cordali saluti ",
        recipient_list=[email],
        from_email='pangeahydroponics@gmail.com'
    )

    #aggiungere al database vendite l' email , ed il prodotto per poter fare la recensione
    v=Vendite.objects.create(email=email,prodotto=Catalogo.objects.get(pk=id))
    v.save() 
# dobbiamo aggiungere anche transazione rifiutata , con magari una view

  return HttpResponse(status=200)


# webhooks view ---



#view pagamento confermato
class SuccessView(TemplateView):
    template_name = "success.html"

#view pagamento senza success
class CancelView(TemplateView):
    template_name = "cancel.html"









# CART CHECKOUT 
def cart_checkout(request):
   
    prices=Price.objects.all()
    cart_prices=Cart.objects.filter(user=request.user)
    line_items=[]
    line_tests=[]
    for price in cart_prices:
        dict={
        
            'price':price.prezzo.stripe_price_id,
            'quantity':price.quantity,
        }
        dict2={
            'product':price.prezzo.product.pk,
            'price':price.prezzo.stripe_price_id,
            'quantity':price.quantity,
        }
        line_items.append(dict)
        line_tests.append(dict2)
    products=[line_test['product'] for line_test in line_tests]
    quantities=[str(line_test['quantity']) for line_test in line_tests]
    
    domain = "https://pangeahydroponics.com"
    if settings.DEBUG:
        domain = "http://127.0.0.1:8000"
    checkout_session = stripe.checkout.Session.create(
        shipping_address_collection={"allowed_countries": ["US", "IT"]},
        payment_method_types=['card'],
        line_items=line_items,
        metadata={
            "product":str(products),
            "quantities": str(quantities),
        },
        mode='payment',
        success_url=domain + '/success/',
        cancel_url=domain + '/cancel/',
    )
    return redirect(checkout_session.url)




