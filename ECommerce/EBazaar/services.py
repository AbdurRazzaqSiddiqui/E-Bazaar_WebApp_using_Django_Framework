from dataclasses import dataclass
from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.db.models import F
from django.template.loader import render_to_string

from .models import Address, Cart, Coupon, Order, OrderItem, Product, User


FREE_SHIPPING_THRESHOLD = Decimal("100.00")
STANDARD_SHIPPING = Decimal("10.00")


class CheckoutError(Exception):
    pass


@dataclass(frozen=True)
class OrderTotals:
    subtotal: Decimal
    discount: Decimal
    shipping: Decimal
    total: Decimal


def send_order_confirmation(order_id: int) -> None:
    order = Order.objects.prefetch_related("items").get(pk=order_id)
    if not order.contact_email:
        return
    send_mail(
        subject=f"E-Bazaar order {order.reference}",
        message=render_to_string(
            "EBazaar/orders/order_confirmation_email.txt", {"order": order}
        ),
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.contact_email],
        fail_silently=False,
    )


def calculate_totals(subtotal: Decimal, coupon: Coupon | None = None) -> OrderTotals:
    discount = coupon.discount_for(subtotal) if coupon else Decimal("0.00")
    discounted_subtotal = subtotal - discount
    shipping = Decimal("0.00") if discounted_subtotal >= FREE_SHIPPING_THRESHOLD else STANDARD_SHIPPING
    if discounted_subtotal == 0:
        shipping = Decimal("0.00")
    return OrderTotals(
        subtotal=subtotal,
        discount=discount,
        shipping=shipping,
        total=(discounted_subtotal + shipping).quantize(Decimal("0.01")),
    )


@transaction.atomic
def create_order(
    *,
    user: User,
    address: Address,
    payment_method: str,
    coupon_code: str = "",
    customer_note: str = "",
) -> Order:
    try:
        cart = Cart.objects.select_for_update().get(user=user)
    except Cart.DoesNotExist as exc:
        raise CheckoutError("Your cart is empty.") from exc

    cart_items = list(cart.items.select_related("product").order_by("product_id"))
    if not cart_items:
        raise CheckoutError("Your cart is empty.")

    products = {
        product.pk: product
        for product in Product.objects.select_for_update().filter(
            pk__in=[item.product_id for item in cart_items]
        )
    }

    subtotal = Decimal("0.00")
    for item in cart_items:
        product = products.get(item.product_id)
        if product is None or not product.is_active:
            raise CheckoutError(f"{item.product.name} is no longer available.")
        if item.quantity > product.stock:
            raise CheckoutError(
                f"Only {product.stock} unit(s) of {product.name} are currently available."
            )
        subtotal += product.price * item.quantity

    coupon = None
    if coupon_code:
        try:
            coupon = Coupon.objects.select_for_update().get(code__iexact=coupon_code)
        except Coupon.DoesNotExist as exc:
            raise CheckoutError("That coupon code is not valid.") from exc
        if not coupon.is_valid_for(subtotal):
            raise CheckoutError("That coupon is expired or cannot be used for this order.")

    totals = calculate_totals(subtotal, coupon)
    order = Order.objects.create(
        user=user,
        contact_email=user.email,
        payment_method=payment_method,
        shipping_name=address.full_name,
        shipping_phone=address.phone,
        shipping_line1=address.line1,
        shipping_line2=address.line2,
        shipping_city=address.city,
        shipping_state=address.state,
        shipping_postal_code=address.postal_code,
        shipping_country=address.country,
        coupon=coupon,
        subtotal=totals.subtotal,
        discount_amount=totals.discount,
        shipping_amount=totals.shipping,
        total=totals.total,
        customer_note=customer_note,
    )

    order_items = []
    for item in cart_items:
        product = products[item.product_id]
        order_items.append(
            OrderItem(
                order=order,
                product=product,
                seller=product.seller,
                product_name=product.name,
                sku=product.sku,
                quantity=item.quantity,
                unit_price=product.price,
                line_total=product.price * item.quantity,
            )
        )
        product.stock -= item.quantity
        product.save(update_fields=["stock", "updated_at"])

    OrderItem.objects.bulk_create(order_items)
    cart.items.all().delete()
    if coupon:
        Coupon.objects.filter(pk=coupon.pk).update(times_used=F("times_used") + 1)
    transaction.on_commit(lambda: send_order_confirmation(order.pk), robust=True)
    return order


@transaction.atomic
def cancel_order(*, order: Order, user: User) -> Order:
    locked_order = Order.objects.select_for_update().get(pk=order.pk)
    if locked_order.user_id != user.pk and not user.is_superuser:
        raise CheckoutError("You cannot cancel this order.")
    if not locked_order.can_cancel:
        raise CheckoutError("This order can no longer be cancelled.")

    items = list(locked_order.items.all())
    product_ids = [item.product_id for item in items if item.product_id]
    products = {
        product.pk: product
        for product in Product.objects.select_for_update().filter(pk__in=product_ids)
    }
    for item in items:
        if item.product_id in products:
            product = products[item.product_id]
            product.stock += item.quantity
            product.save(update_fields=["stock", "updated_at"])

    locked_order.status = Order.Status.CANCELLED
    if locked_order.payment_status == Order.PaymentStatus.PAID:
        locked_order.payment_status = Order.PaymentStatus.REFUNDED
    locked_order.save(update_fields=["status", "payment_status", "updated_at"])
    if locked_order.coupon_id:
        Coupon.objects.filter(pk=locked_order.coupon_id, times_used__gt=0).update(
            times_used=F("times_used") - 1
        )
    return locked_order
