from decimal import Decimal
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


def order_reference() -> str:
    return f"EBZ-{uuid.uuid4().hex[:10].upper()}"


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        SELLER = "seller", "Seller"
        WHOLESALER = "wholesaler", "Wholesaler"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    phone = models.CharField(max_length=30, blank=True)

    @property
    def display_name(self) -> str:
        return self.get_full_name() or self.username

    @property
    def can_sell(self) -> bool:
        return self.is_superuser or self.role in {self.Role.SELLER, self.Role.WHOLESALER}


class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="categories/", blank=True)
    is_active = models.BooleanField(default=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("EBazaar:category", kwargs={"slug": self.slug})


class Collection(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=120, unique=True)
    tagline = models.CharField(max_length=180, blank=True)
    image = models.ImageField(upload_to="collections/", blank=True)
    products = models.ManyToManyField("Product", related_name="collections", blank=True)
    is_active = models.BooleanField(default=True)
    starts_at = models.DateTimeField(blank=True, null=True)
    ends_at = models.DateTimeField(blank=True, null=True)
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["display_order", "name"]

    def __str__(self) -> str:
        return self.name

    @property
    def is_live(self) -> bool:
        now = timezone.now()
        return (
            self.is_active
            and (self.starts_at is None or self.starts_at <= now)
            and (self.ends_at is None or self.ends_at >= now)
        )


class Product(models.Model):
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="products",
    )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    name = models.CharField(max_length=160)
    slug = models.SlugField(max_length=190, unique=True, blank=True)
    sku = models.CharField("SKU", max_length=40, unique=True)
    brand = models.CharField(max_length=80, blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=12, decimal_places=2)
    compare_at_price = models.DecimalField(
        max_digits=12, decimal_places=2, blank=True, null=True
    )
    stock = models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=5)
    weight_kg = models.DecimalField(
        max_digits=8, decimal_places=3, blank=True, null=True
    )
    image = models.ImageField(upload_to="products/", blank=True)
    sizes = models.JSONField(default=list, blank=True)
    colors = models.JSONField(default=list, blank=True)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["slug"], name="ebz_product_slug_idx"),
            models.Index(fields=["sku"], name="ebz_product_sku_idx"),
            models.Index(fields=["is_active", "-created_at"], name="ebz_product_active_idx"),
            models.Index(fields=["category", "is_active"], name="ebz_product_cat_idx"),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(price__gte=0), name="product_price_gte_0"),
            models.CheckConstraint(condition=Q(stock__gte=0), name="product_stock_gte_0"),
        ]

    def __str__(self) -> str:
        return f"{self.name} ({self.sku})"

    def save(self, *args, **kwargs):
        self.sku = self.sku.strip().upper()
        if not self.slug:
            base = slugify(self.name)[:150] or self.sku.lower()
            candidate = base
            counter = 2
            while Product.objects.exclude(pk=self.pk).filter(slug=candidate).exists():
                candidate = f"{base}-{counter}"
                counter += 1
            self.slug = candidate
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("EBazaar:product_detail", kwargs={"slug": self.slug})

    @property
    def in_stock(self) -> bool:
        return self.is_active and self.stock > 0

    @property
    def is_low_stock(self) -> bool:
        return 0 < self.stock <= self.low_stock_threshold

    @property
    def discount_percent(self) -> int:
        if not self.compare_at_price or self.compare_at_price <= self.price:
            return 0
        return round((1 - self.price / self.compare_at_price) * 100)


