from django.contrib import admin

from .models import Category, Expense


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "color", "created_at")
    list_filter = ("user",)
    search_fields = ("name", "user__username")


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("description", "amount", "category", "user", "date")
    list_filter = ("category", "date", "user")
    search_fields = ("description", "user__username")
    date_hierarchy = "date"
    autocomplete_fields = ("category",)
