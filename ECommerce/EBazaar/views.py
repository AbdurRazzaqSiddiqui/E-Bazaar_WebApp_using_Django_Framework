from decimal import Decimal, InvalidOperation
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import connection, transaction
from django.db.models import Avg, Count, F, Q, Sum
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .forms import (
    AddressForm,
    CartQuantityForm,
    CheckoutForm,
    LoginForm,
    ProductForm,
    ProfileForm,
    RegistrationForm,
    ReviewForm,
)
from .models import Address, Cart, CartItem, Category, Collection, Order, OrderItem, Product, Review, Wishlist
from .services import CheckoutError, cancel_order as cancel_order_service, create_order


def seller_required(view_func):
    @wraps(view_func)
    @login_required
    def wrapped(request, *args, **kwargs):
        if not request.user.can_sell:
            messages.error(request, "A seller or wholesaler account is required for that page.")
            return redirect("EBazaar:home")
        return view_func(request, *args, **kwargs)

    return wrapped


def home(request):
    now = timezone.now()
    featured_products = (
        Product.objects.filter(is_active=True, is_featured=True)
        .select_related("category", "seller")[:8]
    )
    if not featured_products:
        featured_products = Product.objects.filter(is_active=True).select_related("category", "seller")[:8]

    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count("products", filter=Q(products__is_active=True))
    )[:6]
    collections = Collection.objects.filter(is_active=True).filter(
        Q(starts_at__isnull=True) | Q(starts_at__lte=now),
        Q(ends_at__isnull=True) | Q(ends_at__gte=now),
    )[:3]
    newest_products = Product.objects.filter(is_active=True).select_related("category")[:8]
    return render(
        request,
        "EBazaar/home.html",
        {
            "featured_products": featured_products,
            "newest_products": newest_products,
            "categories": categories,
            "collections": collections,
        },
    )


