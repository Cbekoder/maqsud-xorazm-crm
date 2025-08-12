from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST

from models import UserNotification, User


@login_required
@require_POST
def archive_all_notifications(request):
    action = request.POST.get("action")

    if action == "archive-all-notifications":
        UserNotification.objects.filter(user=request.user).update(is_archived=True)
    elif action == "mark-as-read-all-notifications":
        UserNotification.objects.filter(user=request.user).update(is_read=True)
    elif action == "turn-off-user-notification":
        User.objects.update(notification_enabled=False)
    elif action == "turn-on-user-notification":
        User.objects.update(notification_enabled=True)

    return redirect(request.META.get("HTTP_REFERER", "/"))


@login_required
@require_POST
def archive_notification(request, pk):
    notification = get_object_or_404(
        UserNotification,
        pk=pk,
        user=request.user
    )

    notification.is_archived = True
    notification.save()
    return redirect(request.META.get("HTTP_REFERER", "/"))


class LoginView(View):
    def get(self, request):
        return render(request, 'users/auth-login.html')

    def post(self, request):
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Get the next parameter from query string
            next_url = request.GET.get('next')

            # If next parameter is provided and it's safe, redirect there
            if next_url and self._is_safe_url(next_url, request):
                return redirect(next_url)

            # Otherwise, redirect based on user role
            return self._redirect_by_role(user)
        else:
            messages.error(request, "Invalid username or password.")

        return render(request, "users/auth-login.html")

    def _redirect_by_role(self, user):
        """Redirect user to appropriate homepage based on their role"""
        role = user.role

        if role == "managers":
            return redirect('/managers/')  # Admin dashboard
        elif role == "teachers":
            return redirect('/teachers/')  # Teachers dashboard
        elif role == "students":
            return redirect('/')  # Students homepage (root URL)
        elif role == "parent":
            return redirect('/parents/')  # Parents dashboard
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

