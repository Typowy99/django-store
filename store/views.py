from django.shortcuts import render, redirect
from .models import Product
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


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