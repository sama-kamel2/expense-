from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Category, Expense
from .translations import DEFAULT_LANGUAGE, translate


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": "form-control"})


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["amount", "category", "date", "description"]
        widgets = {
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "step": "0.01", "min": "0"}
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            # ISO format is required by <input type="date"> in every language.
            "date": forms.DateInput(
                format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
            ),
            "description": forms.TextInput(attrs={"class": "form-control"}),
        }

    def __init__(self, *args, user=None, lang=DEFAULT_LANGUAGE, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(user=user)
        self.fields["category"].required = False
        self.fields["category"].empty_label = translate("uncategorized", lang)


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "color"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "color": forms.TextInput(
                attrs={"class": "form-control form-control-color", "type": "color"}
            ),
        }

    def __init__(self, *args, user=None, lang=DEFAULT_LANGUAGE, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user
        self._lang = lang

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        if (
            self._user is not None
            and Category.objects.filter(user=self._user, name__iexact=name).exists()
        ):
            raise forms.ValidationError(translate("category_exists", self._lang))
        return name


class BudgetAmountForm(forms.Form):
    """One amount field, used for the overall budget and every category budget."""

    amount = forms.DecimalField(
        max_digits=12,
        decimal_places=2,
        min_value=0,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "step": "0.01", "min": "0"}
        ),
    )


class ExpenseFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.none(),
        required=False,
        widget=forms.Select(attrs={"class": "form-select"}),
    )
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
        ),
    )
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(
            format="%Y-%m-%d", attrs={"class": "form-control", "type": "date"}
        ),
    )
    q = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )

    def __init__(self, *args, user=None, lang=DEFAULT_LANGUAGE, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields["category"].queryset = Category.objects.filter(user=user)
        self.fields["category"].empty_label = translate("all_categories", lang)
        self.fields["q"].widget.attrs["placeholder"] = translate("search_placeholder", lang)