def product_list(request, slug=None):
    products = Product.objects.filter(is_active=True).select_related("category", "seller")
    selected_category = None
    if slug:
        selected_category = get_object_or_404(Category, slug=slug, is_active=True)
        products = products.filter(category=selected_category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(brand__icontains=query)
            | Q(sku__icontains=query)
        )

    try:
        if request.GET.get("min_price"):
            products = products.filter(price__gte=Decimal(request.GET["min_price"]))
        if request.GET.get("max_price"):
            products = products.filter(price__lte=Decimal(request.GET["max_price"]))
    except (InvalidOperation, ValueError):
        messages.warning(request, "One of the price filters was ignored because it was invalid.")

    if request.GET.get("in_stock") == "1":
        products = products.filter(stock__gt=0)

    sort_options = {
        "newest": "-created_at",
        "price_low": "price",
        "price_high": "-price",
        "name": "name",
    }
    selected_sort = request.GET.get("sort", "newest")
    products = products.order_by(sort_options.get(selected_sort, "-created_at"))

    page = Paginator(products, 12).get_page(request.GET.get("page"))
    categories = Category.objects.filter(is_active=True).annotate(
        product_count=Count("products", filter=Q(products__is_active=True))
    )
    return render(
        request,
        "EBazaar/product_list.html",
        {
            "page_obj": page,
            "categories": categories,
            "selected_category": selected_category,
            "query": query,
            "selected_sort": selected_sort,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category", "seller"), slug=slug, is_active=True
    )
    reviews = product.reviews.filter(is_approved=True).select_related("user")
    rating = reviews.aggregate(average=Avg("rating"), count=Count("id"))
    related_products = (
        Product.objects.filter(category=product.category, is_active=True)
        .exclude(pk=product.pk)
        .select_related("category")[:4]
    )
    has_purchased = False
    is_wishlisted = False
    existing_review = None
    if request.user.is_authenticated:
        has_purchased = OrderItem.objects.filter(
            order__user=request.user,
            order__status=Order.Status.DELIVERED,
            product=product,
        ).exists()
        wishlist = Wishlist.objects.filter(user=request.user).first()
        is_wishlisted = bool(wishlist and wishlist.products.filter(pk=product.pk).exists())
        existing_review = Review.objects.filter(user=request.user, product=product).first()

    return render(
        request,
        "EBazaar/product_detail.html",
        {
            "product": product,
            "reviews": reviews,
            "rating": rating,
            "related_products": related_products,
            "quantity_form": CartQuantityForm(max_stock=product.stock),
            "review_form": ReviewForm(instance=existing_review),
            "has_purchased": has_purchased,
            "is_wishlisted": is_wishlisted,
        },
    )


def login_view(request):
    if request.user.is_authenticated:
        return redirect("EBazaar:home")
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        requested_next = request.POST.get("next", "")
        if requested_next and url_has_allowed_host_and_scheme(
            requested_next, allowed_hosts={request.get_host()}, require_https=request.is_secure()
        ):
            return redirect(requested_next)
        messages.success(request, f"Welcome back, {form.get_user().display_name}.")
        return redirect("EBazaar:home")
    return render(request, "EBazaar/account/login.html", {"form": form})


@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been signed out.")
    return redirect("EBazaar:home")


def register(request):
    if request.user.is_authenticated:
        return redirect("EBazaar:home")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        Cart.objects.create(user=user)
        Wishlist.objects.create(user=user)
        login(request, user)
        messages.success(request, "Your E-Bazaar account is ready.")
        if user.can_sell:
            return redirect("EBazaar:seller_dashboard")
        return redirect("EBazaar:home")
    return render(request, "EBazaar/account/register.html", {"form": form})


@login_required
def account(request):
    recent_orders = request.user.orders.prefetch_related("items")[:5]
    return render(
        request,
        "EBazaar/account/account.html",
        {"recent_orders": recent_orders, "addresses": request.user.addresses.all()},
    )


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your profile has been updated.")
        return redirect("EBazaar:account")
    return render(request, "EBazaar/account/profile_form.html", {"form": form})


@login_required
def address_create(request):
    form = AddressForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        address = form.save(commit=False)
        address.user = request.user
        address.save()
        messages.success(request, "Address saved.")
        return redirect("EBazaar:account")
    return render(request, "EBazaar/account/address_form.html", {"form": form, "title": "Add address"})


@login_required
def address_edit(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    form = AddressForm(request.POST or None, instance=address)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Address updated.")
        return redirect("EBazaar:account")
    return render(request, "EBazaar/account/address_form.html", {"form": form, "title": "Edit address"})


@login_required
@require_POST
def address_delete(request, pk):
    get_object_or_404(Address, pk=pk, user=request.user).delete()
    messages.info(request, "Address removed.")
    return redirect("EBazaar:account")


@login_required
def cart_detail(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related("product", "product__category")
    return render(request, "EBazaar/cart.html", {"cart": cart, "cart_items": items})


@login_required
@require_POST
@transaction.atomic
def cart_add(request, product_id):
    product = get_object_or_404(Product.objects.select_for_update(), pk=product_id, is_active=True)
    form = CartQuantityForm(request.POST, max_stock=product.stock)
    if not product.in_stock:
        messages.error(request, "That product is currently out of stock.")
        return redirect(product.get_absolute_url())
    if not form.is_valid():
        messages.error(request, "Please choose a valid quantity.")
        return redirect(product.get_absolute_url())

    cart, _ = Cart.objects.get_or_create(user=request.user)
    added_quantity = form.cleaned_data["quantity"]
    item, created = CartItem.objects.select_for_update().get_or_create(
        cart=cart, product=product, defaults={"quantity": added_quantity}
    )
    requested_quantity = item.quantity if created else item.quantity + added_quantity
    if requested_quantity > product.stock:
        messages.error(request, f"Only {product.stock} unit(s) are available.")
        if created:
            item.delete()
        return redirect(product.get_absolute_url())
    item.quantity = requested_quantity
    item.save()
    messages.success(request, f"{product.name} was added to your cart.")
    return redirect("EBazaar:cart")


@login_required
@require_POST
def cart_update(request, item_id):
    item = get_object_or_404(CartItem.objects.select_related("product"), pk=item_id, cart__user=request.user)
    form = CartQuantityForm(request.POST, max_stock=item.product.stock)
    if form.is_valid():
        item.quantity = form.cleaned_data["quantity"]
        item.save()
        messages.success(request, "Cart updated.")
    else:
        messages.error(request, f"Choose a quantity between 1 and {item.product.stock}.")
    return redirect("EBazaar:cart")


@login_required
@require_POST
def cart_remove(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    product_name = item.product.name
    item.delete()
    messages.info(request, f"{product_name} was removed from your cart.")
    return redirect("EBazaar:cart")


@login_required
def wishlist_detail(request):
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    products = wishlist.products.filter(is_active=True).select_related("category", "seller")
    return render(request, "EBazaar/wishlist.html", {"products": products})


@login_required
@require_POST
def wishlist_toggle(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    wishlist, _ = Wishlist.objects.get_or_create(user=request.user)
    if wishlist.products.filter(pk=product.pk).exists():
        wishlist.products.remove(product)
        messages.info(request, f"{product.name} was removed from your wishlist.")
    else:
        wishlist.products.add(product)
        messages.success(request, f"{product.name} was saved to your wishlist.")
    requested_next = request.POST.get("next", "")
    if requested_next and url_has_allowed_host_and_scheme(
        requested_next, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        return redirect(requested_next)
    return redirect(product.get_absolute_url())


@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.items.select_related("product")
    if not cart_items.exists():
        messages.info(request, "Add a product before checking out.")
        return redirect("EBazaar:catalog")

    checkout_form = CheckoutForm(request.POST or None, user=request.user)
    address_form = AddressForm(request.POST or None, prefix="shipping")
    if request.method == "POST" and checkout_form.is_valid():
        address = checkout_form.cleaned_data["address"]
        if address is None:
            if not address_form.is_valid():
                return render(
                    request,
                    "EBazaar/checkout.html",
                    {"cart": cart, "cart_items": cart_items, "checkout_form": checkout_form, "address_form": address_form},
                )
            address = address_form.save(commit=False)
            address.user = request.user
            address.save()
        try:
            order = create_order(
                user=request.user,
                address=address,
                payment_method=checkout_form.cleaned_data["payment_method"],
                coupon_code=checkout_form.cleaned_data["coupon_code"],
                customer_note=checkout_form.cleaned_data["customer_note"],
            )
        except CheckoutError as exc:
            messages.error(request, str(exc))
        else:
            messages.success(request, f"Order {order.reference} has been placed.")
            return redirect("EBazaar:order_detail", reference=order.reference)

    return render(
        request,
        "EBazaar/checkout.html",
        {"cart": cart, "cart_items": cart_items, "checkout_form": checkout_form, "address_form": address_form},
    )


@login_required
def order_list(request):
    orders = request.user.orders.prefetch_related("items")
    return render(request, "EBazaar/orders/order_list.html", {"orders": orders})


@login_required
def order_detail(request, reference):
    order = get_object_or_404(
        Order.objects.prefetch_related("items", "items__product"),
        reference=reference,
        user=request.user,
    )
    return render(request, "EBazaar/orders/order_detail.html", {"order": order})


@login_required
@require_POST
def order_cancel(request, reference):
    order = get_object_or_404(Order, reference=reference, user=request.user)
    try:
        cancel_order_service(order=order, user=request.user)
    except CheckoutError as exc:
        messages.error(request, str(exc))
    else:
        messages.success(request, f"Order {reference} was cancelled and its stock was restored.")
    return redirect("EBazaar:order_detail", reference=reference)


@login_required
@require_POST
def review_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    purchased = OrderItem.objects.filter(
        order__user=request.user,
        order__status=Order.Status.DELIVERED,
        product=product,
    ).exists()
    if not purchased:
        messages.error(request, "Reviews are available after a delivered purchase.")
        return redirect(product.get_absolute_url())

    review = Review.objects.filter(product=product, user=request.user).first()
    form = ReviewForm(request.POST, instance=review)
    if form.is_valid():
        review = form.save(commit=False)
        review.product = product
        review.user = request.user
        review.save()
        messages.success(request, "Thank you for reviewing this product.")
    else:
        messages.error(request, "Please correct the review and try again.")
    return redirect(product.get_absolute_url())


@seller_required
def seller_dashboard(request):
    products = Product.objects.filter(seller=request.user)
    sold_items = OrderItem.objects.filter(seller=request.user).exclude(
        order__status=Order.Status.CANCELLED
    )
    stats = {
        "products": products.count(),
        "low_stock": products.filter(stock__lte=F("low_stock_threshold"), is_active=True).count(),
        "units_sold": sold_items.aggregate(total=Sum("quantity"))["total"] or 0,
        "revenue": sold_items.aggregate(total=Sum("line_total"))["total"] or Decimal("0.00"),
    }
    recent_items = sold_items.select_related("order", "product").order_by("-order__created_at")[:8]
    return render(
        request,
        "EBazaar/seller/dashboard.html",
        {"stats": stats, "products": products.order_by("stock", "name")[:10], "recent_items": recent_items},
    )


@seller_required
def seller_products(request):
    products = Product.objects.filter(seller=request.user).select_related("category")
    page = Paginator(products, 20).get_page(request.GET.get("page"))
    return render(request, "EBazaar/seller/products.html", {"page_obj": page})


@seller_required
def seller_product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user
        product.save()
        messages.success(request, f"{product.name} was added to your catalog.")
        return redirect("EBazaar:seller_products")
    return render(request, "EBazaar/seller/product_form.html", {"form": form, "title": "Add product"})


@seller_required
def seller_product_edit(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, f"{product.name} was updated.")
        return redirect("EBazaar:seller_products")
    return render(request, "EBazaar/seller/product_form.html", {"form": form, "title": "Edit product", "product": product})


@seller_required
@require_POST
def seller_product_deactivate(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    product.is_active = False
    product.save(update_fields=["is_active", "updated_at"])
    messages.info(request, f"{product.name} is no longer visible in the storefront.")
    return redirect("EBazaar:seller_products")


@seller_required
def seller_orders(request):
    orders = (
        Order.objects.filter(items__seller=request.user)
        .distinct()
        .prefetch_related("items", "items__product")
    )
    return render(request, "EBazaar/seller/orders.html", {"orders": orders})


def health(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
    except Exception:
        return JsonResponse({"status": "unhealthy", "database": "unavailable"}, status=503)
    return JsonResponse({"status": "ok", "database": "ok"})
