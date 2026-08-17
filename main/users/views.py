from django.shortcuts import render

def signup(request):
    return render(request, 'signup/signup.html')

def login(request):
    return render(request, 'login/login.html')