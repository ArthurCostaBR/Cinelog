from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm
from django.contrib.auth import authenticate, login, get_user_model

def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        
        if form.is_valid():
            User = get_user_model()

            email = form.cleaned_data.get("email")

            if User.objects.filter(email__iexact=email).exists():
                form.add_error("email", "Email already in use.")
            else:
                user = form.save()
                login(request, user)
                return redirect("catalog:home")
        
        return render(request, 'signup/signup.html', context={"form":form})

    return render(request, 'signup/signup.html', context={"form":SignupForm()})
        

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = authenticate(request, email=email, password=password)
        
            if user is not None:
                login(request, user)
                return redirect('catalog:home')

            else:
                form.add_error(None, "Invalid credentials.")

        return render(request, 'login/login.html', context={"form": form})

    return render(request, 'login/login.html', context={"form": LoginForm()})