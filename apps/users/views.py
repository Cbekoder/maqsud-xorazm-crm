from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
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

