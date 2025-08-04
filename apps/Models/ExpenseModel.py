from . import *

from .UserModel import User


EXPENSE_TYPE_CHOICES = [
    ("Rent", "Rent"),
    ("Salary", "Salary"),
    ("Equipment", "Equipment"),
    ("Other", "Other"),
]


class Expense(models.Model):
    expense_type = models.CharField(max_length=30, choices=EXPENSE_TYPE_CHOICES, blank=True, null=True)
    amount = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True, null=True)
    added_by = models.ForeignKey(to=User, on_delete=models.SET_NULL, related_name="expenses", blank=True, null=True)

    class Meta:
        verbose_name = _("Expense")
        verbose_name_plural = _("Expenses")

