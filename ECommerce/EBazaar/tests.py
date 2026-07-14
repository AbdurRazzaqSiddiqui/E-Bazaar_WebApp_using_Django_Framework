from decimal import Decimal
from io import StringIO
from tempfile import TemporaryDirectory

from django.core import mail
from django.core.management import call_command
from django.db import IntegrityError
from django.test import TestCase
from django.urls import reverse

from .models import Address, Cart, CartItem, Category, Coupon, Order, OrderItem, Product, Review, User, Wishlist
from .services import CheckoutError, calculate_totals, cancel_order, create_order


class StoreFixture(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.seller = User.objects.create_user(
            username="seller",
            email="seller@example.com",
            password="StrongPass123!",
            role=User.Role.SELLER,
        )
        cls.other_seller = User.objects.create_user(
            username="other-seller",
            email="other@example.com",
            password="StrongPass123!",
            role=User.Role.SELLER,
        )
        cls.customer = User.objects.create_user(
            username="customer",
            email="customer@example.com",
            password="StrongPass123!",
            role=User.Role.CUSTOMER,
        )
        cls.other_customer = User.objects.create_user(
            username="other-customer",
            email="other-customer@example.com",
            password="StrongPass123!",
        )
        cls.category = Category.objects.create(
            name="Electronics", slug="electronics", description="Useful technology"
        )
        cls.product = Product.objects.create(
            seller=cls.seller,
            category=cls.category,
            name="Wireless Headphones",
            sku="audio-001",
            description="Comfortable wireless headphones with clear sound.",
            price=Decimal("80.00"),
            compare_at_price=Decimal("100.00"),
            stock=10,
            is_active=True,
            is_featured=True,
        )
        cls.other_product = Product.objects.create(
            seller=cls.other_seller,
            category=cls.category,
            name="Compact Keyboard",
            sku="key-002",
            description="A compact mechanical keyboard.",
            price=Decimal("50.00"),
            stock=3,
            is_active=True,
        )
        cls.address = Address.objects.create(
            user=cls.customer,
            label="Home",
            full_name="Demo Customer",
            phone="+92 300 1234567",
            line1="Street 1",
            city="Karachi",
            postal_code="74000",
            country="Pakistan",
            is_default=True,
        )

    def setUp(self):
        self.cart, _ = Cart.objects.get_or_create(user=self.customer)
        Wishlist.objects.get_or_create(user=self.customer)

    def login_customer(self):
        self.client.login(username="customer", password="StrongPass123!")

    def login_seller(self):
        self.client.login(username="seller", password="StrongPass123!")


class ModelTests(StoreFixture):
    def test_product_normalizes_sku_and_generates_unique_slug(self):
        self.assertEqual(self.product.sku, "AUDIO-001")
        self.assertEqual(self.product.slug, "wireless-headphones")
        duplicate_name = Product.objects.create(
            seller=self.seller,
            category=self.category,
            name="Wireless Headphones",
            sku="AUDIO-NEW",
            description="Another model",
            price=Decimal("90.00"),
            stock=1,
        )
        self.assertEqual(duplicate_name.slug, "wireless-headphones-2")

    def test_product_discount_and_stock_properties(self):
        self.assertEqual(self.product.discount_percent, 20)
        self.assertTrue(self.product.in_stock)
        self.product.stock = 4
        self.assertTrue(self.product.is_low_stock)
        self.product.stock = 0
        self.assertFalse(self.product.in_stock)

    def test_cart_subtotal_and_item_count_are_derived(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        CartItem.objects.create(cart=self.cart, product=self.other_product, quantity=1)
        self.assertEqual(self.cart.subtotal, Decimal("210.00"))
        self.assertEqual(self.cart.item_count, 3)

    def test_cart_rejects_duplicate_product_rows(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        with self.assertRaises(IntegrityError):
            CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_default_address_is_unique_per_user(self):
        second = Address.objects.create(
            user=self.customer,
            label="Office",
            full_name="Demo Customer",
            phone="123",
            line1="Business Road",
            city="Karachi",
            postal_code="74000",
            is_default=True,
        )
        self.address.refresh_from_db()
        self.assertFalse(self.address.is_default)
        self.assertTrue(second.is_default)

    def test_coupon_percentage_and_fixed_discounts_are_capped(self):
        percent = Coupon.objects.create(
            code="save10", discount_type=Coupon.DiscountType.PERCENT, value=Decimal("10")
        )
        fixed = Coupon.objects.create(
            code="BIG", discount_type=Coupon.DiscountType.FIXED, value=Decimal("500")
        )
        self.assertEqual(percent.code, "SAVE10")
        self.assertEqual(percent.discount_for(Decimal("80")), Decimal("8.00"))
        self.assertEqual(fixed.discount_for(Decimal("80")), Decimal("80"))

    def test_shipping_calculation_uses_discounted_subtotal(self):
        coupon = Coupon.objects.create(
            code="HALF", discount_type=Coupon.DiscountType.PERCENT, value=Decimal("50")
        )
        totals = calculate_totals(Decimal("120.00"), coupon)
        self.assertEqual(totals.discount, Decimal("60.00"))
        self.assertEqual(totals.shipping, Decimal("10.00"))
        self.assertEqual(totals.total, Decimal("70.00"))


class PublicStoreTests(StoreFixture):
    def test_home_catalog_category_and_detail_are_public(self):
        urls = [
            reverse("EBazaar:home"),
            reverse("EBazaar:catalog"),
            self.category.get_absolute_url(),
            self.product.get_absolute_url(),
            reverse("EBazaar:health"),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_catalog_search_price_stock_and_sort_filters(self):
        response = self.client.get(
            reverse("EBazaar:catalog"),
            {"q": "headphones", "min_price": "70", "max_price": "90", "in_stock": "1", "sort": "price_low"},
        )
        self.assertContains(response, self.product.name)
        self.assertNotContains(response, self.other_product.name)

    def test_catalog_ignores_invalid_price_without_error(self):
        response = self.client.get(reverse("EBazaar:catalog"), {"min_price": "not-money"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "price filters was ignored")

    def test_inactive_product_is_not_public(self):
        self.product.is_active = False
        self.product.save()
        response = self.client.get(self.product.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_protected_pages_redirect_anonymous_users(self):
        urls = [
            reverse("EBazaar:cart"),
            reverse("EBazaar:wishlist"),
            reverse("EBazaar:orders"),
            reverse("EBazaar:seller_dashboard"),
        ]
        for url in urls:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 302)
                self.assertIn(reverse("EBazaar:login"), response.url)

    def test_registration_creates_customer_cart_and_wishlist(self):
        response = self.client.post(
            reverse("EBazaar:register"),
            {
                "first_name": "New",
                "last_name": "Customer",
                "username": "new-customer",
                "email": "new@example.com",
                "phone": "123",
                "role": User.Role.CUSTOMER,
                "password1": "A-Strong-New-Pass-123!",
                "password2": "A-Strong-New-Pass-123!",
            },
        )
        self.assertRedirects(response, reverse("EBazaar:home"))
        user = User.objects.get(username="new-customer")
        self.assertTrue(Cart.objects.filter(user=user).exists())
        self.assertTrue(Wishlist.objects.filter(user=user).exists())

    def test_logout_requires_post(self):
        self.login_customer()
        self.assertEqual(self.client.get(reverse("EBazaar:logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("EBazaar:logout")), reverse("EBazaar:home"))

    def test_password_reset_request_is_available(self):
        self.assertEqual(self.client.get(reverse("EBazaar:password_reset")).status_code, 200)
        response = self.client.post(
            reverse("EBazaar:password_reset"), {"email": self.customer.email}
        )
        self.assertRedirects(response, reverse("EBazaar:password_reset_done"))

    def test_password_change_requires_login_and_renders_for_customer(self):
        url = reverse("EBazaar:password_change")
        self.assertIn(reverse("EBazaar:login"), self.client.get(url).url)
        self.login_customer()
        self.assertEqual(self.client.get(url).status_code, 200)


class CartViewTests(StoreFixture):
    def setUp(self):
        super().setUp()
        self.login_customer()

    def test_add_merges_repeated_product_and_cart_page_renders(self):
        url = reverse("EBazaar:cart_add", args=[self.product.pk])
        self.client.post(url, {"quantity": 2})
        self.client.post(url, {"quantity": 3})
        item = CartItem.objects.get(cart=self.cart, product=self.product)
        self.assertEqual(item.quantity, 5)
        response = self.client.get(reverse("EBazaar:cart"))
        self.assertContains(response, self.product.name)
        self.assertContains(response, "$400.00")

    def test_add_rejects_quantity_above_stock(self):
        response = self.client.post(
            reverse("EBazaar:cart_add", args=[self.product.pk]), {"quantity": 11}, follow=True
        )
        self.assertContains(response, "Only 10 unit(s) are available")
        self.assertFalse(CartItem.objects.filter(cart=self.cart, product=self.product).exists())

    def test_update_and_remove_cart_item(self):
        item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        response = self.client.post(reverse("EBazaar:cart_update", args=[item.pk]), {"quantity": 4})
        self.assertRedirects(response, reverse("EBazaar:cart"))
        item.refresh_from_db()
        self.assertEqual(item.quantity, 4)
        self.client.post(reverse("EBazaar:cart_remove", args=[item.pk]))
        self.assertFalse(CartItem.objects.filter(pk=item.pk).exists())

    def test_user_cannot_change_another_users_cart(self):
        other_cart = Cart.objects.create(user=self.other_customer)
        item = CartItem.objects.create(cart=other_cart, product=self.product, quantity=1)
        self.assertEqual(
            self.client.post(reverse("EBazaar:cart_update", args=[item.pk]), {"quantity": 2}).status_code,
            404,
        )


class CheckoutTests(StoreFixture):
    def test_create_order_snapshots_prices_and_decrements_stock(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        with self.captureOnCommitCallbacks(execute=True):
            order = create_order(
                user=self.customer,
                address=self.address,
                payment_method=Order.PaymentMethod.COD,
            )
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 8)
        self.assertEqual(order.subtotal, Decimal("160.00"))
        self.assertEqual(order.shipping_amount, Decimal("0.00"))
        self.assertEqual(order.total, Decimal("160.00"))
        item = order.items.get()
        self.assertEqual(item.product_name, "Wireless Headphones")
        self.assertEqual(item.unit_price, Decimal("80.00"))
        self.assertEqual(item.line_total, Decimal("160.00"))
        self.assertFalse(self.cart.items.exists())
        self.assertEqual(mail.outbox[-1].to, [self.customer.email])
        self.assertIn(order.reference, mail.outbox[-1].subject)

    def test_checkout_coupon_and_standard_shipping(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        Coupon.objects.create(
            code="WELCOME10",
            discount_type=Coupon.DiscountType.PERCENT,
            value=Decimal("10"),
            minimum_order_amount=Decimal("50"),
        )
        order = create_order(
            user=self.customer,
            address=self.address,
            payment_method=Order.PaymentMethod.BANK,
            coupon_code="welcome10",
        )
        self.assertEqual(order.discount_amount, Decimal("8.00"))
        self.assertEqual(order.shipping_amount, Decimal("10.00"))
        self.assertEqual(order.total, Decimal("82.00"))
        order.coupon.refresh_from_db()
        self.assertEqual(order.coupon.times_used, 1)

    def test_checkout_rejects_overselling_without_partial_changes(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=10)
        self.product.stock = 2
        self.product.save()
        with self.assertRaisesMessage(CheckoutError, "Only 2 unit"):
            create_order(
                user=self.customer,
                address=self.address,
                payment_method=Order.PaymentMethod.COD,
            )
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 2)
        self.assertEqual(Order.objects.count(), 0)
        self.assertTrue(self.cart.items.exists())

    def test_invalid_coupon_does_not_create_order(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        with self.assertRaisesMessage(CheckoutError, "not valid"):
            create_order(
                user=self.customer,
                address=self.address,
                payment_method=Order.PaymentMethod.COD,
                coupon_code="NOPE",
            )
        self.assertEqual(Order.objects.count(), 0)

    def test_cancelling_order_restores_stock_once(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)
        order = create_order(
            user=self.customer,
            address=self.address,
            payment_method=Order.PaymentMethod.COD,
        )
        cancelled = cancel_order(order=order, user=self.customer)
        self.product.refresh_from_db()
        self.assertEqual(cancelled.status, Order.Status.CANCELLED)
        self.assertEqual(self.product.stock, 10)
        with self.assertRaisesMessage(CheckoutError, "no longer"):
            cancel_order(order=cancelled, user=self.customer)

    def test_cancelling_order_releases_coupon_usage(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        coupon = Coupon.objects.create(
            code="ONEUSE",
            discount_type=Coupon.DiscountType.FIXED,
            value=Decimal("5"),
            max_uses=1,
        )
        order = create_order(
            user=self.customer,
            address=self.address,
            payment_method=Order.PaymentMethod.COD,
            coupon_code=coupon.code,
        )
        coupon.refresh_from_db()
        self.assertEqual(coupon.times_used, 1)
        cancel_order(order=order, user=self.customer)
        coupon.refresh_from_db()
        self.assertEqual(coupon.times_used, 0)

    def test_checkout_page_places_order_with_new_address(self):
        CartItem.objects.create(cart=self.cart, product=self.other_product, quantity=1)
        self.login_customer()
        response = self.client.post(
            reverse("EBazaar:checkout"),
            {
                "address": "",
                "payment_method": Order.PaymentMethod.COD,
                "coupon_code": "",
                "customer_note": "Ring once",
                "shipping-label": "Office",
                "shipping-full_name": "Demo Customer",
                "shipping-phone": "123",
                "shipping-line1": "Office Road",
                "shipping-line2": "",
                "shipping-city": "Karachi",
                "shipping-state": "Sindh",
                "shipping-postal_code": "74000",
                "shipping-country": "Pakistan",
            },
        )
        order = Order.objects.get(user=self.customer)
        self.assertRedirects(response, reverse("EBazaar:order_detail", args=[order.reference]))
        self.assertEqual(order.customer_note, "Ring once")
        self.assertEqual(order.shipping_line1, "Office Road")

    def test_order_detail_is_private_to_owner(self):
        CartItem.objects.create(cart=self.cart, product=self.product, quantity=1)
        order = create_order(
            user=self.customer, address=self.address, payment_method=Order.PaymentMethod.COD
        )
        self.client.login(username="other-customer", password="StrongPass123!")
        self.assertEqual(
            self.client.get(reverse("EBazaar:order_detail", args=[order.reference])).status_code,
            404,
        )


class WishlistAndReviewTests(StoreFixture):
    def setUp(self):
        super().setUp()
        self.login_customer()

    def test_wishlist_toggle_adds_then_removes(self):
        url = reverse("EBazaar:wishlist_toggle", args=[self.product.pk])
        self.client.post(url, {"next": self.product.get_absolute_url()})
        wishlist = Wishlist.objects.get(user=self.customer)
        self.assertTrue(wishlist.products.filter(pk=self.product.pk).exists())
        self.client.post(url, {"next": self.product.get_absolute_url()})
        self.assertFalse(wishlist.products.filter(pk=self.product.pk).exists())

    def test_review_requires_delivered_purchase(self):
        response = self.client.post(
            reverse("EBazaar:review_product", args=[self.product.pk]),
            {"rating": 5, "title": "Great", "body": "Very good"},
            follow=True,
        )
        self.assertContains(response, "after a delivered purchase")
        self.assertFalse(Review.objects.exists())

    def test_delivered_buyer_can_create_and_update_one_review(self):
        order = Order.objects.create(
            user=self.customer,
            contact_email=self.customer.email,
            status=Order.Status.DELIVERED,
            payment_method=Order.PaymentMethod.COD,
            shipping_name="Demo",
            shipping_phone="123",
            shipping_line1="Road",
            shipping_city="Karachi",
            shipping_postal_code="74000",
            shipping_country="Pakistan",
            subtotal=Decimal("80"),
            total=Decimal("80"),
        )
        OrderItem.objects.create(
            order=order,
            product=self.product,
            seller=self.seller,
            product_name=self.product.name,
            sku=self.product.sku,
            quantity=1,
            unit_price=self.product.price,
            line_total=self.product.price,
        )
        url = reverse("EBazaar:review_product", args=[self.product.pk])
        self.client.post(url, {"rating": 5, "title": "Excellent", "body": "Loved it"})
        self.client.post(url, {"rating": 4, "title": "Still good", "body": "Updated"})
        self.assertEqual(Review.objects.count(), 1)
        self.assertEqual(Review.objects.get().rating, 4)


class SellerTests(StoreFixture):
    def test_customer_is_redirected_from_seller_hub(self):
        self.login_customer()
        response = self.client.get(reverse("EBazaar:seller_dashboard"), follow=True)
        self.assertRedirects(response, reverse("EBazaar:home"))
        self.assertContains(response, "seller or wholesaler")

    def test_seller_dashboard_products_and_orders_render(self):
        self.login_seller()
        for name in ("seller_dashboard", "seller_products", "seller_orders"):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(f"EBazaar:{name}")).status_code, 200)

    def test_seller_creates_product_owned_by_them(self):
        self.login_seller()
        response = self.client.post(
            reverse("EBazaar:seller_product_create"),
            {
                "category": self.category.pk,
                "name": "Seller Camera",
                "sku": "cam-900",
                "brand": "Lens",
                "description": "A simple camera",
                "price": "125.00",
                "compare_at_price": "150.00",
                "stock": 4,
                "low_stock_threshold": 2,
                "weight_kg": "1.250",
                "sizes_text": "",
                "colors_text": "Black, Silver",
                "is_active": "on",
            },
        )
        self.assertRedirects(response, reverse("EBazaar:seller_products"))
        product = Product.objects.get(sku="CAM-900")
        self.assertEqual(product.seller, self.seller)
        self.assertEqual(product.colors, ["Black", "Silver"])

    def test_seller_cannot_edit_another_sellers_product(self):
        self.login_seller()
        response = self.client.get(
            reverse("EBazaar:seller_product_edit", args=[self.other_product.pk])
        )
        self.assertEqual(response.status_code, 404)

    def test_seller_can_hide_product(self):
        self.login_seller()
        self.client.post(reverse("EBazaar:seller_product_deactivate", args=[self.product.pk]))
        self.product.refresh_from_db()
        self.assertFalse(self.product.is_active)


class SeedCommandTests(TestCase):
    def test_seed_store_is_repeatable(self):
        output = StringIO()
        with TemporaryDirectory() as media_root, self.settings(MEDIA_ROOT=media_root):
            call_command("seed_store", password="SeedTest123!", stdout=output)
            first_counts = (Category.objects.count(), Product.objects.count(), Coupon.objects.count())
            call_command("seed_store", password="SeedTest123!", stdout=output)
            second_counts = (Category.objects.count(), Product.objects.count(), Coupon.objects.count())

        self.assertEqual(first_counts, (4, 12, 1))
        self.assertEqual(second_counts, first_counts)
        self.assertTrue(User.objects.get(username="demo_seller").check_password("SeedTest123!"))
        self.assertIn("Seeded 12 products", output.getvalue())
