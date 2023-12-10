from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import User,Category, Product, Cart, CartItem, Order, OrderItem, Review, Wishlist, Wholesaler, Auction, Bid, Collection
from django.contrib.auth.models import Group

# Create your views here.
def login_view(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("EBazaar:index"))
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
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

# def register(request):
#     if request.user.is_authenticated:
#         return HttpResponseRedirect(reverse("EBazaar:index"))
#     if request.method == "POST":
#         username = request.POST["username"]
#         email = request.POST["email"]
#         user_type = request.POST["user_type"]

#         # Ensure password matches confirmation
#         password = request.POST["password"]
#         confirmation = request.POST["confirmation"]
#         if password != confirmation:
#             return render(request, "EBazaar/register.html", {
#                 "message": "Passwords must match."
#             })

#         # Attempt to create new user
#         try:
#             user = User.objects.create_user(username, email, password, user_type=user_type)
#             user.save()
#         except IntegrityError:
#             return render(request, "EBazaar/register.html", {
#                 "message": "Username already taken."
#             })
#         login(request, user)
#         return HttpResponseRedirect(reverse("EBazaar:index"))
#     else:
#         return render(request, "EBazaar/register.html")

def register(request):
    # if request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse("EBazaar:index"))
    
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        user_type = request.POST["user_type"]
        company = request.POST["company_name"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "EBazaar/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create a new user
        try:
            user = User.objects.create_user(username, email, password, user_type=user_type)
            
            # Add the user to a group based on user_type
            if user_type == "Wholesaler":
                wholesaler_group = Group.objects.get(name="WholesalerGroup")
                user.groups.add(wholesaler_group)
                user.is_staff = True
                user.save()
                wholesaler = Wholesaler.objects.create(user_id=user,company_name=company)
                wholesaler.save()
            elif user_type == "Seller":
                seller_group = Group.objects.get(name="SellerGroup")
                user.groups.add(seller_group)
                user.is_staff = True
                user.save()

        except IntegrityError:
            return render(request, "EBazaar/register.html", {
                "message": "Username already taken."
            })

        # Log in the user
        login(request, user)
        cart = Cart.objects.create(user_id=user,total_amount=0.0)
        cart.save()

        # Redirect the Wholesaler to the admin page
        if user_type == "Wholesaler" or user_type == "Seller":
            return HttpResponseRedirect(reverse("admin:index"))
        else:
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

    # Display Slider
    sliders = Collection.objects.all()

    cart = Cart.objects.get(user_id=request.user.pk)
    cart_items = CartItem.objects.filter(cart_id=cart.pk)
    cart_products = [Product.objects.get(pk=item.product_id.pk) for item in cart_items]
    categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]
    zipped_data = zip(cart_products,cart_items)
    return render(request, "EBazaar/index.html",{
        "all_products":chunked_products,
        "all_categories":categories,
        "sliders":sliders,
        "cart":cart,
        "cart_products":cart_products,
        "cart_items":cart_items,
        "zipped_data":zipped_data
    })

def category(request, category_id):
    try:
        products = Product.objects.filter(category_id=category_id)
    except IntegrityError:
        products = "No Products Yet."
    total_products = products.count()
    chunked_products = [products[i:i+4] for i in range(0, total_products, 4)]

    cart = Cart.objects.get(user_id=request.user.pk)
    cart_items = CartItem.objects.filter(cart_id=cart.pk)
    cart_products = [Product.objects.get(pk=item.product_id.pk) for item in cart_items]
    categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]
    zipped_data = zip(cart_products,cart_items)
    return render(request, "EBazaar/product.html",{
        "all_products":chunked_products,
        "all_categories":categories,
        "cart":cart,
        "cart_products":cart_products,
        "cart_items":cart_items,
        "zipped_data":zipped_data
    })

def display_categories(request):
    cart = Cart.objects.get(user_id=request.user.pk)
    cart_items = CartItem.objects.filter(cart_id=cart.pk)
    cart_products = [Product.objects.get(pk=item.product_id.pk) for item in cart_items]
    categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]
    zipped_data = zip(cart_products,cart_items)
    return render(request, "EBazaar/all_categories.html",{
        "all_categories":categories,
        "cart":cart,
        "cart_products":cart_products,
        "cart_items":cart_items,
        "zipped_data":zipped_data
    })

def product_details(request,category_id,product_id):
    try:
        product = Product.objects.get(pk=product_id)
        category = Category.objects.get(pk=category_id)
        category_products = Product.objects.filter(category_id=category_id)
        total_products = category_products.count()
        chunked_products = [category_products[i:i+4] for i in range(0, total_products, 4)]

        cart = Cart.objects.get(user_id=request.user.pk)
        cart_items = CartItem.objects.filter(cart_id=cart.pk)
        cart_products = [Product.objects.get(pk=item.product_id.pk) for item in cart_items]
        categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]
        zipped_data = zip(cart_products,cart_items)
    except IntegrityError:
        product = "No Product Found"
        categories = "No Category Found"
    return render(request, "EBazaar/product-detail.html",{
        "product":product,
        "category":category,
        "all_products":chunked_products,
        "all_categories":categories,
        "cart_products":cart_products,
        "cart":cart,
        "cart_items":cart_items,
        "zipped_data":zipped_data
    })

def view_cart(request):
    # if request.method == 'POST':
    #     quantity = request.POST["num-product1"]
    #     update_cart = Cart.objects.get(user_id=request.user.pk)
    #     cart_items = CartItem.objects.get(cart_id=cart_)
    try:
        cart = Cart.objects.get(user_id=request.user.pk)
        cart_items = CartItem.objects.filter(cart_id=cart.pk)
        cart_products = [Product.objects.get(pk=item.product_id.pk) for item in cart_items]
        categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]
        zipped_data = zip(cart_products,cart_items)
    except IntegrityError:
        cart_items = "No Cart Items"
    for product, item in zipped_data:
        print(product.price)
        print(f"Hello {item.total_price}")
    return render(request, "EBazaar/shopping-cart.html",{
        "cart_products":cart_products,
        "all_categories":categories,
        "cart":cart,
        "cart_items":cart_items,
        "zipped_data":zipped_data
    })

def add_to_cart(request, product_id):
    total_quantity = 2
    product = Product.objects.get(pk=product_id)
    if request.method == "POST":
        total_quantity = request.POST["quantity"]
    try:
        new_cart = Cart.objects.get(user_id=request.user)
    except Cart.DoesNotExist:
        new_cart = Cart.objects.create(user_id=request.user,total_amount=0.0)
    
    new_cart_item = CartItem.objects.create(cart_id=new_cart,product_id=product,quantity=total_quantity,total_price=(int(total_quantity)*product.price))
    new_cart.total_amount += (int(total_quantity)*product.price)
    new_cart.save()
    new_cart_item.save()
    try:
        cart = Cart.objects.get(user_id=request.user.pk)
        cart_items = CartItem.objects.filter(cart_id=cart.pk)
        cart_products = [Product.objects.get(pk=item.product_id.pk) for item in cart_items]
        categories = [Category.objects.filter(pk=product.pk) for product in Product.objects.all()]
        zipped_data = zip(cart_products,cart_items)
    except IntegrityError:
        cart_items = "No Cart Items"
    print(cart_items)
    return render(request, "EBazaar/shopping-cart.html",{
        "cart_products":cart_products,
        "all_categories":categories,
        "cart":cart,
        "cart_items":cart_items,
        "zipped_data":zipped_data
    })