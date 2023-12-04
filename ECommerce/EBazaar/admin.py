from django.contrib import admin
from .models import User,Category, Product, Cart, CartItem, Order, OrderItem, Review, Wishlist, Wholesaler, Auction, Bid, Collection
# Register your models here.
admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Wholesaler)
admin.site.register(Auction)
admin.site.register(Bid)
admin.site.register(Collection)