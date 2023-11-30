from .models import Cart
from menu.models import Product

def get_cart_count(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart_items = Cart.objects.filter(user=request.user)
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except:
            cart_count = 0
    return {'cart_count':cart_count}


def get_cart_total(request):
    sub_total = 0
    tax = 0
    grand_total = 0
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
        for cart_item in cart_items:
            sub_total += cart_item.product.price * cart_item.quantity

        grand_total = sub_total + tax
    return {'sub_total':sub_total, 'tax':tax, 'grand_total':grand_total}