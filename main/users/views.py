from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='/accounts/login/')
def profile_view(request):
    if request.method == "POST":
        button = request.POST.get("action")

        if button == "logout":
            logout(request)

            return redirect('accounts:login')

    return render(request, 'profile/profile.html')