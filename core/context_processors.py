from store.models import Cart
from django.contrib.auth.models import User

def cart_number_to_base(request):
    if request.user.is_authenticated:
        cart_objs=Cart.objects.filter(user=request.user)
        sum=0
        for obj in cart_objs:
            sum+=obj.quantity
        return {'somma':sum}
    else:
        sum=0
        return {'somma':sum}