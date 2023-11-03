from django.shortcuts import get_object_or_404, redirect, render
from accounts.views import check_vendor_role
from menu.forms import CategoryForm
from .forms import VendorForm
from accounts.forms import UserProfileForm
from accounts.models import UserProfile
from .models import Vendor
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from menu.models import Category, Product
from .utils import get_vendor
from django.template.defaultfilters import slugify


# Create your views here.
@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def vendorProfile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    vendor = get_object_or_404(Vendor, user=request.user)
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request, 'Information updated')
            return redirect('vendorProfile')
        else:
            pass
    else:
        profile_form = UserProfileForm(instance=profile)
        vendor_form = VendorForm(instance=vendor)
    
    context = {
        'profile_form': profile_form,
        'vendor_form': vendor_form,
        'profile': profile,
        'vendor': vendor,
    }
    return render(request, 'vendor/vendorProfile.html', context)

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def menuBuilder(request):
    vendor = get_vendor(request)
    categories = Category.objects.filter(vendor=vendor)
    context = {
        'categories': categories,
    }
    return render(request, 'vendor/menuBuilder.html', context)

@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def categories(request, pk=None):
    vendor = get_vendor(request)
    category = get_object_or_404(Category, pk=pk)
    products = Product.objects.filter(vendor=vendor, category=category)
    context = {
        'category': category,
        'products': products,
    }
    return render(request, 'vendor/item_by_category.html', context)

def addCategory(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category  = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('menuBuilder')
    else:
        form = CategoryForm()
    context = {
        'form':form,
    }
    return render(request, 'vendor/addCategory.html', context)