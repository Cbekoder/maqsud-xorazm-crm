from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages


class LoginView(View):
    def get(self, request):
        return render(request, 'users/auth-login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            next_url = request.GET.get('next')

            if next_url and self._is_safe_url(next_url, request):
                return redirect(next_url)

            return self._redirect_by_role(user)
        else:
            messages.error(request, "Invalid username or password.")

        return render(request, "users/auth-login.html")

    def _redirect_by_role(self, user):
        """Redirect user to appropriate homepage based on their role"""
        role = user.role

        if role == "manager":
            return redirect('/manager/')  # Admin dashboard
        elif role == "teacher":
            return redirect('/teacher/')  # Teachers dashboard
        elif role == "student":
            return redirect('/student/')  # Students homepage (root URL)
        elif role == "parent":
            return redirect('/parent/')  # Parents dashboard
        else:
            # Default fallback
            return redirect('/')

    def _is_safe_url(self, url, request):
        """Check if the URL is safe to redirect to"""

        return url_has_allowed_host_and_scheme(
            url=url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        )


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
