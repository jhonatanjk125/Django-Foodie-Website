from django.shortcuts import get_object_or_404, redirect, render
from accounts.views import check_vendor_role
from menu.forms import CategoryForm, ProductForm
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
    categories = Category.objects.filter(vendor=vendor).order_by('created_at')
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


@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def addCategory(request):
    """ Handles the request to add a new category """
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


@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def editCategory(request, pk=None):
    """ Handles the request to edit a category """
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category_name = form.cleaned_data['category_name']
            category  = form.save(commit=False)
            category.vendor = get_vendor(request)
            category.slug = slugify(category_name)
            form.save()
            messages.success(request, 'Category updated successfully!')
            return redirect('menuBuilder')
    else:
        form = CategoryForm(instance=category)
    context = {
        'form': form,
        'category': category,
    }
    return render(request, 'vendor/editCategory.html', context)


@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def deleteCategory(request, pk=None):
    """ Handles the request to delete a category """
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    messages.success(request, 'Category has been deleted successfully')
    return redirect('menuBuilder')


@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def addProduct(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product_title = form.cleaned_data['product_title']
            product  = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug = slugify(product_title)
            form.save()
            messages.success(request, 'Category added successfully!')
            return redirect('categories', product.category.id)
    else:
        form = ProductForm()
    context = {
        'form': form,
    }
    return render(request,'vendor/addProduct.html', context)


@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def editProduct(request, pk=None):
    """ Handles the request to edit a product """
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product_title = form.cleaned_data['product_title']
            product  = form.save(commit=False)
            product.vendor = get_vendor(request)
            product.slug = slugify(product_title)
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('categories', product.category.id)
    else:
        form = ProductForm(instance=product)
    context = {
        'form': form,
        'product': product,
    }
    return render(request, 'vendor/editProduct.html', context)


@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def deleteProduct(request, pk=None):
    """ Handles the request to delete a category """
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    messages.success(request, 'Product has been deleted successfully')
    return redirect('categories', product.category.id)