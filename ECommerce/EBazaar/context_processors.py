from django.db.models import Sum

from .models import Cart, Category


def store_context(request):
    cart_count = 0
    if request.user.is_authenticated:
        try:
            cart = request.user.cart
        except Cart.DoesNotExist:
            cart = None
        if cart is not None:
            cart_count = cart.items.aggregate(total=Sum("quantity"))["total"] or 0

    return {
        "nav_categories": Category.objects.filter(is_active=True)[:8],
        "cart_count": cart_count,
    }
