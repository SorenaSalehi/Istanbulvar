from django.urls import path
from .views import (
    add_to_cart_api,
    wishlist_partial,
    add_to_wishlist_api,
    remove_from_wishlist_api,
    cart_partial,
    remove_from_cart_api,
    shop_list,
    checkOut,
    product_view,
    order_detail,
)

app_name = "shop"

urlpatterns = [
    path("product/<str:product_slug>/", product_view, name="product_detail"),
    path(
        "product-attributes/<str:product_slug>/",
        product_view,
        name="product_attribute",
    ),
    path(
        "product_review/<str:product_slug>/",
        product_view,
        name="product_review",
    ),
    path("api/add-to-cart/", add_to_cart_api, name="add_to_cart_api"),
    path("api/add-to-wishlist/", add_to_wishlist_api, name="add_to_wishlist_api"),
    path(
        "api/remove-from-wishlist/",
        remove_from_wishlist_api,
        name="remove_from_wishlist_api",
    ),
    path("api/orders/", order_detail, name="order_detail"),
    path("api/remove-from-cart/", remove_from_cart_api, name="remove_from_cart_api"),
    path("wishlist/partial/", wishlist_partial, name="wishlist_partial"),
    path("cart/partial/", cart_partial, name="cart_partial"),
    path("list/", shop_list, name="shop_list"),
    path("check-out/", checkOut, name="checkOut"),
]
