from django.urls import path
from . import views

app_name = "EBazaar"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:category_id>", views.index, name="index"),
    path("category/<int:category_id>/products", views.category, name="category"),
    path("category/<int:category_id>/product/<int:product_id>", views.product_details, name="product_details"),
    path("category/<int:category_id>", views.category, name="category"),
    path("categories", views.display_categories, name="all_categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("your-cart", views.view_cart, name="view_cart")
]
