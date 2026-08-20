from django.shortcuts import render, redirect
from . forms import SignupForm, LoginForm
from django.contrib.auth import get_user_model, authenticate, login
from django.http import HttpResponse


def signup_view(request):
    form = {
        "form": SignupForm(),
    }

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password2")

        User = get_user_model()

        if User.objects.filter(email__iexact=email).exists():
            return HttpResponse("A user already exists with same email.")

        User.objects.create_user(
            username=username, 
            email=email, 
            password=password,
        )

        return redirect('/account/login/')

    return render(request, 'signup/signup.html', form)

def login_view(request):
    form = {
        "form": LoginForm()
    }

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return HttpResponse(f"Welcome {user.username}.")

        return HttpResponse("Invalid credentials.")

    return render(request, 'login/login.html', form)