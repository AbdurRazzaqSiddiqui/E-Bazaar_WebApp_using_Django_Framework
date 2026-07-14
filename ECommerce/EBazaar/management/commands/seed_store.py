from decimal import Decimal

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from EBazaar.models import Cart, Category, Collection, Coupon, Product, User, Wishlist


CATALOG = [
    {
        "category": ("Electronics", "Devices and accessories for work, play, and everyday life."),
        "products": [
            ("Aurora Wireless Headphones", "EBZ-AUD-001", "Northstar", "79.00", "99.00", 28, ["Black", "Sand"]),
            ("Arc Mechanical Keyboard", "EBZ-KEY-002", "Keywell", "89.00", None, 17, ["Graphite", "Cream"]),
            ("Halo USB Microphone", "EBZ-MIC-003", "Sonora", "64.50", "72.00", 9, ["Black"]),
        ],
    },
    {
        "category": ("Home & Living", "Practical, considered pieces for more comfortable spaces."),
        "products": [
            ("Linen Table Runner", "EBZ-HOM-001", "Woven", "24.00", None, 35, ["Oat", "Sage"]),
            ("Stoneware Serving Bowl", "EBZ-HOM-002", "Morrow", "38.00", "45.00", 12, ["Clay", "Chalk"]),
            ("Soft Glow Desk Lamp", "EBZ-HOM-003", "Luma", "52.00", None, 6, ["Moss", "Ivory"]),
        ],
    },
    {
        "category": ("Style", "Versatile wardrobe essentials with an easy point of view."),
        "products": [
            ("Everyday Canvas Tote", "EBZ-STY-001", "Common Goods", "29.00", None, 44, ["Natural", "Black"]),
            ("Relaxed Cotton Overshirt", "EBZ-STY-002", "Fieldwork", "58.00", "72.00", 21, ["S", "M", "L", "XL"]),
            ("Minimal Leather Wallet", "EBZ-STY-003", "Fold", "42.00", None, 15, ["Tan", "Espresso"]),
        ],
    },
    {
        "category": ("Wellness", "Simple tools for thoughtful routines and restorative moments."),
        "products": [
            ("Cedar Aromatherapy Set", "EBZ-WEL-001", "Still", "33.00", None, 18, ["Cedar", "Citrus"]),
            ("Insulated Daily Bottle", "EBZ-WEL-002", "Current", "26.00", "32.00", 31, ["Sage", "Terracotta", "Ink"]),
            ("Natural Cork Yoga Mat", "EBZ-WEL-003", "Grounded", "67.00", None, 8, ["Natural"]),
        ],
    },
]

DEMO_PRODUCT_IMAGES = [
    "headphone.jpg",
    "keyboard.jpg",
    "mic.jpg",
    "product-01.jpg",
    "product-02.jpg",
    "product-03.jpg",
    "product-04.jpg",
    "product-05.jpg",
    "product-06.jpg",
    "product-07.jpg",
    "product-08.jpg",
    "product-09.jpg",
]


class Command(BaseCommand):
    help = "Create an idempotent demonstration catalog, coupon, and accounts."

    def add_arguments(self, parser):
        parser.add_argument("--password", default="DemoStore123!", help="Password for both demo accounts.")

    def handle(self, *args, **options):
        password = options["password"]
        seller, _ = User.objects.get_or_create(
            username="demo_seller",
            defaults={
                "email": "seller@example.com",
                "first_name": "Demo",
                "last_name": "Seller",
                "role": User.Role.SELLER,
            },
        )
        seller.role = User.Role.SELLER
        seller.set_password(password)
        seller.save()

        customer, _ = User.objects.get_or_create(
            username="demo_customer",
            defaults={
                "email": "customer@example.com",
                "first_name": "Demo",
                "last_name": "Customer",
                "role": User.Role.CUSTOMER,
            },
        )
        customer.role = User.Role.CUSTOMER
        customer.set_password(password)
        customer.save()
        Cart.objects.get_or_create(user=customer)
        Wishlist.objects.get_or_create(user=customer)
        Cart.objects.get_or_create(user=seller)
        Wishlist.objects.get_or_create(user=seller)

        created_products = []
        image_index = 0
        for display_order, entry in enumerate(CATALOG, start=1):
            category_name, category_description = entry["category"]
            category, _ = Category.objects.update_or_create(
                name=category_name,
                defaults={
                    "slug": category_name.lower().replace(" & ", "-").replace(" ", "-"),
                    "description": category_description,
                    "is_active": True,
                    "display_order": display_order,
                },
            )
            category_asset = (
                settings.BASE_DIR
                / "EBazaar"
                / "static"
                / "EBazaar"
                / "images"
                / f"banner-0{display_order}.jpg"
            )
            if not category.image and category_asset.exists():
                with category_asset.open("rb") as source:
                    category.image.save(f"demo-{category_asset.name}", File(source), save=True)
            for index, product_data in enumerate(entry["products"]):
                name, sku, brand, price, compare_at, stock, options_list = product_data
                product, _ = Product.objects.update_or_create(
                    sku=sku,
                    defaults={
                        "seller": seller,
                        "category": category,
                        "name": name,
                        "brand": brand,
                        "description": (
                            f"A carefully selected {name.lower()} from {brand}. "
                            "Built for dependable everyday use and backed by live inventory in E-Bazaar."
                        ),
                        "price": Decimal(price),
                        "compare_at_price": Decimal(compare_at) if compare_at else None,
                        "stock": stock,
                        "low_stock_threshold": 5,
                        "colors": options_list if category_name != "Style" or index != 1 else ["Stone", "Olive"],
                        "sizes": options_list if category_name == "Style" and index == 1 else [],
                        "is_active": True,
                        "is_featured": index < 2,
                    },
                )
                product_asset = (
                    settings.BASE_DIR
                    / "EBazaar"
                    / "static"
                    / "EBazaar"
                    / "images"
                    / DEMO_PRODUCT_IMAGES[image_index]
                )
                image_index += 1
                if not product.image and product_asset.exists():
                    with product_asset.open("rb") as source:
                        product.image.save(f"demo-{product_asset.name}", File(source), save=True)
                created_products.append(product)

        collection, _ = Collection.objects.update_or_create(
            slug="everyday-upgrades",
            defaults={
                "name": "Everyday upgrades",
                "tagline": "Small changes that make routines feel considerably better.",
                "is_active": True,
            },
        )
        collection.products.set(created_products[:6])
        collection_asset = (
            settings.BASE_DIR
            / "EBazaar"
            / "static"
            / "EBazaar"
            / "images"
            / "slide-01.jpg"
        )
        if not collection.image and collection_asset.exists():
            with collection_asset.open("rb") as source:
                collection.image.save(f"demo-{collection_asset.name}", File(source), save=True)

        Coupon.objects.update_or_create(
            code="WELCOME10",
            defaults={
                "discount_type": Coupon.DiscountType.PERCENT,
                "value": Decimal("10.00"),
                "minimum_order_amount": Decimal("50.00"),
                "active": True,
            },
        )

        self.stdout.write(self.style.SUCCESS(f"Seeded {len(created_products)} products in {len(CATALOG)} categories."))
        self.stdout.write(f"Demo seller: demo_seller / {password}")
        self.stdout.write(f"Demo customer: demo_customer / {password}")
        self.stdout.write("Coupon: WELCOME10 (10% off orders of $50 or more)")
