from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Address, Cart, CartItem, Category, Collection, Coupon, Order, OrderItem, Product, Review, User, Wishlist


@admin.register(User)
class StoreUserAdmin(UserAdmin):
    list_display = ("username", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + (("Store profile", {"fields": ("role", "phone")}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Store profile", {"fields": ("email", "role", "phone")}),)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "display_order")
    list_editable = ("is_active", "display_order")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ("name", "is_active", "starts_at", "ends_at", "display_order")
    list_filter = ("is_active",)
    list_editable = ("is_active", "display_order")
    prepopulated_fields = {"slug": ("name",)}
    filter_horizontal = ("products",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "category", "seller", "price", "stock", "is_active", "is_featured")
    list_filter = ("is_active", "is_featured", "category")
    list_editable = ("price", "stock", "is_active", "is_featured")
    search_fields = ("name", "sku", "brand", "seller__username")
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("seller", "category")
    readonly_fields = ("created_at", "updated_at")


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ("user", "updated_at")
    search_fields = ("user__username", "user__email")
    inlines = (CartItemInline,)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product_name", "sku", "quantity", "unit_price", "line_total", "seller")
    can_delete = False


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("reference", "user", "status", "payment_status", "total", "created_at")
    list_filter = ("status", "payment_status", "payment_method", "created_at")
    list_editable = ("status", "payment_status")
    search_fields = ("reference", "user__username", "contact_email", "shipping_name")
    readonly_fields = (
        "reference",
        "user",
        "subtotal",
        "discount_amount",
        "shipping_amount",
        "total",
        "created_at",
        "updated_at",
    )
    inlines = (OrderItemInline,)


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "discount_type", "value", "active", "times_used", "max_uses", "valid_until")
    list_filter = ("active", "discount_type")
    search_fields = ("code",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "is_approved", "created_at")
    list_filter = ("rating", "is_approved")
    list_editable = ("is_approved",)
    search_fields = ("product__name", "user__username", "title", "body")


admin.site.register(Address)
admin.site.register(Wishlist)
