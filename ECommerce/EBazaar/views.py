from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Category, Product, Cart, CartItem, Order, OrderItem, Review, Wishlist, Wholesaler, Auction, Bid, Collection

# Create your views here.
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            try:
                Watchlist.objects.get(user=request.user)
            except Watchlist.DoesNotExist:
                watchlist = Watchlist.objects.create(user=request.user)
                watchlist.save()
            return HttpResponseRedirect(reverse("EBazaar:index"))
        else:
            return render(request, "EBazaar/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "EBazaar/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("EBazaar:index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "EBazaar/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            watchlist = Watchlist.objects.create(user=request.user)
            user.save()
            watchlist.save()
        except IntegrityError:
            return render(request, "EBazaar/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("EBazaar:index"))
    else:
        return render(request, "EBazaar/register.html")

def index(request, category_id=None):
    # Display all Products
    try:
        if category_id is None:
            products = Product.objects.all()
        else:
            products = Product.objects.filter(category_id=category_id)
        total_products = products.count()
        chunked_products = [products[i:i+4] for i in range(0, total_products, 4)]

    except IntegrityError:
        products = "No Products Yet."
        
    # Display Category List
    categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]

    # Display Slider
    sliders = Collection.objects.all()

    return render(request, "EBazaar/index.html",{
        "all_products":chunked_products,
        "all_categories":categories,
        "sliders":sliders
    })

def category(request, category_id):
    try:
        products = Product.objects.filter(category_id=category_id)
    except IntegrityError:
        products = "No Products Yet."
    total_products = products.count()
    chunked_products = [products[i:i+4] for i in range(0, total_products, 4)]
    categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]
    return render(request, "EBazaar/product.html",{
        "all_products":chunked_products,
        "all_categories":categories
    })

def display_categories(request):
    categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]
    return render(request, "EBazaar/all_categories.html",{
        "all_categories":categories
    })