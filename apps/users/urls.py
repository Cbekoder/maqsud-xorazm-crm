from django.urls import path
from . import views


urlpatterns = [
    path("notifications/notifications-form-actions/", views.archive_all_notifications, name="notifications_form_actions"),
    path("notifications/archive/<int:pk>", views.archive_notification, name="archive_notification"),
]
