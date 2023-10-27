from django.http import HttpResponse
from django.shortcuts import redirect,render
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, sendVerificationEmail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied

#Restrict customers from accessing vendor dashboard
def check_customer_role(user):
    if user.role == 2:
        return True
    else:
        redirect('vendorDashboard')
    

# Restrict vendors from accessing customer dashboard
def check_vendor_role(user):
    if user.role == 1:
        return True
    else:
        redirect('customerDashboard')
    
    
def registerUser(request):
    """Handle sign up process for customers"""
        # Handle users who are already authenticated
    if request.user.is_authenticated:
        messages.warning(request, "You're already logged in!")
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            email = email.lower()
            user = form.save(commit=False)
            user.set_password(password)
            user.email = email
            user.role = User.CUSTOMER
            form.save()
            sendVerificationEmail(request,user)
            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else: 
            print(form.errors)
    else:
        form = UserForm()
    context = {'form':form}
    return render(request, 'accounts/registerUser.html', context)


def registerVendor(request):
    """Handle sign up process for vendors"""
     # Handle users who are already authenticated
    if request.user.is_authenticated:
        messages.warning(request, "You're already logged in")
        return redirect('myAccount')
    elif request.method == 'POST':
        form = UserForm(request.POST)
        vendor_form = VendorForm(request.POST, request.FILES)
        if form.is_valid() and vendor_form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            user.role = User.VENDOR
            user.save()
            vendor = vendor_form.save(commit=False)
            vendor.user = user
            user_profile = UserProfile.objects.get(user=user)
            vendor.user_profile = user_profile
            vendor.save()
            sendVerificationEmail(request,user)
            messages.success(request, 'Your account has been registered successfully and is pending approval')
            return redirect('registerVendor')            
    else: 
        form = UserForm()
        vendor_form = VendorForm()
    context = {
        'form':form,
        'vendor_form':vendor_form,
    }
    return render(request, 'accounts/registerVendor.html', context)


def login(request):
    """ Handles the view for the log in screen """
    # Handle users who are already authenticated
    if request.user.is_authenticated:
        messages.warning(request, "You're already logged in")
        return redirect('myAccount')
    elif request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, "You've succesfully logged in")
            return redirect('myAccount')
        else:
            messages.error(request, 'Incorrect login details, please check the email or pasword')
            return redirect('login')
    context = {}
    return render(request, 'accounts/login.html', context)


def logout(request):
    auth.logout(request)
    messages.info(request, "You've sucessfully logged out")
    context = {}
    return redirect('login')


@login_required(login_url='login')
def myAccount(request):
    user = request.user
    redirectUrl = detectUser(user)
    return redirect(redirectUrl)


@login_required(login_url='login')
@user_passes_test(check_customer_role)
def customerDashboard(request):
    context = {}
    return render(request, 'accounts/customerDashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_vendor_role)
def vendorDashboard(request):
    context = {}
    return render(request, 'accounts/vendorDashboard.html', context)

def activate(request, uidb64, token):
    """ Activate user via confirmation link by setting is_active status to true"""
    return