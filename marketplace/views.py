from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from menu.models import Category, Product
from vendor.models import Vendor
from django.db.models import Prefetch

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
    context = {
        'vendor':vendor,
        'categories':categories,
    }
    return render(request, 'marketplace/vendorPage.html', context)


def addToCart(request, product_id):
    return HttpResponse(product_id)