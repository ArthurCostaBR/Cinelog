from django.shortcuts import render, redirect
from . forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        
        if form.is_valid():
            User = get_user_model()

            email = form.cleaned_data.get("email")

            if User.objects.filter(email__iexact=email).exists():
                form.add_error("email", "Email already in use.")
            else:
                form.save()
                return redirect('users:login')
        
        return render(request, 'users/signup/signup.html', context={"form":form})

    else:
        return render(request, 'users/signup/signup.html', context={"form":SignupForm()})
        

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, email=email, password=password)
        
            if user:
                login(request, user)
                return redirect('pages:home')

            else:
                form.add_error(None, "Invalid credentials.")

        return render(request, 'users/login/login.html', context={"form": form})

    return render(request, 'users/login/login.html', context={"form": LoginForm()})

@login_required(login_url='users/login/login.html')
def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('pages:index')