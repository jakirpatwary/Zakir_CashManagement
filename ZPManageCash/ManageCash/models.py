from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models


class AddCash(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="cash_entries",
    )
    source = models.CharField(max_length=100)
    datetime = models.DateTimeField()
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-datetime", "-id"]
        verbose_name = "Cash Entry"
        verbose_name_plural = "Cash Entries"

    def __str__(self):
        return f"{self.source} - {self.amount}"


class Expense(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="expense_entries",
    )
    description = models.CharField(max_length=200)
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    datetime = models.DateTimeField()

    class Meta:
        ordering = ["-datetime", "-id"]

    def __str__(self):
        return f"{self.description} - {self.amount}"
