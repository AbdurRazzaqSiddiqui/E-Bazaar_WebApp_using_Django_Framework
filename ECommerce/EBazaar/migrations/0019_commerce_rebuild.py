"""Rebuild the coursework schema into a transactional commerce schema.

The original prototype committed database files and had no safe data migration
path (including an order-item many-to-many relationship). User accounts are
preserved and normalized; prototype catalog/order data is intentionally reset.
"""

import EBazaar.models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


def normalize_roles(apps, schema_editor):
    User = apps.get_model("EBazaar", "User")
    role_map = {"user1": "wholesaler", "user2": "seller", "user3": "customer"}
    for old_value, new_value in role_map.items():
        User.objects.filter(role=old_value).update(role=new_value)


class Migration(migrations.Migration):
    dependencies = [("EBazaar", "0018_product_colors_product_sizes")]

    operations = [
        migrations.DeleteModel(name="Bid"),
        migrations.DeleteModel(name="Auction"),
        migrations.DeleteModel(name="Wholesaler"),
        migrations.DeleteModel(name="Wishlist"),
        migrations.DeleteModel(name="Review"),
        migrations.DeleteModel(name="OrderItem"),
        migrations.DeleteModel(name="Order"),
        migrations.DeleteModel(name="CartItem"),
        migrations.DeleteModel(name="Cart"),
        migrations.DeleteModel(name="Collection"),
        migrations.DeleteModel(name="Product"),
        migrations.DeleteModel(name="Category"),
        migrations.RenameField(model_name="user", old_name="user_type", new_name="role"),
        migrations.AlterField(
            model_name="user",
            name="role",
            field=models.CharField(
                choices=[
                    ("customer", "Customer"),
                    ("seller", "Seller"),
                    ("wholesaler", "Wholesaler"),
                ],
                default="customer",
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name="user",
            name="phone",
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.RunPython(normalize_roles, migrations.RunPython.noop),
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True)),
                ("slug", models.SlugField(max_length=100, unique=True)),
                ("description", models.TextField(blank=True)),
                ("image", models.ImageField(blank=True, upload_to="categories/")),
                ("is_active", models.BooleanField(default=True)),
                ("display_order", models.PositiveIntegerField(default=0)),
            ],
            options={"verbose_name_plural": "categories", "ordering": ["display_order", "name"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=160)),
                ("slug", models.SlugField(blank=True, max_length=190, unique=True)),
                ("sku", models.CharField(max_length=40, unique=True, verbose_name="SKU")),
                ("brand", models.CharField(blank=True, max_length=80)),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("compare_at_price", models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ("stock", models.PositiveIntegerField(default=0)),
                ("low_stock_threshold", models.PositiveIntegerField(default=5)),
                ("weight_kg", models.DecimalField(blank=True, decimal_places=3, max_digits=8, null=True)),
                ("image", models.ImageField(blank=True, upload_to="products/")),
                ("sizes", models.JSONField(blank=True, default=list)),
                ("colors", models.JSONField(blank=True, default=list)),
                ("is_active", models.BooleanField(default=True)),
                ("is_featured", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="EBazaar.category")),
                ("seller", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["slug"], name="ebz_product_slug_idx"),
                    models.Index(fields=["sku"], name="ebz_product_sku_idx"),
                    models.Index(fields=["is_active", "-created_at"], name="ebz_product_active_idx"),
                    models.Index(fields=["category", "is_active"], name="ebz_product_cat_idx"),
                ],
                "constraints": [
                    models.CheckConstraint(condition=models.Q(("price__gte", 0)), name="product_price_gte_0"),
                    models.CheckConstraint(condition=models.Q(("stock__gte", 0)), name="product_stock_gte_0"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Collection",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100)),
                ("slug", models.SlugField(max_length=120, unique=True)),
                ("tagline", models.CharField(blank=True, max_length=180)),
                ("image", models.ImageField(blank=True, upload_to="collections/")),
                ("is_active", models.BooleanField(default=True)),
                ("starts_at", models.DateTimeField(blank=True, null=True)),
                ("ends_at", models.DateTimeField(blank=True, null=True)),
                ("display_order", models.PositiveIntegerField(default=0)),
                ("products", models.ManyToManyField(blank=True, related_name="collections", to="EBazaar.product")),
            ],
            options={"ordering": ["display_order", "name"]},
        ),
        migrations.CreateModel(
            name="Address",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("label", models.CharField(default="Home", max_length=40)),
                ("full_name", models.CharField(max_length=120)),
                ("phone", models.CharField(max_length=30)),
                ("line1", models.CharField(max_length=180, verbose_name="Address")),
                ("line2", models.CharField(blank=True, max_length=180, verbose_name="Apartment, suite, etc.")),
                ("city", models.CharField(max_length=80)),
                ("state", models.CharField(blank=True, max_length=80)),
                ("postal_code", models.CharField(max_length=20)),
                ("country", models.CharField(default="Pakistan", max_length=80)),
                ("is_default", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="addresses", to=settings.AUTH_USER_MODEL)),
            ],
            options={"ordering": ["-is_default", "-created_at"]},
        ),
        migrations.CreateModel(
            name="Cart",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="cart", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="CartItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("quantity", models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("cart", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="EBazaar.cart")),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="cart_items", to="EBazaar.product")),
            ],
            options={
                "ordering": ["created_at"],
                "constraints": [
                    models.UniqueConstraint(fields=("cart", "product"), name="unique_cart_product"),
                    models.CheckConstraint(condition=models.Q(("quantity__gte", 1)), name="cart_quantity_gte_1"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Coupon",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("code", models.CharField(max_length=30, unique=True)),
                ("discount_type", models.CharField(choices=[("percent", "Percentage"), ("fixed", "Fixed amount")], max_length=10)),
                ("value", models.DecimalField(decimal_places=2, max_digits=10)),
                ("minimum_order_amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("active", models.BooleanField(default=True)),
                ("valid_from", models.DateTimeField(blank=True, null=True)),
                ("valid_until", models.DateTimeField(blank=True, null=True)),
                ("max_uses", models.PositiveIntegerField(blank=True, null=True)),
                ("times_used", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["code"],
                "constraints": [models.CheckConstraint(condition=models.Q(("value__gte", 0)), name="coupon_value_gte_0")],
            },
        ),
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("reference", models.CharField(default=EBazaar.models.order_reference, editable=False, max_length=20, unique=True)),
                ("contact_email", models.EmailField(max_length=254)),
                ("status", models.CharField(choices=[("pending", "Pending"), ("confirmed", "Confirmed"), ("processing", "Processing"), ("shipped", "Shipped"), ("delivered", "Delivered"), ("cancelled", "Cancelled")], default="pending", max_length=20)),
                ("payment_method", models.CharField(choices=[("cod", "Cash on delivery"), ("bank", "Bank transfer")], max_length=20)),
                ("payment_status", models.CharField(choices=[("pending", "Pending"), ("paid", "Paid"), ("failed", "Failed"), ("refunded", "Refunded")], default="pending", max_length=20)),
                ("shipping_name", models.CharField(max_length=120)),
                ("shipping_phone", models.CharField(max_length=30)),
                ("shipping_line1", models.CharField(max_length=180)),
                ("shipping_line2", models.CharField(blank=True, max_length=180)),
                ("shipping_city", models.CharField(max_length=80)),
                ("shipping_state", models.CharField(blank=True, max_length=80)),
                ("shipping_postal_code", models.CharField(max_length=20)),
                ("shipping_country", models.CharField(max_length=80)),
                ("subtotal", models.DecimalField(decimal_places=2, max_digits=12)),
                ("discount_amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("shipping_amount", models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ("total", models.DecimalField(decimal_places=2, max_digits=12)),
                ("customer_note", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("coupon", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to="EBazaar.coupon")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="orders", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["reference"], name="ebz_order_ref_idx"),
                    models.Index(fields=["user", "-created_at"], name="ebz_order_user_date_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=160)),
                ("sku", models.CharField(max_length=40)),
                ("quantity", models.PositiveIntegerField(validators=[MinValueValidator(1)])),
                ("unit_price", models.DecimalField(decimal_places=2, max_digits=12)),
                ("line_total", models.DecimalField(decimal_places=2, max_digits=12)),
                ("order", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="EBazaar.order")),
                ("product", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="order_items", to="EBazaar.product")),
                ("seller", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="sold_order_items", to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])),
                ("title", models.CharField(blank=True, max_length=120)),
                ("body", models.TextField()),
                ("is_approved", models.BooleanField(default=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="EBazaar.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to=settings.AUTH_USER_MODEL)),
            ],
            options={
                "ordering": ["-created_at"],
                "constraints": [models.UniqueConstraint(fields=("product", "user"), name="one_review_per_product_user")],
            },
        ),
        migrations.CreateModel(
            name="Wishlist",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("products", models.ManyToManyField(blank=True, related_name="wishlists", to="EBazaar.product")),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="wishlist", to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
