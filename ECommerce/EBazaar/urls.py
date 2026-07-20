from django.urls import path
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

from . import views
from .forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm


app_name = "EBazaar"

urlpatterns = [
    path("", views.home, name="home"),
    path("catalog/", views.product_list, name="catalog"),
    path("category/<slug:slug>/", views.product_list, name="category"),
    path("product/<slug:slug>/", views.product_detail, name="product_detail"),
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("accounts/register/", views.register, name="register"),
    path(
        "accounts/password-reset/",
        auth_views.PasswordResetView.as_view(
            form_class=PasswordResetForm,
            template_name="EBazaar/account/password_reset_form.html",
            email_template_name="EBazaar/account/password_reset_email.txt",
            subject_template_name="EBazaar/account/password_reset_subject.txt",
            success_url=reverse_lazy("EBazaar:password_reset_done"),
        ),
        name="password_reset",
    ),
    path(
        "accounts/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="EBazaar/account/password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "accounts/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            form_class=SetPasswordForm,
            template_name="EBazaar/account/password_reset_confirm.html",
            success_url=reverse_lazy("EBazaar:password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),
    path(
        "accounts/reset/complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="EBazaar/account/password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    path(
        "accounts/password-change/",
        auth_views.PasswordChangeView.as_view(
            form_class=PasswordChangeForm,
            template_name="EBazaar/account/password_change_form.html",
            success_url=reverse_lazy("EBazaar:password_change_done"),
        ),
        name="password_change",
    ),
    path(
        "accounts/password-change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="EBazaar/account/password_change_done.html"
        ),
        name="password_change_done",
    ),
    path("account/", views.account, name="account"),
    path("account/profile/", views.profile_edit, name="profile_edit"),
    path("account/address/add/", views.address_create, name="address_create"),
    path("account/address/<int:pk>/edit/", views.address_edit, name="address_edit"),
    path("account/address/<int:pk>/delete/", views.address_delete, name="address_delete"),
    path("cart/", views.cart_detail, name="cart"),
    path("cart/add/<int:product_id>/", views.cart_add, name="cart_add"),
    path("cart/item/<int:item_id>/update/", views.cart_update, name="cart_update"),
    path("cart/item/<int:item_id>/remove/", views.cart_remove, name="cart_remove"),
    path("wishlist/", views.wishlist_detail, name="wishlist"),
    path("wishlist/toggle/<int:product_id>/", views.wishlist_toggle, name="wishlist_toggle"),
    path("checkout/", views.checkout, name="checkout"),
    path("orders/", views.order_list, name="orders"),
    path("orders/<str:reference>/", views.order_detail, name="order_detail"),
    path("orders/<str:reference>/cancel/", views.order_cancel, name="order_cancel"),
    path("products/<int:product_id>/review/", views.review_product, name="review_product"),
    path("seller/", views.seller_dashboard, name="seller_dashboard"),
    path("seller/products/", views.seller_products, name="seller_products"),
    path("seller/products/add/", views.seller_product_create, name="seller_product_create"),
    path("seller/products/<int:pk>/edit/", views.seller_product_edit, name="seller_product_edit"),
    path("seller/products/<int:pk>/deactivate/", views.seller_product_deactivate, name="seller_product_deactivate"),
    path("seller/orders/", views.seller_orders, name="seller_orders"),
    path("health/", views.health, name="health"),
]
