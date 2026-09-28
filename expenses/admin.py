from django.contrib import admin

from .models import Budget, Category, Expense, Profile


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


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("user", "category", "amount", "updated_at")
    list_filter = ("user",)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "language", "theme")
    list_filter = ("language", "theme")
