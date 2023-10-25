from django.http import HttpResponse
from django.shortcuts import redirect,render
from .forms import UserForm
from .models import User


# Create your views here.
def registerUser(request):
    # Handle sign up process for customers
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = User.CUSTOMER
            form.save()
            return redirect('registerUser')
    else:
        form = UserForm()
    context = {'form':form}
    return render(request, 'accounts/registerUser.html', context)