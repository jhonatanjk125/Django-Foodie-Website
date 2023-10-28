from django.http import HttpResponse
from django.shortcuts import redirect,render
from vendor.forms import VendorForm
from .forms import UserForm
from .models import User, UserProfile
from django.contrib import messages, auth
from .utils import detectUser, getUserFromPK, sendVerificationEmail
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.exceptions import PermissionDenied
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

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
            email_subject='Please confirm your email address'
            email_template='accounts/emails/verification_email.html'
            sendVerificationEmail(request,user, email_subject, email_template)
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
            email_subject='Please confirm your email address'
            email_template='accounts/emails/verification_email.html'
            sendVerificationEmail(request,user, email_subject, email_template)
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
    user, uid = getUserFromPK(uidb64)
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account has been activated')
        return redirect('myAccount')
    else:
        messages.error(request, 'Invalid activation link')
        return redirect('myAccount')
    

def forgotPassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        if User.objects.filter(email=email).exists:
            user = User.objects.get(email__exact=email)
            email_subject = 'Reset password'
            email_template = 'accounts/emails/reset_password_email.html'
            sendVerificationEmail(request, user, email_subject, email_template)
            messages.success(request, 'A reset link has been sent to your email address')
            return redirect('login')
        else:
            messages.error(request, "An account with the email you entered doesn't exist")
            return redirect('forgotPassword')
    return render(request, 'accounts/forgotPassword.html')


def resetPasswordValidate(request, uidb64, token):
    """Validate user by decoding user primary key and token"""
    user, uid = getUserFromPK(uidb64)

    if user is not None and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.info(request, 'Please reset your password')
        return redirect('resetPassword')
    else:
        messages.error(request, 'This link has expired')
        return redirect('myAccount')

def resetPassword(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            pk = request.session.get('uid')
            user = User.objects.get(pk=pk)
            user.set_password(password)
            user.is_active = True
            user.save()
            messages.success(request, 'Your password has been sucessfully changed')
            return redirect('login')
        else: 
            messages.error(request, "Passwords don't match")
            return redirect('resetPassword')
        
    return render(request, 'accounts/resetPassword.html')