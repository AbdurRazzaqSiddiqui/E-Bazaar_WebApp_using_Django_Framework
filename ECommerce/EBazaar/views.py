from django.shortcuts import render
from django.http import HttpResponse
from .models import User,Category, Product, Cart, CartItem, Order, OrderItem, Reviews, Wishlist, Wholesaler, Auction, Bid

# Create your views here.
def index(request):
    return render(request, "EBazaar/index.html")