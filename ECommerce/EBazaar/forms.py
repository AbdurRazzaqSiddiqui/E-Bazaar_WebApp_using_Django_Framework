from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm as DjangoPasswordChangeForm,
    PasswordResetForm as DjangoPasswordResetForm,
    SetPasswordForm as DjangoSetPasswordForm,
    UserCreationForm,
)

from .models import Address, Order, Product, Review, User


class StyledFormMixin:
    """Apply consistent classes without coupling the forms to a CSS framework."""

    def _style_fields(self):
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"form-control {existing}".strip()
            if field.label and not isinstance(field.widget, (forms.CheckboxInput, forms.RadioSelect)):
                field.widget.attrs.setdefault("placeholder", field.label)


class LoginForm(StyledFormMixin, AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class PasswordResetForm(StyledFormMixin, DjangoPasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class SetPasswordForm(StyledFormMixin, DjangoSetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class PasswordChangeForm(StyledFormMixin, DjangoPasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class RegistrationForm(StyledFormMixin, UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "role",
            "password1",
            "password2",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["role"].help_text = "Choose Seller or Wholesaler to manage a product catalog."
        self._style_fields()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class ProfileForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()

    def clean_email(self):
        email = self.cleaned_data["email"].strip().lower()
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class AddressForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Address
        fields = (
            "label",
            "full_name",
            "phone",
            "line1",
            "line2",
            "city",
            "state",
            "postal_code",
            "country",
            "is_default",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class CartQuantityForm(StyledFormMixin, forms.Form):
    quantity = forms.IntegerField(min_value=1, initial=1)

    def __init__(self, *args, max_stock=None, **kwargs):
        super().__init__(*args, **kwargs)
        if max_stock is not None:
            self.fields["quantity"].max_value = max_stock
            self.fields["quantity"].widget.attrs["max"] = max_stock
        self.fields["quantity"].widget.attrs.update({"min": 1, "inputmode": "numeric"})
        self._style_fields()


class CheckoutForm(StyledFormMixin, forms.Form):
    address = forms.ModelChoiceField(
        queryset=Address.objects.none(), required=False, empty_label="Use a new address"
    )
    payment_method = forms.ChoiceField(choices=Order.PaymentMethod.choices)
    coupon_code = forms.CharField(max_length=30, required=False)
    customer_note = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={"rows": 3}),
        help_text="Optional delivery instructions.",
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.is_authenticated:
            self.fields["address"].queryset = user.addresses.all()
            self.fields["address"].initial = user.addresses.filter(is_default=True).first()
        self._style_fields()

    def clean_coupon_code(self):
        return self.cleaned_data["coupon_code"].strip().upper()


class ReviewForm(StyledFormMixin, forms.ModelForm):
    class Meta:
        model = Review
        fields = ("rating", "title", "body")
        widgets = {
            "rating": forms.Select(choices=[(value, f"{value} star{'s' if value > 1 else ''}") for value in range(5, 0, -1)]),
            "body": forms.Textarea(attrs={"rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._style_fields()


class ProductForm(StyledFormMixin, forms.ModelForm):
    MAX_IMAGE_BYTES = 4 * 1024 * 1024
    ALLOWED_IMAGE_TYPES = {"image/jpeg", "image/png", "image/webp"}
    sizes_text = forms.CharField(
        required=False, label="Sizes", help_text="Comma-separated, for example: S, M, L"
    )
    colors_text = forms.CharField(
        required=False, label="Colors", help_text="Comma-separated, for example: Black, Blue"
    )

    class Meta:
        model = Product
        fields = (
            "category",
            "name",
            "sku",
            "brand",
            "description",
            "price",
            "compare_at_price",
            "stock",
            "low_stock_threshold",
            "weight_kg",
            "image",
            "is_active",
        )
        widgets = {"description": forms.Textarea(attrs={"rows": 6})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["sizes_text"].initial = ", ".join(self.instance.sizes)
            self.fields["colors_text"].initial = ", ".join(self.instance.colors)
        self._style_fields()

    def clean(self):
        cleaned = super().clean()
        price = cleaned.get("price")
        compare_at_price = cleaned.get("compare_at_price")
        if price is not None and compare_at_price is not None and compare_at_price <= price:
            self.add_error("compare_at_price", "The original price must be higher than the sale price.")
        return cleaned

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and hasattr(image, "content_type"):
            if image.size > self.MAX_IMAGE_BYTES:
                raise forms.ValidationError("Upload a product image no larger than 4 MB.")
            if image.content_type not in self.ALLOWED_IMAGE_TYPES:
                raise forms.ValidationError("Use a JPEG, PNG, or WebP product image.")
        return image

    def save(self, commit=True):
        product = super().save(commit=False)
        product.sizes = [value.strip() for value in self.cleaned_data["sizes_text"].split(",") if value.strip()]
        product.colors = [value.strip() for value in self.cleaned_data["colors_text"].split(",") if value.strip()]
        if commit:
            product.save()
        return product
