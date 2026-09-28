from django.urls import path

from . import views

app_name = "expenses"

urlpatterns = [
    # Auth
    path("register/", views.SignUpView.as_view(), name="register"),
    path("login/", views.UserLoginView.as_view(), name="login"),
    path("logout/", views.UserLogoutView.as_view(), name="logout"),
    # Dashboard
    path("", views.dashboard, name="dashboard"),
    # Expenses
    path("expenses/", views.expense_list, name="expense_list"),
    path("expenses/add/", views.expense_create, name="expense_add"),
    path("expenses/<int:pk>/", views.ExpenseDetailView.as_view(), name="detail"),
    path("expenses/<int:pk>/edit/", views.expense_update, name="expense_edit"),
    path(
        "expenses/<int:pk>/delete/",
        views.ExpenseDeleteView.as_view(),
        name="expense_delete",
    ),
    # Budgets
    path("budgets/", views.budgets, name="budgets"),
    # Categories
    path("categories/", views.category_list, name="categories"),
    path(
        "categories/<int:pk>/delete/",
        views.CategoryDeleteView.as_view(),
        name="category_delete",
    ),
]
