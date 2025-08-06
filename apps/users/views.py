from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


class LoginView(View):
    def get(self,request):
        return render(request, 'users/auth-basic-login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to dashboard on success
        else:
            messages.error(request, "Invalid username or password.")

        return render(request, "login.html")