from . import *

from .UserModel import User

MONTH_CHOICES = [
    ("January", "January"),
    ("February", "February"),
    ("March", "March"),
    ("April", "April"),
    ("May", "May"),
    ("June", "June"),
    ("July", "July"),
    ("August", "August"),
    ("September", "September"),
    ("October", "October"),
    ("November", "November"),
    ("December", "December"),
]


class Payment(models.Model):
    student = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="payments", blank=True, null=True)

    month = models.CharField(max_length=25, choices=MONTH_CHOICES, default=MONTH_CHOICES[0][0])
    year = models.PositiveIntegerField(default=2025)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    paid_at = models.DateTimeField(auto_now_add=True)
    is_cash = models.BooleanField(default=True)
    comment = models.TextField(blank=True, null=True)



