from .views import get_cart, get_wishlist
from .models import Brand


def getHeader(request):
    """
    Return a dictionary that includes cart and wishlist items (or anything else)
    for the logged-in user so that it’s available in every template.
    """
    FREE_SHIPPING_THRESHOLD = 5000

    context = {
        "cart_items": [],
        "cart_count": 0,
        "total_price": 0,
        "wishlist_items": [],
        "wishlist_count": 0,
        "brands": Brand.objects.all(),
    }

    total_price = 0
    if cart := get_cart(request):
        items = cart.items.all()
        for item in items:
            price = item.product.discount_price or item.product.price
            total_price += price * item.quantity
        context["cart_items"] = items
        context["cart_count"] = len(items)
        context["total_price"] = total_price

    if wishlist := get_wishlist(request):
        wishlist_items = wishlist.products.all()
        context["wishlist_items"] = wishlist_items
        context["wishlist_count"] = wishlist_items.count()

    return context
