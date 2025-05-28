# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Category,
    Brand,
    Product,
    Attribute,
    AttributeValue,
    ProductMedia,
    Cart,
    CartItem,
    Order,
    OrderItem,
    Wishlist,
    ProductDetail,
    ProductDetailMedia,
    Comment,
    RelatedProduct,
    CommentMedia,
    ShippingCarrier,
    SpecialOffer
)

from django_summernote.admin import SummernoteModelAdmin


class ProductAdmin(SummernoteModelAdmin):
    list_display = ("image", "name", "brand", "final_price")
    list_filter = ("category",)
    search_fields = ("name", "brand__name")

    def final_price(self, obj):
        if obj.discount_price:
            return obj.discount_price
        return obj.price

    final_price.short_description = "Final Price"

    def image(self, obj):
        if obj.media.first():
            return format_html(
                '<img src="{}" width="50" height="50" />',
                obj.media.first().thumbnail.url,
            )

        return obj.name

    image.short_description = "Image"


class MediaAdmin(admin.ModelAdmin):
    list_display = (
        "image",
        "product",
    )
    list_filter = ("media_type",)
    search_fields = ("product",)

    def image(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="50" height="50" />',
                obj.thumbnail.url,
            )

        return obj.product

    image.short_description = "Image"


class ProductDetailAdmin(SummernoteModelAdmin):
    summernote_fields = ("description",)


admin.site.register(Category)
admin.site.register(ShippingCarrier)
admin.site.register(RelatedProduct)
admin.site.register(Brand)
admin.site.register(Attribute)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(Comment)
admin.site.register(CommentMedia)
admin.site.register(SpecialOffer)
admin.site.register(ProductDetail, ProductDetailAdmin)
admin.site.register(AttributeValue)
admin.site.register(ProductDetailMedia)
admin.site.register(ProductMedia, MediaAdmin)
admin.site.register(Product, ProductAdmin)