from django.http import HttpResponse
from django.shortcuts import redirect,render
from .forms import UserForm
from .models import User
from django.contrib import messages


# Create your views here.
def registerUser(request):
    # Handle sign up process for customers
    if request.method == 'POST':
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
            messages.success(request, 'Your account has been registered successfully')
            return redirect('registerUser')
        else: 
            print(form.errors)
    else:
        form = UserForm()
    context = {'form':form}
    return render(request, 'accounts/registerUser.html', context)