from django.urls import path
from apps.users.views import LoginView, LogoutView
from . import views


urlpatterns = [
    path("notifications/notifications-form-actions/", views.archive_all_notifications, name="notifications_form_actions"),
    path("notifications/archive/<int:pk>", views.archive_notification, name="archive_notification"),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("user-qr-image/<int:pk>/qr.png", views.user_qr_image, name="user_qr_image"),
]



