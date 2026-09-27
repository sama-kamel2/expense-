from django.conf import settings
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Expense category, scoped per user so each user manages their own list."""

    name = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    color = models.CharField(
        max_length=7,
        default="#4f46e5",
        help_text="Hex color used for charts/badges, e.g. #4f46e5",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name_plural = "Categories"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name"], name="unique_category_per_user"
            )
        ]

    def __str__(self):
        return self.name


class Expense(models.Model):
    """A single expense entry belonging to a user."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="expenses",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="expenses",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "date"]),
            models.Index(fields=["user", "category"]),
        ]

    def __str__(self):
        return f"{self.description or 'Expense'} - {self.amount}"

    def get_absolute_url(self):
        return reverse("expenses:detail", kwargs={"pk": self.pk})
