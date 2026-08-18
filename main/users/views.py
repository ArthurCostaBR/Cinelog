from django.shortcuts import render
from . forms import SignupForm, LoginForm

def signup(request):
    form = {
        "form": SignupForm(),
    }
    if request.method == "GET":
        return render(request, 'signup/signup.html', form)
    else:
        pass

def login(request):
    form = {
        "form": LoginForm()
    }
    if request.method == "GET":
        return render(request, 'login/login.html', form)
    else:
        pass