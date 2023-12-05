from django.urls import path
from . import views

app_name = "EBazaar"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:category_id>", views.index, name="index"),
    path("category/<int:category_id>", views.category, name="category"),
    path("categories", views.display_categories, name="all_categories"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
