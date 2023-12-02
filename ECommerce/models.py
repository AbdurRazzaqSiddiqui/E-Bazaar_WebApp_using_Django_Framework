# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('EbazaarUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EbazaarAuction(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_bid = models.FloatField()
    current_highest_bid = models.FloatField()
    status = models.IntegerField()
    product_id = models.ForeignKey('EbazaarProduct', models.DO_NOTHING)
    wholesaler_id = models.ForeignKey('EbazaarWholesaler', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_auction'


class EbazaarBid(models.Model):
    id = models.BigAutoField(primary_key=True)
    bid_amount = models.FloatField()
    bid_time = models.DateTimeField()
    auction_id = models.ForeignKey(EbazaarAuction, models.DO_NOTHING)
    wholsaler_id = models.ForeignKey('EbazaarWholesaler', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_bid'


class EbazaarCart(models.Model):
    id = models.BigAutoField(primary_key=True)
    created_at = models.DateTimeField()
    user_id = models.ForeignKey('EbazaarUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_cart'


class EbazaarCartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField()
    total_price = models.FloatField()
    cart_id = models.ForeignKey(EbazaarCart, models.DO_NOTHING)
    product_id = models.ForeignKey('EbazaarProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_cart_item'


class EbazaarCategory(models.Model):
    id = models.BigAutoField(primary_key=True)
    category_name = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ebazaar_category'


class EbazaarOrder(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_date = models.DateTimeField()
    status = models.CharField(max_length=20)
    total_amount = models.FloatField()
    user_id = models.ForeignKey('EbazaarUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_order'


class EbazaarOrderItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    quantity = models.IntegerField()
    unit_price = models.FloatField()
    product_id = models.ForeignKey('EbazaarProduct', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_order_item'


class EbazaarOrderItemOrderId(models.Model):
    id = models.BigAutoField(primary_key=True)
    order_item = models.ForeignKey(EbazaarOrderItem, models.DO_NOTHING)
    order = models.ForeignKey(EbazaarOrder, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_order_item_order_id'
        unique_together = (('order_item', 'order'),)


class EbazaarProduct(models.Model):
    id = models.BigAutoField(primary_key=True)
    product_name = models.CharField(max_length=20)
    description = models.CharField(max_length=20)
    image_url = models.CharField(max_length=200)
    price = models.IntegerField()
    quantity = models.IntegerField()
    category_id = models.ForeignKey(EbazaarCategory, models.DO_NOTHING)
    seller_id = models.ForeignKey('EbazaarUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_product'


class EbazaarReviews(models.Model):
    id = models.BigAutoField(primary_key=True)
    rating = models.IntegerField()
    review_text = models.CharField(max_length=50)
    created_at = models.DateTimeField()
    product_id = models.ForeignKey(EbazaarProduct, models.DO_NOTHING)
    user_id = models.ForeignKey('EbazaarUser', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_reviews'


class EbazaarUser(models.Model):
    id = models.BigAutoField(primary_key=True)
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    user_type = models.CharField(max_length=20)

    class Meta:
        managed = False
        db_table = 'ebazaar_user'


class EbazaarUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(EbazaarUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_user_groups'
        unique_together = (('user', 'group'),)


class EbazaarUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(EbazaarUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_user_user_permissions'
        unique_together = (('user', 'permission'),)


class EbazaarWholesaler(models.Model):
    id = models.BigAutoField(primary_key=True)
    company_name = models.CharField(max_length=20)
    user_id = models.ForeignKey(EbazaarUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_wholesaler'


class EbazaarWishlist(models.Model):
    id = models.BigAutoField(primary_key=True)
    user_id = models.ForeignKey(EbazaarUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_wishlist'


class EbazaarWishlistProducts(models.Model):
    id = models.BigAutoField(primary_key=True)
    wishlist = models.ForeignKey(EbazaarWishlist, models.DO_NOTHING)
    product = models.ForeignKey(EbazaarProduct, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'ebazaar_wishlist_products'
        unique_together = (('wishlist', 'product'),)
