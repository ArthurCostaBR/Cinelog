from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def index_view(request):
    return render(request, 'pages/index/index.html')

@login_required(login_url="/accounts/login/")
def home_view(request):
    return render(request, 'pages/home/home.html')

@login_required(login_url="/accounts/login/")
def profile_view(request):
    if request.method == "POST":
        button = request.POST.get("action")

        if button == "logout":
            logout(request)
            return redirect('pages:index')
    
    return render(request, 'pages/profile/profile.html')