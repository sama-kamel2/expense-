from datetime import date

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, LogoutView
from django.db.models import Sum, Count
from django.db.models.functions import TruncMonth
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, UpdateView

from .forms import BudgetAmountForm, CategoryForm, ExpenseFilterForm, ExpenseForm, RegisterForm
from .models import Budget, Category, Expense


def _budget_summary(user):
    """
    Budget logic (per month):
      * Each category budget is RESERVED from the overall budget immediately.
      * Spending inside a category only reduces that category's own remaining.
      * The overall remaining is reduced only by (a) spending in categories
        that have no budget, and (b) the overflow beyond a category's budget.
    """
    today = date.today()
    month_expenses = Expense.objects.filter(
        user=user, date__year=today.year, date__month=today.month
    )

    category_rows = []
    reserved = 0
    overflow = 0
    budgeted_category_ids = []

    category_budgets = Budget.objects.filter(
        user=user, category__isnull=False
    ).select_related("category")
    for b in category_budgets:
        spent = (
            month_expenses.filter(category=b.category).aggregate(total=Sum("amount"))[
                "total"
            ]
            or 0
        )
        remaining = b.amount - spent
        percent = min(100, int((spent / b.amount) * 100)) if b.amount else 0
        reserved += b.amount
        if remaining < 0:
            overflow += -remaining
        budgeted_category_ids.append(b.category_id)
        category_rows.append(
            {
                "category": b.category,
                "amount": b.amount,
                "spent": spent,
                "remaining": remaining,
                "over_amount": -remaining if remaining < 0 else 0,
                "percent": percent,
                "over": remaining < 0,
            }
        )

    # Spending that is not covered by any category budget
    # (categories without a budget, or expenses with no category).
    unbudgeted_spent = (
        month_expenses.exclude(category_id__in=budgeted_category_ids).aggregate(
            total=Sum("amount")
        )["total"]
        or 0
    )

    overall_budget = Budget.objects.filter(user=user, category=None).first()
    overall = None
    if overall_budget:
        used = reserved + overflow + unbudgeted_spent
        remaining = overall_budget.amount - used
        percent = min(100, int((used / overall_budget.amount) * 100)) if overall_budget.amount else 0
        overall = {
            "amount": overall_budget.amount,
            "reserved": reserved,
            "overflow": overflow,
            "unbudgeted_spent": unbudgeted_spent,
            "free_pool": overall_budget.amount - reserved,
            "remaining": remaining,
            "over_amount": -remaining if remaining < 0 else 0,
            "percent": percent,
            "over": remaining < 0,
        }

    return overall, category_rows


# ---------- Auth ----------

class SignUpView(CreateView):
    form_class = RegisterForm
    template_name = "expenses/register.html"
    success_url = reverse_lazy("expenses:login")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "تم إنشاء الحساب بنجاح، سجّل دخولك الآن.")
        return response


class UserLoginView(LoginView):
    template_name = "expenses/login.html"
    redirect_authenticated_user = True


class UserLogoutView(LogoutView):
    next_page = reverse_lazy("expenses:login")


# ---------- Dashboard ----------

@login_required
def dashboard(request):
    user = request.user
    expenses = Expense.objects.filter(user=user)

    today = date.today()
    total_all_time = expenses.aggregate(total=Sum("amount"))["total"] or 0
    monthly_qs = expenses.filter(date__year=today.year, date__month=today.month)
    total_this_month = monthly_qs.aggregate(total=Sum("amount"))["total"] or 0

    category_stats = (
        expenses.values("category__name", "category__color")
        .annotate(total=Sum("amount"), count=Count("id"))
        .order_by("-total")
    )

    monthly_breakdown = (
        expenses.annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(total=Sum("amount"))
        .order_by("-month")[:6]
    )

    recent_expenses = expenses.select_related("category")[:8]

    overall_budget, category_budgets = _budget_summary(user)

    context = {
        "total_all_time": total_all_time,
        "total_this_month": total_this_month,
        "expense_count": expenses.count(),
        "category_stats": category_stats,
        "monthly_breakdown": monthly_breakdown,
        "recent_expenses": recent_expenses,
        "categories": Category.objects.filter(user=user),
        "overall_budget": overall_budget,
        "category_budgets": category_budgets,
    }
    return render(request, "expenses/dashboard.html", context)


