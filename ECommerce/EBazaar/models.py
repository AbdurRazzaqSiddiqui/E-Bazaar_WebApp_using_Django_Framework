from django.db import models
from django.contrib.auth.models import AbstractUser

USER_TYPE = [
    ('user1', 'Wholesaler'),
    ('user2', 'Seller'),
    ('user3', 'Customer'),
]

class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=USER_TYPE, default='user3')

class Category(models.Model):
    category_name = models.CharField(max_length=20, blank=False)

    def __str__(self):
        return f"ID:{self.pk}, Name: {self.category_name}"

class Collection(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, name="collection_category")
    collection_name = models.CharField(max_length=20, blank=False)
    image = models.CharField(max_length=100, blank=False)

    def __str__(self):
        return f"Name: {self.collection_name}"
    

class Product(models.Model):
    product_name = models.CharField(max_length=20, blank=False)
    description = models.CharField(max_length=20, blank=False)
    image = models.CharField(max_length=100, blank=False)
    price = models.FloatField()
    quantity = models.IntegerField()
    seller_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="product_seller")
    category_id = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="product_category")
    
    def __str__(self):
        return f"ID: {self.pk}, Name: {self.product_name}, Category ID: {self.category_id} Price: {self.price}"
    
class Cart(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="cart_user")
    created_at = models.DateTimeField(auto_now=True)
# auto_now=True //For object updation time
# auto_now_add=True //For object creation time
    def __str__(self):
        return f"ID: {self.pk}, TimeStamp: {self.created_at}"

class CartItem(models.Model):
    cart_id = models.ForeignKey(Cart, on_delete=models.DO_NOTHING, related_name="cart_item_id")
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="cart_product")
    quantity = models.IntegerField()
    total_price = models.FloatField()

STATUS_CHOICES = [
    ('status1', 'Processing'),
    ('status2', 'Shipped'),
    ('status3', 'Delivered'),
]

class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="order_user")
    order_date = models.DateTimeField(auto_now_add=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='status1')
    total_amount = models.FloatField()

    def __str__(self):
        return f"ID: {self.pk}, Delivery Date: {self.order_date}"
    
class OrderItem(models.Model):
    order_id = models.ManyToManyField(Order)
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="order_product")
    quantity = models.IntegerField()
    unit_price = models.FloatField()

    def __str__(self):
        return f"ID: {self.pk}, Product ID: {self.product_id}, Quantity: {self.quantity}, Unit Price: {self.unit_price}, Total Price: {self.quantity * self.unit_price}"

class Review(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="review_product")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_user")
    rating = models.IntegerField()
    review_text = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"ID: {self.pk}, User ID: {self.user_id}, Ratings: {self.rating}"

class Wishlist(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.DO_NOTHING, related_name="wishlist_user")
    products = models.ManyToManyField(Product)

class Wholesaler(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="wholesaler")
    company_name = models.CharField(max_length=20)

    def __str__(self):
        return f"ID: {self.pk}, User ID: {self.user_id}, Company Name: {self.company_name}"
    
class Auction(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.DO_NOTHING, related_name="auction_product_id")
    wholesaler_id = models.ForeignKey(Wholesaler, on_delete=models.DO_NOTHING, related_name="auctioner")
    start_time = models.DateTimeField(auto_now=True)
    end_time = models.DateTimeField(auto_now=True)
    starting_bid = models.FloatField()
    current_highest_bid = models.FloatField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"ID: {self.pk},Product ID: {self.product_id}, Auctioner: {self.wholesaler_id}, Status: {self.status}"

class Bid(models.Model):
    auction_id = models.ForeignKey(Auction, on_delete=models.DO_NOTHING, related_name="bid_auction") 
    wholsaler_id = models.ForeignKey(Wholesaler, on_delete=models.DO_NOTHING, related_name="bid_user")
    bid_amount = models.FloatField()
    bid_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"ID: {self.pk}, User ID:{self.user_id}, Bidding Price: {self.bid_amount}"