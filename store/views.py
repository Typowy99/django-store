from django.shortcuts import render, redirect
from .models import Product

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .forms import SignUpForm


def index(request):
    products = Product.objects.all()
    return render(request, 'store/index.html', {
        "products" : products
    })


def about(request):
    return render(request, 'store/about.html')


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            messages.success(request, ("You have been logged in."))
            return redirect('index')
        else:
            messages.success(request, ("There was an error, please try again!"))
            return redirect('login')
    else:
        return render(request, "store/login.html")


def logout_view(request):
    logout(request)
    messages.success(request, ("You have been logged out."))
    return redirect('index')


def register_view(request):
    # Initialize a SignUpForm instance
    form = SignUpForm()

    if request.method == "POST":
        # Bind form with POST data
        form = SignUpForm(request.POST)
        
        # Check if form data is valid
        if form.is_valid():
            # Save form data to create a new user
            form.save()
            
            # Get username and password for authentication
            password = form.cleaned_data["password1"]
            username = form.cleaned_data["username"]
            
            # Authenticate the user
            user = authenticate(password=password, username=username)
            
            # Log in the user
            login(request, user)
            
            # Add success message
            messages.success(request, ("You have Registered Successfully!"))
            
            # Redirect to 'index' page
            return redirect('index')
        else:
            # If form data is not valid, redirect back to 'register' page with error message
            messages.success(request, ("There was a problem, try again!"))
            return redirect('register')
    else:
        # If request method is not POST, render the 'register' page with an empty form
        return render(request, 'store/register.html', { 'form': form })