# ---------- Expense CRUD ----------

@login_required
def expense_list(request):
    user = request.user
    expenses = Expense.objects.filter(user=user).select_related("category")
    form = ExpenseFilterForm(request.GET or None, user=user)

    if form.is_valid():
        category = form.cleaned_data.get("category")
        date_from = form.cleaned_data.get("date_from")
        date_to = form.cleaned_data.get("date_to")
        query = form.cleaned_data.get("q")

        if category:
            expenses = expenses.filter(category=category)
        if date_from:
            expenses = expenses.filter(date__gte=date_from)
        if date_to:
            expenses = expenses.filter(date__lte=date_to)
        if query:
            expenses = expenses.filter(description__icontains=query)

    total = expenses.aggregate(total=Sum("amount"))["total"] or 0

    return render(
        request,
        "expenses/expense_list.html",
        {"expenses": expenses, "form": form, "total": total},
    )


class ExpenseDetailView(DetailView):
    model = Expense
    template_name = "expenses/expense_detail.html"
    context_object_name = "expense"

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)


@login_required
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST, user=request.user)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, "تمت إضافة المصروف بنجاح.")
            return redirect("expenses:dashboard")
    else:
        form = ExpenseForm(user=request.user, initial={"date": date.today()})
    return render(
        request, "expenses/expense_form.html", {"form": form, "title": "إضافة مصروف"}
    )


@login_required
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "تم تعديل المصروف بنجاح.")
            return redirect("expenses:dashboard")
    else:
        form = ExpenseForm(instance=expense, user=request.user)
    return render(
        request, "expenses/expense_form.html", {"form": form, "title": "تعديل مصروف"}
    )


class ExpenseDeleteView(DeleteView):
    model = Expense
    template_name = "expenses/expense_confirm_delete.html"
    success_url = reverse_lazy("expenses:dashboard")

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

    def form_valid(self, form):
        messages.success(self.request, "تم حذف المصروف.")
        return super().form_valid(form)


# ---------- Categories ----------

@login_required
def category_list(request):
    categories = Category.objects.filter(user=request.user)
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            messages.success(request, "تمت إضافة التصنيف.")
            return redirect("expenses:categories")
    else:
        form = CategoryForm()
    return render(
        request,
        "expenses/category_list.html",
        {"categories": categories, "form": form},
    )


class CategoryDeleteView(DeleteView):
    model = Category
    template_name = "expenses/category_confirm_delete.html"
    success_url = reverse_lazy("expenses:categories")


# ---------- Budgets ----------

@login_required
def budgets(request):
    user = request.user

    if request.method == "POST":
        amount = request.POST.get("amount")
        scope = request.POST.get("scope")  # "overall" or a category id
        form = BudgetAmountForm({"amount": amount})
        if form.is_valid():
            clean_amount = form.cleaned_data["amount"]
            if scope == "overall":
                Budget.objects.update_or_create(
                    user=user, category=None, defaults={"amount": clean_amount}
                )
                messages.success(request, "تم تحديث الميزانية الكلية.")
            else:
                category = get_object_or_404(Category, pk=scope, user=user)
                Budget.objects.update_or_create(
                    user=user, category=category, defaults={"amount": clean_amount}
                )
                messages.success(request, f"تم تحديث ميزانية {category.name}.")
        else:
            messages.error(request, "قيمة الميزانية غير صحيحة.")
        return redirect("expenses:budgets")

    overall_budget, category_budgets = _budget_summary(user)

    # Categories that don't have a budget yet, so the user can add one.
    budgeted_category_ids = [row["category"].id for row in category_budgets]
    categories_without_budget = Category.objects.filter(user=user).exclude(
        id__in=budgeted_category_ids
    )

    return render(
        request,
        "expenses/budgets.html",
        {
            "overall_budget": overall_budget,
            "category_budgets": category_budgets,
            "categories_without_budget": categories_without_budget,
        },
    )

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
