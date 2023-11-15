from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from marketplace.context_processors import get_cart_count
from marketplace.models import Cart
from menu.models import Category, Product
from vendor.models import Vendor
from django.db.models import Prefetch
from django.contrib.auth.decorators import login_required

# Create your views here.
def marketplace(request):
    vendors = Vendor.objects.filter(is_approved=True, user__is_active=True)
    vendor_count = vendors.count()
    context = {
        'vendors':vendors,
        'vendor_count':vendor_count,
    }
    return render(request, 'marketplace/vendors.html', context)


def vendorPage(request, vendor_slug):
    vendor = get_object_or_404(Vendor, vendor_slug=vendor_slug)
    categories = Category.objects.filter(vendor=vendor).prefetch_related(
        Prefetch(
            'products',
            queryset = Product.objects.filter(is_available=True)
        )
    )
    if request.user.is_authenticated:
        cart_items = Cart.objects.filter(user=request.user)
    else:
        cart_items = None
    context = {
        'vendor':vendor,
        'categories':categories,
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/vendorPage.html', context)


def addToCart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the product exists
            try:
                product = Product.objects.get(id=product_id)
                # Check if item is already added to the cart:
                try: 
                    checkCart = Cart.objects.get(user=request.user, product=product)
                    # Increase number of products in cart for products already in it
                    checkCart.quantity += 1
                    checkCart.save()
                    return JsonResponse({'status':'Success', 'message':'Increased number of items in the cart','cart_counter':get_cart_count(request)['cart_count'], 'qty':checkCart.quantity})
                except:
                    checkCart = Cart.objects.create(user=request.user, product=product, quantity=1)
                    return JsonResponse({'status':'Success', 'message':'The product was succesfully added', 'cart_counter':get_cart_count(request)['cart_count'],'qty':checkCart.quantity})
            except:
                return JsonResponse({'status': 'Failed', 'message':"This product doesn't exist"})
        else:
            return JsonResponse({'status': 'Failed', 'message':'Invalid request'})
    else: 
       return JsonResponse({'status': 'notAuthenticated', 'message':'Please login to add items to your cart'})
    

def removeFromCart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the product exists
            try:
                product = Product.objects.get(id=product_id)
                # Check if item is already added to the cart:
                try: 
                    checkCart = Cart.objects.get(user=request.user, product=product)
                    if checkCart.quantity > 1:
                        checkCart.quantity -= 1
                        checkCart.save()
                        return JsonResponse({'status':'Success', 'message':'Decreased number of items in the cart','cart_counter':get_cart_count(request)['cart_count'], 'qty':checkCart.quantity})
                    else:
                        checkCart.delete()
                        checkCart.quantity = 0
                        return JsonResponse({'status':'Success', 'message':'The product was succesfully removed', 'cart_counter':get_cart_count(request)['cart_count'],'qty':0})
                except:
                    return JsonResponse({'status': 'Failed', 'message':"This product isn't in your cart"})
            except:
                return JsonResponse({'status': 'Failed', 'message':"This product doesn't exist"})
        else:
            return JsonResponse({'status': 'Failed', 'message':'Invalid request'})
    else: 
       return JsonResponse({'status': 'notAuthenticated', 'message':'Please login to remove items from your cart'})
    
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    context = {
        'cart_items':cart_items,
    }
    return render(request, 'marketplace/cart.html', context)


def deleteCart(request, product_id):
    if request.user.is_authenticated:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            # Check if the product exists
            try:
                cart_item = Cart.objects.get(id=product_id)
                cart_item.delete()
                return JsonResponse({'status':'Success', 'message':'The product was succesfully removed', 'cart_counter':get_cart_count(request)['cart_count']})
            except:
                return JsonResponse({'status': 'Failed', 'message':"This product isn't in your cart"})
        else:
            return JsonResponse({'status': 'Failed', 'message':'Invalid request'})
    else: 
       return JsonResponse({'status': 'notAuthenticated', 'message':'Please login to remove items from your cart'})