from django.urls import path
from .views import ManagerHomeView, QRScannerView, check_scanned_QR

urlpatterns = [
    path('', ManagerHomeView.as_view(), name='ManagerHome'),
    path("scanner/", QRScannerView.as_view(), name="qr_scanner"),
    path("scanner/check/", check_scanned_QR, name="check_scanned_QR"),
]