class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=40, default="Home")
    full_name = models.CharField(max_length=120)
    phone = models.CharField(max_length=30)
    line1 = models.CharField("Address", max_length=180)
    line2 = models.CharField("Apartment, suite, etc.", max_length=180, blank=True)
    city = models.CharField(max_length=80)
    state = models.CharField(max_length=80, blank=True)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=80, default="Pakistan")
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-is_default", "-created_at"]

    def __str__(self) -> str:
        return f"{self.label}: {self.full_name}, {self.city}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.is_default:
            Address.objects.filter(user=self.user, is_default=True).exclude(pk=self.pk).update(
                is_default=False
            )


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Cart for {self.user}"

    @property
    def subtotal(self) -> Decimal:
        return sum((item.subtotal for item in self.items.select_related("product")), Decimal("0.00"))

    @property
    def item_count(self) -> int:
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="cart_items")
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        constraints = [
            models.UniqueConstraint(fields=["cart", "product"], name="unique_cart_product"),
            models.CheckConstraint(condition=Q(quantity__gte=1), name="cart_quantity_gte_1"),
        ]

    def __str__(self) -> str:
        return f"{self.quantity} × {self.product.name}"

    @property
    def subtotal(self) -> Decimal:
        return self.product.price * self.quantity


class Coupon(models.Model):
    class DiscountType(models.TextChoices):
        PERCENT = "percent", "Percentage"
        FIXED = "fixed", "Fixed amount"

    code = models.CharField(max_length=30, unique=True)
    discount_type = models.CharField(max_length=10, choices=DiscountType.choices)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_order_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    active = models.BooleanField(default=True)
    valid_from = models.DateTimeField(blank=True, null=True)
    valid_until = models.DateTimeField(blank=True, null=True)
    max_uses = models.PositiveIntegerField(blank=True, null=True)
    times_used = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["code"]
        constraints = [
            models.CheckConstraint(condition=Q(value__gte=0), name="coupon_value_gte_0"),
        ]

    def __str__(self) -> str:
        return self.code

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def is_valid_for(self, subtotal: Decimal) -> bool:
        now = timezone.now()
        return (
            self.active
            and subtotal >= self.minimum_order_amount
            and (self.valid_from is None or self.valid_from <= now)
            and (self.valid_until is None or self.valid_until >= now)
            and (self.max_uses is None or self.times_used < self.max_uses)
        )

    def discount_for(self, subtotal: Decimal) -> Decimal:
        if not self.is_valid_for(subtotal):
            return Decimal("0.00")
        if self.discount_type == self.DiscountType.PERCENT:
            discount = subtotal * self.value / Decimal("100")
        else:
            discount = self.value
        return min(discount.quantize(Decimal("0.01")), subtotal)


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        CONFIRMED = "confirmed", "Confirmed"
        PROCESSING = "processing", "Processing"
        SHIPPED = "shipped", "Shipped"
        DELIVERED = "delivered", "Delivered"
        CANCELLED = "cancelled", "Cancelled"

    class PaymentMethod(models.TextChoices):
        COD = "cod", "Cash on delivery"
        BANK = "bank", "Bank transfer"

    class PaymentStatus(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    reference = models.CharField(max_length=20, default=order_reference, unique=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    contact_email = models.EmailField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING
    )
    shipping_name = models.CharField(max_length=120)
    shipping_phone = models.CharField(max_length=30)
    shipping_line1 = models.CharField(max_length=180)
    shipping_line2 = models.CharField(max_length=180, blank=True)
    shipping_city = models.CharField(max_length=80)
    shipping_state = models.CharField(max_length=80, blank=True)
    shipping_postal_code = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=80)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    shipping_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2)
    customer_note = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["reference"], name="ebz_order_ref_idx"),
            models.Index(fields=["user", "-created_at"], name="ebz_order_user_date_idx"),
        ]

    def __str__(self) -> str:
        return self.reference

    @property
    def can_cancel(self) -> bool:
        return self.status in {self.Status.PENDING, self.Status.CONFIRMED}


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True, related_name="order_items"
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="sold_order_items",
    )
    product_name = models.CharField(max_length=160)
    sku = models.CharField(max_length=40)
    quantity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    line_total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.quantity} × {self.product_name}"

    def save(self, *args, **kwargs):
        self.line_total = self.unit_price * self.quantity
        super().save(*args, **kwargs)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=120, blank=True)
    body = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["product", "user"], name="one_review_per_product_user"),
        ]

    def __str__(self) -> str:
        return f"{self.product.name}: {self.rating}/5 by {self.user}"


class Wishlist(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wishlist"
    )
    products = models.ManyToManyField(Product, related_name="wishlists", blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Wishlist for {self.user}"
